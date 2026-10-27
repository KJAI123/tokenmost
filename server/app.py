# -*- coding: utf-8 -*-
"""tokenmost 后端（v0.9）——折扣码众包托管服务。

功能（老板 2026-10-27 拍板）：
- 账号系统：手机号 + 密码注册/登录（HMAC token，纯标准库，零外部依赖）
- 折扣码托管：用户提交 → GLM-4.7-Flash（免费档）自动初审 + 管理员终审 → 上架
- 复制计数：每次复制 +1（同人同日去重）；达到提交者设定的上限自动下架
- 我的码：提交者可看到自己的码被复制的次数

运行：
    pip install -r requirements.txt
    ZHIPU_API_KEY=sk-xxx ADMIN_TOKEN=changeit uvicorn app:app --port 8001
    （不配 ZHIPU_API_KEY 时提交一律进 pending 人工审；ADMIN_TOKEN 用于终审接口）
"""
import os
import re
import json
import hmac
import hashlib
import sqlite3
import base64
import urllib.request
import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

APP_VERSION = "0.9.0"
DB_PATH = os.environ.get("TM_DB", os.path.join(os.path.dirname(__file__), "tokenmost.db"))
SECRET = os.environ.get("TM_SECRET", "dev-secret-change-me")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
FLASH_MODELS = os.environ.get("FLASH_MODELS", "glm-4.7-flash,glm-z1-flash").split(",")  # 免费档降级链（4.7 高峰易过载，z1 兜底）
FLASH_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

app = FastAPI(title="tokenmost API", version=APP_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)

# ---------------- DB ----------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  phone TEXT UNIQUE NOT NULL,
  pw_hash TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS coupons(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id),
  provider TEXT NOT NULL,          -- 平台名，须能对上 sites.json 的站名（前端下拉保证）
  code TEXT NOT NULL,
  note TEXT DEFAULT '',
  max_copies INTEGER NOT NULL DEFAULT 50,
  copies INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'pending',  -- pending/active/unlisted/rejected
  flash_verdict TEXT DEFAULT '',
  review_note TEXT DEFAULT '',
  created_at TEXT NOT NULL,
  kind TEXT NOT NULL DEFAULT 'code'  -- code=折扣码 | link=折扣链接（code 字段存 URL）
);
CREATE TABLE IF NOT EXISTS copy_events(
  coupon_id INTEGER NOT NULL REFERENCES coupons(id),
  actor TEXT NOT NULL,             -- user:<id> 或 ip:<hash>；同人同日只计一次
  day TEXT NOT NULL,
  UNIQUE(coupon_id, actor, day)
);
"""

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

@app.on_event("startup")
def startup():
    c = conn()
    c.executescript(SCHEMA)
    cols = [r[1] for r in c.execute("PRAGMA table_info(coupons)").fetchall()]
    if "kind" not in cols:
        c.execute("ALTER TABLE coupons ADD COLUMN kind TEXT NOT NULL DEFAULT 'code'")
    c.close()

# ---------------- 认证（标准库实现） ----------------

def hash_pw(pw: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 100_000)
    return base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()

def check_pw(pw: str, stored: str) -> bool:
    try:
        salt_b64, dk_b64 = stored.split("$")
        salt = base64.b64decode(salt_b64)
        dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 100_000)
        return hmac.compare_digest(dk, base64.b64decode(dk_b64))
    except Exception:
        return False

def make_token(user_id: int) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"u": user_id, "t": datetime.datetime.utcnow().timestamp()}).encode()).decode()
    sig = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:32]
    return payload + "." + sig

def parse_token(token: str) -> Optional[int]:
    try:
        payload, sig = token.split(".")
        good = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:32]
        if not hmac.compare_digest(sig, good):
            return None
        data = json.loads(base64.urlsafe_b64decode(payload))
        # 30 天有效期
        if datetime.datetime.utcnow().timestamp() - data["t"] > 30 * 86400:
            return None
        return int(data["u"])
    except Exception:
        return None

def current_user(authorization: str = Header(default="")) -> int:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "请先登录")
    uid = parse_token(authorization[7:])
    if uid is None:
        raise HTTPException(401, "登录已过期，请重新登录")
    return uid

# ---------------- Flash 自动初审（免费档 GLM-4.7-Flash） ----------------

RISK_WORDS = ["多号", "小号", "批量", "代充", "合租", "共享号", "接码", "破解", "漏洞", "薅到平台倒闭"]

def flash_review(provider: str, code: str, note: str, kind: str = "code") -> Dict[str, Any]:
    """用 GLM-4.7-Flash（免费档）初审用户提交。返回 {verdict, ok}。
    无 KEY 或调用失败 → ok=None（转人工）。"""
    if not ZHIPU_API_KEY:
        return {"verdict": "未配置审核模型，转人工", "ok": None}
    prompt = (
        "你是折扣优惠信息合规审核员。判断以下用户提交的%s是否可上架：\n"
        "平台：%s\n内容：%s\n说明：%s\n" % ("折扣链接（仅允许官方/授权推广链接）" if kind == "link" else "折扣码", provider, code[:120], note[:200]) + "\n"
        "规则：只允许官方/授权渠道折扣码；涉黑产话术（多号/批量/代充/共享/接码/漏洞）或明显乱码、广告、联系方式 → 拒绝。\n"
        "只输出 JSON：{\"ok\": true} 或 {\"ok\": false, \"reason\": \"一句话\"}"
    )
    try:
        text = ""
        for model in FLASH_MODELS:
            body = json.dumps({
                "model": model.strip(),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
            }).encode()
            req = urllib.request.Request(FLASH_URL, data=body, headers={
                "Content-Type": "application/json", "Authorization": "Bearer " + ZHIPU_API_KEY})
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    text = json.loads(r.read())["choices"][0]["message"]["content"]
                break  # 拿到内容即用；下一个模型只在请求失败时兜底
            except Exception as e:
                last_err = e
                continue
        if not text:
            return {"verdict": "审核模型过载（%s），转人工" % type(last_err).__name__, "ok": None}
        # z1 系思考型模型输出含 <think>，取含 "ok" 键的最后一个 JSON 对象
        verdict = {}
        for m in re.finditer(r"\{[^{}]*\}", text):
            try:
                cand = json.loads(m.group(0))
                if isinstance(cand, dict) and "ok" in cand:
                    verdict = cand
            except Exception:
                continue
        if verdict.get("ok") is True:
            # 规则兜底：黑名单词直接拒，模型只是第二道
            if any(w in (note + code) for w in RISK_WORDS):
                return {"verdict": "命中黑名单话术", "ok": False}
            return {"verdict": "Flash 初审通过", "ok": True}
        return {"verdict": "Flash 拒绝：" + str(verdict.get("reason", ""))[:80], "ok": False}
    except Exception as e:
        return {"verdict": "审核调用失败（%s），转人工" % type(e).__name__, "ok": None}

# ---------------- 模型 ----------------

class AuthBody(BaseModel):
    phone: str = Field(..., pattern=r"^1\d{10}$", description="手机号")
    password: str = Field(..., min_length=6, max_length=64)

class CouponCreate(BaseModel):
    provider: str = Field(..., min_length=2, max_length=40)
    code: str = Field(..., min_length=3, max_length=300)  # kind=link 时存完整 URL
    note: str = Field("", max_length=200)
    max_copies: int = Field(50, ge=1, le=10000)
    kind: str = Field("code", pattern="^(code|link)$")

    @field_validator("code")
    @classmethod
    def code_clean(cls, v):
        if re.search(r"\s{2,}", v):
            raise ValueError("别带连续空格")
        return v.strip()

    @field_validator("kind")
    @classmethod
    def link_must_be_url(cls, v, info):
        if v == "link":
            data = info.data
            code = data.get("code", "")
            if not code.startswith(("http://", "https://")):
                raise ValueError("折扣链接必须以 http(s):// 开头")
        return v

# ---------------- 接口 ----------------

@app.get("/api/health")
def health():
    try:
        conn().execute("SELECT 1").fetchone()
        return {"status": "ok", "version": APP_VERSION, "flash": bool(ZHIPU_API_KEY)}
    except Exception as e:
        raise HTTPException(503, str(e))

@app.post("/api/auth/register")
def register(body: AuthBody):
    c = conn()
    try:
        c.execute("INSERT INTO users(phone, pw_hash, created_at) VALUES (?,?,?)",
                  (body.phone, hash_pw(body.password), datetime.datetime.utcnow().isoformat()))
        c.commit()
        uid = c.execute("SELECT id FROM users WHERE phone=?", (body.phone,)).fetchone()["id"]
        return {"token": make_token(uid), "phone": body.phone}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "该手机号已注册，直接登录")
    finally:
        c.close()

@app.post("/api/auth/login")
def login(body: AuthBody):
    c = conn()
    try:
        row = c.execute("SELECT id, pw_hash FROM users WHERE phone=?", (body.phone,)).fetchone()
        if not row or not check_pw(body.password, row["pw_hash"]):
            raise HTTPException(401, "手机号或密码不对")
        return {"token": make_token(row["id"]), "phone": body.phone}
    finally:
        c.close()

@app.post("/api/coupons", status_code=201)
def submit_coupon(body: CouponCreate, uid: int = Depends(current_user)):
    """提交托管折扣码。Flash 初审通过 → 直接上架（active）；拒绝 → rejected；无审核 → pending 人工。"""
    v = flash_review(body.provider, body.code, body.note, body.kind)
    status = {True: "active", False: "rejected", None: "pending"}[v["ok"]]
    c = conn()
    try:
        cur = c.execute(
            "INSERT INTO coupons(user_id, provider, code, note, max_copies, status, flash_verdict, created_at, kind)"
            " VALUES (?,?,?,?,?,?,?,?,?)",
            (uid, body.provider.strip(), body.code.strip(), body.note.strip(),
             body.max_copies, status, v["verdict"], datetime.datetime.utcnow().isoformat(), body.kind))
        c.commit()
        return {"id": cur.lastrowid, "status": status, "review": v["verdict"],
                "message": {"active": "✅ Flash 初审通过，已上架",
                            "pending": "⏳ 已提交，待人工审核后上架",
                            "rejected": "❌ 未通过初审：" + v["verdict"]}[status]}
    finally:
        c.close()

@app.get("/api/coupons/public")
def public_coupons(provider: Optional[str] = Query(None)):
    """已上架共享码。provider 可选：传则查单平台（卡片小窗）；不传返回全量（首页按钮标记用）。"""
    c = conn()
    try:
        if provider:
            rows = c.execute(
                "SELECT id, provider, code, note, max_copies, copies, created_at, kind FROM coupons"
                " WHERE provider=? AND status='active' AND copies < max_copies"
                " ORDER BY id DESC LIMIT 20", (provider,)).fetchall()
        else:
            rows = c.execute(
                "SELECT id, provider, code, note, max_copies, copies, created_at, kind FROM coupons"
                " WHERE status='active' AND copies < max_copies"
                " ORDER BY id DESC LIMIT 100").fetchall()
        return {"items": [dict(r, remaining=r["max_copies"] - r["copies"]) for r in rows]}
    finally:
        c.close()

@app.post("/api/coupons/{coupon_id}/copy")
def copy_coupon(coupon_id: int, authorization: str = Header(default=""), x_forwarded_for: str = Header(default="")):
    """复制计数：同人同日去重；达到上限自动下架。返回完整码。"""
    token = authorization[7:] if authorization.startswith("Bearer ") else ""
    uid = parse_token(token)
    actor = ("user:%d" % uid) if uid else ("ip:" + hashlib.sha256((x_forwarded_for or "anon").encode()).hexdigest()[:16])
    today = datetime.datetime.utcnow().date().isoformat()
    c = conn()
    try:
        row = c.execute("SELECT * FROM coupons WHERE id=? AND status='active'", (coupon_id,)).fetchone()
        if not row:
            raise HTTPException(404, "码不存在或已下架")
        first = c.execute("SELECT 1 FROM copy_events WHERE coupon_id=? AND actor=? AND day=?",
                          (coupon_id, actor, today)).fetchone() is None
        if first:
            c.execute("INSERT OR IGNORE INTO copy_events VALUES (?,?,?)", (coupon_id, actor, today))
            c.execute("UPDATE coupons SET copies=copies+1 WHERE id=?", (coupon_id,))
            copies = c.execute("SELECT copies FROM coupons WHERE id=?", (coupon_id,)).fetchone()["copies"]
            if copies >= row["max_copies"]:  # 超限自动下架
                c.execute("UPDATE coupons SET status='unlisted', review_note='复制次数达上限，自动下架' WHERE id=?", (coupon_id,))
        c.commit()
        fresh = c.execute("SELECT code, copies, max_copies, status FROM coupons WHERE id=?", (coupon_id,)).fetchone()
        return {"code": fresh["code"], "copies": fresh["copies"], "max": fresh["max_copies"], "status": fresh["status"]}
    finally:
        c.close()

@app.get("/api/my/coupons")
def my_coupons(uid: int = Depends(current_user)):
    """我的码 + 被复制次数（托管者的核心诉求）。"""
    c = conn()
    try:
        rows = c.execute(
            "SELECT id, provider, code, note, max_copies, copies, status, flash_verdict, created_at, kind"
            " FROM coupons WHERE user_id=? ORDER BY id DESC", (uid,)).fetchall()
        return {"items": [dict(r, remaining=r["max_copies"] - r["copies"]) for r in rows]}
    finally:
        c.close()

@app.delete("/api/coupons/{coupon_id}")
def delete_coupon(coupon_id: int, uid: int = Depends(current_user)):
    c = conn()
    try:
        n = c.execute("UPDATE coupons SET status='unlisted', review_note='提交者主动下架'"
                      " WHERE id=? AND user_id=? AND status!='unlisted'", (coupon_id, uid)).rowcount
        c.commit()
        if not n:
            raise HTTPException(404, "码不存在或已下架")
        return {"ok": True}
    finally:
        c.close()

# ---- 管理员（终审 pending / 复活误杀） ----

@app.post("/api/admin/coupons/{coupon_id}")
def admin_review(coupon_id: int, action: str = Query(..., pattern="^(active|rejected)$"),
                 x_admin_token: str = Header(default="")):
    if not ADMIN_TOKEN or x_admin_token != ADMIN_TOKEN:
        raise HTTPException(403, "需要 ADMIN_TOKEN")
    c = conn()
    try:
        n = c.execute("UPDATE coupons SET status=? WHERE id=? AND status IN ('pending','unlisted')",
                      (action, coupon_id)).rowcount
        c.commit()
        if not n:
            raise HTTPException(404, "无此待审码")
        return {"ok": True, "status": action}
    finally:
        c.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
