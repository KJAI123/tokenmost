# SESSION_STATE — 断点状态文件（断线重连后必读）

> 最后更新：2026-10-27 23:35（主会话 v2.2.3+ 公众号扩张轮）
> 用途：本会话断线后，监督任务/新会话读本文件即可无缝续命。

## 项目现状
- tokenmost.com 生产运行（香港服务器 HTTPS + GitHub Pages 镜像），deals.json 共 175 条
- 服务器 30 分钟 cron 自动 git pull；GitHub push 即部署 Pages
- 后端 server/app.py（FastAPI+Flash 初审）systemd 常驻

## 当前任务队列
- [x] v2.7 平台主体归组+总预估可薅+展开键高亮（2026-10-28，老板指令）：tools/groups.json 归组映射（智谱/讯飞/字节/Kimi/阿里云/Google/GitHub/Qoder/腾讯/百度/xAI/SCNet/Cursor/Anthropic 等异名归户，178 条全标 group），聚合键=group 同家信源一户；主行收益=总预估（一次性+日均×30 首月口径）DS等效大字；展开键 accent 绿高亮带条数；v2.7.1 单条组重复渲染修复+v2.7.2 模板反引号崩溃修复（教训：改模板字符串必须浏览器实测+本地语法核验）；线上验证 17 组聚合+19 单行零重复
- [x] v2.6.2 内部信源下架（2026-10-28，老板指令）：神秘喵星人/smzdm/微信关注清单 3 条 intel_source 归档+前端排除——信源只进数据层永不上站；监督任务提速每 15 分钟一轮（增量快跑，无数据 2 分钟内结束）
- [x] v2.6.1 过期清洗（2026-10-28，老板指令）：物理删除 3 条 expired（hunyuan-lite/github-models/together-free）+ anthropic-credits 存疑归档；监督任务每轮自动清洗（expired 即删、stale 不挂主板块）——总库 178 条（0765280）（做完一个划掉一个）
- [x] v2.5（2026-10-28，b71ed1c，老板指令全部落地）：①官方平台每家聚合一条——同 provider 合成主行（收益=一次性+日均 DS等效加总），明细 📎 可展开（数据无损），55 家聚合/15 组可展开，浏览器实测通过；②收益列「一次性+日均」算清；③白嫖总账重构：①注册 ②邀请 ③持续日入（日均折月）④学生，合计=首月口径（一次性+日入×30）；④tokenmost.com 服务器已手动同步（老板报"没同步"=cron 未到点，已 SSH git pull 180 条验证）
- [x] v2.4 等效标准 + v2.4.1 rebase 误伤重建（180 条线上验证）
- [x] v2.3.1 日均预估环节（9 条频次型量化）
- [ ] 待办线索：Command Code（$11/月→$100→$80，单源 X 待核，留 notes）；看广告白嫖 token（单源平台名不详，不入主板块）
- [ ] 老板正在填 Excel Sheet2「待补源协作区」（Spreadsheets 面板可见其选中待补区）→ 填完回填 sources.json/harvest_sources.json
- [ ] 等效系数全量精折：当前仅体验套餐 r7 标 eq_wan=13645，其余通用额度 1:1 保守——后续逐条按模型口径精折（R9 候选任务）

## R8 主管产出合并 SOP（监督员照此执行）
1. `python3 -c "import json;d=json.load(open('data-deep/deep-r8.json'));print(len(d))"` 确认存在
2. 合并脚本：按 id 去重 append 进 deals.json（published 按 deep 里值，一般 false 待核）
3. `python3 tools/check.py` 必须通过（校验+RSS+攻略重建）
4. `git add -A && git commit -m "R8 merge" && git push`（钥匙串凭据已配）
5. 服务器侧 30 分钟内自动同步，无需手动

## 断线恢复指令（监督任务/新会话直接照做）
- 读本文件任务队列 → 从第一个未完成项继续
- 后台 agent 失败（model concurrency limit exceeded）→ 等几分钟重新 Agent 拉起，串行一次一个
- 任何写入冲突：deals.json 只有主会话/监督任务可写，主管只写 data-deep/
- ⚠️ **rebase 铁律（v2.4.1 血泪教训）**：rebase 冲突中 `--ours`=已重放的旧基、`--theirs`=自己的新提交——要保自己的新内容必须用 `--theirs`；用错会静默丢数据（v2.3 曾丢 7 条情报+9 条日均字段）。解冲突后必须核对条数与新增字段再 continue
- ⚠️ push 瞬断用 `git -c http.version=HTTP/1.1 push`；远端有 bot auto-sync 提交时先 `git pull --rebase`

## 巡检水位
- ark-daily-5m 复核结论（03:26）：原文档页 82369/1544109 已 404（浏览器实测重定向文档中心首页），无终止/迁移公告，火山 2026 年整体收紧免费资源（3 月 Coding Plan 变更公告佐证）——维持归档；恢复条件=新官方 URL 或控制台登录实锤（需老板/主管人工）
- excel_last: 助理增量已归档（2026-10-28 02:06）：千人计划达成（1245 唯一源/100 长期/采集器 60 源）+候选源池/长期源清单新 sheet；待核线索裁决（02:22）→①讯飞星辰 Qwen「不限量」已关闭：3.9 元无忧版=已避雷的 deep-xunfei-39-crash 翻车套餐（2026-05 起集体退款），163 文章为翻车前旧宣传 ②小米 MiMo 待核 ③智谱实名 2 亿待查重（疑=zhipu-signup 月上限 2 亿）
- deep 裁决: deep-r5.json 的 deep-tencent-yuanqi 已被 deep-tencent-yuanqi-verified-r6（口径修正版）取代，永不合并防重复

## 汇总水位
digest_last: 2026-10-28T04:06:49+08:00（小时汇总#3 已发）

## 合规红线（永不违反）
多号/批量/接码/代充/共享号/破解/漏洞永不收录；申请制/企业向营销话术不得当普通羊毛上架；CREDENTIALS.md/.env/zhipu.key 不入库不外传。
