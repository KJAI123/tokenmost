# 企鹅号（om.qq.com）发文智能体日志 2 — 2026-11-19 第二轮

## 结果

**发布成功。**《免费云服务器怎么选：5家对比+3个坑》已提交，内容管理列表显示「共 2 条内容 / 图文 / **加工中** / 手工发文 / 全平台分发」，修改于 2026-11-19 12:51:40。纯干货零植入：发布前终检 `ProseMirror a=0`、正文+标题扫描 `tokenmost/http/www./.com/.cn` 全部 0 命中。截图留档 `/tmp/om2-01-editor.png` … `/tmp/om2-08-published-list.png`（关键：om2-02 正文填入、om2-06 自主声明已应用、om2-08 发布成功列表）。

## 账号与额度

- 账号「97后聊跨境」（正式运营），登录态在本轮开始时仍有效（复用 9222 上已有 om.qq.com 标签，未走 userAuth 恢复流程）。
- 昨日/今日额度口径：第一轮日志称今日剩 5 条；本轮发布后账号当日累计 2 篇（第 1 篇「AI 工具选型避坑」01:52 已发布态）。日发 1-2 篇安全线——**今日 2 篇已到线，本日不再发**。

## 文章内容（存档）

标题（18 字）：免费云服务器怎么选：5家对比+3个坑

正文 502 字（编辑器计数 497），13 段纯文本编号，无 Markdown 加粗、无链接：

> 想白嫖台服务器的，先看完这篇再动手。「免费」两个字后面全是规则：有的会停机，有的会扣费，有的到期连数据都给你清了。先上5家对比，再说3个坑。
> 一、5家免费方案一句话对比
> 1. Oracle免费层：号称白嫖之王，但2026年6月起纯免费号ARM砍半成2核12G，7天平均利用率低于20%还可能被停机回收。
> 2. AWS免费层：新用户12个月免费，绑了卡超量直接扣费。
> 3. InstaBox：4核8G免费云电脑，常设计划不用抢，适合挂常驻任务。
> 4. Modal：每月30美元credits，月月刷新，跑短时任务最香。
> 5. E2B：注册送100美元一次性额度，用完就没了。
> 二、3个最常见的坑
> 坑一：停机没商量。Oracle免费实例利用率不达标就回收，服务半夜没了很正常，关键业务别只靠它。
> 坑二：免费变账单。AWS这类按量计费的免费层，超一点就按原价扣，流量、存储、快照都在偷偷算钱。
> 坑三：数据随时清盘。免费层到期或被回收后磁盘直接清零，没人提前通知你备份，重要数据必须异地再存一份。
> 三、怎么选：常驻挂机选InstaBox，跑计算任务用Modal的月度额度，练手拿E2B的赠金。
> 你被哪家坑过？评论区聊聊，帮后来人避个雷。

事实依据：InstaBox 4vCPU/8GiB、Modal Starter $30/月 credits、E2B Hobby $100 一次性 credits 均见 `data-research/freecloud/harvest/freecloud-2026-11-19.md`；Oracle 7 天利用率<20% 回收、2026-06 纯免费号 ARM 砍半 2核12G、AWS 免费层超量扣费为任务给定事实。

## 本轮新踩的坑（补充到 SOP）

1. **视口外的按钮点了白点**：getBoundingClientRect 的 y 超出视口高度（本机 1512x808）时 dispatchMouseEvent 落空，无报错、无反应。必须先 `scrollIntoView({block:'center'})` 再取坐标点击。
2. **自主声明弹窗的「确认」按钮在滚动区里**：弹窗 `omui-dialog-body` scrollHeight 558 > clientHeight 504，确认按钮初始在可视框外，且该点 `elementFromPoint` 命中的是 `omui-dialog-mask`（说明被遮罩挡住，点了等于没点）。先 `body.scrollTop = scrollHeight` 再点，命中 `BUTTON.omui-button--primary` 才有效。**用 elementFromPoint 预检命中元素是判断「点了有没有用」的可靠手段**。
3. **声明弹窗选项结构**：选项是 `label.omui-radio`（textContent=选项名，内含 `input[checked]`），点击 label 中心即可；选中态验证用 `input.checked`，别信 class。
4. **声明选择**：本轮如实选「该文章由AI辅助创作」（SOP 允许 无需标注/AI辅助创作 二选一，AI 撰稿选后者更稳）。应用成功标志：编辑页自主声明行显示「作者声明：该文章由AI辅助创作」+ 弹窗遮罩消失。
5. **DPR 坑**：9222 视口 1512x808、截图 1998px 宽（DPR≈1.32，不是 retina 的 2），OCR 坐标换算走 `png_w/innerWidth`，别写死 2。
6. **发布成功判定**（与第一轮一致）：点发布后 URL 跳 `/main/management/articleManage`，列表卡片带「加工中」徽章。第一篇现已转「已发布」态，说明加工→发布周期约半天内。
7. toast 观察器因页面跳转丢了返回值（None），不影响判定——以 URL 跳转 + 列表状态为准即可。

## 复用要点（增量）

- 连接：`rpa_browser.CDP_HTTP='http://127.0.0.1:9222'` 运行时覆写后再 `from rpa_browser import Tab`（tools 文件默认 9223 是别的任务线的，勿改文件）。
- 逐行输入 ProseMirror + Enter(vk13) 的既有 SOP 完全复用，本轮 13 段无粘连。
- 发布前固定三件套：①终检（links==0 + 植入词扫描 + 字数 400-600）②挂 toast/XHR 观察器 ③elementFromPoint 预检发布按钮命中。

---

# 11-21 第一篇《免费域名怎么搞：3 个正规渠道+2 个坑》— 登录态丢失，未发布

## 结果

**未发布（登录阻断）。** 目标稿件 `data-research/seo/omqq-daily/o3-free-domain.md`（纯文本零植入干货，建议发布窗口 11-21 上午 10:00-12:00）。9223 无头浏览器重启后 om.qq.com 与微信会话双双失效，卡在扫码环节，按预案跳过。今日额度未消耗（0 篇提交），稿件未进任何平台，未做 git。

## 过程与判定依据

1. 9223 CDP 存活（Chrome 158 无头），但无 om.qq.com 标签，`Tab.connect(new_url='https://om.qq.com/main')` 落地 `om.qq.com/userAuth/index`「登录-腾讯内容开放平台」——登录态丢失，符合预期。
2. 按 SOP 走恢复：勾协议（`SPAN.lv2-agreement-check-icon` @938,564，点击后 `input.lv2-agreement-checkbox.checked=true`）→ 点微信登录（`SPAN.lv2-login-way-text` @1050,329）→ 弹出「微信登录」二维码弹窗（iframe `om.qq.com/mindex/userAuth/WxLogin?source=login2`）。
3. 轮询 60 秒无自动跳回（免扫码恢复未发生）。**判定微信会话失效的铁证**：浏览器级 `Storage.getCookies` 全量 217 条，过滤 `qq.com/weixin/wechat` 域 = **0 条**（9223 重启把持久化会话清了）。二维码在等手机扫码，此环节 RPA 无法替代，需老板扫码。
4. 截图 `/tmp/om3-01-login.png`、`/tmp/om3-02-qr-waiting.png`（字节数相同=同一张码仍在等待；注意截图会过期，恢复时重新走一遍勾协议→微信登录出新码即可）。

## 恢复后接续清单（给下一轮执行者）

- 恢复入口：om.qq.com → 勾协议 → 微信登录 → 老板用手机微信扫码确认。
- 稿件就绪：《免费域名怎么搞：3 个正规渠道+2 个坑》，标题 18 字（5-64 合规），正文 13 行纯文本约 550 字，无链接无 Markdown 无植入词（稿件头注释已注明「纯干货零植入 v4」）。直接按 SOP 逐行进 ProseMirror。
- 发布四步不变：标题 contenteditable span → 正文逐行+Enter → 自主声明（选「该文章由AI辅助创作」，弹窗 scrollTop 到底 + elementFromPoint 预检命中 BUTTON 再点）→ 发布后内容管理列表验「加工中/全平台分发」。
- 发布窗口：稿件建议 11-21 上午 10:00-12:00；若实际恢复晚于窗口，当天上午补发即可，日发 1-2 篇安全线照旧。

---

# 11-22《AI 编程订阅怎么选：按使用强度分三档》— 发布成功

## 结果

**发布成功。** 稿件 `data-research/seo/omqq-daily/o4-coding-plan.md`（AI 编程订阅三档选型，纯文本零植入）已提交，内容管理列表显示「共 4 条内容 / 图文 / **加工中** / 手工发文 / 全平台分发 / 修改于 2026-11-22 06:57:10」。发布前终检：links=0、植入词扫描 tokenmost/http/www./.com/.cn 全 0 命中、正文 9 段与稿件逐字一致（编辑器计数 628 字）、标题 19 字在框。截图 `/tmp/om4-01-editor.png` … `/tmp/om4-11-published-list.png`（关键：om4-04 标题入框、om4-05 正文 9 段、om4-09 发布前终检、om4-11 发布成功列表）。另：o3《免费域名怎么搞》已于 11-20 14:04 发布成功（已发布态），11-21 那轮登录恢复后由后续任务补发。

## 登录态与额度

- 9223 无 om.qq.com 标签，`Tab.connect(new_url='https://om.qq.com/main')` 直落 /main 未跳 userAuth——昨天老板扫码 + cookie 迁移的登录态有效，未要求再次扫码。
- 今日（11-22）提交 1 篇，日发 1-2 篇安全线内。账号内容总数 4（11-19 两篇 + 11-20 一篇 + 本篇）。

## 本轮新踩的坑（补充到 SOP）

1. **编辑器会自动恢复孤儿草稿**：打开 /main/creation/article 直接带出 editorCache 里一份残留稿（退货处理主题 1201 字，标题空，repo 内无对应稿件=孤儿缓存），且自主声明 chip 已随缓存恢复。处理：正文/标题 select_all+Backspace 清空后再输入；其余表单项（封面/分类/标签/活动投稿）核过均为空。残留全文存档 `/tmp/om4-leftover-draft.txt`。**下次进编辑器先查正文字数计数器，非 0 先清场**。
2. **标题点不进去的真因是滚动位置**：正文 focus 过后页面 scrollY=295，标题框 getBoundingClientRect y=-2（顶边外、被吸顶工具栏盖住），中心点 elementFromPoint 命中 `EXEDITOR-TOOLBAR-BUTTON`——RPA 点击点在工具栏上，焦点根本没离开 ProseMirror，type_text 全落正文（两次复现，pm 里出现标题文本）。**修复三步**：`window.scrollTo(0,0)` → elementFromPoint 确认命中标题 span → 点击后验证 `document.activeElement === 标题span` 再 insertText，输完再验标题框内容+pm 为空。原「type_text 后焦点会窜」的坑，本质多半就是这一种。
3. **自主声明流程已改版（重要）**：不再有「添加内容自主声明」按钮和弹窗。现在是 `#articlePublish-selfDeclaration` 表单组里直接放一枚 chip（`omui-contentbutton`）「**该文章由AI生成**」+ 移除图标；点 chip/label/说明文字都不再弹窗，旧选项（无需标注/AI辅助创作/虚构演绎）在全 DOM 已不存在。本稿由 AI 撰写，chip 声明与事实相符，直接发布通过，未出「请选择自主声明」toast——与 2025-09 起 AI 内容强制标识的监管要求一致，后续按现状走即可。
4. **`tab.url` 是连接时的快照**：SPA 路由跳转后不更新，点发布后 6 秒内看 `tab.url` 会误判失败。以 `location.href` + 列表卡片状态为准；toast/XHR 观察器也随页面跳转丢失（返回空），不影响判定。
5. 发布按钮 elementFromPoint 预检命中 `SPAN`（按钮内层 span）也算命中（`b.contains(hit)`），正常点。

## 复用要点（增量）

- 清场 → `scrollTo(0,0)` → 标题（activeElement 校验）→ 正文逐行 insertText+Enter(vk13) → 终检（links=0/植入词/标题在框/pm 段落逐字比对）→ 预检发布按钮 → 点发布 → `location.href` 跳 articleManage + 列表验「加工中/全平台分发」。
- 正文 9 段逐行输入无粘连，段落 `children.length` 会比实际段落数多 1（尾部空段落来自最后一个 Enter），比对时按非空段落算。

---

# 11-23《笔记软件免费方案：Obsidian 三件套搭配》— 发布成功

## 结果

**发布成功。** 稿件 `data-research/seo/omqq-daily/o5-open-source-note.md`（Obsidian 三件套免费组合，纯文本零植入）已提交，内容管理列表显示「共 6 条内容 / 图文 / **加工中** / 手工发文 / 全平台分发 / 修改于 2026-11-23 06:51:00」。发布前终检：links=0、植入词扫描 tokenmost/http/www./.com/.cn 全 0 命中、正文 12 段与稿件逐字一致（编辑器计数 570 字）、标题 23 字在框。正文自带三处【核实日期：2026-11-20】标记按「与稿件逐字一致」原样进正文，渲染无异常。截图 `/tmp/om5-01-main.png` … `/tmp/om5-12-published-list.png`（关键：om5-05 声明已应用、om5-07 标题入框、om5-08 正文 12 段、om5-09 发布前终检、om5-12 发布成功列表）。

## 登录态与额度

- 9223 今日重启、cookie 全量迁移：无 om.qq.com 标签，`Tab.connect(new_url='https://om.qq.com/main')` 直落 /main 未跳 userAuth——迁移后的登录态有效。
- 今日（11-23）本任务提交 1 篇。另有另一任务线的《海外仓退货到手…》已于今晨 04:52:47 发布（已发布态，账号内容总数因此为 6）——正是本轮清场的 editorCache 孤儿稿（存档 `/tmp/om5-leftover-draft.txt`），它已从别处发出，清场无损失。

## 本轮新踩的坑（补充到 SOP）

1. **声明弹窗其实还在，「无弹窗」只是「随缓存在位」的特例**：11-22 的缓存带了 chip 所以直接在位；本轮缓存未带声明，`#articlePublish-selfDeclaration` 表单组里是虚线按钮「**添加内容自主声明**」，点击弹出「发布内容自主声明」弹窗（10 个 `label.omui-radio` 单选项：无需标注/该文章由AI生成/AI辅助创作/个人观点/虚构演绎/转载/营销广告/健康医疗/危险行为/事件可考证）。选「该文章由AI生成」→ 弹窗体 `scrollTop=scrollHeight`（558/504，确认按钮在折叠区）→ elementFromPoint 预检命中 `BUTTON.omui-button--primary` → 确认，表单组变「作者声明：该文章由AI生成」。**进编辑器先看声明组是 chip 还是添加按钮，两条路径都要会走。**
2. **PM 清场时点击 focus 会被视口裁剪带偏**：正文 focus 过后 PM 顶边 y 为负，`Math.max(rc.y+60,10)` 把点击点夹到 y=10 落在吸顶工具栏，select_all 全选落在错误元素、Backspace 没删到（正文残留 701 字）。可靠做法：直接 `pm.focus()`（JS，已验 `activeElement===pm`）再 select_all+Backspace，一次干净。
3. 编辑器计数器口径：本轮正文 textContent 617 vs 计数器 570（计数器不吃空格/标记外字符），与 11-19 的 701/673 同口径，字数核查以计数器为准。

## 复用要点（增量）

- 全流程：connect 验登录（`location.href`）→ 开 /main/creation/article → 查正文字数计数器，非 0 先存档再清场（pm.focus() 路径）→ 声明（chip 在位跳过 / 添加按钮走弹窗）→ `scrollTo(0,0)`+elementFromPoint+activeElement 三步标题 → pm.focus() 后逐行 insertText+Enter(vk13) → 终检（links/植入词/逐字比对/计数器）→ 发布按钮 scrollIntoView+预检+RPA → `location.href` 判 articleManage → 列表验「加工中/手工发文/全平台分发」。

---

# 11-24《免费 HTTPS 证书怎么续：Let's Encrypt 三个月续期自动化》— 登录态丢失，未发布

## 结果

**未发布（登录阻断）。** 目标稿件 `data-research/seo/omqq-daily/o6-free-cert.md`（Let's Encrypt 90 天证书续期自动化，纯文本体零植入，标题 37 字 / 正文 7 段 850 字，植入词扫描 tokenmost/http://https://www./.com/.cn 全 0 命中）。9223 上 om.qq.com 登录态失效，按本轮指令「勿要求老板重复扫码」直接跳过，未走任何恢复流程。今日额度未消耗（0 篇提交），稿件未进任何平台，未做 git。

## 过程与判定依据

1. 9223 CDP 存活，但无 om.qq.com 标签（现存的 3 个 page 是 csdn 线 + about:blank）。`Tab.connect(new_url='https://om.qq.com/main')` 落地 `om.qq.com/userAuth/index`「登录-腾讯内容开放平台」，符合 11-21 同款失效形态。
2. 复核证据：再次导航 /main 仍跳 userAuth（排除首跳时序假阴性）；浏览器级 `Storage.getCookies` 全量 161 条，`om.qq.com` 域下仅 `ts_uid / ts_refer / wxky` 3 条埋点 cookie——**无任何会话 cookie**（qq.com 泛域 27 条、weixin 18 条均为其他腾讯域残留，救不了 om.qq.com 的登录）。
3. 截图留档 `/tmp/om6-01-entry.png`（userAuth 落地页）、`/tmp/om6-02-login-check.png`（复核后同页）。登录页标签留在 9223 未关，后续恢复可直接续用。

## 恢复后接续清单（给下一轮执行者）

- 登录恢复：om.qq.com → 勾协议 → 微信登录 → 老板手机微信扫码（与 11-21 流程一致）。
- 稿件就绪零改动：《免费 HTTPS 证书怎么续：Let's Encrypt 三个月续期自动化》，标题 37 字（5-64 合规，含空格），正文 7 段 850 字纯文本，无链接无 Markdown 无植入词。注意稿件头注释的建议发布窗口是 **2026-11-26（周四）上午 10:00-12:00**——今天（11-24）本就早于窗口，恢复登录后在 11-26 窗口内发布即可，无需改稿。
- 发布路径照 11-23 复用要点全流程走：进编辑器先查正文字数计数器（非 0 先存档 /tmp/ 再清场）→ 声明组看 chip 还是「添加内容自主声明」虚线按钮（后者走弹窗 10 选项选「该文章由AI生成」，弹窗体滚到底 + elementFromPoint 预检确认钮）→ 三步标题 → 逐行 insertText+Enter(vk13) → 终检 → 发布验 articleManage 列表「加工中/全平台分发」。

## 🚨 11-25 封面缺失根因确认（老板发现：全 0 流量）

- **根因**：企鹅号发布管线把封面当「选填」全部跳过——无封面图文**不进推荐池**（双列瀑布流必须有图），6 篇已发布全部 0 浏览
- **修复**：封面修复智能体批量补图（每篇仅 1 次修改机会——「单篇最多修改 3 次」且已用 0 次）
- **管线铁律修正**：企鹅号封面**必传**（不再选填）——SOP 新增步骤「封面区 + 号→上传→预览落位验证」，缺封面禁止点发布
- CSDN 同步检查：csdn_publish.py 也无封面上传步骤——CSDN 封面影响推荐同理，后续版本补

---

# 11-24 封面修复（实际执行 2026-11-25 01:16-01:25）— 6 篇全部补上，审核全过

## 结果

**6/6 成功，零失败零重试。** 6 篇已发布文章逐一走「修改→补封面→提交」，全部通过审核回到「已发布」态，列表卡片封面缩略图（168px，inews.gtimg.com）全部落位——0 流量根因（无封面不进推荐池）已消除。每篇消耗 1 次修改额度（3 次上限余 2）。

| # | 文章 | 封面 | 提交时间 | 终态 |
|---|------|------|---------|------|
| 1 | 笔记软件免费方案：Obsidian 三件套搭配 | generic-ai-tools.jpg | 01:16:44 | 已发布+封面 |
| 2 | 海外仓退货到手，先核对安全，再做这 4 个判断 | generic-ai-tools.jpg | 01:18:26 | 已发布+封面 |
| 3 | AI 编程订阅怎么选：按使用强度分三档 | juejin-json2md.jpg | 01:19:06 | 已发布+封面 |
| 4 | 免费域名怎么搞：3 个正规渠道+2 个坑 | omqq-pitfalls.jpg | 01:19:41 | 已发布+封面 |
| 5 | 免费云服务器怎么选：5家对比+3个坑 | bjh-free-token.jpg | 01:20:17 | 已发布+封面 |
| 6 | AI 工具选型避坑：普通用户最容易犯的 3 个错误 | omqq-pitfalls.jpg | 01:20:49 | 已发布+封面 |

终验截图 `/tmp/omcover-final-all-published.png`（6 卡片全带封面缩略图）；每篇过程证据 `/tmp/omcover-{1..6}.png`（列表终态）+ `/tmp/omcover/art{n}-placed.png`（编辑器封面落位后、提交前）。

## 全流程 SOP（每篇 ~90 秒，全部一次成功）

1. 列表卡片「修改」是 `<a href="/main/creation/article?articleId=…&isPubed=1">`——直接 `location.href` 进编辑器（轮询 addCoverBtn/封面 label 出现判定加载完成，~15s）。
2. `window.scrollTo(0, scrollHeight)` 到封面区；已有封面检查（`.coverThumb` 存在则跳过，防止误耗额度）；无封面时封面组文案是「封面/选填」+ `.addCoverBtn`。
3. RPA 点 `.addCoverBtn` → 弹 `omui-dialog--lg`（默认「文内图片」tab）→ 点「本地上传」tab（`LI.omui-tab__label`）。
4. **上传零裁剪步骤**：`DOM.getDocument → DOM.querySelector('.omui-upload-image-trigger input[type=file]') → DOM.setFileInputFiles(jpg 绝对路径)`，~2-4s 后弹窗内出现 `omui-upload-image-item-thumb`（src 已是 gtimg CDN）即完成，无裁剪确认环节。
5. elementFromPoint 预检命「确认」钮（`omui-button--primary`）→ RPA 点击 → 弹窗关闭，编辑器封面组变「封面/更换/编辑」+ `.coverThumb` 落位 → **截图留证后才进下一步**。
6. elementFromPoint 预检「提交」钮 → 点击 → 「发布提醒」弹窗（**提交后进入修改审核中，审核通过前原文不覆盖**——编辑已发布文章独有的确认弹窗）→ 预检命「确定」→ 点击 → 跳回 articleManage。
7. 列表验「加工中/审核中→已发布」+ 封面缩略图出现。实测审核 1-5 分钟内放行，6 篇 01:25 时已全部回「已发布」。

## 本轮新坑/要点（补充到 SOP）

1. **列表状态文案计数陷阱**：articleManage 页 filter 菜单（全部/已发布/审核中/…/加工中）本身含「审核中」「加工中」字样，`innerText.match(/审核中/g)` 轮询时会恒 ≥1——判篇级状态必须逐卡片读，不能整页计数。
2. **加工中/审核中卡片不显示缩略图**：提交后卡片短暂无封面图+无数据，别误判失败；等状态回「已发布」后缩略图出现（每篇 CDN URL 唯一）。
3. 编辑器里「封面选填」文案仍存在——企鹅号表单仍标选填，但推荐池机制要求必传；SOP 已把封面列为发布前必检项（`.coverThumb` 缺失禁止点提交）。
4. 正文/声明在修改流程中原样保留（含「该文章由AI生成」chip 与旧文「作者声明：该文章由AI辅助创作」两种形态），修改不触碰正文即可零风险过审。
5. 连接复用注意：`Tab.connect(url_frag='om.qq.com')` 每次重连同一标签，SPA 内 location.href 跳转后 `tab.url` 快照不更新（11-22 已记），本轮以 `location.href` 实时值为准，无新坑。

## 管线铁律修正（落地）

- 企鹅号发布 SOP 新增必检步骤：「封面区 .coverThumb 落位验证通过才允许点提交」——后续新稿发布时直接带封面，不再需要补图流程。
- 修改额度纪律：每篇编辑消耗 1/3，本轮 6 篇各用 1 次，余量 2 次/篇；补图脚本 `/tmp/omcover/fix_one.py`（n articleId cover.jpg）可复用。
- 未做 git（按指令）。
