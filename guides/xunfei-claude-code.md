# 讯飞 10 亿 Tokens 接进编程工具：Claude Code / Cursor 实操配置

> 核实于 2026-10-27 ｜ 前置：已完成领取（见《xunfei-10yi.md》），额度挂 Spark-X2.6，31 天倒计时已开始

## 先明确三件事（避免白配置）

1. **这批额度是「星辰 MaaS 常规推理额度」**，不是 Coding Plan 订阅——Base URL 用 **`maas-api`** 域名（不是订阅专用的 `maas-coding-api`），两者不通用，用错地址不扣活动额度。
2. **模型是 Spark-X2.6**（讯飞自研旗舰，2026-10-22 发布），额度绑定该模型，调 GLM/Kimi 等第三方模型不在活动额度内。
3. **协议支持**：OpenAI 兼容协议为实测主通道（verified）；Anthropic 协议端点在讯飞文档中存在（Token Plan/Coding Plan 双协议支持），活动额度能否直连 Anthropic 端点**待核实**——建议先用 OpenAI 兼容方式打通。

## 方案一：Claude Code 通过 OpenAI 兼容代理接入

Claude Code 原生走 Anthropic 协议，要用讯飞的 OpenAI 端点需要一层转换（如 claude-code-router / LiteLLM 等本地代理）：

1. `npm install -g @musistudio/claude-code-router`（或任意 OpenAI→Anthropic 转换代理）。
2. 代理配置里填讯飞信息：
   - **API Base URL**：`https://maas-api.cn-huabei-1.xf-yun.com/v2/chat/completions`（实测口径，若报错尝试去掉 `/chat/completions` 用 `/v2`）
   - **API Key**：`ak-xxxxxxxx`（你领取时创建的那个 Key，控制台「API 密钥管理」可查）
   - **模型名**：`Spark-X2.6`（以控制台模型广场显示的精确 ID 为准）
3. 环境变量指向代理后启动 Claude Code；跑一条小指令验证扣的是活动额度（控制台用量页看余额变动）。

⚠️ 若不想折腾代理：讯飞控制台的模型卡片自带「Claude Code 配置模板」（官方文档口径），用模板直连 Anthropic 端点优先，失败再回落方案一。

## 方案二：Cursor（原生 OpenAI 兼容，最省事）

1. Cursor 设置 → Models → OpenAI API Key 区，勾选「Override Base URL」。
2. 填入：
   - Base URL：`https://maas-api.cn-huabei-1.xf-yun.com/v2`（⚠️ Cursor 要求以 `/v1` 结尾时用 `/v2` 平替试试，两种都留一手）
   - Key：`ak-xxxx`
3. 模型列表手动添加 `Spark-X2.6`，Chat/Composer 里选中它即可。
4. 验证：发一条消息 → 控制台「Token 用量」页看消耗是否走活动额度。

## 方案三：workbuddy（实测最顺的路径）

1. 打开 workbuddy → 对话框让 AI「添加自定义模型」。
2. 粘贴 Base URL（同上）+ `ak-` 密钥。
3. 配置成功后模型出现在「对话框下方模型选择的最底部」，选中即用。实测文原话路径，verified。

（Cherry Studio 等其他 OpenAI 兼容客户端同理：Base URL + ak Key + 模型名三件套。具体到 Cherry Studio 的截图级配置**待核实**。）

## ⚠️ 消耗速度管理（重点，这额度烧得飞快）

- 实测口径：**「不到一天就能用完」**（2026-10-26 实测文原话）。X2.6 是长上下文模型，Agent 场景一次任务几十万 token 很正常。
- **倒计时管理**：额度 31 天有效（自领取日起，非自然月）。倒推安排：第 1 周跑验证性小任务，第 2-3 周集中跑大任务，别拖到最后几天（平台限流风险）。
- **任务分层**：日常补全/小问答用免费模型（讯飞侧 Spark-X2-Flash 便宜档或智谱 4.7-Flash 限免），**把 X2.6 额度留给长上下文大重构**——每次任务前清上下文、控 system prompt 体积。
- **盯用量**：控制台「用量统计」页（分钟级）；发现额度异常掉速先查是不是被缓存未命中打爆。
- ⚠️ 再次确认领取时**取消勾选**了「自动转按量计费」——额度用完后如果勾着，X2.6 会继续真实扣费。

## 红线

- 每人限领 1 次；多号=风控对象。
- 免费额度同样禁自动化脚本刷量（平台通用条款），跑批任务用官方批处理能力而非无限循环脚本。

---
**核实于 2026-10-27**。来源列表：
- 实测配置文（Base URL/ak 密钥/workbuddy 路径/消耗速度）：https://www.163.com/dy/article/LA6K9DKK05527PMU.html（2026-10-26）
- 领取教程（多工具支持口径）：https://zhuanlan.zhihu.com/p/2097344549374914581
- 讯飞官方 Token Plan 文档（31 天规则/双协议佐证）：https://www.xfyun.cn/doc/spark/TokenPlan.html
- 官方 Coding Plan 文档（配置模板佐证）：https://www.xfyun.cn/doc/spark/CodingPlan.html
- 待核实项：Anthropic 端点对活动额度的支持、Cherry Studio 截图配置、X2.6 精确 model ID（以控制台为准）。
