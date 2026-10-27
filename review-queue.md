# 人工复核队列（sync.py 每次运行自动重算；人工修复对应条目后自动消失）

机器不能判断的事都在这里：官方页面有变、来源失联、超期未复核、RSS 草稿。
处理方式：改 deals.json 对应条目（核实→更新 value→verify_status:"verified"；不实→删）。

- **待复核** `zhipu-signup`（智谱 BigModel）：源 zhipu-promotion 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `kimi-voucher`（Kimi 开放平台）：源 kimi-trial 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `kimi-k2-deadline`（Kimi 开放平台）：源 kimi-pricing 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `coze-free`（扣子 Coze）：源 coze-edition 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `siliconflow-signup`（硅基流动）：源 siliconflow-billing 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `azure-student`（Azure for Students）：源 azure-students 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deep-stepfun-step5-preview-price`（阶跃星辰 StepFun）：源 stepfun-pricing 页面于 2026-10-27 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **源失联** `linuxdo-rss`：连续 6 次失败（URLError: <urlopen error [Errno 61] Connection refused>）→ 检查 URL 是否失效，或从 tools/sources.json 移除
