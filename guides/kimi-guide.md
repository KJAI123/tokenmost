# Kimi API 15 元券能用 K3 吗？领取条件与 Highspeed 限制

国内新用户完成认证后可领 15 元 API 券，适用于 Kimi K3 和 K3.1 Pro 普通版。K3.1 Pro Highspeed 不适用。

核对日期 2026-11-25。以上适用范围来自 [Kimi 开放平台账号与财务](https://platform.kimi.com/docs/guide/account-and-payments)。

## 领取后去哪里查券？

1. 用国内手机号注册 [Kimi API 开放平台](https://platform.kimi.com/)，在 [用户中心](https://platform.kimi.com/console/auth) 完成实名认证。
2. 登录控制台，打开「费用明细」，查看代金券余额。券到账后会自动用于符合条件的 API 调用。帮助中心列出的有效期为自发放起 **3 个月**，实际以账户显示为准。
3. 用 `kimi-k3` 或 `kimi-k3.1-pro` 前，先核对模型和余额。发出小请求后，可以在费用明细对照现金和券余额的变化。

[官方免费测试权益说明](https://www.kimi.com/help/kimi-api/api-free-trial) · [官方账号与财务说明](https://platform.kimi.com/docs/guide/account-and-payments)

## K3、Highspeed 和扣费规则

- **可用**：Kimi K3 与 K3.1 Pro 普通版。**不适用**：K3.1 Pro Highspeed。其他模型的抵扣资格请以账户显示为准。
- 官方帮助中心仍把 K3 列为不可用，开放平台财务文档明确列为可用。两处文档口径不同，实际扣费请核对账户明细。
- [开放平台变更日志](https://platform.kimi.com/docs/changelog) 写明现金和券同时有余额时各扣 50%，一类耗尽后从另一类全额扣除，已签合同用户依合同。帮助中心仍写券优先扣。最低充值额和账户扣费以当期控制台为准。
- 15 元是按量抵扣金额。可用 Token 取决于模型单价、输入输出和缓存用量。

## Kimi Code 会员额度在哪里看？

API 券在开放平台「费用明细」查看。Kimi Code 使用单独的会员额度，新套餐 Plus 及以上可用，Go 档没有 Kimi Code 额度。Desktop、CLI、VS Code 和第三方工具共用该会员额度。

[Kimi Code 官方会员权益](https://www.kimi.com/code/docs/kimi-code/membership.html)
