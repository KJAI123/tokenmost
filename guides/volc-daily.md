# 火山方舟「每日 500 万」攻略：协作奖励计划怎么开、红线在哪

> 核实于 2026-10-27 ｜ 难度：★★☆（有隐私条款，先看红线再决定）｜ 唯一的「按天给额度」型大厂羊毛

## 机制一句话

火山方舟的「每日最高 500 万 tokens」**不是无条件白送**，而是「协作奖励计划」：你**授权火山采集你的推理数据**（匿名化）→ 换每日等量资源包。**用得越多返得越多**，上限每模型每天 500 万 tokens。

## 开通步骤

1. **注册火山引擎 + 实名认证**：https://www.volcengine.com/product/ark （个人实名即可，企业认证可提额）。
2. **开通模型服务**：进方舟控制台 https://console.volcengine.com/ark →「开通管理」，开通你要用的模型（如 Doubao-Seed-Evolving 等）。⚠️ 新账号先看「开通管理」页的**免费额度**：新注册用户每模型有一笔一次性免费额度（第三方口径 50 万 tokens，官方以控制台实显为准），可先薅这个。
3. **关闭「安心体验模式」**：这是协作奖励计划的硬前提。它本是「只耗赠送额度、用完即停」的防扣费开关——参加协作计划必须关，关了之后超额会真实计费，所以第 4 步的资源包要盯紧。
4. **报名协作奖励计划**：控制台「开通管理」页点「立即参与」；或在模型广场进 Doubao-Seed-Evolving 等在列模型详情页，从模型卡进入。
5. **正常调用**：API 走 Chat/Responses/Messages/Image/Content Generation 在线推理。当天授权模型消耗的量（≤500 万 tokens/天），**次日 T+1 发放等量免费资源包（30 天有效）**；首次授权某模型再给一笔一次性冷启动资源包（数额以活动页公示）。

## 额度用法与优先级

- 免费资源包只抵**按 token 后付费的在线推理**（输入/输出/缓存命中），不抵批量推理、模型单元付费、TPM 包、缓存存储费。
- 抵扣顺序官方明示：**免费额度包 > 协作奖励包 > 资源包 > 按量扣费**。
- 支持协议齐全（含 Anthropic 兼容），可接 Claude Code 等；Coding Plan 用户另有 `ark.cn-beijing.volces.com/api/coding` 专属地址，别混。

## ⚠️ 红线与知情声明（报名前必读）

1. **数据授权是永久的**：官方条款原文「授权期限为永久」，且已采集的数据技术上无法撤回——撤回授权只对以后生效。介意数据被用于模型训练的，别开。
2. **模型名单在收缩**：2026-09-01 退出文本模型 31 款，2026-10-08 又退出 9 款（Doubao-Seed-2.1-pro/turbo、DeepSeek-V4-Pro/Flash、GLM-5.2、Kimi-K3 等都在退出名单里）。**开通前先看活动页当前在列模型**，别冲着已退出的模型去。
3. **一账号原则**：仅同一用户的唯一一个账号可参与，多号=违规。
4. **关了安心体验模式会真实扣费**：资源包 30 天过期清零、当日消耗超 500 万的部分自费——控制台设置用量告警。
5. 「豆包编程模型每日 500 万常态化到 2027」是官方文章口径，与协作计划条款存在矛盾，**以控制台活动页实时规则为准**。

## 顺手的低价档

- 方舟 Coding Plan：Lite ¥40/月（每 5h 约 1200 次）、Pro ¥200/月（约 5 倍）；首购 9.9 元特惠官方公告已于 2026-03-17 暂停，但活动页仍挂「限时 9.9 起」——**下单前在 https://www.volcengine.com/activity/codingplan 实时确认**。模型池含 Doubao-Seed-2.1 系列、Kimi-K3、GLM-5.3、DeepSeek-V4 系。
- ⚠️ Coding Plan 仅限编程工具内使用，当 API 用会封订阅。

---
**核实于 2026-10-27**。来源（官方文档直核，高置信）：
- 协作奖励计划：https://www.volcengine.com/docs/ark/collaboration-reward-program
- 免费推理额度：https://docs.volcengine.com/docs/ark/free-inference-quota
- Coding Plan 个人版概览：https://docs.volcengine.com/docs/ark/coding-plan-personal-plan-overview
- 新用户特惠（9.9 暂停公告）：https://docs.volcengine.com/docs/82379/1528220
- 「每日 500 万」官方文章（软文性质，中置信）：https://www.volcengine.com/article/2605938
- 新人 50 万口径（第三方，待核实）：https://www.aipromonow.com/promos/volcengine-ark-free-500k-tokens-per-model
