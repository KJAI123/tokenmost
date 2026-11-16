# 0 元搭一套 AI 开发环境：免费 token + 免费云 + 免费域名全链路

> 数据截至 2026-11-16 核实，全部官方渠道口径。

---

很多开发者以为「搞 AI」的门槛是订阅费和服务器费。实际 2026 年底，用官方免费渠道可以搭出一条完整的生产级链路。这篇按依赖顺序讲：模型 → 算力 → 域名邮箱。

## 一、模型层：每日刷新型额度是主力

一次性的注册赠送（Today AI 3 亿、FiimeOPC 最高 1 亿）开荒很爽，但烧完就没了。真正的长期饭票是每日刷新型：

1. 智谱 BigModel：GLM-5.3-Flash 每日放量约 3 亿 tokens，OpenAI 兼容端点直连，当主力模型完全够用。
2. 美团 LongCat：560B 开源旗舰 API 每日 5000 万 tokens，Anthropic 协议也能接——Claude Code 用户可以直接喂。
3. AMD Token Factory：开源模型每日免费额度重置（DeepSeek/GLM Flash/MiMo），OpenAI+Anthropic 双端点，20 RPM。
4. 需要顶级模型时再按量付费：DeepSeek 错峰 5 折 + 缓存命中 0.04 元/百万，夜间批量成本忽略不计。

## 二、算力层：给 Agent 配免费云工位

1. InstaBox：免费 4C8G microVM（常设计划非试用），自带浏览器环境，MCP 协议可直接被 Claude Code 指挥——跑自动化任务的神器。
2. Oracle Always Free：永久免费层，⚠️ 但 2026-06 起纯免费号的 ARM 配额砍半为 2 核 12G，且有 7 天闲置回收（利用率 <20% 停机）。
3. Modal：每月 $30 compute credits 月月刷新，GPU 也能用——跑批推理/Embedding 的白嫖首选。
4. GitHub Codespaces：120 core-hours/月，云端开发环境秒开。
5. e2b：Agent 沙盒 10 并发免绑卡，跑代码执行类任务。

## 三、域名邮箱层：0 元收发

1. 域名：Northwest 首个 .com 免费注册（≤$25 它承担）；DigitalPlat 免费二级域接 Cloudflare。
2. DNS/证书：Cloudflare 免费档全包。
3. 收信：Cloudflare Email Routing 无限地址转发；进阶用开源 cloud-mail 自部署 webmail（坑：noRecipient 默认值会导致新地址邮件消失，改 0）。
4. 发信：Resend 免费档每日 100 封，用自有域名。

## 四、组合建议

- 学生/个人项目：智谱每日额度 + InstaBox + DigitalPlat 域名 = 完全 0 元跑起来。
- 小团队：免费额度打底 + DeepSeek 错峰付费补峰值 + Modal 跑批 = 月成本可控在个位数人民币。
- 合规红线提醒：只走官方渠道，别碰代充/共享账号/多号薅——封号风险远大于省下的钱。

## 五、情报层

这些规则变化极快（智谱放量节奏、Oracle 配额、注册商政策说变就变），人工盯不过来。我自己是拿 TokenMost（tokenmost.com）当总账本的：260+ 条情报每条带核实日期、过期自动下架，免费云服务器专区把上面这些平台全部覆盖，还有 DeepSeek 等效口径的比价计算器。数据层 deals.json / llms.txt 开放，可以直接程序化消费。

以上。你搭过的最省钱的 AI 环境是什么配置？评论区交流。
