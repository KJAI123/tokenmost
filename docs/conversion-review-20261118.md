# 额度折算复核 · 2026-11-18

目的：补齐能折算的额度，统一列表、排序、总账、路线图、比价器和平台静态页的单位。此前金额被漏算、已折算数值和金额重复进入排序、月额度伪装成日均、短期体验按长期每日累加。

本轮更正 75 条额度记录，新增权益 0 条、合并归档 0 条；其中 2 条活动标记失效。旧换算保存在条目的 `quota_history`，证据链接保留。

- 原始 Token 直接入账；官方积分公式按明确模型折算，显示原积分及计算依据。
- 模型金额额度按输入:输出 3:1、无缓存、DeepSeek Flash 空闲价作购买力参考：人民币 ¥1.75/百万，美元 $0.2625/百万。不声称这些 Token 实际到账或跨平台通用。
- 日额度按剩余有效天数（最多 30）计；月额度计一次；ZCode 体验只计 5 天。Fiime 红包最高值与任务上限另列，修复原先把月任务重复相加的问题。
- 常规总账仅含已核验且无需付费/申请的可折算权益。学生另列；付费、随机上限、额外领取资格和没有固定 Token 比例的积分/次数/算力不进入常规总额。
- 比价器将每日用量正确乘 30，按目标模型匹配实际 API 抵扣，不把等效购买力或客户端用量当模型余额。

## 主要官方依据

| 核对项 | 官方页面与结论 |
|---|---|
| 折算基准 | [DeepSeek 人民币](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)、[美元](https://api-docs.deepseek.com/quick_start/pricing/)：空闲输入/输出分别 ¥1/4、$0.15/0.60 每百万。 |
| GLM Coding | [个人版用量公式](https://docs.bigmodel.cn/cn/coding-plan/overview)：积分=(输入×系数+缓存×系数+输出×系数)/10000；周和 5 小时同时限额，闲时模型积分减半。按 GLM-5.3、3:1、无缓存、周额度×30/7作月参考，展示高峰到闲时区间，不视为保证月额度。 |
| SCNet | [Token Plan](https://www.scnet.cn/ac/openapi/doc/2.0/moduleapi/plans/token-plan.html)：60000 Credits 官方例为未缓存纯输入720万/纯输出170万；统一3:1无缓存推算约398万。此前3000万是含缓存的综合案例，已更正；次月对应日到期。 |
| MiMo Token Plan | [价格与扣费](https://mimo.mi.com/docs/zh-CN/price/token-plan)：Lite 41 亿 Credits；Flash 未缓存输入 100、输出 200 Credits/token。3:1时约 3280 万原始 Token/月；Pro 模型对应量不同。 |
| ZCode | [连接 BigModel](https://zcode.z.ai/cn/docs/configuration)：5 天内每天 GLM-5.3 300 万 + Flash 500 万原始 Token，按两款模型分别折算。 |
| AutoClaw | [M11W3](https://autoclaw.zhipuai.cn/blog/news/M11W3/)：一次性 10,000 积分=1亿端内 Token，11 月 22 日失效；不作为通用 API 抵扣。 |
| Kimi | [新客测试权益](https://www.kimi.com/help/kimi-api/api-free-trial)：实名后 ¥15，3 个月有效，K3 除外。 |
| GitHub Copilot | [套餐额度](https://docs.github.com/en/copilot/get-started/plans)、[Credits 与模型定价](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)：1 AI Credit=$0.01；Pro/Pro+ 总月额度 1500/7000，分开展示购买力参考，不加入实际 Token 套餐排名。 |
| Vercel / LiveKit / Zed | [Vercel](https://vercel.com/docs/ai-gateway/pricing) $5/月；[LiveKit](https://docs.livekit.io/deploy/admin/quotas-and-limits/) $2.50/月；[Zed 学生](https://zed.dev/education) $10/月，12 个月。保留使用范围和资格。 |
| LLM7 | [限制](https://docs.llm7.io/limits)：免费文本 API 输入输出合计 10 万 Token/24 小时，直接按原数计。 |
| 失效修正 | [Hugging Face](https://huggingface.co/docs/inference-providers/pricing) 当前 Free Users 月赠金=None；[Qoder DeepSeek 限免](https://docs.qoder.com/events/deepseek-flash-free) 10月31日结束。[每日100 Credits](https://docs.qoder.com/events/100credits)仍有独立活动，不使用未知积分比例强转。 |

## 验证与未解决项

本地：数据校验、来源保全审计通过；回归覆盖币种、官方模型公式、日/月周期、截止日期、短期体验、单次与周期不重复计数、API抵扣范围，以及全部 301 条记录的前端/静态页计算一致性。中文 390/768/1440px、英文 320/900px 检查无溢出、桌面首屏完整 4 条、320px微信群码可见、信源可展开、总账与横幅一致，日用量与缓存月费计算正确。

没有官方固定比例的积分、次数、语音生成和 GPU 小时继续保留原单位。既有待复核权益仅更正计算表达，不因算式成立而升级核验状态；智云新疆的比例来自已有历史官网记录，当前可用性仍待实测。汇率 7.2 仅为比价展示的固定假设，人民币与美元购买力分别使用各自价格，不借汇率互推。

线上：发布后核对正式站与镜像的页面、数据、脚本及关键交互，结果记录于发布提交后的交付说明。
