# Google AI Studio / Gemini API — 调研发现（负情报：大幅缩水）

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（官方文档 + 官方开发者论坛多帖）
- **数据可信度**: 高（缩水事实多源一致；当前精确 RPD 因模型/账号而异）

## 结论（可直接进 deals.json，如实标注）

Gemini API 免费层**仍在但已大幅缩水**：2025-12 起 Gemini 2.5 Flash 免费档从 250 RPD 砍至 **约 20 次/天**（社区帖报告部分用户仅 10 次/天），RPD 在太平洋时间午夜重置。**定位调整：从"主力白嫖"降级为"轻量试用"**，站点页面上应如实标注，避免误导。

## 明细

| 项目 | 内容 |
|---|---|
| 免费层现状 | 约 20 RPD（Flash 档，2025-12 缩水后） |
| 缩水幅度 | ~92%（250→20），引发社区抗议 |
| 计费亮点 | 5000 次/月免费搜索请求（Gemini 3+ 模型共享，2027-01-01 起 $14/千次） |
| 查询入口 | AI Studio 限流面板 aistudio.google.com/rate-limit |
| 升级路径 | Tier 1（绑卡按量付费）显著放宽 |

## 来源

- 官方限流文档: https://ai.google.dev/gemini-api/docs/rate-limits
- 官方定价: https://ai.google.dev/gemini-api/docs/pricing
- 缩水事件（官方论坛）: https://discuss.ai.google.dev/t/do-they-really-think-we-wouldnt-notice-a-92-free-tier-quota/111262
- 2026-01 进一步限流报告: https://discuss.ai.google.dev/t/ai-studio-rate-limits/120345

## 待办

- [ ] deals.json 该条 value 改为"轻量试用"定位（负情报如实呈现）

## 与主数据（deals.json）的交叉核对

deals.json 的 google-ai-studio 条目（另一会话维护）记「Gemini 3.8 Flash / 3.5 Flash-Lite / 2.5 系等多款免费层 + $300 试用金辟谣」。本 findings 补充其未覆盖的时间维度：**2025-12 免费档 250→约 20 RPD 的缩水事件**（官方论坛帖为证），建议在 notes 里加一句「免费档自 2025-12 起大幅收紧」，让用户对"额度会缩水"有预期。
