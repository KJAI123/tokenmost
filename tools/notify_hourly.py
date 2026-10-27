#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""notify_hourly.py — tokenmost 每小时汇总推送（经龙虾 OpenClaw 的飞书 bot DM 老板）

用法: python3 tools/notify_hourly.py --text "汇总内容"
      echo "内容" | python3 tools/notify_hourly.py
凭据只从本机 ~/.openclaw/openclaw.json 读取，不打印不外传。
微信侧无主动通道（微信客服 bot 官方限制不能主动发消息），故走飞书 bot。
"""
import json, sys, urllib.request, pathlib

CFG = pathlib.Path.home() / ".openclaw/openclaw.json"

def _cfg():
    c = json.loads(CFG.read_text())["channels"]["feishu"]
    owner = next((k for k, v in c.get("dms", {}).items() if v.get("enabled")), None)
    if not owner:
        raise SystemExit("未找到启用的飞书 DM 目标")
    return c["appId"], c["appSecret"], owner

def _token(app_id, app_secret):
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    if d.get("code") != 0:
        raise SystemExit(f"token 失败: {d.get('msg')}")
    return d["tenant_access_token"]

def send(text):
    app_id, app_secret, owner = _cfg()
    body = {"receive_id": owner, "msg_type": "text",
            "content": json.dumps({"text": text}, ensure_ascii=False)}
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps(body, ensure_ascii=False).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {_token(app_id, app_secret)}"})
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return d.get("code") == 0, d.get("msg", "")

if __name__ == "__main__":
    text = sys.argv[sys.argv.index("--text") + 1] if "--text" in sys.argv else sys.stdin.read()
    if not text.strip():
        raise SystemExit("空消息不发送")
    ok, msg = send(text.strip())
    print("✓ 已发送" if ok else f"✗ 失败: {msg}")
