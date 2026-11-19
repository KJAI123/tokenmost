# React 受控组件用 JS 改不动？原生 setter 的正确打开方式

<!--
目标平台：掘金（文章，技术教程体）
发布日建议：2026-11-22（周日）晚 19:00-21:00 周末晚高峰
结构说明：钩子 → 原理（valueTracker）→ 正确代码 + 两个细节 → 控件变体 → 避坑 → 互动；代码块完整
素材纪律：通用技术知识，无时效数字；无链接、无任何植入
-->

`input.value = '新值'` 赋完值，界面变了，React 的 state 却纹丝不动，下一次重渲染还把你的值改回去。这不是 bug，是 React 的防护机制——绕过它有标准姿势。

### 为什么赋值不生效

React 接管了 input 实例上的 `value` 属性描述符，内部用 valueTracker 记录当前值。直接给实例赋值时：tracker 没更新，React 认为什么都没发生，`onChange` 自然不触发；如果赋的值恰好和 tracker 记录一致，连 DOM 都不会变。

### 正确姿势：借原型上的原生 setter

```js
const nativeSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype,
  'value'
).set;

nativeSetter.call(inputEl, '新值');   // 绕过 React 的劫持
inputEl.dispatchEvent(new Event('input', { bubbles: true }));
```

两个细节缺一不可：

1. **必须从 `HTMLInputElement.prototype` 上拿 setter**。实例上的已被 React 覆盖，原型上的才是浏览器原生实现。
2. **事件必须 `bubbles: true`**。React 的事件委托挂在容器节点上（React 17+ 挂 root，16 挂 document），不冒泡的事件根本到不了 React 手里。另外文本框监听的是 `input` 事件，不是 `change`。

### 其他控件的对应变体

```js
// textarea：换原型，其余同上
Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;

// checkbox / radio：改 checked 后派发 click
const checkedSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'checked'
).set;
checkedSetter.call(checkboxEl, true);
checkboxEl.dispatchEvent(new Event('click', { bubbles: true }));

// 原生 select：改值后派发 change，onChange 正常触发
selectEl.value = 'b';
selectEl.dispatchEvent(new Event('change', { bubbles: true }));
```

### 避坑

1. 用 `change` 事件代替 `input` 是最常见的失败原因——React 文本框的 onChange 绑定在 input 事件上。
2. 不走原生 setter 直接赋值，事件处理器里读到的还是旧值（tracker 没动，React 按旧值算）。
3. 这套方法适用于 E2E 测试和浏览器扩展场景；业务代码里请老老实实 setState，别和框架较劲。

你自动化时还遇到过哪些「改了等于没改」的控件？评论区补充，攒个合集。
