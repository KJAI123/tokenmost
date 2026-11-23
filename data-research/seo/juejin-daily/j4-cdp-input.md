# CDP 自动化输入的三条管线：insertText / dispatchKeyEvent / setFileInputFiles 实测对比

<!--
目标平台：掘金（文章，技术深潜体）
发布日建议：2026-11-24（周二）晚 20:00-22:00 掘金晚间流量峰
结构说明（人味化后）：踩坑开场（换行卡一晚上）→ 三条管线各一节按踩坑顺序展开 → 坑清单叙事化 → 复验说明 → 互动
素材纪律：纯干货零植入 v4；写作与核实日期 2026-11-20；无链接、无任何植入
-->

「让浏览器替你打字」这件事，我原本以为发一条命令就完了。上周调一个自动填报的脚本，光一个换行就卡了我一晚上，最后翻文档才明白：同一个输入动作在 CDP 里有三条管线，选错一条，轻则换行失效，重则文件根本传不上去。按我实测的结果，把三条线讲透。

### 管线一：Input.insertText，粘贴式快输

走 trusted 输入，beforeinput 管线完整触发，整段文本一次到位，速度最快。前提就一个：目标元素已经聚焦，不然你就是把字打进虚空。

我卡了一晚上的坑就在这条线上：`\n` 塞进去不换行。insertText 把它当普通字符处理，多数编辑器里表现为段内空白，或者干脆被吞掉。换行必须拆出来，用按键事件补一枪回车：

```js
await client.send('Input.insertText', { text: '第一行' });
await client.send('Input.dispatchKeyEvent', {
  type: 'keyDown',
  key: 'Enter',
  code: 'Enter',
  windowsVirtualKeyCode: 13,
});
await client.send('Input.insertText', { text: '第二行' });
```

### 管线二：Input.dispatchKeyEvent，逐键仿真

完整走 keydown、keypress、keyup 链路，凡依赖物理按键的逻辑——快捷键、回车提交、联想补全——只能走这条，没有替代品。代价也明摆着：字符串得自己拆成单键逐个发，速度慢，修饰键状态还得自己维护。中文这类不经物理键盘的字符，退回给 insertText 处理就行，两条管线配合着用，别头铁。

### 管线三：DOM.setFileInputFiles，文件上传专用

两条路线，实测结论很明确。nodeId 老路线要先 DOM.getDocument 加 DOM.querySelector 换节点编号，页面一跳转编号就失效；shadow DOM 里更是直接查不到——querySelector 不穿透 shadow 边界。objectId 路线用 Runtime.evaluate 拿到节点的 RemoteObject 直接传，少两次往返、不过期、能穿透。吃过 nodeId 亏的，直接无脑 objectId。

```js
const { result } = await client.send('Runtime.evaluate', {
  expression: "document.querySelector('#upload')",
});
await client.send('DOM.setFileInputFiles', {
  files: ['/tmp/report.pdf'],
  objectId: result.objectId,
});
```

### 坑清单（实测攒出来的）

把血泪攒成一堆：insertText 的 `\n` 不是回车，换行必须 dispatchKeyEvent 发 Enter；输入前没聚焦等于把字打进虚空，每次重渲染后焦点和选区都要重取；nodeId 在 shadow DOM 里失效，文件上传一律走 objectId 路线；dispatchKeyEvent 漏掉 text 和 windowsVirtualKeyCode 时，部分组件收不到字符；最后一条最反直觉——断言结果别看 DOM，读输入框的 value 或导出内容，DOM 只是投影。

哦对，以上行为我 11-20 又在最新稳定版 Chrome 上复验了一遍，都还在。

你的输入自动化还卡在哪条管线上？评论区补充，一起把这份坑清单攒全。
