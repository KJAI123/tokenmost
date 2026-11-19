# AutoClaw 资讯管线复核（2026-11-20，北京时间）

目的：消化最新资讯线索，更新真实可用的额度、折扣及收费条件。采集与核验分开记录。

## 查阅范围与结果

已查阅 AutoClaw 找源巡检（最近一轮 11 月 19 日 20:37）、TG 资讯、公众号第 95/96 轮及 11 月 19 日采集变化告警；本轮用 11 月 20 日可访问的官方资料复核。新增 6 条公开记录，修订/复核 11 条既有记录；CodeHost 1 条转过期，LLM7 1 条降为状态信息并撤出额度估算。7 个官方页面新增监控，原有来源复用；旧 LLM7 Limits 发现任务停用，文档入口复用已有任务。

## 已落地

| 平台 | 处理 |
| --- | --- |
| DeepSeek | 新增搜索计费口径：模型触发工具免单独调用费，仍计模型 Token；独立 Search/Fetch 仍按成功次数收费。复核模型、缓存与空闲时段价格。管线“六折变五折”未具名平台，未当成 DeepSeek 官方新降价事件。 |
| Qoder 国际版 | 11 月 19 日 10:00（UTC+8）起，每日 100 Credits 限 Pro 试用与个人付费；免费账号已停领。保留原始日额和条件估计，排除常规免费总量。新增 Qwen3.8-Max/Flash 错峰四折、Ultimate 第二期二折和 Efficient 条件免扣三条。 |
| Electron Hub | 新增免卡 $0.25/周；周日 21:00 UTC 刷新。按 30/7 周显示购买力参考；广告奖励须完成广告，不当成无条件日赠叠加。增加导航及官方 Logo。 |
| 腾讯 TokenHub | 新增原厂 DeepSeek Search/Fetch 收费消息，分别说明 API 与 TokenPlan 的生效时间、单位；不套用 DeepSeek 官方直连工具费政策。体验包条目补相关证据与说明。 |
| 天翼云星辰 TokenHub | 既有息壤条目按现行免费量包更新为支持模型每款 50 万 Tokens、14 天；旧 2500 万口径与折算保存在历史字段，不再纳入当前参考。保守计一款可领模型，明确用完即停。补官方文档与导航。 |
| OpenCode | 复核 GLM-5.3 Go/Go Plus 单用模型的 $500/$1,000 限额仍在场，至 11 月 22 日。更新 12 个免费型号，注明免费聊天要求 OpenCode、地区限制及 GLM-5.3-Flash Free 已下线。 |
| AutoClaw | 本周登录 1 亿端内 Tokens 活动仍在场，11 月 22 日 23:59 北京时间到期；不当作通用 API 额度。 |
| LLM7 / CodeHost | LLM7 旧 /limits 404，新文档无原日额依据，保留历史证据、撤出估算并保留待复核。CodeHost 已记录活动截止 11 月 17 日，标记过期；不将当前 403 推断为服务停服。 |

Hugging Face 免费推理赠金此前已标过期，本轮核对官方 Free Users=None，沿用处理；同步改正导航中旧“每月 $0.10”口径。

## 暂未上架为已核验

- 星辰智能体云电脑已定位 `agent.teleai.com.cn`，本轮访问转官方手机号/账号登录页。4C8G、磁盘、权益周期、使用时长和资格仍需登录后权益页核对，已追加发现队列；不与千问云电脑混同。
- 纯模型发布、付费额度缩水的用户报告及无法核实的福利，继续留在原管线记录；不据此编造可领取额度。

## 主要官方依据

- [DeepSeek 模型与工具价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)
- [Qoder 每日 100 Credits 资格](https://docs.qoder.com/events/100credits)
- [Qoder 分模型错峰倍率及精确 UTC 截止时间](https://docs.qoder.com/events/offpeakrate)
- [Qoder Efficient 免扣范围](https://docs.qoder.com/events/efficientunlimited)
- [Electron Hub Free 计划](https://www.electronhub.ai/pricing)（浏览器渲染核对）
- [腾讯 TokenHub 搜索收费公告](https://cloud.tencent.com/announce/detail/2538)
- [天翼云免费量包](https://www.ctyun.cn/document/11061839/11100599)、[产品动态](https://www.ctyun.cn/document/11061839/00000000)
- [OpenCode Go 限额](https://opencode.ai/console/go)、[免费型号和下线名单](https://opencode.ai/docs/console/models/)
- [AutoClaw 本周官方活动](https://autoclaw.zhipuai.cn/blog/news/M11W3/)
- [LLM7 当前文档目录](https://docs.llm7.io/llms.txt)

## 验收范围

- 历史来源保留、数据格式及 JS/Python 折算一致性通过，覆盖全部 308 条记录；补充周额度、条件日赠排除及 LLM7 撤额回归断言。
- 中英文首页 1440/768/390/320px 均无横向溢出；桌面首屏均完整显示 4 条，窄屏二维码可见。
- 已验证搜索、空状态重置、额度总账入口、来源展开、Electron Hub Logo 与周额度显示、OpenCode 12 型号展开及独立付费推荐保留。过期 CodeHost 未再显示于云资源区。
- 仅保留相关生成页变化，未刷新其他平台的页面日期。发布后另以真实生产返回核对。
