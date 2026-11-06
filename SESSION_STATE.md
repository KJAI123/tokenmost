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


## ⚠️ 事故复盘：sync.py 后台运行期编辑 deals.json 会被整文件覆盖（2026-10-31）
- **事故**：v2.19 轮 sync.py 后台全量跑（约 8 分钟）期间，主会话更新了 openrouter-free（19 款模型目录）并提交；sync.py 结束时用它**启动时加载的内存快照整文件写回** deals.json → 19 款更新被静默覆盖丢失；爬虫线会话随后把被覆盖态提交上库（远端 17 条 22:58:43 时间戳来源）
- **恢复**：从 422383c 提交取回 19 款版语义合并回库（27f35f3）
- **铁律新增：sync.py / harvest 等任何「读-改-写整个 deals.json」的脚本运行期间，禁止一切 deals.json 编辑；跑脚本前先确认无未提交的 deals 改动，脚本结束后再编辑。** 双会话并行期同样适用（爬虫线也写 deals.json，撞车时以 verified_at/内容新旧做语义合并，禁 git 层面机械取舍）

## 项目现状
- tokenmost.com 生产运行（香港服务器 HTTPS + GitHub Pages 镜像），deals.json 共 212 条（published 145，verified 126）；sites 70 站（agent 层 22）
- 服务器 30 分钟 cron 自动 git pull；GitHub push 即部署 Pages
- 后端 server/app.py（FastAPI+Flash 初审）systemd 常驻

## 当前任务队列
- [x] 云服务器羊毛专区补 5 条（2026-11-07，老板令「可以上吧，直接参考管线数据」，6cf1642）：管线爬到的多为付费 GPU 市场（不合免费原教旨未收），改收**行业常识级永久免费项目**：oracle-cloud-always-free（2×1C8G+4核Arm 24G+200G 行业最慷慨）/aws-freetier-ec2（750h 月×12 个月+Lambda 100 万 Always Free，防扣费告警）/gcp-freetier-vm（e2-micro 永久免费+$300）/github-codespaces-free（120 core-h 月+15G）/hf-spaces-free-cpu（2C16G 容器）；全 verified 官方免费层长期口径+freebies 组件；freecloud 导航 6 站；总库 235 条/170 发布
- [x] 访问统计全链路打通+历史日志真相（2026-11-06 续，SSH 凭据恢复后全程代操作）：
  - **SSH 恢复**：hk-hbgsc.pem 重新可用（此前失效是临时性的），服务器全程代操作
  - ①API 服务已重启，/api/stats 上线（计数从零开始）②②vhost 原本 **access_log off 继承——历史流量从未被记录过，无从回溯**（这是「没有历史数据」的真正原因）③已给 tokenmost.com vhost 加独立 access_log（/www/wwwlogs/tokenmost.com.log）+nginx reload——上线 1 分钟就记录了 27 条真实请求（含一个 Windows Chrome 访客拉 deals.json）
  - 端到端验证：curl 打点→日志记录✓/api/stats 计数✓
  - **后续数据口径**：nginx 独立日志=每日请求级明细（可 awk 分析 UA/路径）；pageviews 表=页面打开次数；两者都可我代查
- [x] 自托管访问统计上线（2026-11-06，老板问「访问数据量如何」，882430c）：结论=此前站点零统计（无第三方脚本/服务器日志 SSH 够不着/GSC 未验证）——装了自托管计数：server/app.py +POST /api/hit（SQLite pageviews）+GET /api/stats（今日/昨日/7 日/总量），index.html 生产域名（含 Pages 跨域上报主域）加载后静默上报；⚠️生效需 systemd 重启一次 tokenmost-api（git cron 只拉代码不重启）——老板宝塔面板点一下即可；历史流量可查宝塔→网站日志（nginx 日志）
- [x] v2.29.3 侧边栏开关位置重做（2026-11-06，老板令「位置按钮不太行」+截图指悬浮按钮压 logo，0aaecb7/7cfd2e3）：展开态=按钮内嵌侧边栏右上角（fixed top16/left174 与 logo 同行右端，logo 加 padding-right 避让），折叠态=左上角浮钮（12,10）；折叠/展开循环+近景截图确认视觉无碰撞；此前 10 次推送失败实为远端竞态非网络（先查 fast-forward 再怪网络）
- [x] 🚑 logo 本地包 20 个损坏文件修复（2026-11-06，老板令「很多logo也没补充」，544372d）：
  - **根因**：首轮图标下载器只验字节>200 未验图片格式——部分站点 favicon.ico 返回的是 HTML 错误页（200+text/html）被存成 .ico，浏览器解码失败→onerror 落外链→icon.horse/s2 境内又慢又被墙→表现为「logo 缺失」（智谱/火山/豆包/千问/LongCat/WorkBuddy 等约 20 个域名）
  - **修复**：全量 magic-bytes 校验（ICO/PNG/JPEG/SVG 四格式头）+四源重下（官网 favicon→icon.horse→s2→www 变体），修复 20 个（.ico→.png/.svg 换扩展名），孤儿 19 个清理，复验零无效
  - Pages 三个样本验证 200（doubao.png/open.bigmodel.cn.png/longcat.chat.svg）；**教训：下载图片必须验 magic bytes，200+字节数不够**
- [x] Kimi 会员助力折扣链接挂载（2026-11-05，老板令+提供专属邀请链，96aff78/9e22657）：kimi-subscribe-invite 新建（type=coupon，经链接完成会员订阅双方 100% 拿奖/最高 1 年会员等值权益，需付费订阅完成口径同拼好模先例；kimi-bot.com/activities 站长渠道含推荐属性，unverified 待实领）；金色折扣链接+加倍专区+Kimi 组聚合；总库 229 条/164 发布
- [x] 爬虫线数据全量消化（2026-11-05，老板令「看下TK的数据都更新吧」，5f58e73）：五条落地——①openai-pro-api-credits verified（官方帮助文档：Pro 月领 $100/$200/$500、Business 每席 $20/$100，订阅福利不折总账）②modelscope-gpu-free compute 层 verified（36h GPU+AMD 1000h+edu+200 魃粒/天）③modelscope-free-infer 补魔粒 ④ecom-token-store-1111 reseller 内容位 verified（五源：天猫 AI 空间站/京东充值馆/0.01 元直播包，⚠️补贴力度小防夸大）⑤api-relay-distill-warning 避雷（187 篇论文蒸馏掺假 83%→37%，中转永不收录立场重申）；总库 228 条/163 发布；遗留待核：GLM-5.1 白嫖 7 天（单源）、龙虾 7.9 元 Coding Plan（单源）、Command Code GOAT $100（待核）
- [x] 商汤小浣熊折扣链接挂载（2026-11-05，老板令+提供专属邀请链，8f74610）：deep-sensenova-xiaohuanxiong url→xiaohuanxiong.com/events/refer 站长专属链（code=a59b9f5d…，含推荐属性），type→coupon 升金色折扣链接按钮+加倍领取专区，6300 积分实测口径保留；rebase 撞车语义合并（叠加 1 条零重叠）
- [x] GLM 又送 token 更新（2026-11-05，老板令「更新新内容+glm 又送 token」，9e48c52/4eb42a1）：官方 promotion 页 webReader 直核——①zhipu-1111-coding-7zhe 新建 verified（GLM Coding Plan 年付 7 折 11-01~11-15 全档，2 月+30%/7 月积分制改版后首次官方降价窗口）②deep-zhipu-weekend-3yi/zhipu-weekend-build 复核在营（每人每周 3 亿，周日 23:00 清零）verified_at 刷新；rebase 撞车语义合并零重叠（远端 18 改/我方 3 改）
- [x] v2.29.0 版面紧凑化（2026-11-05，老板令「版面紧凑一些」+截图指 header 空档，5355012）：header 重构两行制（行1 logo+标语/行2 .hrow=横幅+统计+二维码同排 margin-left:auto 靠右），header 高 280→**145px**；横幅瘦身（5px 12px/主字 1.12rem）、统计 gap10/.7rem、二维码卡片 44px 紧凑、工具条 margin 10px、行 padding 9px 14px、主区 padding 20px；≤1360 隐更新日期/≤1150 隐第二条标语；桌面+移动双端实测 130 行正常
- [x] v2.28.0 侧边栏可收起（2026-11-05，老板令「侧边栏要可收起」，be57d67）：桌面左上角固定开关（展开态显示 ⟨ 收起符、折叠态 ☰），点击切 body.side-folded 隐藏 #side，localStorage tm_side_fold_v1 跨刷新记忆；≤860 移动端不受影响；全链路实测（折叠→记忆→刷新保持→展开）
- [x] v2.27.0 扫码进群指引再突出（2026-11-04，老板令「再更突出一些」，9cba718/4f016de）：二维码整块升级金色卡片（琥珀浅底+金描边+2.4s 脉冲光晕 wxGlow 动画，hover 上浮）；指引标「第一时间了解折扣信息↓」桌面恢复+全端常显（箭头弹跳）；码 52px/移动 44px；卡片内聚 header 流（区别于 v2.26.2 被毙的悬浮飘字）；GitHub 长时段断网（推送重试 20+ 次跨 40 分钟）后恢复推送
- [x] 智云新疆羊毛大升级（2026-11-04，老板令「我要他们的token羊毛信息」，9f57f0a）：官网首页 webReader 直核——**积分/token 换算官方全公开**（deepseek-v4-flash 1 积分/百万全场最低/glm-5.2 8/kimi-k3 20/minimax-m3 2.1/qwen3.7-max 12/emb 0.5）→200 积分券按 DeepSeek 档折 **2 亿 tokens**（tokens_wan 20000 入总账）；unverified→verified（官网直核）；free_models 6 模型挂折叠组件；⚠️质量舆情/社区失效票注记保留（实测一条接口确认质量再加大投入）
- [x] 爬虫线雷达落地四连（2026-11-04，老板令「看下爬虫助理TK新发现」，2411054）：①qiniu-conatus-1e8 补 deadline 11-30+细则 ②claude-for-oss 新建 verified（6 个月 Max 20x≈$1200，1 万名额）③azure-startups-5k 新建 unverified（$1K+$4K）④plans.json 百炼 Coding Essential ¥39.5；积压发现记待办池：OpenAI Pro/Business 月领 $500（待官方页复核）、Perplexity Education $10/月、魔搭 36h GPU+250 魔粒/天、Command Code GOAT $100 永久化、中转站蒸馏掺假避坑内容位、OpenAI ChatGPT↔Codex 额度共享
- [x] CatPaw（美团妙手）入流+logo 本地包（2026-11-04，老板令「增加 catpew 信源」=CatPaw 同音，de41f0f/3f6d8ed）：
  - **catpaw-meituan** agent 层新条目：首登送 1000 Credits 见面礼+每日登录领积分+LongCat-2.0 限免（1.6T/1M 上下文），多端云端运行；美团技术博客+凤凰+官网多源互证，unverified 待实领；agent 导航站 75 站；总库 221 条/156 发布
  - **logo 本地包根治**：127 行审计发现 92 行图标外链慢加载——一次性抓取 147/149 域名图标落盘 assets/logos/（同源秒开），logos.json 全量重写为本地路径；主板块 96 加载 0 失败
  - **🚑 Pages 部署修复**：cp assets/* 不复制子目录致 assets/logos/ 全部 404（行内图标线上一直靠外链兜底）——workflow 改分层拷贝，三图标验证 200
- [x] 智云新疆 AI Store 入流（2026-11-04，老板令「增加智云新疆的信源」，9932338）：maas 层新条目+导航站 74 站——电信新疆 AI Store（ai.xj.189.cn）注册送 200 积分券调站内 GLM/Kimi/DeepSeek/Qwen/MiniMax 等 API，至 11-30；⚠️三重风险标注（社区票 56% 认失效/linux.do「假鸡蛋」输出质量舆情/本机网络不可达 DNS 实证待老板侧复核）；积分制不折总账；运营商云组
- [x] v2.26.2 桌面端删入群指引标（2026-11-04，老板令「电脑端的删」，d2ba95c）：≥861px 隐藏 .wx-callout+去 .wx-corner 顶部补偿内边距，二维码干净立于右上；移动端（≤860）保留「第一时间了解折扣信息↓」指引；双端实测
- [x] v2.26.1 右上角入群指引强化（2026-11-03，老板令「补充扫码进群第一时间了解折扣信息+删顶部通知+做醒目指引」，0676bc4）：顶部通知条删除（wxTopBar HTML+CSS 全清）；二维码上方加琥珀指引标「第一时间了解折扣信息↓」+箭头弹跳动效；移动端保留二维码（≤480 缩 40px）；桌面/移动双端实测
- [x] v2.26.0 入群二维码直挂头部右上角（2026-11-03，老板令「直接挂在右上角，直接一些」，9d38264/80e2b44）：sips 从群海报裁 760×760 正方码 assets/wechat-qr.jpg（三定位角完整，两轮校偏）；header .stats 尾部 .wx-corner=46px 圆角小码+「扫码进群」金字标，hover 放大、点击开大图弹窗，≤480 隐藏（移动端顶部条保留）；GitHub 断网 13 连败后网络恢复推送成功
- [x] TRAE 码力裂变折扣链接挂载（2026-11-03，老板令+提供专属邀请链，cd69203）：trae-code-fission 新建（type=coupon，经链接注册+登录桌面端一次性得 3000 积分叠加 Free 档 500/月；trae.cn/events/code-fission 站长渠道含推荐属性；verified=boss 口径）；金色折扣链接+加倍专区+Trae 国内版组聚合+trae-free-tier 交叉引用；总库 220 条/155 发布
  - ⚠️ 事故复盘：本轮 rebase 解算时 `git checkout --ours` 把语义合并后的 deals.json 一并覆盖（丢 Trae 条目），推后发现重打——**教训：rebase 解算 checkout --ours 必须点名文件，严禁对未冲突/已手工合并文件批量 checkout**
- [x] 🚑 v2.25.2 热修主板块白屏（2026-11-02，老板报「网页主板块也挂了」，485c96a）：
  - **根因**：v2.25 砍登录/供码删了 authBtn/authBtnSide 元素，但 boot 链仍调 authRefreshUI 写 null.textContent → 抛错 → **boot 的 .catch 把已渲染好的 127 行整个清成「数据加载失败」**（banner/导航在抛错前已渲染所以看起来"半死不活"）
  - **修复**：①authRefreshUI 元素守卫 ②boot 链 authRefreshUI/loadShared 改 try/catch 隔离——**数据渲染完成后可选功能抛错不得清空主板块**
  - 定位方法：IAB 打开线上站逐函数 try/catch（renderNav/render/vRender/calcGlobalBanner/loadShared 全 OK，唯独 authRefreshUI THROW）
  - Pages 热修后 127 行恢复验证 ✓；主域 30 分钟 cron 跟进
  - **⚠️ 铁律新增：砍任何 UI 功能时，必须 grep 全部 getElementById 引用并同步清理；boot 链可选步骤一律 try/catch 隔离，绝不让 catch 覆盖已渲染内容**
- [x] v2.25.1 横幅徽章重设计（2026-11-02，老板令「做的太丑了」，39a19d9）：根因=.global-banner b 的 1.35rem 巨字规则命中嵌套裸 <b> 致胶囊巨大；改专属 .gb-pill class（0.7rem/20px 高小 chip，琥珀描边浅底），文案精简「🪙 折扣链接注册额外叠加 35.55 亿」；⚠️ 事故=上轮未提交修改被爬虫线定时 git checkout 清掉（mtime 00:20），重做并立即提交——**共享仓库铁律：改完即 commit，未提交改动随时会被并行会话清掉**
- [x] v2.25.0 四连整改（2026-11-02，老板四连令，9a55477）：
  - **Qoder 折扣链接挂不上的根因**：聚合行金色按钮只看组内最优条目（best），而折扣链接条目非组内收益最高——改为组内任一含折扣码/链接即亮金（新增 aggGold 辅助函数替代深层嵌套 IIFE，顺带消除模板嵌套语法雷：此前内联 IIFE 写错括号触发连环 SYNTAX FAIL，JSC 报错行号有包装偏移需 -2 校正）
  - **分类收窄 13→7**：免费专区/大模型官方（CN+海外合并 data-cat=official）/Agent 平台/云与算力（MaaS+算力+中间商合并 data-cat=infra）/加倍领取/付费区/避雷
  - **刷新回顶部**：history.scrollRestoration='manual'+scrollTo(0,0)
  - **登录/供码下线**：header authBtn+侧边栏 authBtnSide 移除（vault 本地账号库保留）
  - **横幅 🪙 加成琥珀胶囊高亮**（老板截图指位）：bold+amber+#b45309+pill 边框+nowrap
  - **doubao-pro-invite 新条目**：老板专属邀请链（desktop-fission/pro-trial 裂变，inviteCode=72Se9znu18，含推荐属性），豆包组聚合金色按钮+加倍专区，unverified 待实领天数
  - 推版遇 GitHub 断网潮退避 4 次成功；Pages 部署延迟 ~90s 后五项全验证通过
- [x] v2.24.0 折扣链接加成口径上横幅（2026-11-01，老板令「增加通过折扣链接注册可以额外多拿多少token」+截图指横幅，13e5555/f4ddde1）：横幅叠加公式追加「🪙 经折扣/邀请链接注册额外可叠加 35.55 亿」（加倍领取条目按平台去重首月总量）；白嫖总账新增⑤卡「🪙 折扣链接注册加成 35.10 亿」（verified 口径，标注与分类有交叉）；根因修复=横幅函数重复定义旧版覆盖新版+LB reduce 初始值
- [x] Qoder 折扣链接挂载（2026-11-01，老板令+提供推荐链，646f297）：deep-qoder-daily-credits 通用链接→qoder.cn/activities 站长推荐链（referral_code，含推荐属性），type→coupon 升金色折扣链接按钮+加倍领取专区，每日 100 Credits 机制保留
- [x] ZCode 折扣链接挂载（2026-11-01，老板令+提供专属邀请链，0918b57）：zcode-daily-1e8 通用链接→zcode.z.ai/invite/L5BLKJE7（站长专属链，含推荐属性），type→coupon 升金色折扣链接按钮+加倍领取专区，拉新「每天 1 亿」机制保留（老板亲测口径）
- [x] v2.23.0 logo 系统升级+DeepSeek 复核（2026-11-01，老板令「有些logo还没有，好好丰富，deepseek/trae」，dc592ca）：
  - **根因**：行内图标链=icon.horse（境外，限流+墙内不稳）→Google s2（境内被墙）→隐藏——DeepSeek/Trae 等 icon.horse 未收录或限流的域名直接消失
  - **治理**：双轮探测 72 域名（官网 favicon.ico 34 可用+www 变体捞回 12 含 www.deepseek.com/favicon.ico）→ assets/logos.json 46 条官方直连图标；行内链升级四级 LOGOS 覆盖→官网 favicon→icon.horse→s2→隐藏；侧边栏同步接入；pages.yml assets 部署已具备
  - **DeepSeek 三条复核恢复**：定价页 URL 迁移实锤（/quick_price.html 404→/quick_start/pricing），错峰半价规则原文未变，verified；⚠️ 同页官宣 **Search/Fetch API 11-01 起收费 5 元/千次**——deepseek-searchfree 过期清洗删除；prices.json 缓存命中注记校准 0.02/0.04
  - 推送遇 GitHub 断网潮（SSL_ERROR_SYSCALL），退避重试第 4 次成功
- [x] v2.22.1 主板块行内平台 logo（2026-11-01，老板令「主板块需要增加对应的logo」，bd5fee6）：单行/聚合行两模板 provider 前插 15px 圆角 favi（域名取 siteFor 导航站或条目 url，icon.horse+s2 64px+隐藏三级兜底同侧边栏），无站点条目自动跳过；IAB 实测 125 行渲染正常
- [x] v2.22.0 WorkBuddy 免费权益折叠目录（2026-11-01，老板令「workbuddy 也做类似 opencode 的展开」，447c5fb/9b0f07d）：折叠组件泛化 fmMeta/fmBlock 双类型（free_models=FREE 徽章「N 款免费模型·全 $0」/freebies=免费徽章「N 项免费权益」），chips 常显徽标区分；国内版 5 项（公测 5000/每日 100/教师版/绑卡试用/牌价）+国际版 6 项（Free 100/每日活跃 30/补全 5000/自动任务/全模型限免/试用金）结构化；混元 Hy3/Hy4 过期限免从 value/rule 清理；rebase 撞车语义合并（零重叠：远端 17 改/我方 2 改）
- [x] v2.21.0 网页端数据自动同步（2026-11-01，老板令「网页端要同步啊」，6d8e346）：开着页面每 5 分钟自动拉 sites/deals（cache:no-store），sig（条数+id/verify/published 签名）变化即原地重渲染+白嫖横幅更新+底部气泡「🔄 数据已自动同步·N 条」；诊断结论=两端线上当时均已是最新（Pages/主域都有 v2.20+217 条），老板见旧版=开着的旧标签页不会自拉——轮询根治；容错静默不扰 UI
- [x] v2.20.0 免费模型目录折叠+高亮（2026-11-01，老板令「版面不要占这么大，做展开功能，高亮免费模型特点」，2732882/b1151e4）：fm-wrap 改折叠组件——默认一行绿色高亮条（FREE 徽章+N 款免费模型·全 $0+▾ 展开看清单），点击展开完整 chips 清单/▴ 收起；行内 chips 常显「🆓 N 款免费模型」绿徽标（折叠态可见特点）；行高 401→112px（桌面）/500+→232px（移动）；aria-expanded 无障碍；桌面/移动双端开合循环实测
- [x] 华为云码道 CodeArts 入流（2026-10-31，老板令+提供推荐渠道链接，c41b78f）：每日登录客户端领 1000 万 Token（官方 changelog 直核，daily_wan 1000 保守 1:1）+新用户/学生 4000 积分档待核；折扣链接=站长推荐渠道（含推荐属性）；金色按钮+加倍专区+agent 导航站；华为云全家首条（ModelArts Studio 千万 Token 华东二限定/开发者空间百万券=同门待核线索）
- [x] 手机端布局再优化+重验结果推版（2026-10-31 凌晨，老板令「推下版，手机端再优化一下布局」，8081219+746fd0c）：
  - **模型目录块窄屏重排**：:has(.fm-wrap) 行在 ≤860px 目录块独占全宽一行（172px 窄栏 470px 高→全宽 205px），值文案/徽章各行铺满；chips 缩号；360/390/1280 三档实测桌面零回归；不支持 :has 的老浏览器优雅降级
  - **重验结果已推**：sync.py 全量轮收尾——未变源续验证戳、5 源真变化降级（xfyun×2/dify/bigmodel-activity/ark-collab）、review-queue 14 条待复核（多数 10-30 存量）
- [x] v2.19.0 顶部扫码入群+全量重验三层机制（2026-10-31 凌晨，老板三连令，422383c）：
  - **顶部扫码入群**：微信群海报图入库 assets/wechat-group.jpg（966×1530）；页面最顶部金色条「📥 扫码进微信群 · 每天分享 token 折扣码」点击开弹窗；弹窗 280px 宽原比例（0.6335 vs 0.6314 保真不变形）+「本码 11-07 前有效」提示；**pages.yml 已补 assets/ 部署**（此前漏了会 404）；侧边栏/页脚微信群入口同步生效
  - **⚠️ 待办 11-07：群二维码到期换图**（老板海报自带说明，替换 assets/wechat-group.jpg 即全站生效）
  - **全量重验三层**：①sync.py 全量监控源哈希重验（后台跑，页面未变自动续验证戳/变了降级待复核）②OpenRouter 官方 API 直抓：456 款中免费 19 款全目录入流（16→19，新增 thinkingmachines/inkling 1M、dots-3 512K、poolside laguna、gemma-4、nemotron-3-ultra 550B）③搜索互证：智谱每日 3 亿 ✓ 无变化；知乎 27 家清单/火山「每日 200 万」口径为线索待核（火山旧条目口径 500 万已归档）
  - **教训**：爬虫助理子代理派单被平台风控秒拦（"unusual activity"）——并发限额期派单仍不可靠，主会话亲自搜照旧
- [x] OpenCode 10 款免费模型全目录 + 免费 API 站展开扩容（2026-10-31 凌晨，老板贴官方 Console Models 汇总+亲测，c385ccb；客户端 UI 实锤补注 242b480）：
  - **opencode-zen-free 按官方价格表口径重写**：10 款全 $0（输入/输出/缓存全免费、支持工具调用）——Big Pickle（隐身推理）/GLM-5.3-Flash Free/DeepSeek V4.1 Flash Free/Beam Free（1M）/Flint 40B/MiMo-V2.6-Flash（全模态）/Nemotron 3 Ultra/3.5 Lightning/3.5 Super VL/Jev 1.13（结构化判定）；**取代早前「每模型每日上限」口径**（官方=$0 计费制非按 token 扣费，无公布上限，上游可能限速）；只能经 OpenCode 本体（opencode/<id>）+需 Console 登录
  - ⚠️ 合规标注：Beam 中国大陆含港澳不可用；隐私分级（GLM/DS 零保留最稳；Big Pickle/Flint/MiMo 收集数据 30 天；Nemotron 试用端点记日志）；限时免费随时下架
  - **前端扩容**：deals 条目新增 `free_models` 结构化字段 → 行内渲染「🆓 免费模型目录」chips 块（fm-grid，悬停看备注/上下文）——OpenCode 行 10 款/OpenRouter 行 4 款代表作直接展示；明细行 notes 放宽 2 行
  - openrouter-free 补代表作目录+与 OpenCode 机制对比注
- [x] v2.18.0 加倍领取功能+广告位撤下（2026-10-31 凌晨，老板双令「通过折扣加倍领取的功能你还是没做出来啊」「广告位招租先不用」，75157d6）：
  - **加倍领取**：新 tab「🪙 加倍领取」（金色描边）+侧边栏工具入口+兑换弹窗「用码加倍」提示行；筛选口径 isDouble()=有折扣码/折扣链接/邀请奖励条目（邀请链接即码），聚合展示 14 条/8 平台（智谱/小米/恒源云/OhMyGPT/潞晨云/硅基流动/ZCode/Comet）；金色说明条讲清用码逻辑（到账=基础赠送+加成）
  - **数据现状提醒**：实体折扣码仅 2 条（z.ai 9 折码真实/302.AI TM-302 假码被排除）——后续联盟渠道（硅基流动推荐官等，老板注册后发链接）自动进此专区；邀请类加成=站点主力
  - **广告位**：空配置不渲染「招租」占位（.ad-slot:empty 隐藏），TM_ADS 基础设施保留、素材到位即上
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
