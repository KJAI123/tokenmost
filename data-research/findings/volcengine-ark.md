# 火山方舟（豆包）— 调研发现 ⭐ 本轮最大羊毛

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（火山引擎官方公告 + 官方文档）
- **数据可信度**: 高（官方公告原文可查，含政策截止时间）

## 结论（可直接进 deals.json）

**每日免费领取单模型最高 500 万 Tokens，官方长期常态化政策，至少维持至 2027 年底**（调整提前 30 天公告）——按天白嫖、非一次性赠送，是本轮调研中持续性最强的额度。新用户开通另赠 500 AFP 积分。

## 明细

| 项目 | 内容 |
|---|---|
| 每日免费 | 单模型最高 500 万 Tokens/天（免费推理额度） |
| 政策期限 | 官方 Q3 2026 公告：至少至 2027 年底 |
| 新用户 | 赠 500 AFP（AI 统一节省计划）积分 |
| 协作奖励计划 | 加入后每天再得 50 万 tokens |
| 限制 | 仅抵扣按 token 后付费的在线推理；不覆盖插件/知识库/批量推理 |

- 早期（2025）政策为每模型一次性 50 万 tokens，现已升级为按天领取

## 来源

- 官方公告（政策期限）: https://www.volcengine.com/article/2605938
- AFP 积分说明: https://www.volcengine.com/article/2697201
- 免费推理额度文档: https://docs.volcengine.com/docs/ark/free-inference-quota
- 协作奖励计划: https://blog.csdn.net/w605283073/article/details/154007728

## 待办

- [ ] deals.json 该条 type 由 signup_bonus 改为 free_tier（每日发放）
- [ ] 确认"每日领取"入口路径（控制台领取页），写进攻略

## ⭐ 给主会话/另一会话的合并素材（2026-10-27 爬虫助理补充）

deals.json 中 `ark-daily-5m` 条目（stale、published:false）的 TODO 写着「页面 JS 渲染，登录核实原文后与 volc-ark-signup 合并」。本次调研**通过官方公告拿到了缺失的一环，无需登录即可升级该条目**：

- 官方公告（火山引擎 2026 Q3）：**「每日 500 万 Tokens 的免费政策为长期常态化政策，至少维持至 2027 年底，若调整提前 30 天公告」** → https://www.volcengine.com/article/2605938
- 配套文档：免费推理额度使用限制（仅在线推理按量费用） → https://docs.volcengine.com/docs/ark/free-inference-quota
- 建议合并动作：ark-daily-5m 与 volc-ark-signup 合并为一条 `type: free_tier`，value 强调「按天领取、政策至 2027 年底」，notes 带上述两个来源，verify_by 可标 `search`（官方公告经搜索核实，非页面直抓）
- 关联发现：新用户赠 500 AFP 积分（https://www.volcengine.com/article/2697201）；协作奖励计划 +50 万/天
