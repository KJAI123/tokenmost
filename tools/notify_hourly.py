#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notify_hourly.py — tokenmost 每小时汇总推送（经龙虾 OpenClaw 的飞书 bot DM 老板）

用法: python3 tools/notify_hourly.py --text "汇总内容"
      echo "内容" | python3 tools/notify_hourly.py
      python3 tools/notify_hourly.py --text "内容" --mock ok   # 离线自测：不读配置、不发网络
      python3 tools/notify_hourly.py --selftest                # 离线全场景自检
凭据只从本机 ~/.openclaw/openclaw.json 读取，不打印不外传。
微信侧无主动通道（微信客服 bot 官方限制不能主动发消息），故走飞书 bot。

可靠性约定（调度器依赖退出码判断）：
  0 = 发送成功；1 = 确定未送达（内容已暂存 outbox，处理原因后可补发）；
  2 = 参数/配置错误；3 = 发送结果不确定（可能已送达，未自动重发，需人工核对）。

幂等与重试（2026-11-22 返修）：
  - 消息体带官方幂等键 uuid（im/v1/messages 文档：同 uuid 1 小时内最多成功投递一条），
    由内容哈希稳定生成；本地未做真实投递验收，不依赖服务端去重来自动重发。
  - 仅"取 token"阶段允许自动重试（该接口无投递副作用）；消息 POST 阶段绝不自动重发：
    回包丢失时服务器可能已投递，自动重试=重复推送，一律按 unknown 落 outbox 并以
    退出码 3 要求人工核对。
  - 飞书业务拒绝（2xx+code!=0 或 4xx）是确定性失败，不重试。
  - HTTP 状态参与成功判定：非 2xx 即使错误体碰巧 code=0 也不算成功（5xx/解析失败→unknown）。
"""
import argparse
import hashlib
import json
import pathlib
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = pathlib.Path.home() / ".openclaw/openclaw.json"
DEFAULT_OUTBOX = ROOT / "data-research" / "notify-outbox.md"
TOKEN_RETRIES = 1  # 仅 token 阶段追加尝试（共 1+TOKEN_RETRIES 次）；该接口无投递副作用
EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_UNKNOWN = 0, 1, 2, 3
FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
# mock 自测计数：消息 POST 在调用入口即计数（模拟"服务器已收到"先于回包返回/丢失）
MOCK_STATS = {"token_calls": 0, "msg_posts": 0, "msg_uuids": []}

_OUTBOX_HINTS = {
    "unknown·结果不确定": "可能已送达：请先在飞书核对是否收到本条；已收到→忽略，仅在确认未收到并查清原因后手动补发。不能仅凭 uuid 自动重发。",
    "未送达·确定失败": "服务器明确拒绝、未投递：处理失败原因后可手动补发；本轮未验证真实投递或服务端去重效果。",
    "未送达·取token失败": "消息从未 POST：可直接补发。",
}


def _cfg():
    try:
        c = json.loads(CFG.read_text())["channels"]["feishu"]
        app_id, app_secret = c["appId"], c["appSecret"]
        owner = next((k for k, v in c.get("dms", {}).items()
                      if isinstance(v, dict) and v.get("enabled")), None)
        if not all(isinstance(v, str) and v.strip() for v in (app_id, app_secret, owner)):
            raise ValueError("缺少 appId、appSecret 或启用的飞书 DM 目标")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise RuntimeError(f"配置不可用（{CFG}）: {type(e).__name__}: {e}")
    return app_id, app_secret, owner


def _msg_uuid(text: str) -> str:
    """稳定幂等键：由内容哈希生成（≤50 字符，符合官方 uuid 参数限制）。

    同一内容在任何路径下的重发（人工补发/调度重复）都携带同一 uuid，
    服务端按官方语义 1 小时内只成功投递一条；不同内容自然得到不同键。"""
    return "tm-" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:40]


def _real_transport(url, body, headers, timeout=15):
    """统一返回 (http_status, 解析后的JSON或None)。

    HTTP 状态必须上抛给调用方参与判定：非 2xx 而错误体碰巧 code=0 时不得当成功。
    仅传输层不确定（超时/断连/DNS）才抛异常；HTTPError 属"有状态应答"，读出状态与错误体。"""
    req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode(),
                                 headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status = getattr(r, "status", None) or r.getcode()
            raw = r.read() or b""
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            raw = e.read() or b""
        except Exception:
            raw = b""
    try:
        parsed = json.loads(raw) if raw.strip() else None
    except ValueError:
        parsed = None
    return status, parsed


def _mock_reset():
    MOCK_STATS.update(token_calls=0, msg_posts=0, msg_uuids=[])


def _mock_transport(scenario):
    """离线回归用假通道：不读配置、不发网络，按场景模拟飞书返回。

    msg_posts 在调用入口即 +1——对应"服务器已收到 POST"先于回包返回/丢失的真实时序，
    用于验证消息阶段绝不自动重发。"""
    def call(url, body, headers, timeout=15):
        is_token_ep = "tenant_access_token" in url
        if is_token_ep:
            MOCK_STATS["token_calls"] += 1
        else:
            MOCK_STATS["msg_posts"] += 1
            MOCK_STATS["msg_uuids"].append(body.get("uuid"))
        if scenario == "ok":
            return ((200, {"code": 0, "tenant_access_token": "mock-token"}) if is_token_ep
                    else (200, {"code": 0, "data": {"message_id": "mock"}}))
        if scenario == "fail":  # 2xx + 业务码拒绝：确定性失败
            return ((200, {"code": 0, "tenant_access_token": "mock-token"}) if is_token_ep
                    else (200, {"code": 230001, "msg": "mock: receive_id 不可达"}))
        if scenario == "net":  # 消息 POST 回包丢失（服务器可能已收到）
            if is_token_ep:
                return 200, {"code": 0, "tenant_access_token": "mock-token"}
            raise urllib.error.URLError("mock: 读响应超时——服务器可能已收到")
        if scenario == "net_token":  # 取 token 瞬时失败一次（该阶段可安全重试）
            if is_token_ep and MOCK_STATS["token_calls"] == 1:
                raise urllib.error.URLError("mock: token 连接超时")
            if is_token_ep:
                return 200, {"code": 0, "tenant_access_token": "mock-token"}
            return 200, {"code": 0, "data": {"message_id": "mock"}}
        if scenario == "token_5xx":  # token 网关 5xx：按瞬时故障重试
            if is_token_ep and MOCK_STATS["token_calls"] == 1:
                return 502, None
            if is_token_ep:
                return 200, {"code": 0, "tenant_access_token": "mock-token"}
            return 200, {"code": 0, "data": {"message_id": "mock"}}
        if scenario == "token_rej":  # token 业务拒绝：凭据错误，不重试
            return 200, {"code": 10003, "msg": "mock: invalid app_id"}
        if scenario == "http500":  # 消息 POST 服务器 5xx：结果不确定
            if is_token_ep:
                return 200, {"code": 0, "tenant_access_token": "mock-token"}
            raise urllib.error.HTTPError(url, 500, "mock: Internal Server Error",
                                         {"Content-Type": "text/html"}, None)
        if scenario == "code0_502":  # 网关 502 且错误体碰巧 code=0：不得误判成功
            if is_token_ep:
                return 200, {"code": 0, "tenant_access_token": "mock-token"}
            return 502, {"code": 0}
        if scenario == "http4xx":  # 4xx 明确拒绝：确定性失败
            if is_token_ep:
                return 200, {"code": 0, "tenant_access_token": "mock-token"}
            return 403, {"code": 99991663, "msg": "mock: no permission"}
    return call


def send(text, transport=None, creds=None):
    """发送文本；返回 (outcome, detail)。

    outcome ∈ ok / rejected / unknown / token_failed：
      ok            = HTTP 2xx 且业务 code=0
      rejected      = 确定性拒绝（2xx+code!=0 或 4xx）——未投递，不重试
      unknown       = POST 结果不确定（传输异常/5xx/非法成功体）——未自动重发，需人工核对
      token_failed  = token 瞬时失败重试后仍失败——消息从未 POST，可安全补发
    token 阶段可自动重试（无投递副作用）；消息阶段只尝试一次。
    uuid 仅用于请求去重，不作为自动重发或已送达的依据。"""
    call = transport or _real_transport
    app_id, app_secret, owner = creds if creds else _cfg()

    # ---- 阶段一：取 token（该接口无投递副作用，失败可安全重试）----
    token, transient, definitive = None, "", ""
    for attempt in range(1 + TOKEN_RETRIES):
        try:
            status, d = call(FEISHU_TOKEN_URL,
                             {"app_id": app_id, "app_secret": app_secret},
                             {"Content-Type": "application/json"})
        except Exception as e:
            transient = f"{type(e).__name__}: {e}"
            if attempt < TOKEN_RETRIES:
                time.sleep(2)
                continue
            break
        success_http = isinstance(status, int) and 200 <= status < 300
        if (success_http and isinstance(d, dict) and d.get("code") == 0
                and isinstance(d.get("tenant_access_token"), str) and d["tenant_access_token"].strip()):
            token = d["tenant_access_token"]
            break
        if ((isinstance(status, int) and 400 <= status < 500)
                or (success_http and isinstance(d, dict) and d.get("code") not in (None, 0))):
            # 飞书明确业务拒绝（凭据/参数错误，官方惯例 200+code!=0）：确定性失败，重试无意义
            code = d.get("code") if isinstance(d, dict) else None
            msg = d.get("msg") if isinstance(d, dict) else None
            definitive = f"token 失败: {msg} (code {code}, HTTP {status})"
            break
        # 其余（传输异常/5xx/无法解析/缺 token 字段）按瞬时故障处理：
        # token 接口无投递副作用，重试不会重复发消息
        code = d.get("code") if isinstance(d, dict) else None
        transient = f"token 响应异常 (HTTP {status}, code {code})"
        if attempt < TOKEN_RETRIES:
            time.sleep(2)
            continue
        break
    if definitive:
        raise RuntimeError(definitive)  # 配置/凭据错误 → 退出码 2
    if token is None:
        return "token_failed", f"取 token 瞬时失败，消息未发出（未 POST 消息，可安全补发）：{transient}"

    # ---- 阶段二：发消息（只尝试一次；结果不确定禁止自动重发）----
    # 回包超时≠未送达：服务器可能已收到并投递。自动重试会造成同一汇总重复推送，
    # 因此传输层异常一律按 unknown 处理，落 outbox、退出码 3，交人工核对；
    # uuid 按官方文档用于请求去重；不据此假定真实投递结果或跳过人工核对。
    uuid = _msg_uuid(text)
    try:
        status, d = call(FEISHU_MSG_URL,
                         {"receive_id": owner, "msg_type": "text", "uuid": uuid,
                          "content": json.dumps({"text": text}, ensure_ascii=False)},
                         {"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    except Exception as e:
        return "unknown", (f"消息 POST 结果不确定（{type(e).__name__}: {e}）；"
                          f"可能已送达，未自动重发，需人工核对（uuid {uuid}）")
    if isinstance(d, dict) and d.get("code") == 0 and status is not None and 200 <= status < 300:
        return "ok", ""
    if status is not None and 400 <= status < 500:
        code = d.get("code") if isinstance(d, dict) else None
        msg = d.get("msg") if isinstance(d, dict) else None
        return "rejected", f"发送失败: {msg} (code {code}, HTTP {status})"
    if isinstance(d, dict) and d.get("code") not in (None, 0) and status is not None and 200 <= status < 300:
        return "rejected", f"发送失败: {d.get('msg')} (code {d.get('code')}, HTTP {status})"
    # 5xx / 状态缺失 / 非法成功体（非 2xx 却 code=0）/ 无法解析 → 结果不确定
    code = d.get("code") if isinstance(d, dict) else None
    return "unknown", (f"消息 POST 状态异常（HTTP {status}, code {code}）；不能确认是否已投递，"
                       f"未自动重发，需人工核对（uuid {uuid}）")


def _save_outbox(outbox: pathlib.Path, label: str, err: str, text: str):
    """按状态标签暂存失败内容：unknown 与确定失败的处理方式不同，提示必须区分。"""
    outbox.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    hint = _OUTBOX_HINTS[label]
    uuid = _msg_uuid(text)
    with outbox.open("a", encoding="utf-8") as f:
        f.write(f"\n## {ts} 【{label}】{err}\n\n> {hint}\n\n幂等键 uuid: {uuid}\n\n{text}\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="tokenmost 每小时汇总推送（飞书 bot DM）")
    ap.add_argument("--text", help="要发送的内容；缺省时从 stdin 读取")
    ap.add_argument("--mock", metavar="SCENARIO",
                    choices=("ok", "fail", "net", "net_token", "token_5xx", "token_rej",
                             "http500", "code0_502", "http4xx"),
                    help="离线自测：不读配置、不发网络，按场景模拟发送结果")
    ap.add_argument("--outbox", type=pathlib.Path, default=DEFAULT_OUTBOX,
                    help="发送失败时的内容暂存文件（默认 data-research/notify-outbox.md）")
    ap.add_argument("--selftest", action="store_true", help="离线自检：全 mock 场景走一遍")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        print("空消息不发送", file=sys.stderr)
        return EXIT_USAGE
    text = text.strip()
    if args.mock:
        transport, creds = _mock_transport(args.mock), ("mock-app", "mock-secret", "mock-owner")
    else:
        transport, creds = None, None  # send 内部读真实配置
    try:
        outcome, detail = send(text, transport=transport, creds=creds)
    except RuntimeError as e:  # 配置/凭据错误：消息未进入发送流程，不暂存
        print(f"配置错误: {e}", file=sys.stderr)
        return EXIT_USAGE
    if outcome == "ok":
        print("✓ 已发送")
        return EXIT_OK
    label = {"token_failed": "未送达·取token失败", "rejected": "未送达·确定失败"}.get(
        outcome, "unknown·结果不确定")
    try:
        _save_outbox(args.outbox, label, detail, text)
        saved = f"内容已暂存 {args.outbox}"
    except OSError as e:
        # 本地落盘失败不能把 unknown 的退出码降为 1，否则外层可能自动重发。
        saved = f"outbox 保存失败（{type(e).__name__}），请人工保留输入并核对投递结果"
    if outcome == "token_failed":
        print(f"✗ 失败: {detail}（{saved}，消息未 POST）", file=sys.stderr)
        return EXIT_FAIL
    if outcome == "rejected":
        print(f"✗ 失败: {detail}（{saved}，处理原因后可补发）", file=sys.stderr)
        return EXIT_FAIL
    print(f"? 结果不确定: {detail}（可能已送达，{saved}；请先在飞书核对，勿盲目重发）",
          file=sys.stderr)
    return EXIT_UNKNOWN


def selftest() -> int:
    """离线全场景自检：退出码、消息 POST 次数、token 调用数、幂等键稳定性。

    关键断言：任何场景消息 POST ≤ 1 次——传输异常绝不自动重发（v1 缺陷回归）。"""
    expected = {
        "ok": (EXIT_OK, 1, 1), "fail": (EXIT_FAIL, 1, 1), "net": (EXIT_UNKNOWN, 1, 1),
        "net_token": (EXIT_OK, 1, 2), "token_5xx": (EXIT_OK, 1, 2),
        "token_rej": (EXIT_USAGE, 0, 1), "http500": (EXIT_UNKNOWN, 1, 1),
        "code0_502": (EXIT_UNKNOWN, 1, 1), "http4xx": (EXIT_FAIL, 1, 1),
    }
    with tempfile.TemporaryDirectory() as td:
        for scen, (exp_rc, exp_posts, exp_tokens) in expected.items():
            outbox = pathlib.Path(td) / f"outbox-{scen}.md"
            _mock_reset()
            rc = main(["--text", f"selftest 内容 {scen}", "--mock", scen, "--outbox", str(outbox)])
            assert rc == exp_rc, f"场景 {scen}: 期望退出码 {exp_rc}，实际 {rc}"
            assert MOCK_STATS["msg_posts"] == exp_posts, \
                f"场景 {scen}: 消息 POST {MOCK_STATS['msg_posts']} 次，期望 {exp_posts}（结果不确定绝不自动重发）"
            assert MOCK_STATS["token_calls"] == exp_tokens, \
                f"场景 {scen}: token 调用 {MOCK_STATS['token_calls']} 次，期望 {exp_tokens}"
            if exp_rc == EXIT_OK:
                assert not outbox.exists(), f"场景 {scen}: 成功不应写 outbox"
            if exp_posts:
                u = MOCK_STATS["msg_uuids"][0]
                assert u and u.startswith("tm-") and len(u) <= 50, f"场景 {scen}: 幂等键非法 {u!r}"
        # 幂等键稳定性：同内容同键，不同内容不同键
        _mock_reset()
        main(["--text", "同一段汇总", "--mock", "fail", "--outbox", str(pathlib.Path(td) / "a.md")])
        u1 = MOCK_STATS["msg_uuids"][0]
        _mock_reset()
        main(["--text", "同一段汇总", "--mock", "net", "--outbox", str(pathlib.Path(td) / "b.md")])
        u2 = MOCK_STATS["msg_uuids"][0]
        _mock_reset()
        main(["--text", "另一段汇总", "--mock", "fail", "--outbox", str(pathlib.Path(td) / "c.md")])
        u3 = MOCK_STATS["msg_uuids"][0]
        assert u1 == u2 and u1 != u3, "幂等键必须内容稳定：同内容同键、不同内容不同键"
    print("selftest OK: 9 场景退出码/POST 次数/幂等键全部符合约定（消息阶段绝不自动重发；token 阶段可安全重试）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
