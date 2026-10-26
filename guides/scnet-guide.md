# SCNet 国家超算互联网全攻略：tokens、卡时、OpenClaw 三线薅法

> 核实于 2026-10-27 ｜ 难度：★★☆（要实名）｜ 国家队平台，价格屠夫：综合约 1 元/百万 tokens、OpenClaw 续购 0.1 元/百万

## 这平台有什么可薅（三件套）

1. **邀测计划**：100 卡时 GPU + 500G 分布式存储 + 1000 万 tokens 体验额度（verified，官方邀测文档）
2. **OpenClaw 部署福利**：2026-03 活动每人 1000 万 tokens（限时 2 周用完）；续购价 **0.1 元/百万 tokens**（官宣，全网最低档）（中-高）
3. **Token Plan 包月**：¥30/月起，官方折算示例透明（verified）

## 线路一：邀测 100 卡时（GPU 玩家主线）

1. **注册**：https://www.scnet.cn → 右上角注册。
2. **实名认证**：个人实名即可（必须，所有福利的前提）。
3. **进邀测活动页**：https://www.scnet.cn/ycjh/index.html （JS 渲染，登录后看）→ 点「领取算力资源」。
4. **选资源**：选择要测的资源点【立即获取】→ 到账 **100 卡时异构加速卡 + 500G 存储**；另有 **1000 万 tokens 热门大模型体验额度**（DeepSeek-R1 等）。
5. **用法**：控制台部署环境跑训练/推理；或进 Chat 页直接免费对话 DeepSeek-R1（DeepSeek-V4 限时免费对话口径待核实）。

⚠️ 邀测是**限时名额制**，资源池时有时无；100 卡时约等于 4090 连跑 4 天多，按需申请别囤。

## 线路二：OpenClaw 部署（Agent 玩家主线）

1. **入口**：https://www.scnet.cn/ui/chatbot/openclaw →「一键部署 OpenClaw」（部署会同步开通模型 API + 共享存储服务）。
2. **历史活动**：2026-03 面向全体 OpenClaw 用户发过每人 1000 万 tokens（活动期登录自动发放）。**该活动窗口已过，当前是否延续需登录确认**（入口页仍在）。
3. **续购价 0.1 元/百万 tokens**（官宣口径）——如果是重度 Agent 用户，这个价格比官方 DeepSeek API（输出 27 元/百万）低两个数量级，靠的是超算闲时算力。
4. ⚠️ 官方安全提醒原文：核实 Skill 来源、勿装高风险插件、防数据泄露——OpenClaw 插件生态是最大攻击面。

## 线路三：Token Plan 包月（API 玩家主线）

| 档位 | 活动价 | 月度 Credits |
|---|---|---|
| 基础版 | **¥30**（原 ¥50） | 60,000 |
| 标准版 | ¥110 | 240,000 |
| 高级版 | ¥265 | 600,000 |
| 旗舰版 | ¥764 | 1,800,000（送 OpenClaw 2核4G 实例） |

- **官方折算示例（唯一敢给数字的厂商之一）**：6 万 Credits 全部折算 ≈ 缓存命中输入 1.2 亿 tokens，或非缓存输入 720 万，或输出 170 万，**综合约 3000 万 tokens**（以 Kimi-K2.6、倍率 1.0 计）。
- **模型倍率表**（按周调整，2026-09-01 版）：DeepSeek-V4-Flash 0.13 / GLM-5.3-Flash 0.15 / Qwen3.8-Flash 0.14（最便宜三档）；GLM-5.3 2.29 / Kimi-K3 4.12（旗舰反而贵，别用包月跑旗舰）。
- **购买**：控制台 → 模型服务 → Token Plan；专属 Key（`sk-tp-` 开头）与通用 Key 不通用，用错不抵扣。
- ⚠️ 规则：自然月有效到期清零；每账号同时只能持有 1 个套餐；不可升降档；**仅限 AI 工具（Claude Code/OpenClaw/Cursor）交互式使用，禁 API 自动化/后端/批量调用**，违者封 Key；严禁共享。

## ⚠️ 红线与坑

- 实名信息必须真实，活动申请人工审核。
- 「DeepSeek 官方 1/8 价」流传口径**未获官方原文支持**——可核口径是：综合 1 元/百万（倍率 1.0）、Flash 类综合 0.13-0.15 元/百万、OpenClaw 续购 0.1 元/百万。
- Credits 到期清零不结转——按月买、按月用，别一次囤半年。

---
**核实于 2026-10-27**。来源列表：
- 官方 OpenAPI 文档·Token Plan（直核，高）：https://www.scnet.cn/ac/openapi/doc/2.0/moduleapi/plans/token-plan.html
- 官方邀测快速开始文档（直核，高）：https://www.scnet.cn/help/docs/mainsite/activity/invite/quick-test/index.html
- 邀测活动页（JS 需登录）：https://www.scnet.cn/ycjh/index.html
- OpenClaw 入口页（JS 需登录）：https://www.scnet.cn/ui/chatbot/openclaw
- OpenClaw 1000 万活动报道（中-高）：OSCHINA https://www.oschina.net/news/409844 、东方财富
- 3000 万历史活动存档（中）：https://cloud.tencent.com/developer/article/2656573
