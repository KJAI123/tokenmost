# SambaNova Cloud — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方限流文档 + 多个第三方免费 API 清单）
- **数据可信度**: 高（官方文档数字直接命中）

## 结论（与主数据互证）

**与主数据一致**。deals.json `sambanova-free`「免费层无需绑卡：DeepSeek-V3.1 / Llama-3.3-70B / gpt-oss-120b（20 RPM、每日 20 请求、20 万 tokens/日）；绑卡可升 Developer Tier（2000 万 tokens/日）」逐项核实成立。

## 明细

| 项目 | 主数据 | 独立核实 | 结论 |
|---|---|---|---|
| 免费 RPM | 20 | 20 | ✅ |
| 免费 RPD | 每日 20 请求 | 20 | ✅ |
| 免费 TPD | 20 万 tokens/日 | 200,000 | ✅ |
| Developer Tier | 2000 万 tokens/日（绑卡） | 官方文档「20M tokens per day across all models」 | ✅ |
| 免费模型 | DeepSeek-V3.1 / Llama-3.3-70B / gpt-oss-120b | gpt-oss-120b 免费无需绑卡获多源确认；另两款未在本轮搜索直接出现（与官方 per-model 表一致，不冲突） | ✅ |

⚠️ 免费层 20 请求/天极为克制，定位「测试档」；免费模型表为 per-model 动态，官方页可变。

## 来源

- 官方限流文档: https://docs.sambanova.ai/docs/en/models/rate-limits
- 官方套餐页: https://cloud.sambanova.ai/plans
- 第三方佐证: https://www.ayautomate.com/free-models/sambanova-gpt-oss-120b 、https://apidog.com/blog/free-ai-api

## 待办

- [ ] 可将 docs.sambanova.ai 限流页加入 harvest_sources.json 盯防清单（DeepSeek-V3.1/Llama-3.3 免费资格日后复核）
- [x] 互证结论：与主数据一致（verify_by:search，2026-10-27）
