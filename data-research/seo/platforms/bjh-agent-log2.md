
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
