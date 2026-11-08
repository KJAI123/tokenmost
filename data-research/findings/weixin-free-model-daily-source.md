# 信源发现：免费模型日报（公众号「信息技术和课程整合」）

- 发现日期：2026-11-09（老板令「这个信源看一下」）
- 首发 URL：https://mp.weixin.qq.com/s/GB2NBAQ551YDtzWEMnTaqg（11-04 期）
- 账号名（js_name）：信息技术和课程整合 ｜ biz：MzA3NTE2NDUyOQ==
- 栏目/系列名：免费模型日报（日更，标题格式「免费模型日报 MM-DD｜<当日变化>」）

## 信源价值
每日逐平台对照 12 个平台的免费名单（NVIDIA NIM / ModelScope / OpenRouter / AMD Radeon Cloud / 书生·端砚 / OpenCode / Agnes AI / B.AI / 七牛云 / TokenRouter / WorkBuddy 国际站+CN 站），只报变化项（新增/移出/档位收窄），口径注明「免费≠不限量不限速」——与我们站规一致，误报率低，适合作为免费名单变动的高质量盯防源。

## 11-04 期关键情报 vs 站内核对（结论：站内口径已正确，无需改数据）
1. OpenRouter 免费名单 17→18（新增 stealth/crouton-alpha，1.05M 上下文）——我们 openrouter-free 条目口径=:free 后缀 12 款（11-08 核验，比该报口径更严：该报 18 含 4 个非 :free 条目），且 stealth 匿名模型随时下架不立条。**不改**。
2. 定价字段为 0 ≠ 真免费（Lyria 音乐模型按首 $0.08 计费）——我们只收 :free 后缀，天然规避。**不改，口径正确**。
3. B.AI minimax-m3.1-flash 5 折活动结束（打折 4→3 档，活动制持续收窄）——站内无 B.AI 条目，活动制折扣不立条。**不改**。
4. NVIDIA NIM「45 个免费」混 embedding/rerank/parse——我们 NIM 条目口径注意区分即可（TK 采集时 patterns 已含模型 ID 筛选）。

## 巡检接入
已加入 data-research/weixin_accounts.json 盯防名单（TK 公众号管线自动抓新文章→weixin_alerts.md 增量）。
