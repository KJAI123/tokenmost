#!/usr/bin/env python3
"""guides/*.md → guides/<id>.html（站内深色样式攻略页）+ guides/index.json 清单。
被 check.py 末尾调用；pages.yml 需复制 guides/ 目录。纯标准库。"""
import json
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GDIR = ROOT / "guides"
OUT = GDIR

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — tokenmost 攻略</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tokenmost.com/guides/{gid}.html">
<meta property="og:title" content="{title} — tokenmost 攻略">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://tokenmost.com/guides/{gid}.html">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}","description":"{desc}","url":"https://tokenmost.com/guides/{gid}.html","inLanguage":"zh-CN","publisher":{{"@type":"Organization","name":"tokenmost.com","url":"https://tokenmost.com/"}}}}
</script>
<style>
:root{{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#00e5a0;--amber:#d29922;--red:#f85149}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font:15px/1.75 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif;max-width:760px;margin:0 auto;padding:28px 18px 80px}}
a{{color:#58a6ff}}
h1{{font-size:1.5rem;color:var(--accent);margin-bottom:6px}}
.meta{{color:var(--muted);font-size:.8rem;margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--border)}}
h2{{font-size:1.1rem;margin:22px 0 8px;color:var(--accent)}}
h3{{font-size:.98rem;margin:16px 0 6px}}
ol,ul{{padding-left:22px;margin:8px 0}}
li{{margin:5px 0}}
code{{background:#0a0e14;border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:.85em;font-family:monospace;color:#c9d1d9;word-break:break-all}}
pre{{background:#0a0e14;border:1px solid var(--border);border-radius:9px;padding:12px;overflow-x:auto;margin:10px 0}}
pre code{{border:none;padding:0}}
.warn{{background:rgba(248,81,73,.08);border:1px solid var(--red);border-radius:9px;padding:10px 14px;margin:12px 0;font-size:.9rem}}
.tip{{background:rgba(0,229,160,.06);border:1px solid var(--accent);border-radius:9px;padding:10px 14px;margin:12px 0;font-size:.9rem}}
table{{border-collapse:collapse;width:100%;margin:10px 0;font-size:.86rem}}
th,td{{border:1px solid var(--border);padding:6px 10px;text-align:left}}
th{{background:var(--card)}}
.back{{display:inline-block;margin-bottom:16px;color:var(--muted);font-size:.85rem}}
.src{{color:var(--muted);font-size:.78rem;margin-top:26px;padding-top:12px;border-top:1px solid var(--border)}}
</style></head><body>
<a class="back" href="/">← 回 tokenmost 情报流</a>
{body}
</body></html>"""


def md2html(md: str) -> str:
    lines = md.split("\n")
    out, in_code, code_buf = [], False, []
    for ln in lines:
        if ln.strip().startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
            in_code = not in_code
            continue
        if in_code:
            code_buf.append(ln)
            continue
        s = ln.rstrip()
        # 警示/提示块
        if s.startswith("⚠️"):
            out.append('<div class="warn">' + s + "</div>")
            continue
        if s.startswith("💡"):
            out.append('<div class="tip">' + s + "</div>")
            continue
        if s.startswith("### "):
            out.append("<h3>" + s[4:] + "</h3>")
        elif s.startswith("## "):
            out.append("<h2>" + s[3:] + "</h2>")
        elif s.startswith("# "):
            out.append("<h1>" + s[2:] + "</h1>")
        elif re.match(r"^\d+\. ", s):
            n, rest = s.split(". ", 1)
            out.append(f"<ol start='{n}' style='margin:0;padding-left:22px'><li>{rest}</li></ol>")
        elif s.startswith("- "):
            out.append("<ul style='margin:0;padding-left:22px'><li>" + s[2:] + "</li></ul>")
        elif s.startswith("|"):
            out.append(s)  # 表格行原样，稍后包裹
        elif not s:
            out.append("")
        else:
            out.append("<p>" + s + "</p>")
    # 行内 code / 加粗 / 链接
    text = "\n".join(out)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener nofollow">\1</a>', text)
    # 连续表格行包 table
    text = re.sub(r"((?:^\|.*\|\n?)+)", lambda m: "<table>" + m.group(1).replace("\n\n", "\n") + "</table>", text, flags=re.M)
    return text


def main():
    if not GDIR.exists():
        print("guides/ 不存在，跳过")
        return
    index = []
    for f in sorted(GDIR.glob("*.md")):
        md = f.read_text(encoding="utf-8")
        title = md.split("\n")[0].lstrip("# ").strip() if md.startswith("#") else f.stem
        body = md2html(md)
        desc = ""
        m = re.search(r"\n(?!#|\n)([^\n]{20,90})", md)
        if m:
            desc = re.sub(r"[⚠️💡#*`>|]", "", m.group(1)).strip()[:80]
        (OUT / (f.stem + ".html")).write_text(
            TEMPLATE.format(title=html.escape(title), body=body,
                            desc=html.escape(desc, quote=True), gid=f.stem), encoding="utf-8")
        index.append({"id": f.stem, "title": title, "desc": desc})
        print(f"  {f.stem}.html ← {title[:40]}")
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"guides: {len(index)} 篇已构建")


if __name__ == "__main__":
    main()
