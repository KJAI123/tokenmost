# SESSION_STATE — 断点状态文件（断线重连后必读）

> 最后更新：2026-10-27 23:35（主会话 v2.2.3+ 公众号扩张轮）
> 用途：本会话断线后，监督任务/新会话读本文件即可无缝续命。

## 项目现状
- tokenmost.com 生产运行（香港服务器 HTTPS + GitHub Pages 镜像），deals.json 共 175 条
- 服务器 30 分钟 cron 自动 git pull；GitHub push 即部署 Pages
- 后端 server/app.py（FastAPI+Flash 初审）systemd 常驻

## 当前任务队列（做完一个划掉一个）
- [x] 读老板给的公众号文章（神秘喵星人：ClinePass 60亿羊毛）→ 已提取全部线索
- [x] 信息源 Excel 表「信息源清单-协作版.xlsx」生成（3 sheet：总表27源/老板协作区/新羊毛速报）
- [x] 公众号线索全部入流（2026-10-28，v2.3 已推版 c402246）：cline-free-tier（免费档登录即用 V4.1 Flash/K3/GLM5.3）、opencode-go-deepseek（$10/月含$80 配额，verified）、opencode-zen-free（Zen 限时免费 V4 Flash）、qoder-deepseek-free（免费调 V4.1-Flash-1017，verified）、unisound-u2flash-free（云知声限时免费）、cline-pass-deepseek 升级多源 verified——deals.json 共 180 条
- [x] R8 主管两次并发限额翻车 → 主会话亲自 WebSearch 核实入流（R8 职能已由主会话执行）
- [x] 断线恢复机制：SESSION_STATE.md + tools/resume.sh + 每30分钟 CronCreate 监督任务（automation-dd8c8009）
- [ ] 待办线索：Command Code（$11/月→$100→$80，单源 X 待核，现留 opencode 条目 notes）；看广告白嫖 token（单源公众号平台名不详，不入主板块，留 intel-miaowu notes）
- [ ] 等老板填 Excel Sheet2「待补源协作区」→ 回填 sources.json/harvest_sources.json

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

## 合规红线（永不违反）
多号/批量/接码/代充/共享号/破解/漏洞永不收录；申请制/企业向营销话术不得当普通羊毛上架；CREDENTIALS.md/.env/zhipu.key 不入库不外传。
