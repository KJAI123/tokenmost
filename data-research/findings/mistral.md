# Mistral La Plateforme — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方定价页 + 官方 docs/help + 第三方追踪与社区分析）
- **数据可信度**: 高（免费档存在性官方多页确认；具体量级仅第三方来源，标注中可信度）

## 结论（与主数据互证）

**与主数据一致**。deals.json `mistral-free`「La Plateforme 免费档：每月内含用量免费建 key 调用（具体限额在控制台 Limits 页查看）」——免费档确实存在且按月给内含用量；主数据未写具体数额属稳妥表述（数额随政策浮动，官方只承诺在控制台 Limits 页可查）。

## 明细

| 项目 | 内容 | 来源等级 |
|---|---|---|
| 免费档存在 | Free plan（Experiment 档）默认生效，建 key 即可调用 | ✅ 官方 pricing/docs/help 多页 |
| 月内含用量 | 第三方追踪称约 10 亿 tokens/月 | ⚠️ 非官方直核，仅供参考，勿入主数据 |
| 限速 | 约 1 请求/秒/每 key，全模型通用；高峰期低优先级（可能变慢） | ⚠️ 社区+GitHub issue（2026-01），中可信度 |
| 升级路径 | 绑卡转 pay-as-you-go 解锁 Tier 1+ 更高限速 | ✅ 官方 help center |

⚠️ 免费档数据训练 opt-in 政策与限速政策均在变动通道，该条目适合纳入 harvest 盯防（docs.mistral.ai usage-limits 页）。

## 来源

- 官方定价: https://mistral.ai/pricing
- 官方用量/限额文档: https://docs.mistral.ai/admin/billing-usage/usage-limits
- 官方帮助（限速说明）: https://help.mistral.ai/en/articles/698531
- 第三方参考: https://pricepertoken.com/endpoints/mistral/free 、Reddit r/MistralAI 限速池分析

## 待办

- [ ] 可将 docs.mistral.ai usage-limits 页加入 harvest_sources.json
- [x] 互证结论：与主数据一致（verify_by:search，2026-10-27）
