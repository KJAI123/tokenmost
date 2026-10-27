#!/usr/bin/env python3
"""信源内容验证器（零 token）：对候选/长期源逐个抓内容，判定是否真的在聊「羊毛」。
验证分级：relevant(内容相关) / offtopic(可达但无关) / dead(不可达)。
结果回写 source_candidates.json 与 Excel 两个 sheet。可多轮跑，--limit 控制批量。"""
from __future__ import annotations
import concurrent.futures as cf
import json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAND = ROOT / "data-research" / "source_candidates.json"
XLSX = ROOT / "data-research" / "信息源总表-全量版.xlsx"
UA = "tokenmost-harvest/0.1 (+https://tokenmost.com; source-verification research bot)"
KW = re.compile(r"免费|额度|羊毛|白嫖|赠送|折扣码|签到|token|free|credit|tier|pricing|coupon|promo", re.I)

def fetch(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read(300_000).decode("utf-8", "ignore")
    except Exception:
        return ""

def verify_one(url: str) -> tuple[str, str]:
    body = fetch(url)
    if not body:
        return "dead", ""
    title = ""
    m = re.search(r"<title[^>]*>([^<]{2,120})", body)
    if m:
        title = m.group(1).strip()
    text = re.sub(r"<[^>]+>", " ", body)
    n = len(KW.findall(text))
    if n >= 3:
        return "relevant", title
    if n >= 1:
        return "weak", title
    return "offtopic", title

def main() -> int:
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 250
    data = json.loads(CAND.read_text(encoding="utf-8"))
    cands = data["candidates"]
    # 优先验证：长期源标准（score>=5 且 200）→ 其次其余 200 的
    todo = [c for c in cands if c.get("status") == 200 and not c.get("verified")]
    todo.sort(key=lambda c: -c.get("score", 0))
    todo = todo[:limit]
    print(f"待验证: {len(todo)}（--limit 可调）")
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(verify_one, c["url"]): c for c in todo}
        for i, f in enumerate(cf.as_completed(futs), 1):
            c = futs[f]
            try:
                v, title = f.result()
            except Exception:
                v, title = "dead", c.get("title", "")
            c["verified"] = v
            if title and not c.get("title"):
                c["title"] = title
            if i % 50 == 0:
                print(f"进度 {i}/{len(todo)}")
    data["verified_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    CAND.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    stats = {}
    for c in cands:
        if c.get("verified"):
            stats[c["verified"]] = stats.get(c["verified"], 0) + 1
    print(f"验证统计（累计）: {stats}")

    # 回写 Excel
    from openpyxl import load_workbook
    wb = load_workbook(XLSX)
    vmap = {c["url"]: c.get("verified", "") for c in cands if c.get("verified")}
    for sheet_name in ("候选源池", "长期源清单"):
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        hdr = [c.value for c in ws[1]]
        if "验证" not in hdr:
            from openpyxl.styles import Font as _F, PatternFill as _P
            h = ws.cell(row=1, column=len(hdr) + 1, value="验证")
            h.font = _F(bold=True, color="FFFFFF"); h.fill = _P("solid", fgColor="1F6F4A")
        col = hdr.index("验证") + 1 if "验证" in hdr else len(hdr) + 1
        for row in range(2, ws.max_row + 1):
            u = ws.cell(row=row, column=1).value
            if u and u in vmap:
                ws.cell(row=row, column=col, value=vmap[u])
    wb.save(XLSX)
    print("Excel 验证列已回写")
    return 0

if __name__ == "__main__":
    sys.exit(main())
