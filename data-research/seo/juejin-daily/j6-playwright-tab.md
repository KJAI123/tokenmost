# 用 CDP 管理浏览器标签页：复用、导航、防僵尸的三个模式

<!--
目标平台：掘金（文章，技术教程体）
发布日建议：2026-11-28（周六）晚 20:00-22:00 周末晚高峰
结构说明：钩子 → 三模式（复用 / 导航 / 防僵尸）各带代码块 → 检查表 → 互动；Markdown 全语法
素材纪律：纯干货零植入 v4；写作与核实日期 2026-11-20；无链接、无任何植入
-->

标签页管理是自动化脚本的寿命线：开多了内存爆掉，关错了页面丢失，长时间挂机还会连坐拖垮整批任务。三个模式覆盖从复用到善后的完整生命周期。

### 模式一：复用，先查再开

开新页之前先 Target.getTargets 列出全部 target，按 type 和 url 特征匹配，命中就直接 attachToTarget（flatten 设 true）拿 sessionId，不再新建。多数脚本的标签页爆炸，都是少了这一步。

```js
const { targetInfos } = await send('Target.getTargets');
const hit = targetInfos.find(
  (t) => t.type === 'page' && t.url.includes('/dashboard')
);
if (hit) {
  const { sessionId } = await send('Target.attachToTarget', {
    targetId: hit.targetId, flatten: true,
  });
}
```

### 模式二：导航，事件对齐

Page.navigate 发出去就 sleep 是最常见的反模式。正确做法：先 Page.enable 打开事件通道，navigate 之后等 Page.loadEventFired；SPA 还要再确认路由就绪——轮询 Runtime.evaluate 直到关键节点出现，加超时兜底。

```js
await send('Page.enable');
await send('Page.navigate', { url: targetUrl });
await waitEvent(session, 'Page.loadEventFired', 15000);
await waitForSelector(session, '.main-list'); // SPA 再等关键节点
```

### 模式三：防僵尸，对账加兜底

僵尸页三个来源：脚本崩了没关、用户手动新开、页面自己跳走。对策四条：

1. 用完即 Target.closeTarget，随手关是纪律不是优化。
2. 定时 getTargets 对账，不在白名单里的页直接回收。
3. 监听 Target.targetDestroyed，被外部关闭时清掉本地 session 缓存，防止往死连接发消息把整条管线卡住。
4. 进程级兜底：外层 watchdog 定期检查浏览器进程和页数，超限整体重启。

### 发车前的检查表

- attach 之前校验 targetType 了吗？page 和 iframe 不是一回事。
- sessionId 过期有处理吗？连接断开要重连重建，别复用旧句柄。
- 关页用的 closeTarget 还是直接杀进程？前者留余地，后者是核弹。

三个模式搭起来，脚本才敢长期挂机。你的标签页现在攒了几个没关的？对完账评论区报个数。
