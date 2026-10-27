# 找源发现队列（discovery-queue）

> 供每 15 分钟找源巡检自动消费：取最靠前的未完成条目执行 WebSearch（串行），完成后标 ✅ 并把新发现落表（信息源总表-全量版.xlsx 发现日志 + 对应 sheet），可自行在队尾追加新线索。格式：`- [ ] 线索描述 | 建议搜索词 | 去向`

- [x] weixin.sogou.com 可行性 ✅ 2026-10-28：直连可用、已管道化（采集器2查询位）；首查 39 篇文章/3 条线索
- [ ] 搜狗 /link 加密跳转解析（需 SNUID cookie 方案，低优先） | — | 提升公众号文章直达率
- [ ] 「每天10亿token·含K3」聚合平台定位 | 每天 10亿 token 免费额度 聚合平台 | 线索→主管
- [x] 智谱实名2亿 ✅ 2026-10-28：未证实（降级）；意外收获=官方 promotion 页现已列 Weekend Build 3亿/ZCode 1亿/1024节5亿——zcode-linuxdo 可升级
- [x] 小米 MiMo ✅ 2026-10-28：100T 免费计划已领完（5月中旬），转永久降价 99% 常态化；MiMo-2.5 低价条目候选→主管
- [ ] 讯飞星辰 Qwen 不限量 Token 官方页 | 讯飞星辰 Qwen 不限量 2026 | 线索→主管
- [x] MonkeyCode/TRAE ✅ 2026-10-28 定位完成：长亭科技 monkeycode.cn（文档/仓库已入采集器）；数额多源出入（标准1000万/日·活动期3000万·7天试用·历史促销500亿+¥200）→⏳主管按控制台口径核实；TRAE 五档 Free/$8/$20/$60/$200
- [x] Google Antigravity ✅ 2026-10-28：免费档 250→20 RPD(-92%)、RPM 10→5；积分制（Pro 1000/月·Ultra 25000/月·不滚存）；7天锁机制；负情报，无收录价值
- [x] 每日登录类 ✅ 2026-10-28：各平台无统一签到中心；智谱「每日一亿领取」单源线索→主管；其余=注册赠送+邀请奖励模式
- [ ] smzdm 最新 AI 免费权益聚合帖（替代每周人肉翻） | smzdm AI 免费权益 2026 | 社区→总表
- [x] v2ex 摸底 ✅ 2026-10-28：竞品站 token.pencilai.top⭐+MiMo 重置50倍修正+快手/美团线索；掘金/即刻下轮
- [x] 学生认证补全 ✅ 2026-10-28：GitHub Copilot 学生免费 3-12 终止+Student 计划 4 月暂停——⏳主管复核主数据 github-student-pack 条目；Copilot Free 层仍有效
- [x] OpenRouter API 快照 ✅ 2026-10-28：主会话 sources.json 已含 api/v1/models——不重复建源，闭环
- [x] Cursor / Windsurf ✅ 2026-10-28：两定价页入采集器；Cursor 10-12 改版为 X 订阅（Free/Plus$8/Premium$30/Super$100/Ultra$200 与 Grok 共享池）——⌨️Coding 面板变更线索→主管；Windsurf 免费档≈25 Flow Actions/月
