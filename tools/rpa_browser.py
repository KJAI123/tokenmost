# -*- coding: utf-8 -*-
"""
rpa_browser.py — OCR-CDP-RPA 三合一浏览器自动化助手（TokenMost SEO 线）
老板纪律（2026-11-14）：浏览器动作一律 OCR+CDP+RPA 结合——
  CDP  = JS 求值/导航/输入事件（Input.insertText 真实管线）
  RPA  = 真实鼠标/键盘事件模拟（dispatchMouseEvent / dispatchKeyEvent）
  OCR  = macOS Vision 截图识别（rpa_ocr.js），DOM 够不着的（CF 盾/验证码/canvas/渲染验证）用 OCR 定位与核验
铁律：所有对外内容必须植入 tokenmost.com（自然植入，不硬广）。

用法（py3.9 兼容）：
  from rpa_browser import Tab
  tab = Tab.connect(url_frag='v2ex.com')      # 连已有标签（fragment 匹配 URL）
  tab.activate()                              # CF 盾必先激活到前台
  tab.screenshot('/tmp/x.png')                # 截图
  text = tab.ocr('/tmp/x.png')                # OCR 文本
  box = tab.ocr_find('/tmp/x.png', '登录')    # OCR 定位关键词 → 视口坐标
  tab.click(x, y)                             # RPA 真实点击
  tab.type_text('你好')                       # CDP insertText（落点=当前光标）
  tab.click_text('发布')                      # OCR+DOM 混合：DOM 定位失败回退 OCR 坐标
"""
import base64
import json
import os
import subprocess
import time
import urllib.request
import websocket

CDP_HTTP = "http://127.0.0.1:9222"
HERE = os.path.dirname(os.path.abspath(__file__))
OCR_JS = os.path.join(HERE, "rpa_ocr.js")


class Tab(object):
    def __init__(self, target, ws):
        self.tid = target["id"]
        self.url = target.get("url", "")
        self.ws = ws
        self._mid = [0]

    # ---------- 连接管理 ----------
    @classmethod
    def connect(cls, url_frag=None, new_url=None, wait=8):
        """连已有标签（url_frag 子串匹配）；或 new_url 开新标签。"""
        if new_url:
            req = urllib.request.Request(CDP_HTTP + "/json/new?" + new_url, method="PUT")
            urllib.request.urlopen(req, timeout=8).read()
            url_frag = url_frag or new_url.split("//")[-1].split("/")[0]
            time.sleep(wait)
        ts = json.loads(urllib.request.urlopen(CDP_HTTP + "/json", timeout=5).read())
        tgt = None
        for t in ts:
            if t.get("type") != "page":
                continue
            if url_frag is None or url_frag in t.get("url", ""):
                tgt = t
                break
        if tgt is None:
            raise RuntimeError("no tab matching %r" % url_frag)
        ws = websocket.create_connection(tgt["webSocketDebuggerUrl"], timeout=120)
        return cls(tgt, ws)

    def activate(self):
        """把标签带到前台——CF 盾在后台标签会卡死，先激活再等。"""
        req = urllib.request.Request(CDP_HTTP + "/json/activate/" + self.tid, method="PUT")
        urllib.request.urlopen(req, timeout=8).read()

    def close(self):
        try:
            urllib.request.urlopen(CDP_HTTP + "/json/close/" + self.tid, timeout=8).read()
        except Exception:
            pass
        try:
            self.ws.close()
        except Exception:
            pass

    # ---------- CDP 基元 ----------
    def send(self, method, params=None):
        self._mid[0] += 1
        i = self._mid[0]
        self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == i:
                return m.get("result", {})

    def ev(self, expr):
        """JS 求值；异常返回 {'__exc': ...}。"""
        r = self.send("Runtime.evaluate",
                      {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in r:
            d = r["exceptionDetails"]
            desc = (d.get("exception", {}).get("description") or d.get("text") or "")[:200]
            return {"__exc": desc}
        return r.get("result", {}).get("value")

    def navigate(self, url, wait=6):
        self.send("Page.navigate", {"url": url})
        time.sleep(wait)

    def reload(self, wait=7):
        self.send("Page.reload")
        time.sleep(wait)

    def wait_cf(self, timeout_s=60, poll=6):
        """等 Cloudflare 盾放行（配合 activate 使用）。"""
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            ttl = str(self.ev("document.title") or "")
            if "请稍候" not in ttl and "moment" not in ttl.lower():
                return True
            time.sleep(poll)
        return False

    # ---------- RPA：真实输入 ----------
    def mouse(self, kind, x, y, **kw):
        p = {"type": kind, "x": x, "y": y, "button": "left", "clickCount": 1}
        p.update(kw)
        self.send("Input.dispatchMouseEvent", p)

    def click(self, x, y):
        self.mouse("mousePressed", x, y)
        self.mouse("mouseReleased", x, y)

    def key(self, code, vk, mods=0):
        for t in ("keyDown", "keyUp"):
            self.send("Input.dispatchKeyEvent",
                      {"type": t, "windowsVirtualKeyCode": vk, "code": code,
                       "key": code, "modifiers": mods})

    def type_text(self, text):
        """真实输入管线（Draft.js/受控组件唯一可靠路径）。落点=当前光标。"""
        self.send("Input.insertText", {"text": text})

    def select_all(self):
        for t in ("keyDown", "keyUp"):
            self.send("Input.dispatchKeyEvent",
                      {"type": t, "commands": ["selectAll"], "windowsVirtualKeyCode": 65,
                       "code": "KeyA", "key": "a", "modifiers": 4})

    # ---------- OCR ----------
    def screenshot(self, path):
        r = self.send("Page.captureScreenshot", {"format": "png"})
        with open(path, "wb") as f:
            f.write(base64.b64decode(r["data"]))
        return path

    def ocr(self, png_path):
        """整页 OCR → 文本行列表。"""
        out = self._ocr_raw(png_path)
        return [l["text"] for l in out.get("lines", [])]

    def ocr_find(self, png_path, keyword):
        """OCR 定位关键词 → {x, y, w, h}（视口坐标，命中块左上角+尺寸）或 None。"""
        out = self._ocr_raw(png_path)
        for l in out.get("lines", []):
            if keyword in l.get("text", "") and "x" in l:
                return l
        return None

    def _ocr_raw(self, png_path):
        # PNG 尺寸（IHDR：宽在偏移16，高在偏移20）+ 视口尺寸 → DPR 换算
        with open(png_path, "rb") as f:
            head = f.read(24)
        import struct
        png_w, png_h = struct.unpack(">II", head[16:24])
        dim = self.ev("JSON.stringify({w: innerWidth, h: innerHeight})") or "{}"
        try:
            dim = json.loads(dim)
        except Exception:
            dim = {"w": png_w, "h": png_h}
        vw = float(dim.get("w") or png_w)
        dpr = png_w / vw if vw else 1.0  # retina 截图=视口 2 倍
        cmd = ["osascript", "-l", "JavaScript", OCR_JS, png_path,
               str(png_w), str(png_h)]
        raw = subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
        try:
            data = json.loads(raw)
        except Exception:
            return {"n": 0, "lines": []}
        # 坐标从图像像素换算回视口像素
        for l in data.get("lines", []):
            for k in ("x", "y", "w", "h"):
                if k in l:
                    l[k] = int(round(l[k] / dpr))
        return data

    # ---------- 混合定位 ----------
    def click_text(self, text, prefer_ocr=False):
        """OCR+DOM 混合点击：先 DOM 精确定位（零宽字符归一化），失败回退 OCR 坐标。"""
        if not prefer_ocr:
            hit = self.ev("""((mm) => {
              const norm = s => (s||'').replace(/\u200b/g,'').trim();
              const c = [...document.querySelectorAll('button, a, [role="button"]')]
                .filter(b => b.offsetWidth > 0 && norm(b.textContent) === mm);
              if (!c.length) return null;
              const rc = c[0].getBoundingClientRect();
              return { x: rc.x + rc.width/2, y: rc.y + rc.height/2, how: 'dom' };
            })(%s)""" % json.dumps(text))
            if isinstance(hit, dict) and "x" in hit:
                self.click(hit["x"], hit["y"])
                return hit
        png = "/tmp/rpa_shot_%d.png" % int(time.time())
        self.screenshot(png)
        box = self.ocr_find(png, text)
        if box:
            cx, cy = box["x"] + box["w"] // 2, box["y"] + box["h"] // 2
            self.click(cx, cy)
            return {"x": cx, "y": cy, "how": "ocr"}
        return None
