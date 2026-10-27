# 找源发现队列（discovery-queue）

> 供每 15 分钟找源巡检自动消费：取最靠前的未完成条目执行 WebSearch（串行），完成后标 ✅ 并把新发现落表（信息源总表-全量版.xlsx 发现日志 + 对应 sheet），可自行在队尾追加新线索。格式：`- [ ] 线索描述 | 建议搜索词 | 去向`

- [ ] weixin.sogou.com 微信搜索「token 免费额度」可行性测试（反爬评估， robots 优先） | sogou 微信搜索 token 免费额度 | 可能成为公众号发现管道
- [ ] 智谱实名送 2 亿 Token 线索核实（SegmentFault 帖，主管 lane 或直接核实官方页） | 智谱 实名 2亿 token | 线索→主管
- [ ] 小米 MiMo 免费计划官方入口与现状 | 小米 MiMo token 免费 官方 | 线索→主管
- [ ] 讯飞星辰 Qwen 不限量 Token 官方页 | 讯飞星辰 Qwen 不限量 2026 | 线索→主管
- [ ] MonkeyCode / TRAE 免费额度官方页 | MonkeyCode TRAE 免费额度 | 线索→主管
- [ ] Google Antigravity 免费情况（liurb 博客提及） | Google Antigravity free tier | 线索→主管
- [ ] 各大厂「每日登录领 token」类活动页汇总（博客园攻略提及的签到机制） | 大模型 每日登录 领 token 活动 | 官方页→采集器
- [ ] smzdm 最新 AI 免费权益聚合帖（替代每周人肉翻） | smzdm AI 免费权益 2026 | 社区→总表
- [ ] v2ex / 掘金 / 即刻 的 AI 羊毛帖活跃度摸底 | v2ex AI token 免费 | 社区→总表
- [ ] 各家「教育优惠/学生认证」官方页（Azure 已有，补 GitHub/Copilot/Notion 等） | AI 学生认证 免费额度 官方 | 官方页→采集器
- [ ] OpenRouter 免费模型 API 快照源（https://openrouter.ai/api/v1/models，若 sync.py 未覆盖再补） | — | 待与主会话确认分工
- [ ] Cursor / Windsurf 等 AI IDE 免费档官方页（v1.9 主数据已有横评，盯防官方变动页） | Cursor pricing free | 官方页→采集器
