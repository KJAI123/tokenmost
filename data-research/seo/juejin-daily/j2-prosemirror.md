# ProseMirror 编辑器自动化踩坑记：从 insertText 到 DOM 粒度操控

<!--
目标平台：掘金（文章，技术深潜体）
发布日建议：2026-11-20（周五）晚 20:00-22:00 掘金晚间流量峰
结构说明：开头 2 句钩子（完读率优化）→ 原理一段 → 4 条路线（编号短小节）→ 顺带 Draft.js → 避坑 → 互动；小节短、代码少而准
素材纪律：通用技术知识，无时效数字；无链接、无任何植入
-->

给富文本编辑器写自动化，第一课就是：你以为你在操作 DOM，其实是编辑器在操作 DOM。`innerText = 'hello'` 改完要么没反应，要么下一秒被打回原形——这篇记录完整踩坑路线。

### 为什么不能直接改 DOM

ProseMirror 的真相源是 `state`（文档模型 + 光标选区），DOM 只是渲染结果。直接改 DOM，下次事务 dispatch 就被重渲染覆盖；合成事件 `isTrusted` 为 false，部分处理路径还会静默忽略。

### 路线一：真实输入（insertText）

CDP 的 `Input.insertText` 是真实 trusted 输入，beforeinput 管线照常走，前提是光标位置要对：

```js
const el = document.querySelector('.ProseMirror');
el.focus();
const sel = window.getSelection();
sel.selectAllChildren(el);
sel.collapseToEnd();   // 光标折叠到位，再 insertText
```

### 路线二：粘贴事件

对粘贴处理完善的编辑器，构造 `ClipboardEvent('paste')` 挂 `DataTransfer` 的 `text/plain`，大段内容一次进，且走完整解析管线。

### 路线三：拿到 view 直接 dispatch

`editor.view.dispatch(tr.insertText(...))` 最正统，但自动化场景里 view 常闭包在模块作用域拿不到——拿得到就走这条。

### 路线四：文件上传 objectId 路线

`DOM.setFileInputFiles` 两条路：老路线用 `nodeId`，得先 `DOM.getDocument` + `DOM.querySelector` 换节点，页面跳转即失效；新路线用 `objectId`，`Runtime.evaluate` 拿 `input[type=file]` 的 RemoteObject 直接传，少两次往返也不过期。

### 顺带说说 Draft.js

同坑重灾区：受控 contenteditable，字符数据存在自己的 editorState 里，`insertText` 经常无效，改走 paste 或注入 `beforeinput`。

### 避坑

1. 断言结果别看 DOM，看编辑器导出的 HTML 或 markdown——DOM 只是投影。
2. 中文、emoji 是 surrogate pair，按字符数算光标偏移会插歪。
3. 每次输入前重新取焦点和选区，重渲染后旧 Selection 已过期。

你的编辑器自动化卡在哪一步？评论区对个暗号。
