# 掘金发布智能体 第二轮日志（2026-11-19）

## 结果：发布成功

- 草稿：7709326059737989161《30 行 Python 把任意 JSON 转成 Markdown 表格（附完整脚本）》
- 发布验证：点「确定并发布」后 URL 由 /editor/drafts/7709326059737989161 → **https://juejin.cn/published**，页面显示「发布成功！恭喜达成首次发布文章任务！获得矿石10000！」
- 文章链接 /post/{id}：未取到（/editor_api 与 /interact_api 相关端点在页内 fetch 均返回 HTML，需带特定 Referer 或走别的端点；后续可从创作者中心或搜索拿）

## 执行过程

1. 打开草稿页，CodeMirror getValue = 1764 字，标题 42 字，内容完好。
2. DOM 定位顶栏「发布」按钮 (1358,32)，点击后发布设置弹窗打开。可见按钮：上传封面 / 取消 / 确定并发布。
3. 弹窗内状态：
   - 分类「后端」已选中（蓝色高亮，截图 /tmp/jj2-dlg.png）
   - 摘要已预填 100/100
   - **标签为空**（之前情报说 Python 已带上——实测发布弹窗里标签不随草稿保存，需每次现选）
   - 封面为空
4. 封面上传：
   - 点击弹窗内「上传封面」(1063,400)
   - CDP：DOM.enable → DOM.getDocument(depth:1) → querySelector `input.file-input`（nodeId 38）→ DOM.setFileInputFiles（juejin-json2md.jpg）
   - 第一次设置 `.file-input` 未生效；对 `input[type=file]`（第一个，无 class）设置后生效，封面预览出现（p0-xtjj-private.juejin.cn CDN 图）
5. 标签添加（byte-select 组件，Input.insertText 可用、dispatchKeyEvent 逐字符无效）：
   - 点击第一个 `.byte-select` 容器 → 焦点落在 `input.byte-select__input` → `Input.insertText('Python')` → 下拉出现 Python/IPython/bpython → 点击 Python (1134,361) → 标签选中，「你还能添加 0 个标签」
6. 点「确定并发布」(1355,772，scrollIntoView 后当轮取坐标)，3 秒后 URL 变 /published = 成功。本轮一次成功，无需 Tab 导航兜底。

## 经验沉淀

- 发布弹窗的标签/分类/封面/摘要都不持久：标签必须每次在弹窗内重选（必填，红星）。
- 标签输入：byte-select 用 `Input.insertText`；`dispatchKeyEvent` 不触发其受控输入。
- 封面 file input：生效的是第一个 `input[type=file]`（无 class），不是 `.file-input`。
- 「确定并发布」在弹窗开时 DOM 可见可定位，坐标点击可靠；之前第一轮失败大概率是标签必填缺失导致校验拦截。
