# OpenRouter — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方 docs + FAQ，两源一致）
- **数据可信度**: 高（官方文档口径）

## 结论（可直接进 deals.json）

**:free 后缀模型零成本调用**。额度规则：未充值账户 **50 次/天**；**一次性充值 $10**（credits 永不过期）即解锁 **1000 次/天**——这是"花小钱办大事"的典型薅点。免费模型统一 20 次/分钟上限。2026-02-01 上线免费路由端点 `openrouter/free`（自动在免费模型间路由，支持文本+图像）。

## 明细

| 项目 | 内容 |
|---|---|
| 基础额度 | 50 requests/day（从未充值账户） |
| 解锁额度 | 1000 requests/day（一次性 $10，永不过期） |
| 频率上限 | 20 RPM（充不充值都一样） |
| 免费路由 | `openrouter/free` 端点自动选免费模型 |
| 错误码 | 429=限流，402=余额不足 |

## 来源

- 官方限流文档: https://openrouter.ai/docs/api_reference/limits
- 官方 FAQ: https://openrouter.ai/docs/faq

## 待办

- [ ] deals.json value 补充 50→1000 解锁话术（低投入高回报，用户爱看）

## 采集器巡检发现（2026-10-27，harvest 直抓官方页）

免费模型目录出现**轮换**（match 集合变化，diff 告警捕获）：

- 消失：一个「$0.06 /M input tokens $0 /M output」的免费档条目
- 新增：nace-ai 模型（Oct 21, 2026 上架，$0.12/M input、$0/M output，定位 routing/classification/policy 打分）＋ **NVIDIA: Nemotron 3.5 Embed 1B (free)** 免费嵌入模型（223M tokens 标注）

含义：:free 目录是动态的，「17 个」这类静态计数会很快过时。主会话 sync.py 的 OpenRouter 结构化 API 直更应已自动覆盖本变化，本条仅作双线互证与「目录动态性」的实证记录；建议站内条目避免写死免费模型数量，改为「免费模型列表见 openrouter.ai/models?max_price=0」。
