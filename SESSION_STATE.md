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
- [x] Cline Pass + 神秘喵星人公众号 2 条入 deals.json
- [ ] R8 主管：OpenCode 深挖 + 国外羊毛全景 + 公众号线索核实（U2 Flash/看广告白嫖/Qoder）→ 产出 data-deep/deep-r8.json（上次并发限额翻车，已重拉）
- [ ] deep-r8.json 合并入 deals.json（按 id 去重）→ tools/check.py → git push 推版
- [ ] 等老板填 Excel Sheet2「待补源协作区」→ 回填 sources.json/harvest_sources.json
- [ ] Excel 打开给老板审阅（spreadsheets 面板）

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
