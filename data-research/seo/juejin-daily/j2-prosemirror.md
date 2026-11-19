# ProseMirror 编辑器自动化踩坑记：从 insertText 到 DOM 粒度操控

<!--
目标平台：掘金（文章，技术深潜体）
发布日建议：2026-11-20（周五）晚 20:00-22:00 掘金晚间流量峰
结构说明：开头 2 句钩子（完读率优化）→ 原理一段 → 路线编号短小节（完读率友好）→ Draft.js 同坑 → 避坑 → 互动；纯干货零植入 v4
写作与核实日期：2026-11-20；无链接、无任何植入
-->

给富文本编辑器写自动化，第一课就是：你以为你在操作 DOM，其实是编辑器在操作 DOM。直接赋值不是没反应，就是下一秒被打回原形——这篇记录完整踩坑路线。

### 为什么不能直接改 DOM

ProseMirror 的真相源是 `state`（文档+选区），DOM 只是渲染结果：改 DOM 会在下次事务 dispatch 时被覆盖；合成事件 `isTrusted=false`，部分路径静默忽略。

### 路线一：insertText

CDP 的 `Input.insertText` 是真实 trusted 输入，beforeinput 管线照常走，前提是光标位置要对：

```js
const el = document.querySelector('.ProseMirror');
el.focus();
const sel = window.getSelection();
sel.selectAllChildren(el);
sel.collapseToEnd();   // 光标折叠到位，再 insertText
```

### 路线二：view.dispatch

`editor.view.dispatch(tr.insertText(...))` 最正统，但自动化场景里 view 常闭包拿不到，拿得到就走这条。

### 路线三：文件上传 objectId

`DOM.setFileInputFiles` 两条路：`nodeId` 老路线要先 `DOM.getDocument` + `DOM.querySelector` 换节点，页面跳转即失效；`objectId` 路线用 `Runtime.evaluate` 拿 RemoteObject 直接传，少两次往返也不过期。

### Draft.js 同坑

受控 contenteditable，字符数据在自己 editorState 里，`insertText` 常无效，改走 paste 事件或注入 `beforeinput`。

### 避坑

1. 断言结果别看 DOM，看导出内容——DOM 只是投影。
2. 中文、emoji 是 surrogate pair，按字符数算光标偏移会插歪。
3. 每次输入前重新取焦点和选区，重渲染后旧 Selection 已过期。

你的编辑器自动化卡在哪一步？评论区对个暗号。
