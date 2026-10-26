# Cohere — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方限流文档原文 + 官方 FAQ + 第三方免费档追踪）
- **数据可信度**: 高（官方 docs 数字直接命中）

## 结论（与主数据互证）

**与主数据一致**。deals.json `cohere-trial`「Trial Key 免费：每月 1000 次 API 调用，Chat 全模型 20 请求/分（含 Command A+）」逐项核实成立，官方限流文档原文直接命中。

## 明细

| 项目 | 主数据 | 独立核实 | 结论 |
|---|---|---|---|
| 月调用上限 | 1000 次/月 | Trial keys（及新 Chat 型号的 prod keys）限 1,000 API calls/month | ✅ |
| Chat 限速 | 20 请求/分 | 20 req/min（Command A+ 同为 20） | ✅ |
| Embed 限速 | （未主张） | 约 5 次/分 | 补充 |
| 使用限制 | （未主张） | **Trial key 禁止生产/商用用途**，超限返回 429 | 补充 |

## 来源

- 官方限流文档: https://docs.cohere.com/docs/rate-limits
- 官方 FAQ: https://docs.cohere.com/docs/cohere-faqs
- 官方定价: https://cohere.com/pricing
- 第三方佐证: https://benchlm.ai/free-tier/cohere

## 待办

- [ ] 建议 `cohere-trial` 的 rule 补「Trial key 不可用于生产/商用」（合规提示，非纠错）
- [x] 互证结论：与主数据一致（verify_by:search，2026-10-27）
