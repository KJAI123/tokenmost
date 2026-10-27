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
