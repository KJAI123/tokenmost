# Kimi 开放平台 — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方帮助文档 + platform.kimi.com 官方文档多页）
- **数据可信度**: 高（官方文档多页一致）

## 结论（与主数据互证）

**与主数据一致**。deals.json `kimi-voucher` 条目「新用户实名认证后自动发放 15 元代金券（3 个月内有效，自动优先扣减），不能用于 K3 模型」经独立搜索核实成立，官方文档直接载明。

## 明细

| 项目 | 内容 |
|---|---|
| 福利 | 国内手机号注册 + 完成实名认证 → 赠 15 元代金券 |
| 有效期 | 自发放之日起 3 个月，过期自动失效 |
| 适用范围 | 大部分模型可用；**K3 不支持**，官方另载明 **K3.1 Pro 亦不支持** |
| 平台域名 | platform.kimi.com（与主数据 notes「已从 platform.moonshot.cn 迁移」一致） |

## 来源

- 官方文档「账号与财务」: https://platform.kimi.com/docs/guide/account-and-payments
- 官方帮助「免费试用额度说明」: https://www.kimi.com/help/kimi-api/api-free-trial
- 官方帮助「账号注册与认证」: https://www.kimi.com/help/kimi-api/api-account-and-auth

## 待办

- [ ] 建议 deals.json `kimi-voucher` 的 rule 补一句「K3 与 K3.1 Pro 均不支持代金券」（细节增强，非纠错）
- [x] 互证结论：与主数据一致（verify_by:search，2026-10-27）
