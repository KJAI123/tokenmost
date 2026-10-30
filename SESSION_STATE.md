# SESSION_STATE — 断点状态文件（断线重连后必读）

> 最后更新：2026-10-30 深夜（v2.17.0 手机端专项整修已推版）
> 用途：本会话断线后，监督任务/新会话读本文件即可无缝续命。

## 会话接管记录（2026-10-30 深夜）
- **tokenmost店铺会话（session_2d698e01）于 22:21 起被 provider 1301 内容过滤连续拦截三连（老板「改善一下/继续/咱整改吧」均未获回复）**——历史上下文已被平台标记，该会话不可再用
- 老板令新会话「接管【tokenmost店铺】会话的所有内容、任务和技能」→ 新会话已接管产品线（本文档+记忆+tokenmost/ 仓库为交接载体）；爬虫助理线（72167d）并线协议见 data-research/HANDOFF.md（单写入方已解除，双向流动）
- 接管后首夜完成：①收口店铺会话挂起的共绩算力入流（1e63e29）②爬虫线容器化产物入库（7205ec9）③v2.16.2 广告位两处落地（e99b72f）④**v2.17.0 手机端专项整修（560bf03，老板令「补充手机端版本，比例失调很严重」）**

## v2.17.0 手机端整修要点（2026-10-30，后续改移动端必读）
- **根因①（行宽失调）**：桌面 4 列 grid 的操作列是 max-content，flex 容器 max-content 测量**忽略换行把全部按钮宽度加总**（实测 ops 列 172px，中栏被压到 64px）——移动端改**固定窄操作列 80px（≤480:78px）+ 列内 flex-wrap**：领取主按钮 order:-1 + flex-basis:100% 独占第一行，小按钮组（⚡🎁☆展开）换行其下右对齐
- **根因②（横幅溢出）**：.global-banner b 1.35rem + i nowrap → 390px 放不下；移动端全宽+缩字号（b .95rem/i .62rem）+white-space:normal
- **根因③（底部遮挡）**：bottomNav fixed 无对应 padding → #main/页脚 padding-bottom:calc(72px+safe-area)
- 其余：token 列 82px+小字换行（**内联 style 的 nowrap 用样式表 !important 覆盖**——.r-tok .unit[style] 技巧）；统计条一行排布 ≤480 隐藏更新日期（.stat:nth-child(4)）；广告位移动端 40px 压扁；面板 92vh 收边距；tabs ≤640 横滚隐藏滚动条
- 实测矩阵：360/390/430/1280 四档截图+聚合展开+比价面板+页底+桌面零回归；改移动端 CSS 必须重跑这套矩阵（教训：CSS 事故 vm/JSC 门抓不到，只能截图实测）
- **等老板事项池**：①微信群二维码图（放 repo assets/wechat-group.png 即自动显示）②GSC 验证码（埋 head→提交 78 URL sitemap）③联盟链接注册（硅基流动推荐官等，见 tools/affiliate_channels.md）④TG 频道名⑤models.dev 231 家挂巡检池点头⑥广告素材（给了就填 index.html 脚本顶部 TM_ADS 配置，两位置即上）

## 项目现状
- tokenmost.com 生产运行（香港服务器 HTTPS + GitHub Pages 镜像），deals.json 共 212 条（published 145，verified 126）；sites 70 站（agent 层 22）
- 服务器 30 分钟 cron 自动 git pull；GitHub push 即部署 Pages
- 后端 server/app.py（FastAPI+Flash 初审）systemd 常驻

## 当前任务队列
- [x] WorkBuddy 国内/国际版羊毛区分（2026-10-31 凌晨，老板令「国内版和国外版不太一样你关注一下」，3ef135d）：
  - **双版本实锤**：本机 App（com.tencent.workbuddy.mac v5.9.3）asar 内双域并存（workbuddy.cn 31 处/workbuddy.ai 15 处）——与国际版 Trae 同款分轨产品
  - **国内版**（workbuddy.cn/腾讯云，group=腾讯 WorkBuddy→腾讯）：公测 5000 Credits+每日 100 积分+教师版 2000/月×12+Hy 系限免（10-31 止）；workbuddy-free 条目已标版本口径
  - **国际版**（workbuddy.ai，group=WorkBuddy 国际版独立成组，Trae 先例）双条新建：workbuddy-intl-free（Free 100 credits/月+限时每日活跃奖 30/日≈1000/月+补全 5000 次/月限免不限量+自动任务 3→99 限免+全模型限免含 Hi-4 Preview）+workbuddy-intl-pro（付费区：Pro $10 首月 $7=2000 credits+每日 50/年付 $96/Team $40 座）；官方定价页 webReader 直核（2026-09-30 build）
  - ⚠️ 风险标注：第三方称新账号免费 credits 曾因滥用临时暂停（风控期注册可能限领）；有源称国际版以香港等区域为先
  - sites.json 双站分轨（腾讯 WorkBuddy 国内版/WorkBuddy 国际版）；总库 216 条（published 151）；pSEO 67 页（+workbuddy-国际版）
- [x] 四家羊毛补全（2026-10-30 深夜，老板令「补充 trae、opencode、mimo code、nvidia nim 的羊毛信息」，099a5fb）：
  - **小米 MiMo Code 双条新建**：xiaomi-mimo-code（agent 层，MIT 开源免费/OpenCode 二开/终端直连 V2.6；⚠️内置 V2.5 初期限免已于 6 月结束勿再宣传）+ xiaomi-mimo-tokenplan（付费区，官方定价页 webReader 直核：Lite ¥39=41 亿 Credits/Standard ¥99/110 亿/Pro ¥329/380 亿/Max ¥659/820 亿，首购 88 折+包年 88 折+夜间 0 点-8 点 0.8x+TTS 限免）；plans.json 补行（credits 参考组）；agent 导航站+「小米 MiMo Code」
  - **NVIDIA NIM 复活**：论坛+搜索互证注册 1000/上限 5000 credits 口径未变——10-28 降级系 build.nvidia.com 改版误伤，stale 清除恢复 verified/published
  - **Trae 国际版重核**：2026-02-24 起 Dollar 额度制（Free $0/Pro $10 含 $20 使用额度+无限 Autocomplete+10 并发云任务；年付 Pro $80/Pro+ $200/Max $600），旧「600 次快速请求」口径作废；trae-free-tier 国际段同步；issue #2318 争议对应旧制
  - **OpenCode Zen 升级**：limited_promo→free_tier 免费池口径——免绑卡每日刷新（mimo-v2-pro-free/nemotron-3-super-free 各 100 万/日最高档，其余 20-40 万，目录动态勿写死数量）；早期 DeepSeek V4 Flash 限免已轮换出池；opencode-go-deepseek 补「协议有效至 10-31 届满复核」备注
  - 总库 214 条（published 149/verified 130）；pSEO 66 页（+nvidia-nim/trae-国际版）；浏览器实测四条渲染+付费区+Coding 比价面板全过
- [x] v2.16.2 广告位两处落地（2026-10-30，老板拍板「先不做开屏广告吧，到时候做到右上角和底部就好」+「咱整改吧」）：
  - 右上角：header 内 flex 末位 .ad-slot.ad-top（176×56 桌面 / 移动端全宽），页底：footer 上方 .ad-slot.ad-bottom（920×90 / 移动 72px）
  - **配置驱动**：脚本顶部 `TM_ADS={top:{},bottom:{}}`——素材到位填 {img,url,alt} 即渲染真实广告（自动带「广告」角标+rel="sponsored nofollow noopener" Google 合规）；空对象=优雅「广告位招租」虚线占位
  - JSC 语法门 PASS；IAB 浏览器实测：桌面头部/页底/移动端三截图 ✓、真实素材渲染路径 evaluate 实测 ✓（anchor/rel/img/角标/还原全对）
- [x] 共绩算力条目复活上架（2026-10-30，老板问「共绩云的为啥没有补充进来」；店铺会话核完未推即被 1301 杀，接管会话收口推版 1e63e29）：gongji-subsidy stale→verified，个人开发者计划 50 元体验积分（进群+填表，审核制最高 1500 元/月 200 元起持续）+MaaS 公测 1 亿 tokens 口径存疑未采信防虚高；prices.json 补共绩 DeepSeek V4 Flash 1/2 元低价行；pSEO 共绩页 64 页
- [x] v2.16.0 公众号双信源入库（2026-10-30，老板发两个 mp.weixin.qq.com 链接作信源）：
  - **抓取通道备忘：WebFetch 被微信「环境异常」验证页拦截（老边界），webReader（Z.ai 内置）两篇全量直抓成功——公众号正文首选 webReader，失败再退 TK 管线/人肉**
  - ①《每月白送5亿token，这次是国家队出手》→ 书生·端砚墨点计划 deep-intern-inkpoint **复活上架**（TK R6 曾被 JS 壳挡）：每月 10 墨点、1 墨点上限 5000 万 token；保守折 1250 万/月（缓存命中 5 亿口径不采信防虚高）；DeepSeek-V4 全系/GLM-5.3/Kimi-K2.6/MiniMax-M3 阵容；书生-S2/Agents-A1/Atria-Dawn-Preview 三款 0 墨点限免；OpenAI+Anthropic 双协议（Claude Code 直连）；微信扫码无需绑卡；⚠️ 墨点月清零；unverified 待复核
  - ②《白嫖9000积分！DeepSeek免费用》（果核）→ 商汤小浣熊 deep-sensenova-xiaohuanxiong 新建：三端各 3000 积分（网页/桌面/手机）共 9000；平台内 DeepSeek-V4.1-Flash-1017 免费；积分制不折总账（poe 先例）；agent 层+导航站第 70 站；并入商汤聚合组
  - 书生端砚自动生成 pSEO 平台页；浏览器实测双条目渲染+AGENT 22 ✓；推版 61520b2
- [x] **广告位决策备忘（老板原话「先不做开屏广告吧，到时候做到右上角和底部就好」）**：未来广告位只做两处——右上角+页底；开屏广告不做。未写任何代码，纯决策记录；实现时再找老板要广告素材
- [x] v2.15.0 折扣兑现三选一弹窗+微信群入口（2026-10-30，老板双指令）：
  - ①券领点击→「折扣兑现」面板：📋 复制折扣码（无码类隐藏）/🔗 直接跳转/📱 扫码领取（qrserver 二维码，手机直达不用传链接）——券码虚线框展示，标题带平台名
  - ②微信群弹窗：侧边栏「📥 微信交流群」+页脚「微信交流群」→ 二维码面板；**待老板把群二维码图放 repo assets/wechat-group.png 即自动显示**（面板内置 7 天过期换图说明+企业微信无限期入群码建议）
  - 浏览器实测：智谱券领弹窗（Y2H91IWSU3+三选项+扫码展开）✓、微信群待配置态 ✓；JSC PASS；推版 9b67948
  - **待老板**：①提供微信群二维码图（或企业微信无限期码）②有自己联盟链接继续发（硅基流动推荐官等，见 tools/affiliate_channels.md）
- [x] v2.14.0 官方层豆包+海外丰富+上移（2026-10-30，老板指令）：①官方 CN 组+豆包站（doubao.com，天天领额度 hot），doubao-daily-quota 条目 agent→official_cn、group 独立=豆包（与字节分开）；②海外官方 4→7 站：+OpenAI Platform/xAI Console/Meta AI（xAI 条目已有 3 条）；③tab+侧边栏组顺序：海外上移到国内正下面（官方CN→官方海外→MaaS→Agent→算力→中间商）；sites 65→69、pSEO 62 页自动重建（豆包页）；推版 8fb20c6（push 瞬断重试 OK）
- [x] v2.11.3 折扣链接渠道机制（2026-10-30，老板指令「加折扣链接渠道咋搞」）：
  - 前端：type=coupon 无 coupon 字段→金色「🔗 折扣链接」（复制链接+直达）；有码→「🎁 券领」（复制码+直达）——两条金色路径齐了
  - **tools/affiliate_channels.md 渠道手册**：A 站长联盟链接（商业化主力：硅基流动推荐官双方¥16 无上限/七牛 20% 返佣/腾讯云最高 35%/阿里云 10-35%/z.ai ic= 已入库；**需老板亲自注册拿专属链接→发会话→建条自动金色**）；B TK 管线（查询词池加 折扣码/优惠码/邀请码/兑换码——待 TK 下轮适配）；C 用户供码（已有功能零维护）
  - 合规红线：返利条目 notes 必标「含推荐属性」（zai 先例）；用户真实拿到折扣优先；不碰代充灰产
  - 推版 b6e00b6
- [x] v2.13.0 程序化 SEO 上线（2026-10-30，老板指令「看爬虫助理信息源+GitHub seo 邪修找好方案」）：
  - TK 增量已读：150 源超重型运转+TG 管线战果（4 频道收编）+DeepSeek 搜索 API 白嫖至 11 月（待核入流）+GLM-5 免费渠道汇总文+Tibo Pro 翻倍事件；11 月聚焦活动源
  - GitHub SEO 调研（4 轮搜索）：黑帽（隐身文字/门页/cloaking/关键词堆砌）=Google 拉黑风险不碰；**最优方案=合法 pSEO（模板+结构化数据批量产长尾落地页，GitHub 有 cms-programmatic-seo-demo 等范式）+llms.txt（AI 搜索引用通道）**
  - 落地：tools/build_seo.py——deals.json 按平台聚合生成 platform/ 61 页（title「XX免费额度领取攻略：N 亿 DS Flash 等效可薅」+WebPage/FAQPage 双 JSON-LD+可见 FAQ 3 问+领取卡+关联攻略内链）；check.py 挂接自动重建（数据更新→页面同步）
  - llms.txt（精选地图）+llms-full.txt（211 条全量 Markdown，ChatGPT/Perplexity 可直接引用）；sitemap 12→75 URL；pages.yml 部署补 platform/+llms*.txt
  - 中文 slug（platform/智谱-bigmodel.html）URL/canonical/sitemap 三处一致，Google 可索引
  - 抽验：deepseek/智谱/302.ai 三页 title+JSON-LD×2 ✓；JSC 语法门 PASS；推版 173d94f
  - **待办**：GSC 验证码仍等老板（埋 head→验证→提交 75 URL sitemap）；1111 临近 TK 聚焦活动源
- [x] v2.12.0 OpenCode 提供商生态调研（2026-10-29，老板指令「好好操作一下我本机的 opencode」）：
  - 挖矿路径：/Applications/OpenCode.app→~/.local/share/opencode/opencode.db（SQLite）→kv 表 models-dev:v2:catalog→**双解嵌套 JSON 得 231 家提供商全量清单**（截图那 12 家只是冰山一角）；站内比对 20+ 未收录
  - 子代理双次被 API 风控秒拦（411/530ms）→主会话亲自 7 搜索调研
  - 入流 5 条：**七牛云 Conatus 每日 1 亿 token（实名）→10 亿（充值 100 元）**=聚合平台最大方（daily_wan 10000 万）、ZenMux 注册 Gifts 可试旗舰（unverified）、Poe 每日积分 3000→300 缩水、Baseten $30 试用金（$25K 初创线）、AI/ML API startup 1000 万（单源待核）；总库 211 条 published 142
  - 排除 7 家：Chutes（免费档 2026-02-27 已死）、NanoGPT（按次付费）、Berget.AI/Charm Hyper（无免费层）、Boundless（仅企业试点）、Vercel/CF AI Gateway/Helicone（网关自带 Key）、Amazon Bedrock（云托管，AWS Activate 已覆盖）
  - **防污染案例**：搜索聚合站称 Cerebras 免费层 1M/天=旧信息，站内 deep-cerebras-free-trial 已核 2026-07 改版取消——未新建，聚合站信息不可直接采信
  - 推版 edaac01；TK 可将 models.dev 231 家清单加入巡检池（监控目录 diff）
- [x] v2.11.1 领取按钮分类+券库补货（2026-10-29，老板指令「领取分直接领取和折扣券领取，折扣要突出」）：①有 coupon 条目操作列=金色渐变「🎁 券领」（点击复制券码+直达页一步完成，a 默认跳转不被拦截），无码=绿色「领取」；聚合主行同规则（best.coupon）；②券库原为空（历史折扣码全被时效清洗）→补首条实体：z.ai 国际版 9 折邀请码 Y2H91IWSU3（unverified 标注第三方来源+官方拼好模机制背书，失效即清洗）；实测有码 tab 金色券领渲染 ✓；推版 10c0cd7；published 137
- [x] v2.10.9 智谱归组去重（2026-10-29，老板指令「智谱别搞 3 个条，夹带私货嫌疑」）：group 字段三种值并存（「智谱」×6/None→「智谱 BigModel」×2/ZCode×5）致同家裂三组（智谱 BigModel 90 亿+智谱 21 亿+ZCode）——统一智谱 BigModel 8 条一组、ZCode 6 条独立（老板此前指令）、CodeGeeX 独立行；groups.json map 智谱系全部指向「智谱 BigModel」防复发；实测主板块智谱系仅剩 ZCode+智谱 BigModel 两组；推版 b8bcf59
- [x] v2.10.8 html 防缓存 meta（2026-10-29，老板「你是不是没推版」）：实测 main=origin/main+线上已含 FAQ/千问（cron 已同步）——老板看到旧页=浏览器缓存 index.html；head 加 no-cache/no-store/Pragma meta 根治；推版 50fac18。今日累计 10 版全在库。**说明话术：主域 30 分钟 cron+浏览器强刷 Cmd+Shift+R**
- [x] v2.10.7 下架 n8n+全行业体验档横评（2026-10-29，老板截图指令「这三条都删了」）：n8n-selfhost（自部署工具）+deep-trial-tier-matrix-r7（横评攻略）归档；AutoClaw=旧缓存（v2.10.6 已下架）；published 138→136；推版 e27cb56。同类残留提示：Dify/FastGPT 亦为自部署编排工具，待老板示下
- [x] v2.11.0 整站彻底 SEO（2026-10-29，老板指令「qa 啥的都搞，Google 可收录」）：
  - head：title/desc/keywords 重写（关键词=AI 大模型免费额度/token 羊毛/折扣码/白嫖）+OG 全套+Twitter Card+RSS alternate+preconnect(icon.horse/google)
  - 结构化数据：首页 WebSite+Organization、FAQPage 8 问（与可见 FAQ 同步）、guides 每页 Article
  - FAQ 区块 8 条 details（tokenmost 是什么/DS Flash 等效/收益算法/最大额度平台/可信度/折扣码/比价器/更新频率）
  - noscript 静态兜底（无 JS 爬虫可读核心情报+攻略链接）；h1 补齐（logo span→h1，CSS 类选择器不受影响）
  - sitemap.xml 全量 12 URL（首页 daily 1.0+10 攻略 weekly 0.8+rss）；guides 模板补 desc/canonical/og 重建 10 篇
  - 0 万口径修复：无数额条目（如千问机制条）显示「免费·额度未公布」不再显示误导性「0 万」
  - 校验：JSON-LD 合法性+JSC 语法门+浏览器实测（rows 46/FAQ 8/h1 ✓）；推版 decbeca（顺带 TK 的 telegram_monitor.py 管线文件入库）
  - **GSC 待老板操作**：search.google.com/search-console→网址前缀验证（HTML meta 或文件法，验证码给我可埋 head）→提交 sitemap.xml→请求编入索引
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
