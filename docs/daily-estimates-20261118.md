# 每日免费额度情景估计 · 2026-11-18

用户要求对有固定日免费次数/积分的产品提供估计折算。本轮为 20 条记录补 `daily_estimate`，共 18 个独立额度池；新增权益 0 条、归档 0 条。Groq 一条来源状态由 verified 改为 stale：当前官方公开限额表主要展示 Developer 档，免费账号记录的 1000 次/天需在个人 Limits 中核对，不冒称是新确认的官方免费额度。

## 估计方法

- 次数型：默认每次合计 1000 / 4000 / 8000 输入输出 Tokens，用户可修改参考值，低/高随之按 ¼ / 2 倍调整。OpenRouter 默认仅取未充值的50次，不套用付费解锁的1000次。
- 积分售价型：按平台公开积分包或套餐单价区间折 DS Flash 购买力，不声称实际到账 Token；国内与国际 WorkBuddy 分别使用对应币种与价格。套餐含其他功能，因此不叫积分面值。
- Neurons：Cloudflare 使用官方给出的三款免费可用模型计价，假设输入:输出=3:1、无缓存；未套用需要付费账号的模型。
- 无公开比例的文本积分：提供可调整的站内示意假设，默认500/1000/2000 tokens/积分。Poe和clixad分别按0.05和0.1倍率示意；这些数是展示量级的人工假设，既非官方兑换率，也不是统计置信区间。界面与信源详情明确写出，允许替换为个人实测。
- 音乐生成、GPU小时等不套文本积分假设。WPS月估计按前6天100智点、后24天200智点；未把新客奖励当作每日奖励。

## 公开依据

| 平台 | 依据 |
|---|---|
| OpenRouter | [共享免费模型限额](https://openrouter.ai/docs/api_reference/limits)：未充值默认50次/天；多个免费模型共用额度。 |
| Qoder | [套餐及加量包](https://docs.qoder.com/account/pricing)：Pro $20/2000 Credits，加量包$20/1500 Credits；[每日领取](https://docs.qoder.com/events/100credits)为100 Credits。 |
| WorkBuddy 中国 | [腾讯云计费概述](https://cloud.tencent.com/document/product/1831/134333)：标准档¥99/2000基础积分（加赠时4000）、高级档¥199/4000。日送100积分沿用原记录，未借售价复核提升赠送政策状态。 |
| WorkBuddy 国际 | [定价](https://www.workbuddy.ai/docs/workbuddy/pricing)：Free活跃日30 Credits、月基础100；Pro月$10含1000基础+1000加赠，加量包$15/500。 |
| MiniMax Code | [官方购买积分包](https://platform.minimaxi.com/subscribe/token-plan)：¥30/4489、¥150/22460、¥500/74900。签到400积分沿用记录，是否同积分体系与适用模型以账号为准。 |
| Cloudflare | [Workers AI定价](https://developers.cloudflare.com/workers-ai/platform/pricing/)：10000 Neurons/天；模型情景为Llama 3.3 70B fp8 fast、Llama 3.1 8B fp8、Llama 3.2 1B。 |
| Groq | [限额说明](https://console.groq.com/docs/rate-limits)：RPM、RPD、TPM、TPD分别限制，先触顶者生效，具体看账号。 |

其他积分型记录沿用其现有信源与核验状态。本轮只添加公开标注的估计，不用估计结果证明日赠政策有效。

## 展示与计算

列表金额位置显示每日估计区间，保留原始日额度，点击「估算依据」可进入弹窗。表头提供「日额度估计」入口，输入假设保存在本机浏览器，调整后列表排序与弹窗联动。已核验总账保持独立，估计不抵扣API账单。

OpenRouter与ERNIE免费模型共享池只计一次；魔搭调用次数与魔粒视图同池，汇总优先采用次数视图。首月估计不超过30天或活动剩余天数；低/参考/高分别折月，不把月积分摊成新发的每日积分。

新增4个售价页面监控，均 `auto_verify:false`；Cloudflare沿用既有监控。价格变化后进入待复核，不自动确认估计比例。

## 验证

回归检查覆盖次数乘用量、官方Neurons模型费率、积分售价币种、可调假设、WPS分阶段奖励、截止日期、重复池、已核验额度与API抵扣隔离，以及全部301条记录前端/静态页公式一致性。

本地浏览器检查中文390/768/1440px、英文320/900px：无横向溢出，桌面首屏至少4条，320px微信群码可见；20条估计/18池、参数修改与保存、恢复默认、来源假设、键盘Escape关闭、原总账数值稳定均通过。发布后再检查正式站与镜像的页面及脚本。
