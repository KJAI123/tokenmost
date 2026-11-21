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
