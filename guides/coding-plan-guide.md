# Coding Plan 选购攻略：谁的积分最值钱，谁在挖坑

> 核实于 2026-10-27 ｜ 全文只列各厂商**官方公布的数字**，官方不公布的一律标注。

## 先看一张表：官方敢公布折算的只有这三家

绝大多数编程套餐的「积分」是黑箱，官方不给 token 换算。敢把公式写在文档里的目前只有三家：

| 厂商 | 计量 | 官方折算口径（原文） | 出处 |
|---|---|---|---|
| 智谱 GLM Coding Plan | 积分 | 消耗积分=(输入×系数+缓存×系数+输出×系数)÷10000；GLM-5.3 系数 6.9/1.7/24、GLM-5.3-Flash 2.3/0.56/8；1 积分=1 万加权 token | docs.bigmodel.cn/cn/coding-plan/overview |
| 讯飞 Token Plan | 积分 | 每百万 token 耗积分表：Spark-X2-Flash 输入 100/输出 200（最便宜档），GLM-5.2 800/2800，DeepSeek-V4-Pro 1200/2400 | xfyun.cn/doc/spark/TokenPlan |
| SCNet Token Plan | Credits | 官方示例：6 万 Credits ≈ 缓存命中输入 1.2 亿 / 输出 170 万 / **综合约 3000 万 tokens**（Kimi-K2.6，倍率 1.0） | scnet.cn 官方 OpenAPI 文档 |

**快算口诀**：按智谱公式，Lite 档（¥94.4 首月/¥118 续费）周额度 10000 积分 ≈ **Flash 输出 1250 万 tokens/周**；把重活排到「非高峰时段」（工作日 14-18 点以外，按 50% 计）直接翻倍。

## 积分→token 快速换算表（仅列官方数字可推的）

- **智谱 Lite**：2000 积分/5h + 10000/周 ≈ Flash 输出 250 万/5h 或 1250 万/周（闲时口径再 ×2）
- **智谱 Pro/Max**：12000/60000 与 28000/140000（同公式线性放大）
- **讯飞基础版**：¥30/月 6 万积分 ≈ Flash 输出 3 亿 tokens 或 Kimi 综合约 3000 万
- **SCNet 基础版**：¥30/月 6 万 Credits ≈ 综合 3000 万 tokens（倍率 1.0 模型；Flash 类倍率 0.13-0.15 可放大 6-7 倍）
- **不可换算的黑箱**：Kimi（官方只给"简单请求约 ¥0.03、复杂任务约 ¥1.6"）、Claude（官方拒绝公布绝对数，Settings>Usage 进度条是唯一口径）、Copilot（AI Credits 无 token 换算）

## 决策树：你该买包月还是按量

1. **每天写代码 <2 小时 / 只是偶尔问问题** → 别买包月。用免费层：智谱 8 款免费模型 + GLM-5.3-Flash 限免、Qoder 社区版月 100 Credits、CodeBuddy 体验版 500 Credits/月、Trae 免费档 500 积分/月，轮着够用。
2. **重度但能接受限定模型** → 首选**智谱包月**：官方公式透明、闲时 5 折、Flash 限免兜底；¥49 V2 老价若还能续（老用户权益）是全场最划算档。
3. **要多模型聚合（GLM+DeepSeek+Kimi 一份钱）** → **讯飞 Token Plan ¥30 档**或 **SCNet ¥30 档**，两家都有官方折算且 Flash 类倍率极低；注意都禁 API 自动化调用（仅编程工具交互式使用）。
4. **海外模型刚需（Claude/GPT 原生）** → Claude Max/Team 订阅满 7 天可领 API credits（限 Max/Team，非 Pro）；GitHub Copilot 按新 AI Credits 体系选档。
5. **算力侧需求（微调/跑模型）** → 走 GPU 租赁（并行智算/智星云/AutoDL 学生价），别用编程套餐硬凑。

## ⚠️ 翻雷清单（2026 年实雷，收录站实测/官方口径）

1. **讯飞 ¥3.9 不限量 Coding Plan——已翻车**：2026-03 上线、4 月宣传"不限量"，5 月起 system busy，8-13 用户称"几乎瘫痪"（GLM 系上下文被压到 50K），8-18 微博/小红书集中退款；官方仅口头"服务器超载"。现行文档最低档已改 ¥199。教训：**超低价"不限量"不可持续，订阅一律按月不囤年卡**。
2. **GitHub Copilot 已改 AI Credits 计量**：老口径"Pro 300 / Pro+ 1000 premium requests"作废；现为 Pro $10=1500 credits、Pro+ $39=7000、Max $100=20000（官方 docs 直核）。看旧攻略买 Copilot 会算错账。
3. **Cursor 已并入 X Subscription**：SpaceX 收购 Anysphere 后（2026-08-14 交割），2026-10-12 起官方档位变成 Plus $8 / Premium $30 / Super $100 / Ultra $200 的共享池（周刷新，Grok 模型为主）。**老攻略"$20 Pro=500 fast requests"全部过期**；社区正抱怨套餐重叠混乱，建议观望再入。
4. **Kimi 新老会员双轨**：新会员（Plus ¥99 及以上）Kimi Code 取消周限额、只有 5 小时滚动窗口；老会员仍有周限额。Go 档（¥49）**没有** coding 额度，别买错。
5. **Trae 计费争议**：GitHub issue #2318 用户称 2026-02 计费变更令权益缩水 5-10 倍、GPT-5.3-Codex 仅 Ultra 档可用。国内版现为五档积分制（Free 500 积分起，官方页直核），下单前看当前规则。
6. **文心快码 Auto-Free"不限量"是旗舰档福利**：免费档只有补全；专业版 Auto-Free 限 150k tokens/h；"不限量至 2026-12-31"绑 ¥199/月旗舰版（官方文直核）。看到"免费不限量"标题党的先看绑定档位。
7. **智谱多 IP 风控**：官方明文禁共享、3 次违规封号，社区已有"服务器+多 IP+出差"被封 Lite 的实锤。单人单环境最安全。
8. **火山协作奖励计划**：数据授权"永久且已采集不可撤回"（官方原文），且 2026-09/10 两轮共 40 款模型退出名单——报名前看在列模型 + 想清楚隐私。

## 一句话总结

**要透明买智谱（有公式），要便宜买讯飞/SCNet 基础档（¥30 有官方折算示例），要白嫖先薅各家免费层，翻雷区记住一条：所有"不限量"都问一句"限制条件写在哪一页"。**

---
**核实于 2026-10-27**。来源列表：
- 智谱官方文档（.md 直核）：https://docs.bigmodel.cn/cn/coding-plan/overview ｜ /usage-revision ｜ /faq ｜ /usage-notes
- 讯飞官方文档：https://www.xfyun.cn/doc/spark/TokenPlan.html ｜ /CodingPlan.html
- SCNet 官方文档：https://www.scnet.cn/ac/openapi/doc/2.0/moduleapi/plans/token-plan.html
- 讯飞 3.9 翻车复盘：https://post.smzdm.com/p/a4q5znk8 ｜ 新浪财经实测：http://finance.sina.com.cn/wm/2026-04-20/doc-inhvcewk6911910.shtml
- Copilot AI Credits：https://docs.github.com/en/copilot/get-started/plans-for-github-copilot
- Cursor/X Subscription：https://cursor.com/pricing ｜ https://x.ai/news/x-subscription
- Kimi 会员权益：https://www.kimi.com/code/docs/kimi-code/membership.html
- 文心快码价格与 Auto-Free：https://cloud.baidu.com/article/8412345（官方域）
- Trae 国内价目：https://www.trae.cn/pricing ｜ 计费争议：https://github.com/Trae-AI/TRAE/issues/2318
- Kimi K3 与多 IP 封号案例（中置信）：linux.do / Telegram 社区帖
