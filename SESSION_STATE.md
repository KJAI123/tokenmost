# SESSION_STATE — 断点状态文件（断线重连后必读）

> 最后更新：2026-10-29 17:20 UTC（主会话 v2.10.6 OpenClaw/AutoClaw 下架轮）
> 用途：本会话断线后，监督任务/新会话读本文件即可无缝续命。

## 项目现状
- tokenmost.com 生产运行（香港服务器 HTTPS + GitHub Pages 镜像），deals.json 共 204 条（published 139/verified 134）
- 服务器 30 分钟 cron 自动 git pull；GitHub push 即部署 Pages
- 后端 server/app.py（FastAPI+Flash 初审）systemd 常驻

## 当前任务队列
- [x] v2.10.6 下架 OpenClaw/AutoClaw（2026-10-29，老板截图指令「这俩去掉」）：自部署接任意 Key 类无平台方 token 羊毛属性，双条归档出主板块（published 140→138，总库 205）；推版 d6e779a
- [x] v2.10.5 收益列排序修复（2026-10-29，老板指令「token收益无法排序，推一下版」）：
  - 根因×2：①聚合模式组间排序写死收益降序、不接 sortKey——点「核验」只亮灯不动列表；②**显示与排序口径分裂**——单条组主行显示条目自身字段（云知声 720 万），排序却按组口径（daily 2 亿/天×30=60 亿），视觉上「720 万排在 31 亿前」=乱序感
  - 修复：组间 sort 接 sortKey 双键（收益=once+daily×30 降序 / 核验=verified 纯度→最新 verified_at）；tokCell 加 ov 组口径分支（首月可薅大字+一次性＋日均小字），单条组 rowHtml 透传组值
  - 实测：收益序 90.2→60.07→31.67→25.02→21.15→15→13.11→12 亿严格降序；核验序=最新验证在前（千问/小米/Comet）；双键切换可逆；JSC 语法门 PASS
  - 推版 73b1787（本轮累计 2fff086→13b9379→39e9116→73b1787 四连发）
- [x] v2.10.3/4 侧边栏整理+千问口径（2026-10-29，老板指令）：
  - 侧边栏：agent 组内同 URL 重复合并（'WorkBuddy'+'腾讯 WorkBuddy'→留后者，66→65 站）；agent 21 站排序=编程 Agent（ZCode 打头）→编排平台（扣子/元器/Dify/FastGPT/n8n）→对话助手（智谱清言）；老板看到的 MonkeyCode 在官方组=主域旧缓存（v2.10.2 已修），Pages 镜像即时生效、主域等 cron
  - 千问建条（qwen-app-5h-limit，agent 层 group=千问，老板亲测截图直核）：千问客户端「工作」模式免费试用额度有 5 小时滚动上限，到点自动恢复（实测 02:29），订阅专业会员后发「继续」续跑；具体 token 数官方未公布不虚折；总库 205 条
  - 推版 39e9116
- [x] v2.10.1/2 logo「太大且不高清」根因修复（2026-10-29，老板二轮反馈）：
  - **根因**：v2.7 renderNav 模板事故把 `#side .favi` 与 `.nav-grid .site b .favi` 两条尺寸规则切进了 `#side a.slink{...}` 花括号内成 CSS 嵌套——嵌套后代组合器（`#side a.slink #side .favi`）在 DOM 里永不匹配，**尺寸约束从未生效，图标一直原生大小裸奔**（此前两轮缩尺寸 commit 都在改死数字）
  - 修复：恢复三条顶层独立规则（slink favi 10px/底部 11px/radius 3px）；图源 s2 32/64px→icon.horse 高清主源+s2 128px 两级 onerror 兜底最终隐藏
  - sites.json 归位：腾讯 WorkBuddy/MonkeyCode/Cline 从官方层挪 agent 组——官方 CN 8 站/海外 4 站（Google AI Studio/Mistral/Cohere/Anthropic）全为基座
  - **验证方式升级**：本会话无 node→JSC（osascript JXA new AsyncFunction）做语法门+python http.server 8899+IAB 浏览器截图实测（侧边栏 10px 小图标清晰、分组计数 大模型官方 10/MAAS 11/AGENT 19/算力 7/聚合商 14/海外 5 全对）
  - 推版 2fff086；教训：CSS 事故 vm 门抓不到（语法合法但结构错）——改 CSS 也必须浏览器截图实测
- [x] v2.10.0 官方层瘦身重分类（2026-10-29，老板指令「官方模块改为大模型官方，只保留官方的大模型基座」）：
  - 66 条重分类：编程 Agent/工具 45+ 条归 agent 层（ZCode 5 条 group 保持 ZCode 独立组/豆包/腾讯元器/Trae/Qoder×4/CodeBuddy/Comate×2/CodeGeeX/MonkeyCode/WorkBuddy/横评条/Copilot×4/Cline×2/OpenCode×2/Cursor X Sub×2/Windsurf/Comet/Gemini CLI×2/Claude Code 限额+归档批 ZCode 大礼包/AutoClaw/清言/端砚/Fitten/STEPX Neo）
  - SCNet×5 → compute；Novita/Fireworks/DeepInfra/火山方舟警示/Azure/AMD → maas；天猫旗舰店 → reseller
  - 留官方=纯基座：智谱 BigModel（含 weekend-build 每日3亿/拼好模/Coding Plan 积分与体验卡）、DeepSeek×5、Kimi×6、MiniMax×4、讯飞×3、商汤、阶跃、云知声、LongCat、小米×2、Google AI Studio/学生、Mistral、Cohere、Anthropic API credits/Claude 订阅、xAI API 现状
  - 前端：tab「官方」→「大模型官方」、「海外」→「大模型官方·海外」；侧边栏 SHORT 同步；本会话无 node→语法门改用 macOS JavaScriptCore（osascript JXA new AsyncFunction 编译，PASS）
  - 分布：official_cn 32/official_global 9/agent 45/maas 30/compute 14/reseller 9（published 139）；推版 4784c19
  - 技术备忘：主板块过滤自动排除 type=warning 与 expired（避雷区专属）；PAID=type in (price_low,pricing_plan) 双区显示
- [x] v2.9.13/14 logo 缩小+TK 情报批量入流（2026-10-29，老板指令「logo都太大了，看下爬虫助理有没有新信息」）：
  - logo：侧边栏 favi 14→12px、底部导航 16→13px（6e059eb）
  - 小米 MiMo 官方页全量实锤：新客注册+实名=¥5 赠金（xiaomi-mimo-free5）、邀请双方各¥10 上限30人（xiaomi-mimo-refer）；「百万亿创造者激励计划」官方新闻页实锤收官→xiaomi-mimo-compute 改 expired；TTS 系列官网「限时免费」；V2.5 已下线现役 V2.6
  - 运营商云新组（group=运营商云）：天翼云息壤 2500 万新用户长期额度（TK 四源互证 verified）+联通云 600 万（公众号单源 unverified 上站带⚠️）
  - 海外：Perplexity Comet 浏览器全面免费（原$200/月）+邀请 $10-15 现金（comet-free）；初创额度双条 AWS Activate $200K 封顶/Google for Startups $200K+科研 $5K（均按保守下限 $1K/$2K 折算防总账虚高）
  - 「白捡900块」公众号长文=小程序壳页（2.6MB 正文空），TK 诊断静态抓取天花板→细节清单需微信人肉打开；标题级信息已由官方一手核毕
  - 推版 4dbe420；服务器 SSH 凭据本会话失效（hk-hbgsc.pem/hbgsc-deploy 双密钥×ubuntu/root 均拒），依赖 30 分钟 cron 自动同步
  - TK 巡检节奏已切 5 小时（老板令）；HANDOFF 遗留待裁决：AI 浏览器分区扩充（Dia/夸克）、移动云 Coding Plan 40元/月（付费暂缓）
- [x] ⏸️ 自动监督任务已暂停（2026-10-28 21:5x，老板指令「自动监督先暂停」）——automation-dd8c8009 已删除；恢复方式：老板说一声「恢复监督」即重建（每15分钟一轮+每小时飞书汇总全套参数存本文件历史条目）
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
- 快手/可灵线索裁决（07:52）：可灵 API 仅测试额度+商务申请制（1000 次/3 个月，难度高价值低）——关闭不入流；Kolors 试用已含在智谱体验卡条目；待核队列清空（剩 Kimi/Coze/硅基流动登录核+weekend 周五复查+MiMo 实锤，均需人工/登录）
- CSR 复核结论（06:25）：kimi-voucher/coze-free/siliconflow-signup 三条=首页着陆页无公开权益口径（静态+IAB 浏览器双路核过），需控制台登录实锤——老板方便时开一次 Kimi/Coze/硅基流动控制台即可批量恢复或清洗；维持归档
- ark-daily-5m 复核结论（03:26）：原文档页 82369/1544109 已 404（浏览器实测重定向文档中心首页），无终止/迁移公告，火山 2026 年整体收紧免费资源（3 月 Coding Plan 变更公告佐证）——维持归档；恢复条件=新官方 URL 或控制台登录实锤（需老板/主管人工）
- excel_last: 助理增量已归档（2026-10-28 02:06）：千人计划达成（1245 唯一源/100 长期/采集器 60 源）+候选源池/长期源清单新 sheet；待核线索裁决（02:22）→①讯飞星辰 Qwen「不限量」已关闭：3.9 元无忧版=已避雷的 deep-xunfei-39-crash 翻车套餐（2026-05 起集体退款），163 文章为翻车前旧宣传 ②小米 MiMo 待核 ③智谱实名 2 亿待查重（疑=zhipu-signup 月上限 2 亿）
- deep 裁决: deep-r5.json 的 deep-tencent-yuanqi 已被 deep-tencent-yuanqi-verified-r6（口径修正版）取代，永不合并防重复

## 汇总水位
digest_last: 2026-10-28T21:50:49+08:00（补发汇总#9 已发,断线13h后恢复）

## 合规红线（永不违反）
多号/批量/接码/代充/共享号/破解/漏洞永不收录；申请制/企业向营销话术不得当普通羊毛上架；CREDENTIALS.md/.env/zhipu.key 不入库不外传。
