# GitHub 外链发射日志

> 配套主台账：`data-research/seo-backlinks.md`（全局作战台账）。本文件专注 GitHub PR/Issue 线的逐发记录与轮查存档。

## 11-20 第二轮挖掘（2026-11-20 执行）

### 一、在途轮查（8 个 open，0 merged / 0 closed）

| 仓 | 编号 | 形式 | 状态 | 新动态 |
|---|---|---|---|---|
| guihuashaoxiang/FreeLLM-API-KeyHub | #13 | PR | 🔄 open | 无（0 评论，11-13 提交后未动） |
| mahonzhan/awesome-coding-plan | #44 | PR | 🔄 open | 无（0 评论） |
| mehmetkahya0/AI-Catalog | #205 | PR | 🔄 open | 无（0 评论） |
| dalisoft/awesome-ai-coding | #171 | PR | 🔄 open | ⚠️ **github-actions[bot] Spam Guard 评论**（11-13 18:30）：标记账号 27 天/0 粉丝/9 公开仓，属「advisory，maintainer 自行判断」非拒绝——唯一收到机器人提示的发，观察 maintainer 态度 |
| mdruhulkuddus/awesome-free-ai-tools | #83 | PR | 🔄 open | 无（0 评论） |
| wynx1123/ai-welfare-hub | #12 | Issue | 🔄 open | 无（0 评论） |
| panxunying/ai-coding-welfare | #63 | Issue | 🔄 open | 无（0 评论） |
| jiuyuan233/wool-gathering | #1 | Issue | 🔄 open | 无（0 评论） |

- ai-megalist #81 已 merged（11-14 确认），本轮不再查。
- 总评：8/8 全部存活且零负反馈，建仓 5-7 天待审属正常周期；下轮轮查重点看 #171 的 bot 提示是否引来 maintainer 处理。

### 二、挖掘过程（英文族 5+1 关键词，GitHub Search API）

搜索词：`free LLM API list` / `free AI credits` / `LLM free tier` / `AI tools directory` / `awesome free AI` / `free AI resources list`。
筛选口径：⭐≥50 或近 7 天（≥2026-11-13）有 push；排除已提交/已跳过仓（FreeLLM-API-KeyHub、awesome-coding-plan、AI-Catalog、awesome-ai-coding、awesome-free-ai-tools、ai-coding-welfare、wool-gathering、ai-welfare-hub、ai-megalist、linktre-tools、liuda30201/AI-Coding、YD4223/aihub、QAInsights、agentdeals）。
命中候选 16 个，逐仓拉 README 判定合身度：

| 候选 | 星级 | 判定 |
|---|---|---|
| mnfst/awesome-free-llm-apis | 13659★ | ❌ 弃——纯 API 提供商清单（每条=endpoint+key 页），全文无资源/相关清单节，TokenMost 非 API 商，硬塞不合身 |
| open-free-llm-api/awesome-freellm-apis | 5795★ | ❌ 弃——README 含 AUTO_STATS/AUTO_UPDATE_BADGE 自动段+每日自 freellm.net 重刷，PR 会被自动化覆盖；且内容纯 API |
| 12britz/awesome-free-models | 2664★ | ✅ **入选**——「A curated list of free AI models, APIs, and **tools**」，含 🏆 Resources & Leaderboards 节且已收录同类导航 FreeLLM.net；CONTRIBUTING 明文 fork→PR 流程；人工维护（Last checked 日期制） |
| OuterSpacee/free-ai-apis | 465★ | ❌ 弃——15 类 API 分类表（API/Free Tier/Auth/Docs 列），收录对象必须是 API 本体 |
| mvalentsev/awesome-free-ai-coding | 248★ | ❌ 弃——update.yml/expire.yml/ci.yml 全套自动化+「probe-verified twice a week」，行=offer 非资源站 |
| abbosaliboev/free-ai-bible | 225★ | ❌ 弃（存疑暂记）——weekly-update.yml 自动仓风险+落点不明确；已三选满不再拉伸 |
| peter123023/awesome-free-llm-api | 228★ | ❌ 弃——明文「只收录能通过 API Key 和 endpoint 调用的永久/限时免费接口」 |
| amardeeplakshkar/awesome-free-llm-apis | 220★ | ❌ 弃——「permanently free LLM APIs」同上口径 |
| ShaikhWarsi/free-ai-tools | 1107★ | ✅ **入选**——大而全人工清单（83KB，contributions welcome），尾部 Related Resources 节收同类清单+外部网站（coding-with-ai.dev 先例）；无 workflows；明文禁的是「paid, expensive personal projects」不涉本站 |
| precis1onz/tokenation | 54★ | ❌ 弃——条目=offer 评分表（无资源节、无 Contributing） |
| CYBIRD-D/FREE-LLM-API-Provider | 123★ | ❌ 弃——free LLM provider 口径 |
| oniondas/Awesome-Hidden-AI-Credits-Free | 116★ | ❌ 弃——条目=平台 offer 且带个人推广码，非资源清单 |
| velo4705/awesome-free-byok-models | 86★ | ❌ 弃——BYOK 模型清单 |
| pacocartones/free-llm-api-hub | 125★ | ❌ 弃——「dataset of free-tier & trial-credit LLM APIs」数据集口径 |
| codertesla/ai-coding-deals | 143★ | ❌ **明文排除弃**——CONTRIBUTING「Out of Scope」白纸黑字：*Content sites, price-comparison aggregators, and directories that are not themselves a coding tool or inference endpoint*（内容站、比价聚合站与非工具型目录）——TokenMost 正是此类，严守不硬塞 |
| AIPMAndy/FreeToken | 173★ | ✅ **入选**——定位双胞胎：中文免费额度导航+逐条核验日期+过期降级不宣传，与本站「核实日期/自动下架」完全同构；收录位=CATALOG.md「开源免费 LLM API 资源列表与工具」表（收免费资源汇总类项目，cheahjs 先例） |

**结论：候选 16 → 提交 3，宁缺毋滥率 81%。**

### 三、本轮新提交（3 发，全部 PR）

| 仓 | 星级 | 形式 | 链接 | 状态 | 落点与措辞定制 |
|---|---|---|---|---|---|
| 12britz/awesome-free-models | 2664★ | PR | https://github.com/12britz/awesome-free-models/pull/98 | 🔄 open | 🏆 Resources & Leaderboards 节，锚文本=FreeLLM.net 行（assert 通过后紧随插入）；条目用节内 `—` 长破折风：「Chinese-language intelligence site tracking 260+ free-credit and discount offers…delisted automatically」；body 说明与 FreeLLM.net 同位互补+2026-11-20 核验+维护者披露 |
| ShaikhWarsi/free-ai-tools | 1107★ | PR | https://github.com/ShaikhWarsi/free-ai-tools/pull/136 | 🔄 open | Related Resources 节末行，锚文本=awesome-ai-startups 行；条目用节内 `-` 短横风：「AI token free-quota and discount intelligence site: tracks 260+ verified free-credit offers…pulled automatically once it expires」；body 预答「非 paid personal project」排除条款+2026-11-20 核验 |
| AIPMAndy/FreeToken | 173★ | PR | https://github.com/AIPMAndy/FreeToken/pull/8 | 🔄 open | CATALOG.md 开源资源表末行，锚文本=CliRelay 行；核对提示沿用表内谨慎语气（「限时活动仍建议回官方页面复核」，规避其「不写永久免费」红线）；body 按 CONTRIBUTING 给官方入口+核验日期 2026-11-20+修改范围声明（不涉主表/providers.json）+利益披露 |

**三发措辞全部独立改写**：锚文本逐仓不同（FreeLLM.net 行 / awesome-ai-startups 行 / CliRelay 行），条目句式三版（em-dash 长句 / colon 短句 / 中文表格核对提示），body 论证角度各异（同位互补 / 排除条款预答 / 定位同构+红线合规），无群发同句。

### 四、工程坑沉淀（本轮）

- **`security find-internet-password` 会间歇性挂死**（keychain 交互弹窗），连累整条命令 120s 超时且后台化——两发均中招。对策：token 一次取出后本轮复用字面值；git push 加 `GIT_TERMINAL_PROMPT=0`。后台任务被杀时 commit 可能未落盘（`git status` 验证再重推，勿假设成功）。
- macOS 无 `timeout` 命令（zsh: command not found），用 `--max-time`（curl）与 Bash 工具自带 timeout 替代。
- fork 三仓：KJAI123/awesome-free-models、KJAI123/free-ai-tools、KJAI123/FreeToken（本地 shallow clone 在 /tmp/tm_work/，branch：add-tokenmost-resources / add-tokenmost-related-resources / add-tokenmost-catalog）。

### 五、下轮待办

- 轮查口径扩为 11 发（在途 8 + 本轮 3），重点：#171 Spam Guard 后续、FreeToken #8（维护者活跃，CONTRIBUTING 严谨，可能要求补材料）、awesome-free-models #98（该仓 11-14 刚做过全链接复检，maintainer 在线概率高）。
- 本轮弃选中的 abbosaliboev/free-ai-bible（225★）如后续需要第四发可重评（需先确认 weekly-update.yml 不重写 README 正文）。

## 11-21 第三轮挖掘（2026-11-21 口径执行）

> 注：机器系统时钟显示 11-19，本节日期沿用任务指定口径 2026-11-21（前两轮同惯例）；#171 回复的 GitHub 时间戳实际显示为 11-19，下轮核对时勿误判。

### 一、在途轮查（10 open，累计 1 merged / 0 closed）

| 仓 | 编号 | 形式 | 状态 | 新动态 |
|---|---|---|---|---|
| guihuashaoxiang/FreeLLM-API-KeyHub | #13 | PR | 🔄 open | 无（0 评论） |
| mahonzhan/awesome-coding-plan | #44 | PR | 🔄 open | 无（0 评论） |
| mehmetkahya0/AI-Catalog | #205 | PR | 🔄 open | 无（0 评论） |
| dalisoft/awesome-ai-coding | #171 | PR | 🔄 open | ⚠️ ** Spam Guard advisory 无变化**（仍只有 11-13 那条 bot 提示）；但 **漏网动态**：maintainer dalisoft 11-14 已留 CHANGES_REQUESTED review——「I don't see English version of website, can you give link to English version?」（第二轮台账只记了 bot 提示、漏了这条 review）。**本轮已回复**：给出英文版 https://tokenmost.com/en.html （en.html 确认 HTTP 200、语言切换器互链、偏好记忆），并主动提出如需可把列表内链接改为英文版 URL。回复：issuecomment-7011143870。该仓 11-16 仍有 push，维护者在线 |
| mdruhulkuddus/awesome-free-ai-tools | #83 | PR | 🔄 open | 无（0 评论） |
| wynx1123/ai-welfare-hub | #12 | Issue | 🔄 open | 无（0 评论） |
| panxunying/ai-coding-welfare | #63 | Issue | 🔄 open | 无（0 评论） |
| jiuyuan233/wool-gathering | #1 | Issue | 🔄 open | 无（0 评论） |
| 12britz/awesome-free-models | #98 | PR | 🔄 open | 无（0 评论，updated=提交时刻） |
| ShaikhWarsi/free-ai-tools | #136 | PR | 🔄 open | 无（0 评论，updated=提交时刻） |
| AIPMAndy/FreeToken | #8 | PR | 🔄 open | 无（0 评论，updated=提交时刻） |

- **新资产沉淀**：tokenmost.com 英文版路径 `https://tokenmost.com/en.html`（title: TokenMost — Free AI Tokens & LLM API Credits, Daily-Verified）——后续投英文仓可考虑直接用英文版 URL 或在 body 里附上。
- **教训**：轮查不能只看 `comments` 数——CHANGES_REQUESTED review 不计入 issue comments，#171 的 maintainer 提问晾了 5 天。下轮轮查必须同时拉 `/pulls/N/reviews`。

### 二、挖掘过程（六个新搜索族 + 6 变体词，与前两轮零重叠）

搜索词：`awesome AI tools list` / `free developer resources` / `AI API directory` / `LLM pricing` / `student developer pack` / `free tier cloud`；变体补搜：`AI tools directory` / `free developer stuff` / `developer freebies` / `llm price comparison` / `free cloud credits` / `free AI deals`。
筛选口径：⭐≥30 或近 7 天（≥2026-11-12）push；排除前两轮已提交/已弃仓。命中候选 17 个，逐仓判定：

| 候选 | 星级 | 判定 |
|---|---|---|
| best-of-ai/ai-directories | 902★ | ✅ **入选**——「List of AI Directories」目录的目录，CONTRIBUTING 一句话规则「know an AI Directory not listed here, send a PR, put it in right place alphabetically」，无自动化 workflow；T 节有 12 条同类先例 |
| mahseema/awesome-ai-tools | 6604★ | ✅ **入选**——6.6k★ 人工维护大清单，README 明文邀请 PR（无 CONTRIBUTING、无 workflow）；Other 节收信息型/查询型站点（Have I Been Trained、PromptBase 先例）；缺点：上次 push 2025-12-31，偏停滞 |
| hilmanski/freeStuffDev | 1976★ | ✅ **入选**——freeStuffDev.com 数据仓（Astro+frontMatter，965 条）；Rules 排除框架特定/库/文档链接但**不排除目录型站点**，已有 aihunt.dev、ai-collective-tools 两个 AI 聚合站先例（tag: ai-resources）；TokenMost 100% 免费过其「free or ≥1yr trial」门槛 |
| couponswift/awesome-student-software-deals | 66★ | ❌ **明文排除弃**——CONTRIBUTING「❌ No 'coupon code' sites」+「Direct Links Only（官方 vendor 页）」+学生专属要求，TokenMost 折扣情报站类型正中排除条款（与 codertesla 同类教训，严守不硬塞） |
| t3-sh/cloudcredits.io | 89★ | ❌ 弃——条目=厂商信用计划 YAML（src/content/providers + programs 双文件+logo SVG），「listings that function solely as lead generation」不允许；TokenMost 是情报站非信用计划，类型不合 |
| CelaDaniel/free-ai-resources-x | 1007★ | ❌ 弃——纯学习资源口径（Quality Criteria 要求 teach something specific + 难度标签），TokenMost 非教学内容 |
| rupali-codes/LinksHub | 1015★ | ❌ 弃——Next.js 站点 JSON schema 数据流、16 个 CI workflow（含 spam guard/link check）、学习资源口径，重流程+口径不合 |
| dalisoft/awesome-hosting | 971★ | ❌ 弃——hosting 最低套餐口径不含 AI token；且与 #171 待审同一维护者，避免「被 review 未回先投另一仓」的观感 |
| jhaxce/student-perks | 56★ | ❌ 弃——学生身份门控口径（student ID/university email），TokenMost 非学生专属 |
| wauputr4/bansos | 73★ | ❌ 弃——印尼语 promo 目录（AI credits 在范围内，合身度高），但贡献走 GitHub 登录表单+管理员审核（D1 数据库运行时），且条目=单个 offer 非聚合站 |
| kawsarlog/Ultimate-API-List | 120★ | ❌ 弃——「auto-updated」75k 通用 API，自动化风险+非 AI 免费额度口径 |
| flanker/llmprice.cn | 31★ | ❌ 弃——LiteLLM 数据静态比价页（工具页非清单），无资源节无落点 |
| codeSTACKr/free-developer-resources | 924★ | ❌ 弃——全栈 web 开发资源分类，无 AI 节，2024-07 起停滞 |
| pydantic/genai-prices | 418★ | ❌ 弃——价格计算库/数据集，非目录清单 |
| hanzohanzhe/Grandet | 1411★ | ❌ 弃——找最便宜 API 的 agent skill，非清单 |
| github-education-resources/Student-Developer-Pack-Current-Partners-FAQ | 265★ | ❌ 弃——GitHub 官方 Student Pack 现有合作伙伴 FAQ，非合作伙伴不可入 |
| apimart* 系列（4 仓） | 81-93★ | ❌ 弃——同一网关产品的推广模板仓群（同文案多账号），spam 特征明显，反向不可碰 |

**结论：候选 17 → 提交 3，宁缺毋滥率 82%。**

### 三、本轮新提交（3 发，全部 PR）

| 仓 | 星级 | 形式 | 链接 | 状态 | 落点与措辞定制 |
|---|---|---|---|---|---|
| best-of-ai/ai-directories | 902★ | PR | https://github.com/best-of-ai/ai-directories/pull/527 | 🔄 open | T 节，按 CONTRIBUTING 字母序放 ToolFinder 前（初插 There's An AI 之后发现 t-o 排在 t-h 前不合字母序，二推修正——assert 两条先做再 replace）；条目沿节内短句风：「AI token free-credit & discount intelligence site, 260+ offers verified daily」；body：目录型资源定位+2026-11-21 核验+团队身份披露 |
| mahseema/awesome-ai-tools | 6604★ | PR | https://github.com/mahseema/awesome-ai-tools/pull/2827 | 🔄 open | Other 节末行（锚文本=Melies 行，assert 后插入）；条目用节内一句长描述风：「Tracks 260+ free-credit and discount offers…delisted automatically」；body 论证 Other 节适配性（对照 Have I Been Trained?/PromptBase 信息型先例）+2026-11-21 核验+披露 |
| hilmanski/freeStuffDev | 1976★ | PR | https://github.com/hilmanski/freeStuffDev/pull/2333 | 🔄 open | 新增 `src/content/tools/tokenmost.md`（非 README，走其数据文件规范）；frontMatter tags=["ai-resources"]（沿用 ai-collective-tools 先例）、thumbnail=官方 og-image.png；正文 4 行 free features；body 逐条对照其 Rules（100% 免费非试用/非框架特定/非文档链接）+2026-11-21 核验+披露 |

**三发措辞全部独立**：锚点/载体三样（字母序插入 / Other 节末 append / 新数据文件），条目句式三版（site, 260+ offers verified daily / Tracks 260+…分号长句 / snippet+features 列表），body 论证角度各异（目录的目录定位 / 节内同类先例对照 / Rules 逐条合规预答），无群发同句。三发 diff 均已抓 .diff 核验为干净的单行/单文件增量。

### 四、工程坑沉淀（本轮）

- **zsh 小写 `path` 是 `$PATH` 的绑定数组**：循环变量名用 `path` 会覆盖 PATH，循环体内 curl/python3 全部 command not found（本轮连踩两次才定位）。循环变量避开 path/PATH/status 等保留名。
- zsh 不对 `$var` 做词分割，`set -- $pr` 拆不出两个参数——多参数用普通 for 循环传独立词，或 `read -r` 从字符串读。
- fork 三仓：KJAI123/ai-directories、KJAI123/awesome-ai-tools、KJAI123/freeStuffDev（shallow clone 在 /tmp/tm_work3/，branch：add-tokenmost-directory / add-tokenmost-other-tools / add-tokenmost）。push 均用 `https://x-access-token:$TOKEN@github.com/...` + GIT_TERMINAL_PROMPT=0，本轮无 keychain 挂死（token 取一次落盘 /tmp/tm_token_3rd 复用）。

### 五、下轮待办

- 轮查口径扩为 14 发（在途 11 + 本轮 3）；**轮查动作必须含 `/pulls/N/reviews`**（防 #171 式漏网）。
- 重点：#171（dalisoft 对英文版答复的下一步——接受/改链/close）、FreeToken #8（维护者严谨，可能要求补材料）、freeStuffDev #2333（模板合规性，可能被要求换 thumbnail 尺寸）、awesome-ai-tools #2827（仓已 11 个月未动，预期周期长）。
- 英文版资产：投英文仓时可附 `https://tokenmost.com/en.html`（#171 答复已公开此链接）。
