# ProseMirror 自动化踩坑记：从 insertText 到 DOM 粒度操控

<!--
目标平台：掘金（文章，技术深潜体）
发布日建议：2026-11-20（周五）晚 20:00-22:00 掘金晚间流量峰
结构说明：踩坑叙事体——失败现场 → 原理 → 三条路线 → Draft.js 同坑 → 避坑
写作与核实日期：2026-11-20；人味化：2026-11-23；无链接、无任何植入；纯干货零植入 v4
-->

上周三晚上给后台一个 ProseMirror 编辑器写自动填充，图省事直接改 DOM，页面看着改好了，一次重渲染回来，内容全弹回原样，气得我差点拍键盘。后来才明白：给富文本编辑器写自动化，你以为你在操作 DOM，其实是编辑器在操作 DOM。这篇记下完整踩坑路线。

### 为什么不能直接改 DOM

我一开始还以为是个小 bug，翻了源码才反应过来：ProseMirror 的真相源是 `state`（文档+选区），DOM 只是渲染结果。你在 DOM 上的任何改动，下次事务 dispatch 时都会被原样覆盖回去。合成事件更鸡贼，`isTrusted=false`，部分路径直接静默忽略，连报错都不给。

### 路线一：insertText，最省事

CDP 的 `Input.insertText` 是真实 trusted 输入，beforeinput 管线照常走。我第一次用它字全插歪了，排查半天才发现是光标没摆对——先把焦点和选区弄到位：

```js
const el = document.querySelector('.ProseMirror');
el.focus();
const sel = window.getSelection();
sel.selectAllChildren(el);
sel.collapseToEnd();   // 光标折叠到位，再 insertText
```

### 路线二：view.dispatch

`editor.view.dispatch(tr.insertText(...))` 最正统，文档也这么教。问题在自动化场景里 view 经常关在闭包里摸不到。摸得到就走这条，摸不到别硬凿，回路线一。

### 路线三：文件上传的 objectId

上传文件走 `DOM.setFileInputFiles`，我在这绕的弯最大。一开始用 `nodeId` 老路线，得先 `DOM.getDocument` 再 `DOM.querySelector` 换节点编号，页面一跳转编号就失效，过会儿又挂，来回折腾。后来才发现 `objectId` 路线：`Runtime.evaluate` 拿到节点的 RemoteObject 直接传，少两次往返，不过期。

### Draft.js 同坑

顺嘴提一句 Draft.js，病根差不多：受控 contenteditable，字符数据存在它自己的 editorState 里，`insertText` 经常打水漂，得改走 paste 事件或注入 `beforeinput`。

### 三条避坑

断言结果别看 DOM，看导出内容——DOM 只是投影。中文和 emoji 是 surrogate pair，按字符数算光标偏移会插歪，别问我怎么知道的。哦还有，每次输入前重新取焦点和选区——重渲染后旧 Selection 已过期。

你的编辑器自动化卡在哪一步？评论区对个暗号。
