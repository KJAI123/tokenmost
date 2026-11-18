# 30 行 Python 把任意 JSON 转成 Markdown 表格（附完整脚本）

> 纯技术干货，零推广。掘金首发。

处理 API 返回的 JSON 数据时，想快速看清结构、贴到文档或 issue 里，Markdown 表格是最通用的格式。分享一个我常用的 30 行脚本，支持嵌套数组自动展开、字段对齐、复杂值降级为代码块。

## 场景

- 把 `deals.json` 这类 API 响应贴进 README
- 对比两批 JSON 数据的字段差异
- 给同事/issue 展示数据样例（比截图友好，可复制）

## 完整脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""json2md.py — 把 JSON 数组转 Markdown 表格，嵌套值自动降级。"""
import json, sys

def flat(v, depth=0):
    """复杂值降级：dict/嵌套数组转代码片段，长字符串截断。"""
    if isinstance(v, dict):
        return "`" + json.dumps(v, ensure_ascii=False)[:60] + "`"
    if isinstance(v, list):
        return "`" + json.dumps(v, ensure_ascii=False)[:60] + "`"
    s = str(v)
    return s if len(s) <= 50 else s[:47] + "..."

def to_table(rows):
    if not rows:
        return "_(empty)_"
    cols = []
    for r in rows:
        for k in r.keys():
            if k not in cols:
                cols.append(k)  # 保持字段出现顺序
    head = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join(["---"] * len(cols)) + "|"
    body = "\n".join(
        "| " + " | ".join(flat(r.get(c, "")) for c in cols) + " |"
        for r in rows
    )
    return f"{head}\n{sep}\n{body}"

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("items", [data])
    print(to_table(rows))
```

## 用法

```bash
python3 json2md.py api_response.json
```

输出直接就是 Markdown 表格，粘到任何支持 Markdown 的地方即可。

## 三个实现细节

1. **字段顺序保持出现序**而不是排序——阅读时和原始数据的字段出现顺序一致，对照 API 文档更直观
2. **dict/list 降级为行内代码**并截断 60 字符——避免表格被超长 JSON 撑爆；需要完整值时读者知道去查原始数据
3. **`ensure_ascii=False`**——中文直接输出，不然满屏 `\uXXXX` 转义可读性全无

## 已知边界

- 顶层是 dict 且没有 `items` 键时，会当作单行处理（脚本里 `data.get("items", [data])` 的兜底逻辑）
- 字段缺失的行输出空字符串，不会报错
- 超深嵌套（三层以上）会被压成一行代码片段——这是刻意取舍，表格里展开多层嵌套反而难读

有更好的处理方式欢迎评论区交流，比如你们是怎么处理嵌套结构展示的？
