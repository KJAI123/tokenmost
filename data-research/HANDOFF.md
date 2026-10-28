# HANDOFF — 给并行会话的补充包

> 生成：2026-10-27，爬虫助理首轮调研收尾时。另一会话若在读这份文件：这是你要的「补充」，全部为增量，未触碰你维护的 deals.json 与 tools/ 下你的脚本。

## 1. 我是谁、干了什么

我是本项目的**数据调研爬虫助理**（第 4 角色，见 `../token-deals/team/roles.md`）。本轮完成：

1. **六平台真实数据调研**（WebSearch 多源交叉，全部带来源与核实时间），落盘在 `data-research/findings/`（7 个文件）
2. **零 token 采集器** `tools/harvest.py` + 源清单 `tools/harvest_sources.json`——纯标准库、Python 3.9 兼容、守 robots.txt、2 秒限速，**2026-10-27 首跑成功：12 源全通、11 源命中、零 LLM 参与**，快照在 `data-research/harvest/harvest-2026-10-27.md`
3. **与你的 deals.json 数据做了交叉核对**（结论见 §3）

## 2. 交叉核对结果：你的数据 vs 我的独立调研

| 条目 | 你的 deals.json | 我的独立调研 | 结论 |
|---|---|---|---|
| zhipu-signup | 邀请双方各 2000 万 + 新客 2500 万，月上限 2 亿 | harvest 抓官方活动页：完全一致 | ✅ 互证通过 |
| groq-free | gpt-oss-120b 30RPM/1000RPD/8K TPM | 一致 | ✅ 互证通过 |
| openrouter | 50→1000 次/天（$10 永久解锁）、20 RPM | 一致 | ✅ 互证通过 |
| siliconflow | 14 元额度 + 免费池不含 Qwen/DeepSeek/GLM 主力 | 我此前的「16 个 L0 模型」来自 8 月知乎帖，**你的更准确** | ⛳ 采你的 |
| github-models | 已于 2026-07-30 退役 | （我未单独调研） | ⛳ 你的更新 |

## 3. 三条增量发现（供你合入 deals.json，素材都在 findings 文件里）

1. **`ark-daily-5m` 的 TODO 可以销了**：无需登录——火山引擎官方公告（2026 Q3）已确认「每日 500 万免费 Tokens 为长期常态化政策，至少至 2027 年底」。素材与建议合并动作见 `findings/volcengine-ark.md` 的「合并素材」节。
2. **google-ai-studio 缺时间维度**：2025-12 免费档 250→约 20 RPD 缩水事件（官方论坛可查），建议 notes 补「免费档持续收紧」预期管理。见 `findings/google-ai-studio.md`。
3. **groq-free 趋势标注**：RPD 14400→约 1000（2026-09），持续收缩通道，建议高频重验。见 `findings/groq.md`。

## 4. 工具说明（避免撞车）

- `tools/harvest.py`（我的）：抓官方页 → 关键词上下文快照，**零 token**。运行 `python3 tools/harvest.py`（全量）/ `--only volc`（单源）/ `--selftest`（离线自检）。输出 `data-research/harvest/`。
- 你的 `tools/sources.json` 与我的 `tools/harvest_sources.json` 目前并存、URL 有重叠。两套合并与否由你定；不合并也不冲突（输出目录不同）。
- 我看到你已有 `check.py`/`sync.py`——QA 曾登记 BUG-114 要发布校验脚本，如果 check.py 就是它，QA 台账可以销这条。

## 5. 当前项目状态快照（截至 2026-10-27 凌晨）

- 代码：v0.2.1（QA 三个 S1/S2 阻断全部闭环 + 注入回归通过），**代码侧具备上线条件**
- 主数据：deals.json 60 条（57 published / 55 verified），多由你以 verify_by:auto 维护
- 待老板拍板：Q?13 详情页形态；上线运营三件事（真码、重验、Brevo）
- 合规提醒：你处理 zcode-linuxdo（拒收多号玩法）的方式正确，是全项目的红线先例

## 6. 我的下一步（不会与你有写入冲突）

覆盖 findings 缺口平台做交叉验证 → harvest 增补源 → v3 diff 告警脚本。产出照旧只落在 `data-research/` 与 `tools/harvest*`。

---

## 2026-10-27 智能体首轮（crawler-assistant 正式注册后）

> 本轮四件事：harvest 采集、v3 diff 告警脚本验证、七平台交叉验证、源清单增补。deals.json 与你的 tools/{sync,check}.py、sources.json 未触碰。

### 1. harvest 结果（12 源，全通）

- 11/12 命中；`bailian-pricing` 0 命中（JS 渲染页，快照已标注需人工核查 pattern）
- 快照：`data-research/harvest/harvest-2026-10-27.md` + `latest.json`

### 2. v3 `tools/harvest_diff.py` 状态：可用

- `--selftest` 通过：数量/内容/状态/增删源五类变化识别 + 告警落盘 + 基线滚动自愈，Python 3.9.6 实机验证
- 实跑检出 1 源变化：`openrouter-free-models` 命中内容变化，告警在 `alert-2026-10-27.md`
- **调参积压**：该变化实为动态页上下文漂移（match 集合与 HEAD 完全一致，纯 context 窗口文本变了）——fingerprint 目前含 context 会误报此类噪声；改进方向：指纹只取 match 集合，或对 context 做归一化。不阻塞 v3 上线
- **源清单已扩容（我的命名空间）**：`moonshot-pricing` URL 迁至 platform.kimi.com（旧域名今日仅 1 命中）；新增 minimax / sambanova / together / cerebras / mistral / cohere 共 6 源，全部预验证可达（1–30 命中）。**下轮 harvest 起 19 源，diff 会首次报 6 个「新增源」，属预期，无需惊慌**

### 3. 七平台交叉验证（findings 已落盘，均带来源+核实时间 2026-10-27）

| 平台 | deals.json 条目 | 互证结论 | 要点 |
|---|---|---|---|
| Kimi | kimi-voucher（15 元券） | ✅ 与主数据一致 | 官方文档直核；补：**K3.1 Pro 亦不支持代金券** |
| MiniMax | minimax-m3-half（M3 五折 2.1/8.4） | ◑ 基本一致 | 五折（2026-06-15 起）与输入 ¥2.10 多源印证；**输出 8.4 与 M3.1-Flash 1/4 元未直核，待控制台确认** |
| SambaNova | sambanova-free | ✅ 与主数据一致 | 官方限流文档逐项命中（20 RPM/20 RPD/20 万 TPD/Developer 2000 万） |
| Together | together-free | ✅ 与主数据一致 | Bonsai-27B 全免费、Tev1-4B 输出免费均印证；免费款属推广位，变动快 |
| Cerebras | cerebras-credits（$5） | ⚠️ **有出入** | $5/30 天/无持续免费层一致，但官方定价页明示**需先绑有效支付方式才发 $5**——主数据「注册送」（difficulty 1, via register）漏了绑卡门槛 |
| Mistral | mistral-free | ✅ 与主数据一致 | 免费档存在；主数据不写数额属稳妥；第三方参考约 10 亿 tokens/月、1 req/s（勿入主数据） |
| Cohere | cohere-trial（1000 次/月） | ✅ 与主数据一致 | 官方 docs 直核；补：**Trial key 禁止生产/商用** |

### 4. 给主会话的合并要点（素材均在 findings/*.md，由你裁决合入）

1. **cerebras-credits（唯一实质性出入）**：建议 value/rule 补「需绑卡后发放，不会自动扣费」，difficulty 1→2，via 改 register+card；notes 可补 Free Trial 限速（约 5 RPM / 30K TPM / 100 万 tokens/日）。见 `findings/cerebras.md`
2. kimi-voucher：rule 补「K3 与 K3.1 Pro 均不支持代金券」。见 `findings/kimi.md`
3. cohere-trial：rule 补「Trial key 不可用于生产/商用」。见 `findings/cohere.md`
4. minimax-m3-half：维持现状，输出价待控制台确认；已入 harvest 盯防，页面变化会出告警。见 `findings/minimax.md`
5. sambanova / together / mistral：无需改动

### 5. 我的下一步

harvest 源清单 JS 渲染页（bailian、kimi 新域名）pattern 调优 → fingerprint 归一化降噪 → 其余缺口平台（AIHubMix 等）入源。

---

## 2026-10-27 ZCode 活动专项跟进

> 应老板专项指令，对 ZCode 自家周期性活动做渠道与时间线深挖。deals.json 只读未动。完整素材：`findings/zcode-activities.md`。以下处置建议**由你拍板**。

### 给主会话的处置建议（zcode-linuxdo 条目）

**建议：维持 stale，不升级 verified。** 理由三条：

1. **当前无可核实的在场活动**——1024 轮已于 10-26 09:00 失效，周末计划暂无新一轮。verified 语义应是「现在去领能领到」，此刻该条目不满足；强行升级会破坏你 verified/stale 的语义纪律。
2. **事件本身已由更好的条目承载**——你已建 deep-zhipu-weekend-3yi / deep-zhipu-1024-5yi（均 verified，带官方活动页与多源）。zcode-linuxdo 作为独立条目事实上已被拆解覆盖，可考虑：a) 归档或与 deep-zhipu-weekend-3yi 合并；b) 保留为「周期性活动节奏」占位（下一节点预测 1111）。二选一由你定，我不动。
3. **linux.do 无法升级为可引来源**——本日实测：topic 3005638、latest.rss、robots.txt 全部 403（全域 Cloudflare，未绕过）。该帖定性维持「社区佐证、多号玩法拒收」不变。

**监控方案（stale 期间的眼睛）**：
- 已入 harvest 我的命名空间：`zcode-changelog`（zcode.z.ai/changelog，官方 changelog 偶发活动上线公告，实测 4 命中）+ `zhipu-hangzhou-rules`（官方文档活动规则页先例，实测 30 命中；12-09 后撤源）。下轮 diff 会报 2 个新增源，属预期。
- 人工渠道：ZCode 客户端左下角活动卡片（领取入口本体）+ 智谱公众号推送。docs.bigmodel.cn/cn/update/promotion **实测不含客户端活动**，别指望它。
- 1111 节点（约两周）届时优先复查；出现新 bigmodel.cn/activity/* 页面后 real 浏览器实锤，即可按 deep-zhipu-* 格式建新 verified 条目。

### 本轮增量素材（均过期或在场性待核，合入与否你定）

1. **9-28 代码上传争议补偿**（新时间线数据点）：全体用户 1 亿 token × 10 天连发 + 付费用户重置卡。双源媒体（凤凰/搜狐）。已过期，建议作「意外发粮窗口」参考入档。
2. **客户端 v3.15.1「邀请好友·免费蹬蹬」活动**（官方 changelog 直核「上线」）：**可能仍在场**，deals.json 尚无客户端邀请条目——需人工开客户端核实规则/数额，核实后可对标 API 侧邀请（双方各 2000 万）建条目。
3. **杭州 Coding Plan 减免**（官方规则页直核，9-10~12-09）：个人 44%/51% 综合减免，需社保/学籍材料走飞书表单审核——资质型优惠，如收录建议 difficulty 3。

## 巡检 2026-10-27 03:4x（爬虫助理自动巡检 #1）

- 采集：19 源全通（含 ZCode changelog/杭州规则页两个新源，均命中）；diff 报 9 项=8 新增源首基线+1 已知动态页漂移，**无实质内容变化**
- 已修积压：harvest_diff.py fingerprint 改为只取 match 集合（动态页措辞漂移不再误报，selftest 五类变化识别通过，重跑全源 no change）
- 佐证：zcode.z.ai/changelog 今日仍列 v3.15.1「邀请好友·免费蹬蹬」——与 findings/zcode-activities.md 的「可能仍在场」互证，建议主会话按 1111 节点方案处理，无需提前建条
- 2026-10-27 05:5x 巡检：无变化（20 源全通）

## 巡检 2026-10-27 07:5x（爬虫助理自动巡检 #3）

- **真变化 1 项：openrouter-free-models 目录轮换**（-1 个 $0.06/M 档免费条目，+nace-ai 模型与 NVIDIA Nemotron 3.5 Embed 1B 免费嵌入版），来源即官方页直抓，详见 findings/openrouter.md 巡检发现节
- 判断：主会话 sync.py 的 OpenRouter 结构化 API 直更应已自动覆盖，**无需手动合入**；建议站内不写死免费模型数量（目录动态）
- 其余 19 源无变化

## 巡检 2026-10-27 10:5x（爬虫助理 #4：协作清单对齐轮）

- **查收「信息源清单-协作版.xlsx」**：总表 28 源归属清晰（sync.py 自动 / harvest 盯防 / 人工），待补源协作区留老板填，5 条新挖羊毛线索归主管 lane（ClinePass/opencode/U2 Flash/看广告/Qoder）——助理不动，等核实结论
- **按清单完成源对齐**：①新增指派的 3 源——kimi-membership（30 命中）、azure-students（30 命中）、gemini-pricing（本轮超时，下轮重试）②火山源从 free-inference-quota（已 302+正文 JS 化）切到清单确认的 collaboration-reward-program（6 命中，活页）③openrouter-free-models 静态页源移除（页面转 CSR，:free 目录以 sync.py 的 API 直更为准，避让重复劳动）
- 本轮 diff 10 项全部为上述源结构调整，**非情报变化**；另 5 源（gemini/groq/sambanova/mistral 系）瞬时超时，下轮自愈
- 备忘：zhipu-hangzhou-rules 按清单备注 12-09 活动结束后撤源

## 老板指派信源落地（2026-10-27，doubao.com/pc/agent-explore）

- **实为在场活动**：豆包电脑版「天天领额度」（激励三期）——每日签到+任务领活动赠送额度（30 天/笔，免费/付费用户皆可领，消耗优先于付费额度），双端进度打通，官方明禁多号（与红线一致，只收单账号）
- **规则原文直核**：活动规则 CDN 页静态可抓——已入采集器 doubao-quota-rules 源（规则改版/期数更替即告警）；/pc/agent-explore 网页为 CSR 壳留观察位
- **给主会话**：候选条目「豆包电脑版·天天领额度」（type: free_tier，数额以客户端活动页为准，difficulty 1）——具体数额需客户端实锤（老板机器装有豆包）；完整调研见 findings/doubao-agents.md

## 找源节奏升级（2026-10-28，老板指令「15分钟一轮、找到没算力为止」）

- **全量信源 Excel**：data-research/信息源总表-全量版.xlsx（4 sheet：总表 51 源=主会话 27+助理补充+8 社区聚合源+3 平台线索；采集器 24 源；公众号 6 行；发现日志 7 条）——此后每轮找源巡检负责增量维护
- **自动化已升频**：2 小时 → **每 15 分钟**（automation-66c52f99），新流程=harvest+diff → 消费 discovery-queue.md 队列（1-2 条/轮，串行 WebSearch）→ 新源入表/入采集器 → 一行日志
- **公众号结论**：外部搜索引擎不收录公众号内容——公众号发现只能靠聚合帖间接引流+微信内人工搜索，已写入公众号 sheet 备注；第一轮搜到 8 个社区聚合源（知乎 27 家清单/FreeLLM-API-KeyHub/博客园/腾讯云/CSDN/liurb 等）+3 条平台线索（小米 MiMo、讯飞星辰 Qwen 不限量、智谱实名 2 亿——均标 ⏳ 主管核实）
- **发现队列**：discovery-queue.md 12 条初始线索待自动消费

## 外网薅羊毛开线 + 自愈闭环（2026-10-28，老板四连令）

- **外网第一轮**：5 个海外源入表——母矿 mnfst/awesome-free-llm-apis（仅永久免费层）、r/LocalLLaMA 550+ 清单、Reddit 三大追踪帖、OpenRouter 官方 13 家横评、StationX 指南；下轮评估 OpenRouter 博客入采集器
- **自愈三件套**（老板令「抽自己一巴掌，不要断了要我手动拉起」）：①heartbeat.txt——15 分钟巡检每轮写心跳 ②**龙虾 watchdog**（openclaw cron c71c134c，每 30 分钟）心跳 >35 分钟未跳→Mac 系统弹窗+watchdog.log（Feishu 通道缺 chatId 暂 fail-closed，本机通知兜底；老板如需远程推送可补 chatId）③Obsidian 自动同步 export_obsidian_md.py
- **Obsidian 落地**：~/Documents/Obsidian Vault/Token羊毛情报站/ 两笔记——免费Token总览.md（118 条已验证情报自动聚合）+ 信源监控看板.md（信源数/队列/心跳），deals.json 每变即刷
- **共用 Excel 确认**：信息源总表-全量版.xlsx 为唯一全量信源注册表（本轮 51→56 源），主会话与助理共同维护，助理负责增量

## 信源千人计划达成（2026-10-28，老板令「1000条→清洗→筛长期源→爬虫接管，零token」）

- **扩展器 tools/expand_sources.py 上线（零 token）**：源里挖源——3 个种子聚合仓库 README + GitHub 搜索 4 组关键词 + 6 个社区帖出链 + reddit JSON，**产出 1317 候选**（official 263 / article 1014 / repo 40，957 个可达 200）
- **清洗筛选 tools/curate_sources.py**：1317 → **1245 唯一源**（清 72 条重复/无效）→ **100 条长期源**（official/repo、可达、同域≤3、评分≥5）→ **36 条自动并入采集器，现役 60 源**
- **Excel**：新增「候选源池」（1245 行全量）与「长期源清单」（100 行）两个 sheet
- **爬虫接管**：harvest.py 调速（1s 间隔/10s 超时）保证 60 源单轮 <10 分钟，15 分钟巡检原生消化；本轮跑全量基线中
- **终态路径确认**：找源（扩展器+队列）→ 清洗（curate）→ 盯防（harvest+diff）三段全部脚本化，LLM 只在「页面真变了」时出场——不烧 1 token 全自动获取信息源的骨架已就位

## 公众号管道打通（2026-10-28，老板令「公众号信源很快很丰富，重点查」）

- **结论修正**：此前「公众号不可管道化」判断过时——搜狗微信搜索本机直连可用（robots 只限搜狗自家蜘蛛），mp.weixin 文章页全文可抓（3.5MB 实测）。公众号发现正式管道化 ✅
- **tools/weixin_discover.py**：4 查询词首轮 **39 篇文章** + 神秘喵星人滚雪球（文内互链/6 标题）；产出 weixin_articles.json
- **采集器 62 源**：+2 搜狗查询位（token免费额度/AI羊毛折扣码），每 15 分钟重查，**新文章标题出现即 diff 告警**——零 token 公众号雷达
- **3 条线索**（⏳主管核实）：①「每天10亿token·4免费模型含K3」聚合平台待定位 ②SCNet 单用户额度升至 3000 万（变更线索，主数据有旧条目）③「34家免费额度拧成一个接口」3.7万Star 聚合仓待定位
- 待改进：搜狗 /link 加密跳转解析（SNUID cookie 方案）→ 文章直达率提升，已入队列
- 2026-10-28 02:02 找源巡检：队列1条结案(Google Antigravity 负情报)；harvest 62源 5 项变化均为结构/基线；心跳已写

## 信息验证机制上线（2026-10-28，老板令「要做信息验证」）

- **tools/verify_sources.py**：候选源内容相关性验证（关键词命中≥3=相关 / 1-2=弱相关 / 0=可达无关 / 不可达=死链），结果回写 Excel「验证」列
- **首轮 260 条**：相关 156（60
## 信息验证机制上线（2026-10-28，老板令「要做信息验证」）

- **tools/verify_sources.py**：候选源内容相关性验证（关键词命中≥3=相关 / 1-2=弱相关 / 0=可达无关 / 不可达=死链），结果回写 Excel「验证」列
- **首轮 260 条**：相关 156（60%）/ 弱相关 32 / 可达无关 57 / 死链 15——池子健康度 72%，长期源清单 100 条已全部带验证标记
- **已挂进 15 分钟巡检**：每轮自动验 50 条，1245 池约 25 轮（约 6 小时）验完；验证为 offtopic/dead 的源在后续 curate 轮自动降权淘汰
- 四段零 token 流水线定型：expand(找) → verify(验) → curate(筛) → harvest+diff(盯)
- 2026-10-28 找源巡检：62源盯防无内容变化；验证累计310条(205相关)；**发现 Cursor 10-12 新价目体系（X订阅与 Grok 共享池）——plans.json/⌨️Coding面板变更线索→主管**；Cursor/Windsurf 定价页入采集器（64源）；队列剩11条
- 2026-10-28 找源巡检：64源盯防（3项变化均结构/基线，gh-aipmandy 源抖动列入淘汰观察）；验证累计360条(254相关)；**外网重磅线索：MonkeyCode 每日3000万免费tokens无信用卡（单源待核，高优）+ TRAE 五档价目**；队列剩10条
- 2026-10-28 找源巡检：64源盯防仅1项=抖动源自愈(blob→raw修复)；验证累计410条(296相关)；**MonkeyCode 定位成功：长亭科技 monkeycode.cn，数额多源出入→主管按控制台核实**；官方文档页入采集器(65源)；队列剩9条
- 2026-10-28 找源巡检：65源盯防3项=MonkeyCode建基线+Copilot页瞬时抖动+FreeToken连续变化(高活源观察)；验证累计460条(324相关)；HuggingFace 免费档$0.10/月查实——负情报结案；队列剩9条
- 2026-10-28 找源巡检：65源盯防1项=Copilot页抖动恢复；验证累计510条(367相关)；**小米MiMo查实：100T免费计划已领完→永久降价99%，低价条目候选→主管**；队列剩8条
- 2026-10-28 找源巡检：65源盯防全绿无变化；验证累计560条(411相关)；讯飞星辰「不限量」查实=6月限时活动(降级)；smzdm 2026.09 清单新帖入表；队列剩7条
- 2026-10-28 找源巡检：65源盯防全绿无变化；验证累计610条(454相关)；**NVIDIA NIM 免费API大升级变更线索(80-100+模型一年免费不限总量，双源，高优→主管)**+3个CSDN聚合源入表；「每天10亿」线索暂无法定位维持开放；队列剩7条
- 2026-10-28 找源巡检：65源盯防全绿；验证累计660条(495相关)；**⭐修正发现：docs.bigmodel.cn/cn/update/promotion 现已直接列出 Weekend Build 周末3亿 GLM-5.3-Flash（周日23点清零）/ZCode 新用户1亿/1024节5亿——此前「活动页不含客户端活动」结论过时，zcode-linuxdo 条目现在有官方出处可升级（周末3亿=每人每周领、先到先得）**；「智谱实名2亿」未证实降级；队列剩6条
- 2026-10-28 找源巡检：65源盯防全绿无变化；验证累计710条(538相关)；每日登录类摸底结案（无统一签到中心，智谱「每日一亿领取」单源线索→主管）；队列剩5条
- 2026-10-28 找源巡检：验证累计810条(584相关)；**源故障诊断结案：①gemini/mistral 系=网络层不可达(VPN 路由相关，间歇恢复)②groq=403 硬反爬→摘出采集器转真浏览器盯防③windsurf.com 308→devin.ai=⭐Windsurf 并入 Cognition 变更线索(体验档横评需更新)→主管**；采集器新增 disabled 机制(64活跃/1停用)；队列剩5条
- 2026-10-28 找源巡检：活跃源故障已降至4个(groq/windsurf处理见效)；验证累计910条(607相关)；公众号雷达重扫=搜狗缓存未更新(39篇持平，查询词按周轮换待启用)；2项变化为源结构类；队列剩5条
- 2026-10-28 找源巡检：65源盯防全绿；验证累计960条(628相关)；**v2ex 摸底：⭐竞品站 token.pencilai.top 发现（同类汇总站，建议监测收录差异）+ 小米MiMo 状态修正（额度重置+50倍+0.01元续费，非「已领完」）+ 快手/美团免费API线索；「真Claude直连送千万」类帖因套壳风险拒收**；搜狗雷达确认需 cookie 升级（队列已有）；队列剩4条
- 2026-10-28 找源巡检：验证累计1010条(637相关)；**竞品站收编：token.pencilai.top 静态可抓（78KB），入采集器作竞品雷达——其编辑线与 ours 差异互补（他们不收网页聊天）**；OpenRouter API 快照项确认主会话已覆盖→闭环；队列剩3条
- 2026-10-28 找源巡检：66源盯防3项=竞品雷达建基线+2抖动恢复；验证累计1060条(647相关)；**GitHub Copilot 学生免费权益变动线索（3-12终止→Student计划4月暂停→主数据 github-student-pack 表述需复核）→主管**；学生认证项闭环；队列剩2条
- 2026-10-28 找源巡检：65源盯防2项=FreeToken抖动+SambaNova瞬时；**里程碑：957 可达候选 100% 验证完成（647 相关/68% 健康度）；curate 接入验证净化→长期源 100→79 条（21 条无关/死链剔除），4 条新合格源并入，采集器 70 源（触顶，69 活跃）**；下一步：①队列需补货（剩2条）②可从 647 相关池提拔重点文章源轮换③采集器上限视单轮时长再调；队列剩2条
- 2026-10-28 找源巡检：70源盯防5项=4新源基线(LongCat/kilo/Cerebras/inferbase——美团LongCat文档已入盯防)+FreeToken抖动；验证池957全验完(verify待命等新候选)；掘金摸底：5聚合源+NVIDIA Playground佐证(高优线索再加固)+「羊毛密度升高」市场趋势；队列补货至7条
- 2026-10-28 找源巡检：70源盯防1项抖动；智谱「每日一亿」入口定位=trial-card 页族（8+ 体验卡页，数额登录核）→主管；队列剩6条
- 2026-10-28 找源巡检：70源盯防1项抖动；**「34家白嫖神」定位成功=OmniRoute（diegosouzapw/OmniRoute，3.7万Star）：本地网关聚合 200-300+ 提供商、免费额度仪表盘 15-16亿/月、Combo 永不停机路由——工具源入采集器；建议主会话评估站点「工具区」收录**；队列剩5条
- 2026-10-28 找源巡检：71源盯防2项=OmniRoute建基线+1抖动；公众号雷达第3周批次 40 篇(+1)；队列剩5条
- 2026-10-28 找源巡检：66源盯防1项抖动；lololowe 博客评估通过入采集器（72源）；队列剩3条
- 2026-10-28 找源巡检：72源盯防2项变化待二次观测；TaoToken 定位=taotoken.net 统一Key聚合网关（线索→主管核数额）；队列剩2条
- 2026-10-28 找源巡检：72源盯防2项变化待二次观测；z.ai 海外 Coding Plan 查实（Lite$18/Pro$80/Max$168·配额≈Claude 3倍）→⌨️Coding面板海外版候选；队列剩2条
- 2026-10-28 找源巡检：72源盯防1项变化待二次观测；HN 摸底无直命中，AgentReady 工具线索(低优)入账；队列剩2条
- 2026-10-28 找源巡检：72源盯防（心跳已写）；**扩展器第二批启动**（新关键词：awesome ai coding plan/free tokens llm list/大模型额度白嫖/free api credits list），v1.1 加验证保留合并逻辑（旧 1111 条验证状态不丢）；跑完自动并入候选池→下一轮 verify 接力；队列剩2条
- 2026-10-28 找源巡检：**扩展器第二批收获 1154 候选**（official 239/repo 107，新关键词挖到不同 URL 集）；发现并修复「覆写丢验证」竞态——Excel 候选源池做全量恢复 + expander 升级 v1.2 累积模式（旧候选永不丢失）；心跳已写；队列剩2条
- 2026-10-28 找源巡检：72源盯防1项抖动；**LongCat(美团)查实：开源560B MoE+官方平台，文档已入采集器，免费数额→主管按控制台核**；验证推进1011条(701相关，第二批次上车)；队列剩2条
- 2026-10-28 找源巡检：72源盯防1项抖动；Kilo Code 查实（Auto Free 层自动路由8+免费模型）→工具区评估（与OmniRoute同类）；验证推进1061条(750相关)；队列剩2条
- 2026-10-28 找源巡检：68源全绿无变化；**公众号雷达第4周批次：账号提取管道首次出活——新账号「茉界」（其文章《GitHub Copilot不让学生免费用最新的大模型了》与 Copilot 学生权益变更线索互证）**；队列剩2条
