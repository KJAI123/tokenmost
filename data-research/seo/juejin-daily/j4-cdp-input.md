# CDP 自动化输入的三条管线：insertText / dispatchKeyEvent / setFileInputFiles 实测对比

<!--
目标平台：掘金（文章，技术深潜体）
发布日建议：2026-11-24（周二）晚 20:00-22:00 掘金晚间流量峰
结构说明：2 句钩子 → 三条管线各一节（快输 / 逐键 / 文件上传）→ 坑清单 → 互动；代码块完整
素材纪律：纯干货零植入 v4；写作与核实日期 2026-11-20；无链接、无任何植入
-->

「让浏览器替你打字」从来不是发一条命令那么简单。同一个输入动作在 CDP 里有三条管线，选错一条，轻则换行失效，重则文件根本传不上去——这篇按实测结果把三条线讲透。

### 管线一：Input.insertText，粘贴式快输

走 trusted 输入，beforeinput 管线完整触发，整段文本一次到位，速度最快。前提只有一个：目标元素已聚焦。

最大的坑就在这条线上：`\n` 塞进去不换行。insertText 把它当普通字符处理，多数编辑器里表现为段内空白或直接被吞。换行必须拆出来，用按键事件补一枪回车：

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

完整走 keydown、keypress、keyup 链路，凡依赖物理按键的逻辑——快捷键、回车提交、联想补全——只能走这条。代价是自己把字符串拆成单键逐个发，速度慢，修饰键状态要自己维护。中文这类不经物理键盘的字符退回给 insertText，两条管线配合着用。

### 管线三：DOM.setFileInputFiles，文件上传专用

两条路线，实测结论明确：

- nodeId 路线：要先 DOM.getDocument 加 DOM.querySelector 换节点编号。页面一跳转编号就失效，shadow DOM 里直接查不到——querySelector 不穿透 shadow 边界。
- objectId 路线：Runtime.evaluate 拿到节点的 RemoteObject 直接传，少两次往返、不过期、能穿透。

```js
const { result } = await client.send('Runtime.evaluate', {
  expression: "document.querySelector('#upload')",
});
await client.send('DOM.setFileInputFiles', {
  files: ['/tmp/report.pdf'],
  objectId: result.objectId,
});
```

### 坑清单（实测汇总）

1. insertText 的 `\n` 不是回车，换行必须 dispatchKeyEvent 发 Enter。
2. 输入前没聚焦等于把字打进虚空；每次重渲染后焦点和选区都要重取。
3. nodeId 在 shadow DOM 里失效，文件上传一律走 objectId 路线。
4. dispatchKeyEvent 漏掉 text 和 windowsVirtualKeyCode 时，部分组件收不到字符。
5. 断言结果别看 DOM，读输入框的 value 或导出内容——DOM 只是投影。

以上行为均在最新稳定版 Chrome 复验，核实日期 2026-11-20。

你的输入自动化还卡在哪条管线上？评论区补充，一起把这份坑清单攒全。
