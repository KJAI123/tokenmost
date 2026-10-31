# tokenmost 网页设计优化方案 v3

> 产出方：MiniMax Code（MCode）｜日期：2026-10-31
> 面向：zcode 主会话（`session_8e2059382547d95228b3f16fd5aaa048`「接管tokenmost店铺会话内容与任务」）
> 状态：**产物已就绪，`index.html` 未改动、未提交 git**（避让主会话单写入方纪律）

---

## 一、结论先行

tokenmost 的设计系统本身是干净的（4px 间距基数 / 1.25 字阶 / 单主色 emerald + 语义色），
问题不在审美，而在**三个结构性 bug 吃掉了大半体验**。修掉这三处，
收益远大于任何配色、圆角、字号的调整。

| 硬伤 | 严重度 | 实测值（改版前） | 实测值（改版后） |
|---|---|---|---|
| 移动端整页横向滚动 | P0 | `scrollWidth = 1120`（视口 390） | `scrollWidth = 390` ✓ |
| 表头与数据列整体错位 | P0 | Δ 109px | Δ 0px ✓ |
| 免费模型目录常驻渲染 | P1 | 单行 400px（手机 1000px+） | 单行 ~90px（−91%） |

连带效果：手机首屏可见平台数 **1.5 → 6+**。

---

## 二、实测方法（可复现）

macOS 上 Chrome headless 的窗口宽最小被钳到 500px，直接 `--window-size=390` 截图会得到
**500px 渲染后裁到 390 的假图**（这会掩盖溢出问题，也容易误判成溢出）。

本次采用的做法：

1. 起本地静态服务：`cd tokenmost && python3 -m http.server 8931`
2. 用 `measure.html` 套一层 **width 精确指定的 iframe**，iframe 内部才是真实 390px 视口
3. 在 iframe 文档内读 `documentElement.scrollWidth` 与 `getBoundingClientRect()`，跨文档通信用 `@@...@@` 标记
4. 截图走 `shot.html`（iframe 居中）再 `sips -c 1600 390` 居中裁切，得到真 390px 图

> ⚠️ 这条经验建议沉淀进 `SESSION_STATE.md`：**CSS 事故 JSC 语法门抓不到，截图必须确认视口宽度真实值**，
> 否则会把「裁切假象」当成「布局溢出」。

---

## 三、三个硬伤的根因与修复

### P0-1 移动端整页横向滚动

**根因链**：`≤640px` 时 `.tabs` 含 12 个不可断行按钮 → min-content 宽 1108px；
作为 flex item 未重置 `min-width` → 撑大 `.toolbar`；
`.toolbar > span` 的 `margin-left:auto` 在 **column** 容器里是 cross-axis 外边距，把筛选区推到最右 →
`scrollWidth = 1120`。

```css
@media(max-width:640px){
  .tabs{min-width:0;max-width:100%;width:100%;overflow-x:auto}
  .toolbar>span{margin-left:0!important;min-width:0;width:100%}
  #search{width:100%;min-width:0;flex:1 1 140px}
}
```

### P0-2 表头与数据列错位 109px

**根因**：`.lhead` 与 `.row` 都用 `96px minmax(0,1fr) 116px max-content`，
但第 4 列是 `max-content`——表头里是「操作」（24px），数据行里是按钮组（133px）。
中间的 `1fr` 吸收 109px 差值，把第 3、4 列整体右推。

```css
:root{--cols:96px minmax(0,1fr) 116px 156px}
.lhead,.row,.skel{grid-template-columns:var(--cols)}
```

注意 `.skel`（骨架屏）也要一起改，否则加载态同样错位。

### P1 免费模型目录常驻渲染

`.fm-wrap` 由常驻 `<div>` 改为 `<details class="fm-wrap fm-fold">` + `<summary>`，默认收起。

---

## 四、v3 主动升级（6 项）

| # | 改动 | 价值 |
|---|---|---|
| 1 | **收益条形图**（`tokSort/MAXTOK` 比例） | 「哪个最薅」从读数字变成扫读 |
| 2 | **CTA 三级分级**（≥1亿 实心 / ≥1000万 描边 / 其余 幽灵） | 87 个同质按钮 → 3–5 个焦点 |
| 3 | **模型目录默认折叠** | 手机首屏平台数 1.5 → 6+ |
| 4 | **详情展开面板**（完整 value/rule/notes/口径/截止/核验时间/官方入口） | 解决 749px 中栏被 ellipsis 截断；手机上不用靠 hover |
| 5 | **暗色模式**（`prefers-color-scheme` + 手动开关 + localStorage） | 仅改 CSS 变量，组件层零改动 |
| 6 | **顶部入群条降噪** | 黄金位让给「349 亿总账」，转化路径不删 |

外加顺手修的**文案 bug**：原 catch 块无论何种失败都提示「file:// 协议无法 fetch」，
HTTPS 线上真故障时会把排查方向带偏。改版区分本地预览 / 网络异常，并给「重试」按钮。

---

## 五、交付物清单

```
design/
├── DESIGN-PLAN.md      ← 本文件
├── proposal.html       ← 可视化方案页（前后对比 + 示意图）
├── index-v3.html       ← 改版后完整页面（相对原版 +8.9KB，12 处精确替换）
├── patch-v3.css        ← 纯 CSS 补丁（只修 P0，低风险，可直接追加进主 <style>）
├── demo/               ← ★ 离线交互 Demo（双击 design/demo/index.html 即开，无需起服务）
│   ├── index.html      ←   启动器：现状 v1 / 改版 v3 / 并排对比 三态切换
│   ├── v1.html         ←   改版前页面（数据已内嵌）
│   ├── v3.html         ←   改版后页面（数据已内嵌）
│   └── data.js         ←   数据快照（绕开 file:// 无法 fetch 的限制）
└── shots/
    ├── before-1440.png  before-390.png
    └── after-1440.png   after-390.png
```

**Demo 说明**：`design/demo/index.html` 双击即可打开（推荐 Chrome）。数据以快照形式内嵌在
`data.js`，绕开 `file://` 协议无法 fetch 的限制；顶栏可切「现状 / 改版 / 并排」，
视口可切「自适应 / 平板 768 / 手机 390」。手机 390 视口下能直接看到改版前的整页横向滚动
（tab 行右侧被截断）与改版后的零溢出。URL 支持 `#split` / `#phone` 直达。

**两种合并方式**，按风险偏好选：

- **A 保守（推荐先做）**：只把 `patch-v3.css` 追加到 `index.html` 主 `<style>` 块尾部
  → 单独就修掉 P0-1 / P0-2，改动 < 30 行，回归面最小。
- **B 完整**：用 `index-v3.html` 整体替换，或把 12 处替换逐段摘进现有 `index.html`。

---

## 六、验收清单（沿用 zcode 既有纪律）

- [ ] **360 / 390 / 430 / 768 / 1440 五档截图实测**（CSS 改动 JSC 语法门抓不到，只能截图）
- [ ] 桌面端：表头「核验」「操作」与数据列**像素级对齐**（Δ=0）
- [ ] 手机端：`scrollWidth === innerWidth`，无横向滚动
- [ ] 手机端：首屏可见平台数 ≥ 6
- [ ] 深浅两套主题各截一次，层级与对比度正常
- [ ] 目录折叠：展开/收起正常，`open` 态 arrow 旋转
- [ ] 详情面板：字段完整，`<dl>` 布局不破
- [ ] 桌面零回归：旧有 12 个 tab、聚合展开、比价面板、账号库抽屉全部照常
- [ ] 数据加载失败路径：断网时看到真实原因 + 重试按钮

---

## 七、已知取舍 / 未做项

1. 手机端「折扣链接」按钮在 78px 操作列里仍会折成两行——次要问题，本轮未处理。
2. 收益条形图用 `tokSort`（含美元/人民币折算）做比例，与「收益」排序键一致，不会出现排序与条长打架。
3. 未做暗色下的 `<img>`/海报类资源适配（当前仅微信群海报，无实际影响）。
4. **未改动 `index.html`、未提交 git**，避让 zcode 主会话单写入方纪律；请主会话确认后再合并。

---

## 八、给主会话的一句话

> 先把 `design/patch-v3.css` 追加进主 `<style>` 尾部并跑五档截图；
> 这一步零风险、直接消灭「手机整页横向滚动」和「表头错位 109px」两个 P0。
> 确认无回归后，再决定是否整体切到 `design/index-v3.html` 吃下四项体验升级。
