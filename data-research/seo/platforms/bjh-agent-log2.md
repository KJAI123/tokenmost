
## 2026-11-19 第二轮：发布成功
- 标签：2601B47FD26F338EF846E0D734243FAB（4 个 edit 标签共享同一草稿，取第一个）
- 验证：标题 div 命中、正文 iframe 507 字均在
- 封面：智能封面未走成（弹窗默认 tab=本地上传），直接 CDP DOM.setFileInputFiles(objectId=accept:image/* 的 input) 上传 bjh-free-token.jpg → 预览出现（本地上传(1)）→ 点「确定 (1)」(1180,697) → 弹窗关闭、编辑器出现 198x148 封面预览（picproxy 图）
- 发布：点 (916,776) 的「发布」button → 无确认弹窗 → URL 跳转 /builder/rc/clue?...firstPublish=und（发布成功落地页）
- 验证截图：/tmp/bjh2-published.png

## 11-21（11-20 执行）第 1 篇：学生 5 项权益（b2-student-pack）发布成功
- 环境：9223 无头重启过 → 首进编辑器跳登录页 → CDP Storage.getCookies 从 9222 只读迁 39 条 baidu.com cookie（BDUSS/STOKEN 在）→ setCookies 后登录态恢复
- 标题：contenteditable div（558 宽 y=187）focus → insertText，「学生党必领的 5 项 AI 权益清单（附核实日期）」
- 正文：ueditor_0 iframe body.innerHTML（<p>/<b>，### 转 <b>）+ input 事件 + UE fire contentchange；回读 689 字 / 6 个加粗小标题均在
- 封面新坑（FeEditorApp 新 UI）：
  1. setFileInputFiles 后立刻点「确定」→ toast「封面裁剪处理中，请稍后再点击确定」，封面未落位（弹窗关、占位还在）
  2. 重试轮检测误报：body.innerText 里残留隐藏 toast 文本致「裁剪中」恒真 + 宽松正则把裁剪框内元素误判为确定钮（532,448）；实际图已进裁剪器、4:3 预览已出
  3. 正解：等裁剪预览渲染后，DOM 精确 BUTTON textContent=「确定 (1)」(1145,672) 点击 → picproxy 198x148 预览、占位消失
  4. 副作用：多次 setFileInputFiles 使弹窗内同图缩略图堆到 4 张，选中 1 张不影响发布
- 发布：滚顶核对标题 → 点 (880,726)「发布」→ 无确认弹窗 → URL /builder/rc/clue?...firstPublish=undefined + toast「文章发布成功」+ 页面「提交成功，正在审核中...」
- 备注：底部「字数 0 已保存」计数器不认 innerHTML 注入，但不影响发布校验；验证截图 /tmp/bjh_pub/published.png

## 11-22：办公场景 AI 免费用法三例（b3-office-ai）发布成功
- 环境：9223 登录态直接有效（BDUSS 昨日迁移后仍存活），无标签时 Tab.connect(new_url) 开编辑器即进，未跳登录页、未迁 cookie
- 标题：contenteditable div（558 宽 y=206）focus → insertText 一次成功，回读「办公场景 AI 免费用法：会议纪要、周报、邮件三例」
- 正文：ueditor iframe body.innerHTML（10 <p> / 4 <b>，### 转 <b>）+ input/change + UE contentchange；回读 511 字、4 个加粗小标题均在
- 封面（沿用 11-21 正解路线，一次走通）：
  1. 坑：首试点「选择封面」容器中心 y=1128 在视口外点击落空（页面未滚动）；改 scrollIntoView({block:'center'}) 后取新坐标 (379,392) 再点，弹窗正常开
  2. 弹窗内 button 空列表是常态（「确定(1)」渲染在后），setFileInputFiles(nodeId 路线，accept=image/* 的 input) → 等 4s 裁剪预览渲染 → DOM 精确 BUTTON「确定 (1)」(1145,672) → 弹窗关、picproxy 198x148 预览落位，未撞「裁剪处理中」toast
- 发布：滚顶核对标题 → DOM「发布」(880,726) → 无确认弹窗 → URL /builder/rc/clue?...firstPublish=undefined + toast「文章发布成功」+ 页面「提交成功，正在审核中...」
- 备注：右侧满意度调研弹窗未关不挡操作；验证截图 /tmp/bjh4-published.png（封面弹窗过程 /tmp/bjh4-crop1.png、落位 /tmp/bjh4-cover-done.png）

## 11-23：免费可商用素材站三类盘点（b4-material-sites）发布成功
- 环境：9223 登录态直接有效（连着第三天无需迁 cookie），Tab.connect(new_url) 开编辑器即进
- 标题新坑（FeEditorApp 受控组件）：标题 contenteditable div 是状态托管的——
  1. `tab.ev` 回读带 JSON.stringify 引号包裹，拿它直接 `== TITLE` 比较必失败 → 误判成功并重复 insertText，标题堆出 4 份拼接串；正确姿势是先 json.loads 再比
  2. DOM 级清空（focus+selectNodeContents+execCommand('delete')）会被框架按旧状态回滚，清不掉；唯一可行 = 真实键盘事件：dispatchKeyEvent commands:["selectAll"] + Backspace(8)，一轮即空
  3. 清空后焦点常掉进正文 IFRAME（activeElement=IFRAME），此时 insertText 会把标题文本打进正文第 1 段（今天 23 字标题污染了首段、凭空多 1 个 <p>）——type_text 前必须 click 标题框并核对 activeElement 是 DIV/contenteditable
  4. 正文污染修复：ueditor body.innerHTML 整体重注（该路径注入内容过审核、编辑器自动保存不回滚），首段恢复干净
- 正文：ueditor_0 iframe body.innerHTML（10 <p>/4 <b>，### 转 <b>）+ input/change；回读 620 字、4 个加粗小标题（图片类/图标类/字体类/存证习惯）均在，无残留标题串
- 封面（正解路线一次走通）：「选择封面」scrollIntoView({block:'center'}) → (309,368) 点开弹窗 → setFileInputFiles(objectId 路线，accept=image/* input，objectId=8666089361546901382.7.1) 上传 generic-ai-tools.jpg → 等 4s → 精确 BUTTON「确定 (1)」(1074,660) → 弹窗关、picproxy 198x148 落位，未撞「裁剪处理中」
- 发布：滚顶三查（标题/封面/正文 10p4b）→ DOM「发布」(810,701) → 无确认弹窗 → URL /builder/rc/clue?...firstPublish=und + 页面「提交成功，正在审核中...」
- 验证截图 /tmp/bjh5-published.png（标题 /tmp/bjh5-title.png、封面落位 /tmp/bjh5-cover-done.png、正文 /tmp/bjh5-body-clean.png）
