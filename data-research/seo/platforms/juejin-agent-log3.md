# 掘金发布智能体 第三轮日志（2026-11-19 下午）

## 结果：沸点 + 文章双双发布成功

| 任务 | 结果 | 证据 |
|---|---|---|
| 首条沸点（+5000 矿石） | 成功 | toast「发布沸点成功」；个人主页沸点流可见（"刚刚"）；系统通知「你的沸点已被推荐至沸点首页」 |
| 第 2 篇文章 | 成功 | URL 变 **https://juejin.cn/published**，页面显示「发布成功！」；正式链接 /post/7709680714967466047 |
| 矿石余额 | 10000 → **15001** | 福利中心「矿石余额：15001」（首条沸点 +5000 到账；第 2 篇文章无矿石奖励，+10000 为首篇一次性） |

## 任务 A：首条沸点

- 内容（104 字，纯干货零植入）：`#每天一个知识点#`（真实话题 chip，非纯文本）+ console.table 调试 tip + JSON.stringify(v, null, 2) 附注
- 路径：juejin.cn/pins/recommended → 点 rich-editor → 输入 `#` 触发话题选择器 → 点「话题」tab → 搜索框输入「每天一个知识点」→ 点选 `#每天一个知识点#` 项 → 光标 JS 折叠到末尾、删掉触发残留 `#` → insertText 正文 → 点「发布」(1050,317)
- 验证：juejin.cn/user/3401269753690923/pins 出现沸点（含话题 chip）；截图 shots/jj3-pin-on-profile.png
- 附加：系统通知确认沸点被推荐至沸点首页（话题标签的流量加持生效）

## 任务 B：第 2 篇文章《记一次 JSON 深坑：stringify 顺序不确定性导致的缓存错配》

- 草稿 7709530253715095571，CodeMirror 内容 1199 字（正文约 600 字 + 完整代码块），标题 35 字，4 个 `##` 小节 + 4 个 ``` 围栏齐全
- 发布设置：分类「后端」；标签 Python / JavaScript / 后端（3 个全挂上）；封面 generic-ai-tools.jpg 经 DOM.setFileInputFiles 上传（CDN 预览 p0-xtjj-private.juejin.cn）；摘要预填 100/100
- 发布：点「确定并发布」→ 7 秒后 URL 变 /published → 站内搜索拿到正式 id → 打开 /post/7709680714967466047 确认标题/正文/tag 栏三项全对（相关文章侧栏的前端/面试是推荐不是我的标签）
- 截图：shots/jj3-article-published.png、jj3-article-final.png、jj3-welfare-15001.png

## 踩坑与解法（本轮新经验，重要）

1. **byte-select 标签组件的 disabled 死局**：此前轮次的标签提交把组件状态写坏后，草稿会把这个脏状态持久化到服务端——重开弹窗后所有下拉选项恒为 `--disabled`（连没选过的 React.js 也 disabled），`el-ui` 的 `selected` 镜像数组出现 `[null,null]`。绕过方式：**直接改数据不用 UI**——从下拉 option 组件的 `$props.value` 收集三个 tag 对象，然后 `vm.$props.value.splice(0, len, py, js, hd)`（引用共享、Vue 响应式生效），同步 `$data.selected`，父级 `v-model` 立即正确。发布请求带上了全部 3 个标签，验证成功。
2. **byte-select 的镜像 span 陷阱**：`.byte-select__input` 类名同时挂在真实 `<input>` 和一个隐藏的测量 `<span>` 上；焦点不在 input 时 `Input.insertText` 会打进 span（value 不变、下拉不出）。修复：JS `querySelector('input.byte-select__input').focus()` 后再 insertText。
3. **沸点话题 chip 流程**：`#` 触发的是侧挂选择器（不是内联联想）；选完话题后编辑器会残留触发用的 `#`，需 JS Range collapse 到末尾 + Backspace 清理；`End` 键定位无效，必须用 `window.getSelection` + Range。
4. **封面**：本轮 `input[type=file]` 两个（nodeId 53/58）都设置后生效（与 log2「只第一个无 class 的生效」不完全一致，多设无害）。
5. **article query_list API 返回空**（即便不带 status）；拿文章 id 走站内搜索 API（search_api/v1/search）最可靠。
6. 沸点页会自动跳转签到福利页（本日已签到，无额外矿石）。
7. Chrome 9222 复用纪律执行：全程只导航了 3 个既有 juejin 标签（notification、editor、pins 侧的一个），未碰其他平台标签。

## 矿石/收益台账

- 首篇文章（第二轮）：+10000（已入账）
- **本轮：首条沸点 +5000（已入账，余额 15001）**
- 第 2 篇文章：无矿石（首篇奖励为一次性）；沸点被推荐至首页属流量收益，不计矿石
