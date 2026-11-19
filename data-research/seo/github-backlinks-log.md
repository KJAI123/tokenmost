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
