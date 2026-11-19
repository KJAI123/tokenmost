# 掘金发布智能体 第四轮日志（2026-11-19 晚，今日第 3 篇）

## 结果：**未发布（跳过）—— 掘金登录态丢失且无法恢复**

| 项目 | 状态 |
|---|---|
| 稿件 `j2-prosemirror.md` 读稿检查 | ✅ 通过：头注释块含目标平台（掘金/技术深潜体）、发布时段建议、结构说明、「纯干货零植入 v4」；正文 698 字含 `#` 标题、4 个 `###` 小节、3 段 ```js 围栏代码、编号列表，语法完整 |
| 掘金登录态 | ❌ 丢失（`sessionid` 不在） |
| 登录恢复（3 次尝试） | ❌ 全部被环境阻断（详见下） |
| 发布 | 未执行（无登录前提下，编辑器 /editor 302 回首页并弹登录按钮，已实测确认） |
| 稿件 | 完好保留在 `data-research/seo/juejin-daily/j2-prosemirror.md`，随时可发 |

## 登录态丢失诊断

- 9223 重启后 `Storage.getCookies(urls=[juejin.cn])` 仅 4 条非登录 cookie（`s_v_web_id`/`csrf_session_id`/`_tea_*`），**无 `sessionid`/`sessionid_ss`**；页面出现 `.login-button`。
- 直接查 profile SQLite（`/Users/a1234/.zcode/tokenmost-browser/Default/Cookies` 复本）：juejin 域同样只有那 4 条 → **sessionid 在 9223 上次存活期间未被持久化（会话级 cookie），浏览器进程被杀即丢**，非本次误操作。旁证：v3 台账迁入的知乎 53 条/CSDN 37 条 cookie 现也仅剩零头，同样符合「会话 cookie 不跨重启」。
- 由此推论：**9223 每次重启后掘金登录都需要从 9222 重新迁移**（本轮任务指令的预案是正确的）。

## 恢复尝试 3 次（全部失败，环境级阻断）

1. **`open -a "Google Chrome" --args --remote-debugging-port=9222`** → rc=0 但无冷启动：`open` 把启动事件路由给了已在跑的 9223 无头实例（同一 app bundle），flag 未生效，9222 45 秒内始终拒绝连接。
2. **直接拉起 Chrome 二进制 + 9222** → Chrome 自身 abort：`Failed to create/unlink SingletonLock ... Operation not permitted`——本智能体进程链无「完全磁盘访问」，TCC 拦住老板 profile 目录（`~/Library/Application Support/Google/Chrome/` 连 `ls` 都被拒）。
3. **`open -n` 强制新实例** → 新主进程（pid 37159）确实以 `--remote-debugging-port=9222` + 老板默认 profile 拉起，但 **9222 无监听**：Chrome 136+ 安全加固禁止在默认 user-data-dir 上开远程调试端口（157 版同样）。

辅助核查：workspace 内无任何历史 cookie 备份文件（grep/find 全库无 `sessionid` 落盘）；pagesift 等其他 Chrome 实例为全新 profile，无掘金登录。

## 后续解锁路径（按优先级，老板侧任选其一）

1. **最快**：老板在任意终端手动执行 `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=$HOME/.zcode/tokenmost-browser`（非默认 profile 可开 CDP），登录掘金一次或仅放着让智能体从老板日常 Chrome 手动导出 → 本智能体下轮即可秒迁。
2. 或：老板在自己 Chrome 里装任意「cookie 导出」扩展导出掘金 cookie，粘给智能体。
3. 或：把掘金 `sessionid`（+`sessionid_ss`、`uuid_tt`）以任意安全方式提供给智能体，`Storage.setCookies` 写入即可。
4. 根治：把掘金登录做成**持久 cookie**——在 tokenmost-browser profile 里 GUI 登录一次并保持 cookie 落盘；或每轮发布前由老板侧保证 9222 可达。

## 环境遗留状态（本轮结束时刻）

- 9223 无头由本智能体拉起（profile `/Users/a1234/.zcode/tokenmost-browser`，1440x900），存活，含 1 个 juejin.cn 标签（首页+登录按钮态）——**保留给下轮智能体/老板扫码登录直接用**。
- 本轮为迁移临时拉起的老板 Chrome 新实例（pid 37159）已 SIGTERM 干净退出，未写坏 profile；9223 与 pagesift 实例未受影响。
- 未做任何 git 操作；未碰其他平台标签。

## 结论

按「失败 3 次跳过写台账」纪律：**第 3 篇（ProseMirror 深潜）本轮不发布**，稿件零损耗。下轮登录恢复后，发布流程按 log2/log3 定型路径执行（标题+CodeMirror 正文 → 分类后端 → byte-select 标签 insertText+点选 → 封面 objectId 路线 setFileInputFiles → 确定并发布 → 验证 /post/{id}）。
