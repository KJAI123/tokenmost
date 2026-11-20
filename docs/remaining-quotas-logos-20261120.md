# 剩余额度与 Logo 复核 · 2026-11-20

本轮以 origin/main `8850913` 为基线，逐项扫描 308 条记录，定向更正 12 条。保留全部既有证据及旧额度快照，没有覆盖主工作区或自动同步的新状态。目标是补可解释的换算，修正旧数量与失效入口。

## 补充与更正

| 平台 | 本轮结果 | 官方依据 |
|---|---|---|
| 秒悟 Meoo | 旧 miaowu.pro 错链改为 meoo.com；补新人首月 5,000 积分和每日首次登录 2,000。按 Kimi K3 / DS V4.1 Flash / GLM-5.3-Flash 三个替代模型情景，输入:输出假设 3:1、无缓存。参考情景每日约 57.1 万、首月约 1,857.1 万 Token；同池模型不相加。 | [积分与模型扣费表](https://docs.meoo.com/pricing) |
| Drex / Nace | 注册 $5；首次月赠在注册满一个月后到账，此后每月 $5。官方推理价 $0.03/百万输入 Token，$5 约覆盖 1.6667 亿输入 Token；不估输出，不再把同笔 $5 加一份 DS 购买力。保留 Google / 满30天 GitHub / 验卡三选一及邮箱、防滥用条件。 | [当前定价与免费余额规则](https://console.nace.ai/docs/drex/reference/pricing) |
| FastGPT | 补原始 100 AI 积分，首月保守只计一次。用 ¥599/25,000 至 ¥99/4,000 的套餐均价代理，约 136.9–141.4 万 DS 购买力参考；套餐还含其他资源，并非官方独立积分售价或实际 Token。免费刷新周期未明确，不额外累计。 | [官方定价及 FAQ](https://fastgpt.cn/price)、[积分计费说明](https://doc.fastgpt.cn/guide/workspace/usage-and-billing) |
| 腾讯 ADP | 官方确认体验版每月 15,000 PU、1 PU=¥0.001，因此补约 857.1 万 DS 购买力参考。保留原 PU、Auto 模型限制及实名认证主账号手动领取条件。模型、插件、知识库等共享 PU，不称作 Auto 的实际 Token 数。 | [新版套餐与 PU 面值](https://cloud.tencent.com/document/product/1759/139268)、[PU 抵扣范围](https://adp.tencent.com/zh/document/216860748853170176)、[当前价格页](https://adp.tencent.com/pricing/home) |
| Devin / Windsurf | 当前免费档为轻量 Agent 配额与无限 Tab / inline 编辑；旧 50 credits 无现行依据，移入历史。免费记录与另购 $20 / $200 套餐拆清，未凭订阅价格虚构免费量。 | [Devin 当前定价](https://devin.ai/pricing) |
| NVIDIA NIM | 当前目录可确认免费推理，但 1,000 / 5,000 credits 仅找到 2024 年员工答复。旧数字移入历史，当前数量继续待复核，不将旧积分当现行请求量。导航同步删除旧数量宣传。 | [当前目录](https://build.nvidia.com/)、[2024 年历史答复](https://forums.developer.nvidia.com/t/cannot-find-request-more-option-for-nim-api-credits/309462/2) |
| 商汤日日新 | 当前实时官网确认 Free 公测、Flash Lite / U1 Fast、最多20个 API Key；实时 HTML 未列旧 12万/5h、120万/周。搜索缓存的6万/5h与社区所述不同模型池也不能代替当前账号条款。保留历史，暂不外推日/月 Token。未混用另一 TokenPlan 站点的积分计价。 | [当前官方公测入口](https://www.sensenova.cn/token-plan) |
| DeepSeek 4 条 | 人工重核高峰、空闲、缓存与服务端搜索计费。人民币基准仍为 ¥1.75/百万、美元仍为 $0.2625/百万（空闲、3:1、无缓存），公式不变。 | [中文价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)、[国际价格](https://api-docs.deepseek.com/quick_start/pricing/) |
| AgentRouter | 官方主页及图标均返回安全验证页；继续待复核，不采用验证页图片或第三方仿制 Logo。 | [官方入口](https://agentrouter.org/) |

## 图标与导航

新增或更新 5 个官方素材：Meoo、Nace（Drex 母品牌）、Devin、FastGPT 矢量图、腾讯 ADP 产品标识。素材保存在本地，抓取页、原始素材 URL 和 SHA-256 记入 `assets/logo-sources.json`。

仙童旧域名 HTTPS 失败，HTTP 返回 Porkbun 的 Coming Soon 停放页，没有可确认的业务入口或品牌图。移除失效导航，原条目完整保存在本轮审计。补入 Meoo、Drex、ADP 导航后共 98 个入口，均有本地图标；国家超算中心使用已标明的分类图标。权益记录中尚缺可确认品牌素材的只有 AgentRouter；“API 中转站”是风险分类，不是品牌。

## 换算规则与范围

- 增加 `model_rates`：按官方积分/千 Token 表估算，模型是同池的替代情景。
- 增加 `model_budget`：只算指定模型输入预算，原金额 `convert:false`，避免与 DS 购买力重复。
- 增加 `starts_after_days`：限制首月窗口；满一个月才发的月赠首月排除，保留原文日历月规则。
- 现有 39 条记录提供 51 个额度视图，常规免费总计按 40 个独立池去重；付费、邀请、资格上限和 API 抵扣规则保持独立。
- 音乐、音视频、GPU 小时、云主机/部署金等继续保留原单位。NVIDIA、商汤、AgentRouter、阶跃会员天数、AutoClaw 邀请奖励中缺少数量或同活动扣费公式的部分不编 Token。

## 实际验证

- 308 条记录的 JS / Python 公式与情景结果一致；额外测试月赠延后、输入预算、积分模型情景、套餐均价代理和共享池去重。
- `source_audit.py --against` 保留证据检查通过；`check.py` 生成静态页与订阅文件通过。已有导航名称匹配提示仍保留，未当成新错误。
- 中英文 320 / 390 / 768 / 1440 像素通过同源 iframe 的实际内容宽度检查，无横向溢出；1440×900 各有4条完整情报。检验搜索重置、信源展开、估算依据和新 Logo。
- 最终 178 个引用素材在浏览器中全部加载，零损坏、零等待；ADP 320 像素条目也显示产品图标。
- 线上发布使用已核对的香港 `/www/wwwroot/tokenmost`，保留远端 `server/venv/`。正式域与 GitHub Pages 的发布后真实响应校验另存本轮工作目录 `outputs/`，不与本地预览混写。

逐条结果及退役导航见 `data-research/audits/remaining-quotas-logos-20261120.json`。
