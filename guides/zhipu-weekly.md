# 智谱 ZCode 大礼包攻略：周期性 3~5 亿 tokens 怎么薅

> 核实于 2026-10-27 ｜ 难度：★☆☆ ｜ 核心结论：智谱的大额礼包是「周期活动」，入口永远在 ZCode 客户端里，拼的是手速和盯梢。

## 规律先看清（verified 历史数据）

- 2026-08：1 亿 tokens → 8.28「周末计划」3 亿（GLM-5.3-Flash）→ 10.23「1024 程序员节」5 亿（GLM-5.3 + Flash，20 万份待核实）。
- 节奏 ≈ **每月 1~2 轮**，下一轮大概率挂在双 11 / 年末节点。
- 窗口极短：38~61 小时（如周六 09:00 生效 → 周日 23:00 到期），**过期作废不补**。
- 全部「先到先得」，单轮 10 万份起，新老用户均可领、不要求付费套餐。

## 领取步骤

1. **下载/更新 ZCode 客户端**：https://zcode.z.ai （macOS/Windows/Linux 全平台，当前 v3.16.3）。⚠️ 旧版看不到活动卡，周末计划要求 v3.10 以上。
2. **登录**：用智谱开放平台（https://bigmodel.cn 或 open.bigmodel.cn）账号登录客户端。
3. **点左下角活动卡片**：活动期客户端左下角会出现「XX 亿 Tokens」活动按钮，点「打开大礼包」即领。看不到卡片 = 先升级客户端再看。
4. **立刻用掉**：礼包额度直接在 ZCode 里调 GLM-5.3 / GLM-5.3-Flash 生效，绑定 bigmodel 账号的各编程工具同样可用。
5. **叠加项（老板客户端截图直核 2026-10-27）**：新用户开 **体验套餐 ¥0/5 天** = **GLM-5.3 每日 300 万 + GLM-5.3-Flash 每日 500 万 tokens（每日刷新，5 天合计约 4000 万）**，另含 BYOK 自带 Key 接入与 Weekend/Global Build 活动资格——比社区流传「300 万总额」大 13 倍。领取：客户端左下角「升级套餐」页 → 体验套餐。历史 1024 期新人包窗口（10-28 23:59）与体验套餐是两回事，以套餐页实显为准。

## 体验套餐值多少 & Weekend/Global Build 是什么

- **体验套餐（¥0/5 天）**：GLM-5.3 每日 300 万 + Flash 每日 500 万，**每日刷新、5 天合计约 4000 万**，含 BYOK 与活动资格——每日 800 万 ≈ 中型项目每天 1-2 轮完整 Agent 会话，**新人别只领礼包，直接开体验套餐**。
- **Weekend Build（周末计划）**：周期性活动，每人 3 亿 Flash tokens，免费档可领；窗口 38-61 小时（周五 20:00→周一 09:00 等多轮变体），客户端 v3.10+ 左下角活动卡领取。
- **Global Build（夜间场）**：2026-09-03→09-20 历史活动，每晚 23:00–次日 09:00 付费档 Flash 归零、其他工具翻倍——「夜猫子场」，可能复刻。
- **不定期免费领取的历史节奏**：8 月 1 亿 → 周末 3 亿×多轮 → 夜间场（9 月）→ 国庆每日 1 亿×10 万份（9/28-10/7）→ 1024 五亿（10/23-26）。**月均 1-2 轮+节假日加码，入口全在客户端活动卡**。

## ⚠️ GLM-5.3-Flash「限免」勘误（2026-10-27 定价页复核）

- 官方定价页实际口径：GLM-5.3-Flash 为**付费模型（0.8/2.8 元/百万）**，「限时免费」**仅指缓存存储费**（原文：「缓存存储当前限时免费」）。
- 输入/输出全免的只有 4.7-Flash / 4-Flash / Z1-Flash / 4.6V-Flash / 4V-Flash / 4.1V-Thinking-Flash / CogView-3-Flash / CogVideoX-Flash 八款（无截止日，长期口径）。
- 本攻略此前「Flash 限免」表述有误；API 免费档用 4.7-Flash，跑 5.3-Flash 走体验套餐每日 500 万。

## 想薅得爽？积分制用法（官方公式，verified）

- 2026-07-30 起套餐改积分制，**官方公式：消耗积分 =（输入 token×系数 + 缓存 token×系数 + 输出 token×系数）÷ 10000**——即 **1 积分 = 1 万加权 token**。按模型系数直接换算：
  - GLM-5.3-Flash（输出系数 8）：**1 积分 ≈ 1250 个 Flash 输出 token** → Lite 周额度 10000 积分 ≈ **Flash 输出 1250 万 tokens/周**
  - GLM-5.3（输出系数 24）：1 积分 ≈ 417 个输出 token → Lite ≈ 417 万 GLM-5.3 输出 tokens/周
  - 混合对话场景按加权平均，实际大约在两者之间。
- **闲时半价（最实用）**：工作日 14:00–18:00（UTC+8）以外时段，积分按 **50%** 抵扣；周末全天按闲时算。批量任务挂夜间跑，等于额度翻倍。
- 免费层：**GLM-4.7-Flash / GLM-4-Flash / GLM-Z1-Flash / GLM-4.6V-Flash / GLM-4V-Flash / GLM-4.1V-Thinking-Flash / CogView-3-Flash / CogVideoX-Flash** 八款长期免费（输入/输出全免、无截止日）；⚠️ GLM-5.3-Flash 为付费模型（0.8/2.8 元/百万，仅缓存存储限免）——以定价页实时为准：https://docs.bigmodel.cn/cn/guide/start/pricing

## ⚠️ 红线声明（重要，官方明文 + 封号实锤）

1. **套餐仅限订阅人专享，禁止共享/多人共用**（官方使用须知原文）。3 次以上违规可封号；倒卖、中转、套利是永久封禁判定项。
2. **实锤案例**：linux.do/Telegram 已有用户因「服务器登录 + 多 IP + 出差异地」组合被风控封掉 Lite 套餐。单人使用也请尽量固定环境，避免公司服务器/家宽/热点频繁混登。
3. 多号注册薅礼包=官方明令风控场景，本站不收录此类玩法。
4. 体验卡/邀请活动是官方通道：老用户可向好友赠 7 天体验卡（2000 积分）；ZCode 3.15.1 上线「邀请好友·免费蹬蹬共得权益」端内活动——要用就用官方邀请通道。

## 下轮活动怎么盯

- 盯 ZCode 客户端左下角（活动卡只在窗口期出现）；
- 盯智谱系公众号/官方 X（@zcode_ai）；
- bigmodel.cn 活动页需登录：https://bigmodel.cn/activity/glm-coding-1024

---
**核实于 2026-10-27**。来源（官方文档 .md 直出，高置信）：
- 套餐积分制总览：https://docs.bigmodel.cn/cn/coding-plan/overview
- 修改公告（2026-07-30）：https://docs.bigmodel.cn/cn/coding-plan/notice/usage-revision
- 使用须知/红线：https://docs.bigmodel.cn/cn/coding-plan/usage-notes
- FAQ（体验卡/重置卡）：https://docs.bigmodel.cn/cn/coding-plan/faq
- 定价/免费模型：https://docs.bigmodel.cn/cn/guide/start/pricing
- 推荐有礼：https://docs.bigmodel.cn/cn/update/promotion
- ZCode changelog：https://zcode.z.ai/cn/changelog
- 周末计划实测复盘（smzdm）：https://post.smzdm.com/p/aqrx263p ；1024 教程（知乎）：https://zhuanlan.zhihu.com/p/2097344549374914581
- Start Plan/体验套餐：体验套餐真口径（¥0/5 天=5.3 日 300 万+Flash 日 500 万+BYOK+活动资格）为**老板客户端截图直核**（高）；Flash「限免」勘误依据=官方定价页复核（高）。
