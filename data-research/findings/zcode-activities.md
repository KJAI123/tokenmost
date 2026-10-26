# ZCode（智谱编程智能体）官方活动专项调研

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch 串行 7 条 + WebFetch 直核 6 个 URL（官方页/文档/linux.do）
- **任务背景**: 老板专项指令——跟进 ZCode 自家周期性活动（周末 3 亿 / 1024 节 5 亿等），补齐官方公告渠道缺口；deals.json 只读，产出仅供主会话合入
- **交叉核对说明**: 主会话已深挖过 deals.json 的 `zcode-linuxdo` 并另建 5 条 `deep-zhipu-*` 条目（均 2026-10-27 verified）——本文件不重复其结论，聚焦**官方渠道清单、完整时间线、监控方案**三个增量

## 一、结论

1. ZCode 大额活动的**真实发布入口是客户端活动卡片（左下角，v3.10+）**，官方公告渠道是**智谱/BigModel 微信公众号**（linux.do 社区共识：活动非每周固定，以公众号推送为准）。
2. **官方文档促销页不收录 ZCode 客户端活动**（本日 WebFetch 直核 docs.bigmodel.cn/cn/update/promotion：仅 API 侧促销，无周末 3 亿/1024 5 亿条目）——主会话「官方公告页未找到」的判断成立，且现在有了实核依据。
3. linux.do 全域对本环境 **403**（含 robots.txt 与 RSS），社区渠道只能人工关注，无法也不应自动化。
4. 活动节奏 ≈ **每月 1-2 轮**，节点型（周末/百日/1024/补偿），下一节点预测 1111（主会话原判断，本次时间线佐证）。**新增可自动化监控点：zcode.z.ai/changelog**（静态可抓，历史上有活动上线公告）。
5. 增量发现：**ZCode 客户端 v3.15.1（10-12）上线「邀请好友·免费蹬蹬」活动**——deals.json 尚无客户端邀请条目，待人工核实在场状态（见 §四）。

## 二、已知活动时间线（2026-06 → 2026-10，均单账号规则）

| 时间 | 活动 | 内容 | 佐证来源 | 可信度 |
|---|---|---|---|---|
| 2026-06 | 新用户免费体验 | GLM-5.2 试用 5 天，500 万 token/日，1M 上下文 | 腾讯云开发者文章 cloud.tencent.com/developer/article/2696805 | 中（单源第三方） |
| 2026-08-11 | 用户破 100 万庆祝 | GLM Coding Plan 全体用户周额度当日 13:00 统一重置回满 | 新京报 m.bjnews.com.cn/detail/1786430136129187、证券时报 stcn.com/article/detail/4069038.html、腾讯新闻 | 高（多源媒体一致） |
| 2026-08-16 | 首登送 1 亿 | 首次登录自动到账 1 亿 GLM-5.3 token，**1 小时后官方喊停** | smzdm post.smzdm.com（搜索摘要） | 中-高（单源细节） |
| 2026-08-21~24 | 新用户 1 亿 | 5 万新用户每人 1 亿 GLM-5.3，截至 8-24 09:00 | bilibili 视频页（搜索摘要） | 中（单源） |
| 2026-08-28/29 起 | **周末计划 WEEKEND BUILD** | 每人 3 亿 GLM-5.3-Flash，新老均可领；共 4+ 期，窗口 38-61 小时（如第 IV 期周六 9:00→周日 23:00） | 知乎 zhuanlan.zhihu.com/p/2077004759647654161 + smzdm post.smzdm.com/p/aqrx263p + linux.do/t/topic/2821770 | 高（多源，deals.json deep-zhipu-weekend-3yi 已 verified） |
| 2026-09-03~09-20 | 夜间 Global Build | 每晚 23:00–次日 09:00 ZCode 内 GLM-5.3-Flash 消耗归零（付费套餐专属） | 知乎 zhuanlan.zhihu.com/p/2084215301269472614 | 高（deals.json deep-zhipu-night-global 已 verified） |
| **2026-09-28~10-07** | **代码上传争议补偿**（deals.json 未收录，新数据点） | 全体用户**每日发放 1 亿 token × 连续 10 天**；付费用户另得 4 张周额度重置卡 + 4 张 5 小时重置卡（因「静默上传代码」问题致歉） | 凤凰网 feng.ifeng.com、搜狐 sohu.com（两源媒体一致） | 高（双源媒体） |
| 2026-10-12 | 邀请活动上线 | 客户端 v3.15.1 changelog：「邀请好友·免费蹬蹬，共得权益活动上线」 | **官方** zcode.z.ai/changelog（本日直核） | 高（官方一手，规则待客户端核实） |
| 2026-10-23~26 | **1024 程序员节 5 亿** | 每人 5 亿（GLM-5.3 2 亿 + Flash 3 亿），20 万份先到先得；领取入口 10-23 20:00 开放，额度 10-26 09:00 过期 | 官方活动页 bigmodel.cn/activity/glm-coding-1024（主会话 real 浏览器实锤）+ linux.do/t/topic/3066966、3066104 + 知乎想法（10-24） | 高（deals.json deep-zhipu-1024-5yi 已 verified） |
| 2026-09-10~12-09 | 杭州 Coding Plan 减免（地区型，非 token 礼包） | 个人季卡综合减免 44%、年卡 51%（Lite 年卡 1416→693.84 元）；企业年卡 55%；限 1 次；需杭州社保/学籍证明走飞书表单审核 | **官方** docs.bigmodel.cn/cn/coding-plan/hangzhou-rules（本日直核，静态文档） | 高（官方一手） |

节奏判断：8-11 重置 → 8-16/8-21 礼包 → 8-28 周末计划 → 9 月夜间 → 9-28 补偿连发 → 10-23 1024 → **1111 预测**。每月 1-2 轮、逢节点加码，与主会话判断一致。补偿型活动（9-28 先例）说明产品争议也可能触发发粮，属「意外窗口」。

## 三、官方渠道清单（含可监控性评估）

| 渠道 | URL | 内容 | 自动监控可行性 |
|---|---|---|---|
| ZCode 客户端活动卡片 | 客户端内（v3.10+，左下角） | **领取入口本体**，活动真相源 | ❌ 需登录+客户端，人工 |
| BigModel 官方活动页 | https://bigmodel.cn/activity/glm-coding-1024（活动型 URL，逐期变化） | 活动规则/数额 | ❌ JS 渲染 + 需登录（harvest 纯 stdlib 抓不到；1024 轮由主会话 real 浏览器实锤过） |
| BigModel 促销更新页 | https://docs.bigmodel.cn/cn/update/promotion | 仅 API 侧促销（邀请/资源包/Coding Plan） | ✅ 已在 harvest（zhipu-promo）——**但实测不含 ZCode 客户端活动，勿指望它** |
| ZCode 官网 changelog | https://zcode.z.ai/changelog | 版本日志，**偶有活动上线公告**（3.15.1 邀请活动先例） | ✅ **本轮新增入 harvest（zcode-changelog），实测 4 命中** |
| 官方文档活动规则页 | https://docs.bigmodel.cn/cn/coding-plan/hangzhou-rules（先例） | 地区/专项活动规则，静态 Mintlify | ✅ 本轮新增入 harvest（zhipu-hangzhou-rules，实测 30 命中；活动 12-09 结束后可撤源） |
| 智谱/BigModel 微信公众号 | （无公开 RSS） | **客户端活动的主要公告渠道**（社区共识） | ❌ 需人工关注 |
| linux.do 社区 | linux.do/t/topic/*（见 §二来源列） | 第一时间的用户实报 | ❌ **全域 403**（见 §五） |

## 四、合规收录建议（只收单账号规则）

1. **只收单账号可完成的动作**：更新客户端 → 点活动卡片领取 → 用掉。此路径零成本、合规，全部时间线条目均符合。
2. **不收**（linux.do 帖内出现的批量玩法先例，维持拒收）：「一机号双站各领」「多号切换囤额度」——记录在案、标注不予收录。
3. **杭州减免页提醒**：需提交社保/学籍等**个人证明材料**，属资质审核型优惠而非纯羊毛；如收录，difficulty 建议 3 并注明材料要求，且不代填任何表单。
4. **用户受益实证**（诚实记录）：本爬虫助理自身即跑在 ZCode 活动赠送的 GLM-5.3 系额度上（账号体系 account:bigmodel-start-plan）——「活动真实可领且可用」的第一手证明；但此为单账号正常受益，不构成多号理由。

## 五、linux.do 拦截现状（本日实测，未做任何绕过）

| 目标 | 结果 |
|---|---|
| https://linux.do/t/topic/3005638 （zcode-linuxdo 原始佐证帖） | **HTTP 403 Forbidden** |
| https://linux.do/latest.rss | **HTTP 403 Forbidden** |
| https://linux.do/robots.txt | **HTTP 403 Forbidden**（连 robots 都读不到 → 整域对本环境封锁，更无爬取依据） |

与主会话经验一致。**结论：社区渠道定为「人工关注」，不给 harvest 加源**。建议监控方式：老板/主会话人工刷 linux.do 搜「ZCode」或「发粮」关键词（活动帖标题高度模式化：*Zcode又送/发粮/速领*），或继续以 WebSearch 间接观察（本轮即以此拿到 3005701 等帖号）。另注意原条目帖 3005638 与 3005701 为相邻帖，应为同一轮「速领 3 亿」活动。

## 六、待办（移交主会话/后续轮次）

- [ ] **zcode-linuxdo 处置**：维持 stale 或归档（建议与理由见 HANDOFF.md 本轮小节，主会话拍板）
- [ ] **新条目素材①**：9-28 补偿方案（1 亿 × 10 天 + 重置卡）——已过期，建议作节奏/风险参考入档（类型可仿 deep-zhipu-night-global 的存档做法），是否入 deals.json 由主会话定
- [ ] **新条目素材②（可能仍在场）**：客户端 v3.15.1「邀请好友·免费蹬蹬」活动——changelog 只证「上线」，**在场状态/规则/数额需人工开客户端核实**；核实后可对标 API 侧邀请活动（双方各 2000 万）建条目
- [ ] 1111 节点临近（约两周）：届时优先跑 `python3 tools/harvest.py --only zcode` + 人工看客户端卡片；若出现新活动页 URL（bigmodel.cn/activity/*），real 浏览器实锤后按 deep-zhipu-* 格式建条目
- [ ] zhipu-hangzhou-rules 源在 2026-12-09 活动结束后从 harvest_sources.json 撤下（防 0 命中噪声）

## 来源汇总（本轮新增核实）

- 官方：zcode.z.ai、zcode.z.ai/changelog、docs.bigmodel.cn/cn/update/promotion、docs.bigmodel.cn/cn/coding-plan/hangzhou-rules、bigmodel.cn/activity/glm-coding-1024（主会话 real 实锤）
- 媒体：新京报 m.bjnews.com.cn/detail/1786430136129187、证券时报 stcn.com/article/detail/4069038.html、腾讯新闻 news.qq.com/rain/a/20260811A08AFB00、凤凰网 feng.ifeng.com、搜狐 sohu.com
- 社区/第三方（佐证用，不作收录依据）：linux.do/t/topic/{2821770, 2856309, 2824764, 3001382, 3005638, 3005701, 3066104, 3066966, 2975817, 2791024, 2760055}、知乎 zhuanlan.zhihu.com/p/2077004759647654161 与 /p/2084215301269472614、smzdm post.smzdm.com/p/aqrx263p、腾讯云 cloud.tencent.com/developer/article/2696805、bilibili
