# 人工复核队列（sync.py 每次运行自动重算；人工修复对应条目后自动消失）

机器不能判断的事都在这里：官方页面有变、来源失联、超期未复核、RSS 草稿。
处理方式：改 deals.json 对应条目（核实→更新 value→verify_status:"verified"；不实→删）。

- **源失联** `linuxdo-rss`：连续 5 次失败（HTTPError: HTTP Error 403: Forbidden）→ 检查 URL 是否失效，或从 tools/sources.json 移除
