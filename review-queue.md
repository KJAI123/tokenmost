# 人工复核队列（sync.py 每次运行自动重算；人工修复对应条目后自动消失）

机器不能判断的事都在这里：官方页面有变、来源失联、超期未复核、RSS 草稿。
处理方式：改 deals.json 对应条目（核实→更新 value→verify_status:"verified"；不实→删）。

- **待复核** `zhipu-signup`（智谱 BigModel）：源 zhipu-promotion 页面于 2026-11-09 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `bailian-signup`（阿里云百炼）：源 bailian-quota 页面于 2026-11-05 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deepseek-price`（DeepSeek）：源 deepseek-pricing 页面于 2026-11-05 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deepseek-offpeak`（DeepSeek）：源 deepseek-pricing 页面于 2026-11-05 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `kimi-voucher`（Kimi 开放平台）：源 kimi-trial 页面于 2026-11-08 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `qianfan-signup`（文心千帆）：源 qianfan-quota 页面于 2026-11-07 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `xinghuo-signup`（讯飞星火）：源 xfyun-spark-docs 页面于 2026-11-06 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `minimax-m3-half`（MiniMax 开放平台）：源 minimax-pricing 页面于 2026-11-06 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `dify-selfhost`（Dify 自部署）：源 dify-pricing 页面于 2026-11-05 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `scnet-coupon`（国家超算互联网 SCNet）：源 scnet-activity 页面于 2026-11-06 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `nvidia-nim`（NVIDIA NIM）：源 nvidia-build 页面于 2026-11-07 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `ohmygpt-referral`（OhMyGPT）：源 ohmygpt-pricing 页面于 2026-11-08 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `google-student`（Google AI Studio）：源 gemini-students 页面于 2026-11-07 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `zcode-linuxdo`（智谱 ZCode）：源 zcode-changelog 页面于 2026-11-04 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `zhipu-flash-free`（智谱 BigModel）：源 bigmodel-pricing 页面于 2026-10-31 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `github-copilot-free`（GitHub Copilot）：源 copilot-plans 页面于 2026-10-31 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `xfyun-offpeak`（讯飞星火）：源 xfyun-coding-plan 页面于 2026-11-06 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deep-copilot-ai-credits`（GitHub Copilot）：源 copilot-plans 页面于 2026-10-31 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deep-volc-coding-promo`（火山方舟）：源 volc-ai618 页面于 2026-11-06 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **待复核** `deep-xunfei-coding-plan`（讯飞星辰 MaaS）：源 xfyun-coding-plan 页面于 2026-11-06 变更（连续 2 次观测一致） → 核实后更新 value/notes 并改 `verify_status:"verified"`
- **源失联** `linuxdo-rss`：连续 33 次失败（HTTPError: HTTP Error 403: Forbidden）→ 检查 URL 是否失效，或从 tools/sources.json 移除
