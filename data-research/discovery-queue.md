# 找源发现队列（discovery-queue）

> 供每 15 分钟找源巡检自动消费：取最靠前的未完成条目执行 WebSearch（串行），完成后标 ✅ 并把新发现落表（信息源总表-全量版.xlsx 发现日志 + 对应 sheet），可自行在队尾追加新线索。格式：`- [ ] 线索描述 | 建议搜索词 | 去向`

- [x] weixin.sogou.com 可行性 ✅ 已管道化；/link 解析单会话 3/3 攻克，但脚本内 4 查询连发触发反爬（0/3）——改进项：每轮只解析 1 条或分离会话 | 状态: 雷达标题层可用，直达层待改
- [ ] 搜狗 /link 加密跳转解析（需 SNUID cookie 方案，低优先） | — | 提升公众号文章直达率
- [x] 「每天10亿token·含K3」聚合平台定位 ✅ 2026-11-11（AutoClaw接管轮）：定位=七牛云模型广场（qiniu-conatus-1e8 日领1亿/充值日领10亿 + qiniu-invite-3m 已在库）；新增量=Kimi K3 免费版上架 moonshotai/kimi-k3-free（1M 上下文·免费不计费，OSCHINA 10-21 三方佐证）→ ⏳主管直核官方页后建条，详见 findings/2026-11-11-qiniu-kimi-k3-free.md
- [x] 千问云电脑免费档官方页定位 ✅ 2026-11-13（AutoClaw接管轮·负结论）：累计 4 组搜索词（11-11×3 + 11-13「千问 云电脑 通义 App 免费 4核8G 上线」）均未命中官方页——与「千问 App 内嵌入口站外不可索引」假设一致，WebSearch 轨到此为止；立条唯一可行轨=weixin 管线搜狗主题词「千问 云电脑」（QUERIES 追加属管线代码改动，待主管裁决，参考 TK 接线方案先例）| 去向：主管
- [x] 阿里云「千问AI双11」官方活动页直核 ✅ 2026-11-11（AutoClaw接管轮）：官方页=aliyun.com/activity/hub/qianwenai1111（本机 fetch 直核在线）；页面口径：Token Plan 个人版提额 78%·新客低至 5 折（Lite 2 万 Credits/月·Essential 4.5 万 Credits/月——与 11500→提额 78%≈2 万互证，月价页面未直出）、千问办公 29.9 元起、Qoder 低至 19.9 元、新认证企业至高 2728 元 AI 礼包、150+ 模型通享节省计划新客低至 4.5 折（20/60/100 元档）、OPC 助力计划 Token 补贴 1000 元~100 万；19.5 元首月=developer.aliyun.com 文章口径待登录核；⚠️ deadline 类：活动 11-02 启动、三方称 11-11/12 截止，过期转 expired → ⏳主管建条
- [x] 智谱实名2亿 ✅ 2026-10-28：未证实（降级）；意外收获=官方 promotion 页现已列 Weekend Build 3亿/ZCode 1亿/1024节5亿——zcode-linuxdo 可升级
- [x] 小米 MiMo ✅ 2026-10-28：100T 免费计划已领完（5月中旬），转永久降价 99% 常态化；MiMo-2.5 低价条目候选→主管
- [x] 讯飞星辰 Qwen 不限量 Token 官方页 ✅ 2026-11-11（AutoClaw接管轮）：定位=maas.xfyun.cn/modelSquare 模型集市（模型提供方可筛「阿里巴巴」）；线索证实=2026-06 起多源一致（知乎/segmentfault/163/腾讯云开发者社区/einkcn 汇总）：Qwen3.6-35B-A3B+Qwen3.5-35B-A3B 0 元/百万 Token，「不限量」为社区口径、官方口径=0 元定价档无明确额度；直核受阻=模型集市 SPA 静态抓取 0 模型（价格需登录渲染）→ ⏳主管登录核 0 元档现势后建条；注意 xfyun.cn/doc/spark/TokenPlan.html=企业包月订阅另一物勿混淆
- [x] MonkeyCode/TRAE ✅ 2026-10-28 定位完成：长亭科技 monkeycode.cn（文档/仓库已入采集器）；数额多源出入（标准1000万/日·活动期3000万·7天试用·历史促销500亿+¥200）→⏳主管按控制台口径核实；TRAE 五档 Free/$8/$20/$60/$200
- [x] Google Antigravity ✅ 2026-10-28：免费档 250→20 RPD(-92%)、RPM 10→5；积分制（Pro 1000/月·Ultra 25000/月·不滚存）；7天锁机制；负情报，无收录价值
- [x] 每日登录类 ✅ 2026-10-28：各平台无统一签到中心；智谱「每日一亿领取」单源线索→主管；其余=注册赠送+邀请奖励模式
- [x] smzdm 最新 AI 免费权益聚合帖 ✅ 2026-11-12（AutoClaw接管轮）：定位两稳定产出帖——post.smzdm.com/p/awwdxlwp（11-09「每天白赚几百AI大模型免费薅羊毛」：豆包/DeepSeek/GLM/Kimi/GPT-6 Astra/Opus 5.5 渠道汇总）+ /p/arzrqn2w（10-17「全网AI产品免费权益清单」）；⚠️帖内「腾讯元器新用户直送1亿Token」与库内官方直核条目 deep-tencent-yuanqi-verified-r6（每月100万token，官方文档口径）冲突→不采信帖口径；Today AI/腾讯TokenHub 帖中线索均已在库（today-ai-free/deep-tencent-tokenhub）；smzdm 站内搜索 ajax 化反爬严，直抓入采集器前需先核 robots → 主管裁量是否列入周翻源
- [x] v2ex 摸底 ✅ 2026-10-28：竞品站 token.pencilai.top⭐+MiMo 重置50倍修正+快手/美团线索；掘金/即刻下轮
- [x] 学生认证补全 ✅ 2026-10-28：GitHub Copilot 学生免费 3-12 终止+Student 计划 4 月暂停——⏳主管复核主数据 github-student-pack 条目；Copilot Free 层仍有效
- [x] OpenRouter API 快照 ✅ 2026-10-28：主会话 sources.json 已含 api/v1/models——不重复建源，闭环
- [x] Cursor / Windsurf ✅ 2026-10-28：两定价页入采集器；Cursor 10-12 改版为 X 订阅（Free/Plus$8/Premium$30/Super$100/Ultra$200 与 Grok 共享池）——⌨️Coding 面板变更线索→主管；Windsurf 免费档≈25 Flow Actions/月
- [x] TaoToken ✅ 2026-10-28：定位=taotoken.net 统一Key聚合网关（注册送免费额度）；数额口径⏳主管核
- [x] lololowe 博客 ✅ 2026-10-28：评估通过入采集器（98KB·21免费命中·11平台直链）
- [x] 34家白嫖神 ✅ 2026-10-28 定位=OmniRoute(diegosouzapw/OmniRoute 3.7万Star)：本地网关+免费额度仪表盘；已入采集器，站点工具区收录建议→主管
- [ ] weixin 雷达第3周查询词轮换 | — | 公众号管道
- [x] 智谱每日一亿 ✅ 2026-10-28：入口定位=bigmodel.cn/activity/trial-card 页族（8+ 体验卡页）；数额登录核→主管
- [ ] 免卡小 VPS 批量核验（码上AI记 2026-11 VPS 指南二手）：Vyce.Cloud（英 2G 纯IPv6 GitHub登录每日续期）**【11-13 部分核验：官网 vyce.cloud 自述 2GB RAM/独立 IPv6/SSH root/免费确认；GitHub topic「vyce」已有 keep-alive/auto-renew 跑分类社区工具=周期续期机制侧证；续期细节与立条需 freecloud 线注册实测】**/ Woiden.id（德 NAT TG登录3天续）**【11-13 官方页核：woiden.id/vps-renew 自述=到期前至少3天可续+TG群+共享IPv4/SSH；/vps-nat 另指 HAX.co.id 免费 IPv6-only；立条需注册实测】**/ Openworld.eu.org（洪都拉斯 1C512M Discord 7天续）**【11-13 官方页核：LET 2026-08-24 帖证实=Discord 账号登录+7 天续期周期+IPv6-only；1C512M 规格需注册实测】**/ ASCS Cloud（加 2C2G LXC 30天）**【11-13 搜索级核：外网无公开佐证（泛列表页均无收录，唯一信源=码上AI记二手）→立条需注册实测】**/ nat.freecloud.ltd（港德 NAT 签到）/ vipserver.cloud（洛杉矶 2C2G 独立IPv4 社区续期）**【11-13 搜索级核：外网无公开佐证（泛列表页均无收录）→立条需注册实测】** | 平台名+free vps 续期规则 | freecloud 线核验后立条
- [x] FFxF console.ffxf.net 优惠码 TRY10=10 CAD 赠金核验 ✅ 2026-11-12（AutoClaw接管轮）：官方自证=ffxf.net/blog/newsletter-october-2026.html（2026-10-05 月刊原文「10 CAD of free credit with code TRY10，long-time customer or brand new 均可」）——代码存在性与新老客户适用官方确认；10-05 月刊距今 5 周，当前时效建议 console 实测下单页确认后立条 → freecloud 线
- [ ] 免费域名其余渠道批量核验（码上AI记 10-31 全搜罗）：Gname eu.cc（3 张全额券 30 天过期，续费只走 gname.vip 推广页）**【11-13 官方页核修正：gname.com tld-eu-cc 页自述=所有用户 3 个永久免费注册名额（高级经销商至多 20 个），券领后 30 天有效（官方公告 2026-01-23/2025-06-12）；三方 2026-08 补充=溢价域名不免费、续费须到期前 90 天内走活动页（非 gname.vip）】**/ eu.org（人工审核常以月计，先配 NS 再申请）/ is-a.dev+js.org（GitHub PR）**【11-13 官方页核：is-a.dev 官网=is-a-dev/register 仓库 PR（新推 .is-a.bot）；js.org 官网四步=GitHub Pages+js-org/js.org 仓库 PR、限 JS 相关项目】**/ .pp.ua（名义免费但下单须绑卡+手机激活，同号 30 天限 3 次）/ 多姿态 duozitai.cc（QQ 微信登录，仅厂商自述口径）/ KataBump kdns.fr（托管附赠，免费档 4 天续期）/ Stackryze（细节未核实，单页宣传站）| 各平台名 | freecloud 线
- [ ] CodeHost .cv 截止提醒：2026-11-17 活动截止（条目 codehost-cv-free 活动 2026-08-17~11-17，结账码 CODEHOST $0），站内 codehost-cv-free 条目需在截止后标注（过期转 expired）；11-12 预核：官网活动页 fetch 被反爬拦（invalid response，与库内反爬注明一致），截止后标注动作不变 | CodeHost cv deadline | freecloud 线
