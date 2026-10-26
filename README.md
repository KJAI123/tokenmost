# tokenmost.com

五层来源 AI token 折扣情报站：大模型官方（国内）/ Agent 平台 / 算力 / Token 中间商 / 大模型官方（海外）。

## 三层信息结构

| 层 | 内容 | 变化频率 | 载体 |
|---|---|---|---|
| 导航层 | 五类来源的直达入口（hao123 式） | 几乎不变 | sites.json |
| 时效层 | 折扣情报 + 折扣码（带验证时间戳） | 每天变 | deals.json |
| 个人层 | 账号库（本地 localStorage，不联网） | 用户自己 | 浏览器 |

关于「一键登录托管」的诚实边界：网页无法跨站自动填密码（浏览器安全模型）。MVP 用本地账号库 + 直达登录链接 + 指引配合浏览器密码管理器实现「准一键」；真·一键登录是二期浏览器扩展的活。折扣码卡片支持一键复制。

## 文件树

```
tokenmost/
├── index.html           # 全站（导航+卡片流+账号库抽屉+一键接入+比价计算器）
├── sites.json           # hao123 导航数据（五层）
├── deals.json           # 折扣情报+折扣码
├── prices.json          # 模型单价表（每百万 token，比价计算器数据源）
├── rss.xml              # 由 tools/check.py 自动重生成
├── robots.txt / sitemap.xml
├── tools/
│   ├── check.py         # 数据校验 + rss 重生成（改数据必跑）
│   ├── sync.py          # 零 token 自动流水线（GitHub Actions 定时跑）
│   └── sources.json     # 数据源注册表（33 源：API/监控页/RSS）
├── .github/workflows/sync.yml   # 每日 2 次定时同步 + 自动提交
├── .sync-state.json     # 源哈希基线/失败计数（自动维护）
├── review-queue.md      # 人工复核队列（自动重算的实时视图）
├── DEPLOY.md            # GitHub → Cloudflare Pages 部署指南
└── README.md
```

## 本地预览

    python3 -m http.server 8000

（file:// 协议无法 fetch JSON，必须走 HTTP）

## 部署

GitHub push → Cloudflare Pages（构建命令留空，输出目录 `/`）→ 绑定 tokenmost.com

## 自动运营架构（v0.4，2026-10-27 落地）

**目标：不烧 token 的全自动折扣站。** 机器核机器的，人只看机器看不懂的。

- **GitHub Actions 每日 2 跑**（北京 06:30 / 18:30，`.github/workflows/sync.yml`，公共仓免费）：抓源 → 更新数据 → 校验 → 自动提交 → Cloudflare Pages 自动部署。全程纯规则脚本（Python 标准库），**无任何 LLM 参与**。
- **三类数据源**（`tools/sources.json` 注册，加源只改这个文件）：
  1. `json` 结构化 API（OpenRouter / ModelScope 公开端点）→ 直接更新情报文案与比价行
  2. `watch` 官方页面哈希监控（30 个定价/活动页）→ 页面没变 = 自动续验证戳（卡片显示 🤖 自动核验）；变了 = 相关情报降级「待复核」并写明原因
  3. `rss` 社区源（linux.do）→ 关键词白/黑名单过滤 → 只生成 `published:false` 草稿（多号/合租/代充等黑名单词直接拒收）
- **稳定性机制**：哈希前归一化（剥离 script/nonce/CSRF/长随机串）；**两次观测确认制**——同一新哈希连续出现 2 次（可按源调 `confirm_runs`）才算真变更，计数器/轮换 banner 类抖动页永不误报。
- **规则引擎**：`deadline` 过期自动标「已失效」；`verified_at` 超 14 天未被任何源续期自动降级「待复核」（防僵尸数据）。
- **review-queue.md = 人工复核队列**：从当前数据状态实时推导（待复核条目 / RSS 草稿 / 连续失联 ≥3 次的源）。人工在 deals.json 里核实修复后，下一轮自动出队。
- **人工只剩 5 分钟/天**：扫一眼 review-queue.md → 处理待复核和草稿 → 拿到真实折扣码时替换占位码。其余（续期、失效、比价、RSS、部署）全部自动。

已知边界：需登录才能看的数额（火山方舟控制台、讯飞礼包）无法自动核，依赖 14 天老化提醒人工复核；linux.do 被 Cloudflare 拦（403）时该源优雅降级为「源失联」提醒；GitHub Actions 定时可能有几分钟到半小时延迟，属正常。

## 每日 5 分钟人工维护（全自动之上的补充）

1. 看 `review-queue.md`：待复核条目 → 核实官方页 → 更新 value 并改 `verify_status:"verified"`（顺手删 `stale_reason`）
2. RSS 草稿（`published:false` + 🤖 开头 notes）→ 核实官方来源后上架或删
3. 拿到真实折扣码 → 填 coupon 字段并删 placeholder 标记
4. 改完任何数据跑 `python3 tools/check.py`（本地）——CI 也会自动跑

## 数据契约

- sites.json：稳定入口层，很少改。可选 `api` 字段 `{base_url, model, env}`——配置了即可生成「⚡ 一键接入」代码（cURL/Python/Node/客户端配置），字段均可在面板中编辑，端点与模型名以官方文档为准
- deals.json：五层 category 对齐 sites 的 layer key；deal 的 provider 通过首词匹配关联 sites 条目（如「硅基流动」↔「硅基流动 SiliconFlow」）。可选 `deadline` 字段（ISO 日期）显示截止提醒，**到期由 sync.py 自动标失效**；`verified_at` 由数据源自动续期时附带 `verify_by:"auto"`（卡片显示 🤖）；降级时附带 `stale_reason`（维护者可见的原因，人工复核后删除）；`placeholder:true` 标记占位示例码——卡片禁用复制并显示「示例码」角标，不与真实码同权展示
- notes 字段以 `TODO` 或 `⚠️` 开头的内容视为维护者备注，不在卡片上展示
- coupon 字段存在时卡片自动出现「复制」按钮（placeholder 除外）
- 账号库纯 localStorage（key: `tm_vault_v1`），无后端
- 「已领」标记纯 localStorage（key: `tm_claimed_v1`），配合「⭐ 已领」筛选 chip
- prices.json：比价计算器数据源。字段 `{model, provider, layer, currency:"CNY"|"USD", input, output, free?, note?, verified_at}`，input/output 为每百万 token 单价；只收录官方定价页确认过的数字，USD 排序按 1:7.2 粗折算（面板有脚注声明）
- 302.AI 官方示例把 base_url 写成含 `/chat/completions` 的完整地址——照抄会拼错，SDK 里应以 `https://api.302.ai/v1` 结尾（本站已按正确格式预填）
- tools/check.py：数据校验 + rss.xml 自动重生成，改完数据必跑

## 一键接入（v0.2 核心特性）

羊毛卡片的「⚡ 接入」按钮：选平台 → 面板预填 base_url / 模型名 / KEY 环境变量名 → 一键生成 cURL、Python、Node.js 或客户端（Cherry Studio/ChatBox/Cline 等）配置，复制即跑通第一条 API。KEY 用环境变量传递，本站不收集任何密钥。

## ⚠️ 上线前两件事（交付纪律）

1. **替换占位折扣码**——`SILICON-MOST` 是演示复制按钮 UI 的假码（已加 `placeholder:true` 技术闸：复制禁用 + 「示例码 · 非真实优惠」角标，不会被当真实优惠发布），拿到真实码后仍必须替换并删除 placeholder 标记
2. **一键接入模型名控制台复核**——2026-10-27 全量重验中，base_url 均已按官方文档直核；以下模型名置信度中，上线前登录各控制台再过一遍：`kimi-k3`（平台刚迁移至 platform.kimi.com，新端点未直核）、`glm-4.7-flash`、`qwen-plus` / `doubao-1.5-pro-32k`（旗舰已到 Qwen3.8/新豆包代次）、`hy3-preview`、`MiniMax-M3.1-Flash`（大小写）、中转商默认 `gpt-4o` 系（302/OhMyGPT/API2D/DMXAPI/AIHubMix）、`mistral-large-latest`、NIM `meta/llama-3.3-70b-instruct`、`step-2-16k`。面板内可改，错了不致命但要复核

（2026-10-27 老板拍板：邮箱订阅相关功能——Brevo 表单、mailto 兜底/纠错——**全部砍除，不再回加**，站内联系方式仅保留 RSS。）

## 2026-10-27 全量情报重验（v0.3，5 路子代理并行核实）

41 条情报（36 发布 / 34 官方验证），重大更正与新增：
- **GitHub Models 已退役**（2026-07-30 全下线）→ 条目标失效 + 指向 Azure AI Foundry；导航移除
- **腾讯混元平台停服**（2026-09-30）→ 替换为 TokenHub 新人包（每模型 100 万 tokens/1 年）
- **DeepSeek 换代**：deepseek-chat/reasoner 停售，现售 flash（2/8 元）+ v4-pro（9/27 元）；错峰半价为长期政策；Search/Fetch 免计费 **11-01 截止**
- **Kimi 迁移 platform.kimi.com**：新用户 15 元代金券；K2 对新用户 **10-31 截止**
- 智谱改为邀请制赠送（双方各 2000 万）；Coze 免费档缩水（0 积分）；共绩云更名 suanli.cn；FastGPT 迁 fastgpt.io
- 新增：硅基「推荐官」16 元×2、Google AI Pro 学生年费免单（12-31 截止）、GitHub Student Pack / Azure $100、SambaNova / Together 免费层、OhMyGPT 推荐 $20×2、AIHubMix 67 免费模型、DMXAPI 7 折、SCNet 用户体验官 500 万×2、恒源云邀请 20+10、OpenRouter 17 个 :free（充值 ≥$10 日限 50→1000）
- 草稿区（待核）：ZCode 周末活动（官方公告未找到，**多号玩法已拒收**）、阿里云 100 元券、火山方舟每日 500 万

折扣码的真实来源：Linux.do 的福利帖、各中间商公众号活动、官方 Agent 平台的邀请裂变——这是初期人肉收集的主战场，收到一条填一条 coupon 字段。

账号库的安全声明不能删——它给了用户存敏感信息的信任前提（本地 + 不上传），删了这套说辞，出事就是站方的责任。

## 二期路线

- 浏览器扩展（Chrome Extension 注入各平台登录页 + Bitwarden 类密码填充）实现真·一键登录
- usage API 轮询做额度监控——账号库从「记事本」进化成「面板」
- ~~用量计算器/比价~~ ✅ 2026-10-27 已落地（v0.3）：工具条「🧮 比价」面板，prices.json 驱动
