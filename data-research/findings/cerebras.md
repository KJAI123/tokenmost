# Cerebras Inference — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方定价页原文 + 官方限流文档 + 第三方追踪）
- **数据可信度**: 高（官方定价页原文直接命中）

## 结论（与主数据互证）

**有出入（门槛细节）**。deals.json `cerebras-credits`「注册送 $5 一次性 credits（30 天内用完，无持续免费层）」：
- ✅ $5 / 30 天 / 无持续免费层：一致（2026-07 起原免费档确已取消，改为 Free Trial 制）
- ⚠️ **出入**：官方定价页明示「Add a valid payment method to receive a one-time $5 promotional credit」——**需先绑有效支付方式才发放 $5**，主数据「注册送」（via: register, difficulty 1）未提绑卡门槛

## 明细

| 项目 | 主数据 | 独立核实（官方页） | 结论 |
|---|---|---|---|
| 金额 | $5 一次性 | $5 one-time promotional credit | ✅ |
| 有效期 | 30 天内用完 | expires 30 days after activation | ✅ |
| 获取条件 | 注册即送（difficulty 1） | **需添加有效支付方式后发放**；不会自动扣费 | ⚠️ 出入 |
| 持续免费层 | 无 | 原免费 tier 约 2026-07 取消，改 Free Trial 制 | ✅ |
| 附加情报 | — | Free Trial 期内限约 5 RPM / 30K TPM / 100 万 tokens/日；用完充值 $10 起步解锁 10 倍限速 | 补充 |

## 来源

- 官方定价页: https://www.cerebras.ai/pricing
- 官方限流文档: https://inference-docs.cerebras.ai/support/rate-limits
- 第三方追踪: https://pricepertoken.com/endpoints/cerebras/free

## 待办（供主会话裁决，本助理不改主数据）

- [ ] 建议 `cerebras-credits` 的 value/rule 补「需绑卡后发放（不会自动扣费）」，`via` 改 register+card 或 `difficulty` 上调至 2
- [ ] 可补充 Free Trial 限速（约 5 RPM / 30K TPM / 1M TPD）进 notes
- [x] 互证结论：有出入——绑卡门槛（verify_by:search，2026-10-27）
