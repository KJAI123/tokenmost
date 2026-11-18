# 企鹅号（om.qq.com）发文智能体日志 — 2026-11-19

## 结果

**发布成功。**《AI 工具选型避坑：普通用户最容易犯的 3 个错误》已提交，内容管理列表显示「共 1 条内容 / 图文 / **加工中** / 手工发文 / 全平台分发」，修改于 2026-11-19 01:52:08。纯干货零植入：正文 0 链接、无任何品牌提及（发布前用 `document.querySelectorAll('div.ProseMirror a').length` 验证 = 0）。截图留档 `/tmp/om-01-main.png` … `/tmp/om-33-published-list.png`（关键：om-16 内容终检、om-29 自主声明弹窗、om-33 发布成功列表）。

## 账号

- 账号「97后聊跨境」，134452，正式运营态，内容发布可用。
- 今日剩余发文额度：5 条（发布时 toast「今天还能发布5条」）。

## 编辑器结构（om.qq.com/main/creation/article）

| 项 | 结构 | 备注 |
|---|---|---|
| 入口 | 后台首页左侧「内容发布」→ `https://om.qq.com/main/creation/article` | SPA 路由，页面 URL 常停留在 /main，判断页面要看 DOM 不看 URL |
| 标题 | `span.omui-inputautogrowing__inner`（contenteditable 自动增高） | placeholder「请输入标题（5-64个字）」，计数「25/64」 |
| 正文 | `div.ProseMirror.ExEditor-basic`（ProseMirror，非 iframe） | 聚焦后 `Input.insertText` 输入；换行必须 `Input.dispatchKeyEvent` vk=13（工具库 `tab.key('Enter','Enter')` 的 vk 传字符串无效，会全挤成一段） |
| 封面 | 选填（单图/三图） | 无封面可直接发 |
| 分类 | 选填（「请选择分类」） | 无分类可直接发 |
| 标签 | 选填，最多 9 个，空格/回车分隔 | — |
| 活动投稿 | 选填 | — |
| **自主声明** | **必填** | 点「添加内容自主声明」→ 弹窗选声明（无需标注/AI辅助创作/虚构演绎/转载等）→ 确认。不选直接点发布会静默失败，只有 toast「请选择自主声明」 |
| 按钮 | 发布 / 定时发布 / 存草稿 / 预览 | 发布走 `om.qq.com/editorCache/update` 等 XHR |
| 自动保存 | 有（「已保存」指示） | — |

## 平台规则与坑（本次实测）

1. **登录态会失效但 cookie 未过期**：直开 /main 或 /main/creation/article 会被重定向到 `om.qq.com/userAuth/index` 登录页（此前已登录的 SPA 标签仍显示在线，是假象）。
2. **恢复登录路径（免扫码）**：userAuth 页 → 勾选「我已阅读并同意」checkbox → 点「微信登录」→ 弹出 `om.qq.com/mindex/userAuth/WxLogin` iframe → 浏览器内已有微信会话，**自动登录跳回 /main**，无需扫码。
3. **CDP 点击失效的元凶是标签未激活**：`Input.dispatchMouseEvent` 落点正确但页面无反应（MutationObserver 零变化）——必须先 `/json/activate/{id}` 把标签带到前台，点击才生效。每次重新连接后都要 activate。
4. **发布校验顺序**：字数/标题 → 自主声明（必填，见上）→ 发文额度。校验失败只出 toast，不弹窗、不改 URL，容易误判成功；必须用 MutationObserver/PerformanceObserver 抓 toast 与 XHR 确认。
5. **发布成功验证**：编辑器跳转到内容管理（`/main/management/articleManage`），列表出现该文并带状态（本次「加工中」）。内容管理筛选：全部/已发布/审核中/未通过/草稿/加工中/发布失败/定时发布。
6. 正文 503 字（要求图文正文 ≥ 一定字数，500+ 通过；下限未测）。
7. 内容全平台分发（腾讯视频/QQ浏览器/腾讯新闻/腾讯体育/腾讯微视）。

## 复用要点（下次发文）

- Tab.connect(url_frag='om.qq.com') → activate() → 若被踢到 userAuth：勾协议 → 点微信登录 → 等自动跳回。
- 标题：click 标题 span → insertText。正文：JS `focus()` ProseMirror → select_all+Backspace 清空 → 逐段 insertText + vk13 换行。
- 发布前必做：点「添加内容自主声明」→ 选声明（纯干货人选「无需标注」或如实选「该文章由AI辅助创作」）→ 确认 → 再点「发布」→ 等 URL 跳内容管理并核对列表。
