# TokenMost 全量换算与 Logo 复核 · 2026-11-20

本轮核对全部 308 条数据的计算和展示，修订 30 条，没有新增权益记录。没有把全部旧记录提升为当前已核验。完整逐项分类见 `data-research/audits/quota-logo-20261120.json`。

当前非警示在架 202 条：47 条有明确额度或金额购买力参考，36 条提供独立情景估计，11 条保留非文本原单位，108 条为未定额、免费模型、会员、折扣或规则信息。情景共 47 个周期视图，常规免费合计按 36 个独立池去重。

## 计算与展示

- 新 `quota_estimates[]` 兼容旧日额度字段，支持一次性、月、周、日多个周期。一次性与月额分别计一次，日额最多 30 天，周额按活动有效天数÷7。
- 补齐 TRAE、CodeBuddy、WorkBuddy、小浣熊、华为码道、AStudio、MonkeyCode、Cohere、百炼、Qoder CN、GitHub Copilot 等原始额度与估计；金额、模型示例和未知积分假设分别说明依据。
- CodeBuddy 与 WorkBuddy 国内月 500 积分共池，只算一次。付费 Pro、Rovo Dev 的 Jira 资格、邀请等奖励单列，不进常规免费合计。
- Clixad 使用当前官方 60,000 共享日用量上限和每轮 20,000 输入+1,500 输出的三模型示例，替代旧 120,000 与人工倍率。全站日预算可提前耗尽，不是保证能调用的 Token 量。
- Copilot 按每月 2,000 次短代码补全、每次 50/200/400 输入输出 Tokens 作可调情景；没有把补全次数当成聊天次数或 AI Credits。Cohere 的 1,000 次是月限，不是日赠。
- Qoder CN 的 300 试用积分只计一次，使用中国区人民币套餐价格；没有混用国际版美元价格。百炼保守计一款典型 100 万包，各模型额度不可转移。
- 果办改正为注册 300、免费日赠 50。MiniMax 补充包使用当前中国区 4,489/22,460/74,900 积分和人民币价格，不继续引用旧美元包。
- 3 条云服务历史 Token 估值撤回并保存在历史字段。音频、图片、PU、GPU 小时、云工作空间和会员估值保留原单位；无限量、动态限额和滚动窗口不编造 Token 总量。
- NVIDIA 旧积分、AutoClaw 邀请上限的适用对象和任务条件等，仍需对应现行权益证据，未借其他活动比例强算进免费总量。

## Logo

- 增补/替换 18 份官方品牌素材；多中心超算目录另用 1 个自绘分类标识。来源、文件哈希和分类说明见 `assets/logo-sources.json`。
- 识别 16 个旧灰底字母图片并禁止重新引用；图片能加载不再等于品牌核验。当前映射引用 175 份图片。
- 导航图标覆盖 95/96；仙童智算仍用文字标识，其官网本轮浏览器访问报 SSL 版本/密码套件不兼容，未绕过安全校验。
- AgentRouter 当前入口有验证页，秒悟/Drex 等老站未取得可确认的官方图标，保留文字标识；未使用验证码页或随机目录图片冒充 Logo。
- 修正导航中 AutoClaw 的旧独立域名，指向智谱官方 AutoClaw。加载成功前保留文字，图片失败时回退；文档域名和邀请链按提供方匹配，资讯站/CDN 不能冒充品牌。
- 新增 12 个官方变化监控页，均 `auto_verify:false`，原有监控按 URL 复用；页面哈希不代替人工核验。

## 验证

- 数据检查、来源保留检查、JS/Python 全部 308 条计算一致性通过。补充混合周期、周额有效天数、共享池、条件排除、短补全情景及完整聚合显示断言。
- 中英文 320/390/768/1440px 内容视口均无横向溢出；1440×900 首屏完整 4 条，320px 二维码可见。完整列表有 98 个平台行，无“加载更多”。
- 原生浏览器视口覆盖在此会话未生效，使用同源 iframe 的真实内容宽度并断言 `clientWidth` 完成响应式验收，未将默认 1280px 误报为手机验收。
- 验证 320px 估算弹窗、多周期说明、共享池标记、参数即时修改、恢复默认和 Escape 关闭。每次请求 4000→8000 时，OpenRouter 参考日估计从 20 万增至 40 万；随后恢复默认。
- 已恢复 92 个仅日期变化的生成页，只保留有内容变化的页面。生产和镜像发布后另核对实际返回。

## 主要官方依据

- [Qoder CN 计费](https://docs.qoder.cn/product-overview/billing-description) · [TRAE 当前积分](https://docs.trae.cn/ide_plans-and-billing) · [CodeBuddy 共享额度](https://www.codebuddy.cn/docs/ide/Account/pricing)
- [Cohere 月调用限制](https://docs.cohere.com/docs/rate-limits) · [百炼模型独立额度](https://help.aliyun.com/zh/model-studio/new-free-quota) · [Copilot 补全与 AI Credits](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing)
- [Clixad 模型示例](https://clixad.io/free-ai-models-for-coding/) · [MiniMax 当前 M Plan](https://www.minimax.cn/m-plan) · [OfficeAce 免费档](https://activity.huaweicloud.com/officeace.html)
- [硅基流动认证券与邀请券](https://www.siliconflow.cn/developer-talk/od7wj9rr23p95uhihmhrombp) · [WorkBuddy 国际版](https://www.workbuddy.ai/docs/workbuddy/pricing) · [Rovo Dev 资格与积分价格](https://support.atlassian.com/subscriptions-and-billing/docs/how-billing-works-for-rovo-dev-standard/)
