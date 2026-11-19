
## 2026-11-19 第三轮（今日第 2 篇）：发布成功
- 主题：《免费云服务器避坑指南：3 个用前必看的规则》（与上午「免费 Token 盘点」错开主题）
- 浏览器：本机 Chrome 9222（覆盖 rpa_browser.CDP_HTTP=9223 默认，仅碰 baijiahao 域标签，复用 clue 页标签导航到 edit?type=news）
- 标题 21 字：contenteditable div（FeEditorApp-editor，w=558 y=187）focus → type_text。坑：加载后立刻 insertText 会丢（focus 竞态，第一次落空），重试 click+insertText 落字成功
- 正文：iframe#ueditor_0 body.innerHTML 结构化 HTML（8 段 <p>/<b>，一/二/三小标题+加粗），dispatchEvent input；iframe 内 512 字（去空白），3 处「截至 2026-11-20 核实」+结尾互动「你在免费云上踩过什么坑？」均在。编辑器底栏「字数 0」是 innerHTML 注入后计数未刷新，不影响发布（UE model 未暴露，React FeEditorApp）
- 纯度终检：title+正文扫 tokenmost/http/www./.com/.cn/链接 = 0 命中
- 封面：generic-ai-tools.jpg。「选择封面」文字 span 点击不触发弹窗（cursor:auto 无 handler），点容器 FeEditorApp-list 中心 (622,426) 才开弹窗（tab 默认=正文/本地上传）→ DOM.enable → Runtime.evaluate 拿 input[type=file][accept=image/*]（cheetah-upload，第 2 个）objectId=4553677735619160874.17.1 → DOM.setFileInputFiles → blob 预览 + tab 变「本地上传(1)」→ 点「确定 (1)」(1180,697) → 弹窗关，编辑器出现 198px picproxy 封面
- 发布：点「发布」(916,776) → URL 跳 /builder/rc/clue?...firstPublish=undefined + toast「文章发布成功」+ 落地页「提交成功，正在审核中...」
- 截图：/tmp/bjh3-01-editor.png（标题+正文）、bjh3-02-cover-dialog.png（弹窗）、bjh3-02b-cover-preview.png（上传预览）、bjh3-03-cover-done.png（封面应用）、bjh3-04-after-publish.png（发布成功落地页）
- 失败重试：0 次（发布一次过）
