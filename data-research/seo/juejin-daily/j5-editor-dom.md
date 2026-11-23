# contenteditable 富文本编辑器自动化：Draft.js 与 ProseMirror 的差异实战

<!--
目标平台：掘金（文章，技术教程体）
发布日建议：2026-11-26（周四）晚 20:00-22:00 掘金晚间流量峰
结构说明（人味化后）：迁移翻车开场 → 三场景按实战顺序讲（React setter 法 / iframe 正文 / byte-select）→ 差异速查表 → 互动
素材纪律：纯干货零植入 v4；写作与核实日期 2026-11-20；人味化：2026-11-23；无链接、无任何植入
-->

前阵子我把自动化脚本从一个 ProseMirror 站点迁到 Draft.js 站点，本以为改改选择器就能跑，结果一套打法整个作废。同样是 contenteditable，换个编辑器框架，自动化就得推倒重写。这篇按三个实战场景拆开讲，省得你们再踩一遍我踩过的。

### 场景一：Draft.js，主体靠事件注入

Draft.js 是受控组件，真相源在 editorState，DOM 只是 React 的渲染投影：直接改 contenteditable 会被下一次 render 冲掉，合成的 input 事件也经常被静默忽略。病根跟 ProseMirror 差不多，但药方不一样。

落地分两路。编辑器主体走事件注入：聚焦后派发 paste 或 beforeinput，让 Draft.js 自己的处理器接管，文本才会真正进 editorState。同页那些隐藏的 input、textarea（标题栏、标签输入框这类）走 React setter 法：从原型上拿原生 value setter 赋值，再派发 bubbles 为 true 的 input 事件，React 的委托层才会收到 onChange。

```js
const setter = Object.getOwnPropertyDescriptor(
  window.HTMLTextAreaElement.prototype, 'value'
).set;
setter.call(el, '新标题');
el.dispatchEvent(new Event('input', { bubbles: true }));
```

### 场景二：ProseMirror，以及藏在 iframe 里的正文

ProseMirror 自持文档状态，DOM 会被它按 schema 归一化——塞进去不合规的节点，下一帧就被改写得面目全非。所以断言结果永远看导出内容，别看 DOM。

更阴的是另一个坑，我在上面耗了小半天：不少论坛和邮件编辑器把正文塞进 iframe，我在主文档里 querySelector 了半天，永远返回 null，一开始还以为是选择器写错了。得切进 contentDocument 找编辑区，事件也必须派发给 iframe 内部——跨文档的事件不会自己穿越文档边界。

```js
const inner = frameEl.contentDocument;
const editorEl = inner.querySelector('[contenteditable="true"]');
editorEl.focus();
```

### 场景三：byte-select 标签组件，让组件自己插

@提及、话题标签这类 byte-select 风格的组件，你对它 insertText，它只会回你一个光秃秃的纯文本 @，带数据的提及节点压根生成不了。正确顺序是：键入触发字符，轮询等下拉渲染完，再模拟点击候选项——让组件走自己的插入逻辑，节点才合法。等待用轮询加超时兜底，别死等固定毫秒，机器一卡就翻车。

### 差异速查

| 维度 | Draft.js | ProseMirror |
| --- | --- | --- |
| 真相源 | React editorState | 自持 state |
| 改 DOM 的下场 | 下次 render 冲掉 | 按 schema 归一化 |
| 稳妥路线 | paste / beforeinput 注入 | trusted 输入或事务 dispatch |

两种编辑器，共同点其实就一条：别把它当普通 div 改。你现在对付的是哪种？评论区报个框架名，我把对应的路线展开写。
