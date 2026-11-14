# 给 AI Agent 搭一个 0 元算力栈：免费 token + 免费云服务器（2026-11 核实）

> 掘金开发者向。目标读者：跑 Claude Code / Codex / 自建 Agent 的开发者。

前端时间帮团队把「跑 Agent 的固定开销」压到了接近 0，方案核心是**官方免费额度 + 免费云层**组合。分享实测清单，全部官方口径，核实于 2026-11-14。

## 一、每日/每周刷新型（耐耗主力）

- **智谱 BigModel**：GLM-5.3-Flash 每日 3 亿 tokens（Weekend Build 已升级为每日放量），OpenAI 兼容端点直连
- **ZCode 客户端**：11-13 起每人 5 亿 tokens 新礼包；周末另有周常福利
- **AutoClaw**：每周登录送 40M~132M（本周 100M）
- **AMD Token Factory**：开源模型 API 每日免费额度重置（DeepSeek-V4 Flash/GLM Flash/MiMo），OpenAI+Anthropic 双兼容端点，20 RPM

## 二、注册一次性（新号开荒）

- Today AI：3 亿 tokens + 3 个月 Pro
- FiimeOPC：算力红包单个最高 1 亿 + 每日任务 5000 万
- 阿里云百炼：每模型 100 万 tokens 开通即发（90 天）
- 文心千帆：17 个模型各 100 万

## 三、免费云工位（Agent 落脚）

- Oracle Always Free（⚠️2026-06 纯免费号 ARM 砍半为 2C12G + 7 天闲置回收）
- InstaBox：4C8G microVM 常设计划，MCP 可接 Claude Code
- Modal：每月 $30 credits 月月刷新（GPU 可用）
- e2b：Agent 沙盒 10 并发免绑卡

## 四、接入与省费技巧

- DeepSeek 错峰全模型 5 折（北京工作日白天以外），批量任务放夜间
- 缓存命中低至 0.04 元/百万——改稿/调试类会话务必复用上下文

## 五、情报层

渠道规则天天变（本周 AutoClaw 是 100M，上周 50M），人工盯不过来的话可以用 [TokenMost](https://tokenmost.com)（tokenmost.com）：260+ 条情报每条带核实日期、过期自动下架，免费云服务器专区 + DeepSeek 等效比价，数据层 deals.json 开放可程序化消费。

求验证过的渠道补充，评论区对口径。
