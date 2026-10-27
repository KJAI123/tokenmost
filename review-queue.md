# 人工复核队列（sync.py 每次运行自动重算；人工修复对应条目后自动消失）

机器不能判断的事都在这里：官方页面有变、来源失联、超期未复核、RSS 草稿。
处理方式：改 deals.json 对应条目（核实→更新 value→verify_status:"verified"；不实→删）。

- **待复核** `volc-ark-signup`（火山方舟）：源 ark-freequota 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `dify-selfhost`（Dify 自部署）：源 dify-pricing 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `ark-daily-5m`（火山方舟）：源 ark-collab 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `github-copilot-free`（GitHub Copilot）：源 copilot-plans 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deep-copilot-ai-credits`（GitHub Copilot）：源 copilot-plans 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **源失联** `linuxdo-rss`：连续 5 次失败（URLError: <urlopen error [Errno 61] Connection refused>）→ 检查 URL 是否失效，或从 tools/sources.json 移除
