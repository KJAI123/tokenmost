# React 受控组件用 JS 改不动？原生 setter 的正确打开方式

<!--
目标平台：掘金（文章，技术教程体）
发布日建议：2026-11-22（周日）晚 19:00-21:00 周末晚高峰
结构说明（人味化后）：踩坑叙事开场 → 原理（valueTracker）→ 正确代码 + 两个细节掰开讲 → 控件变体 → 避坑 → 互动
素材纪律：通用技术知识，无时效数字；无链接、无任何植入
写作与核实日期：2026-11-20；人味化：2026-11-23
-->

上周五联调的时候，我为了绕一个表单回填的问题直接 `input.value = '新值'`，界面上明明变了，提交时 React 拿到的还是旧值，下次重渲染还把我的值改回去。盯着屏幕怀疑了好几分钟人生，后来才意识到：这不是 bug，是 React 的防护机制。绕过它有标准姿势，这篇讲清楚。

### 为什么赋值不生效

React 接管了 input 实例上的 `value` 属性描述符，内部用 valueTracker 记录当前值。你直接给实例赋值，tracker 是不知情的：React 认为什么都没发生，`onChange` 自然不触发。更绝的是，如果赋的值恰好和 tracker 里记的一致，连 DOM 都懒得变。

### 正确姿势：借原型上的原生 setter

```js
const nativeSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype,
  'value'
).set;

nativeSetter.call(inputEl, '新值');   // 绕过 React 的劫持
inputEl.dispatchEvent(new Event('input', { bubbles: true }));
```

两个细节，缺一个都不行，我都是分开踩过才总结出来的。

**必须从 `HTMLInputElement.prototype` 上拿 setter。** 实例上的那个早被 React 换掉了，原型上留着的才是浏览器原生实现。

**事件必须 `bubbles: true`。** React 的事件委托挂在容器节点上——React 17+ 挂 root，16 挂 document——不冒泡的事件压根到不了 React 手里。对了，还有个最容易栽的坑：文本框监听的是 `input` 事件，不是 `change`。

### 其他控件的变体

textarea 最简单，换个原型，其余照抄：

```js
Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
```

checkbox 和 radio 是另一套逻辑：改完 checked 派发的是 click 事件，别搞混。

```js
const checkedSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'checked'
).set;
checkedSetter.call(checkboxEl, true);
checkboxEl.dispatchEvent(new Event('click', { bubbles: true }));
```

原生 select 反而最省心，改完值派发 change 就完事，onChange 正常触发：

```js
selectEl.value = 'b';
selectEl.dispatchEvent(new Event('change', { bubbles: true }));
```

### 避坑

拿 `change` 代替 `input` 是我见过的最常见失败原因——React 文本框的 onChange 绑在 input 事件上，逐字检查你的事件名。不走原生 setter 直接赋值的话，事件处理器里读到的还是旧值，因为 tracker 没动，React 按旧值算。最后说句掏心窝的：这套方法用在 E2E 测试和浏览器扩展场景，业务代码请老老实实 setState，别和框架较劲，较劲没有好下场。

你自动化时还遇到过哪些「改了等于没改」的控件？评论区补充，攒个合集。
