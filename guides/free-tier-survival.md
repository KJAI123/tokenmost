# 海外免费层生存指南 2026：Gemini / Groq / Cerebras / Mistral / Cohere / OpenRouter

> 2026-11-23 更新 Groq、Mistral、Cohere 和 OpenRouter；其他章节核实于 2026-10-27。

 总基调：海外「注册白送大额 token」时代已结束，免费获取全部转向**限速免费层 + 一次性行用金**。本文教你在新规则下活着。

## 1. Gemini——免费层全面动态化，CLI 本体已停服（重大更正）

- **⚠️ 2026-06-18 起 Gemini CLI 已被 Antigravity CLI 取代**（官方开发者博客+README 过渡通知直核），旧 CLI 与 Code Assist 扩展当日停止为免费层/Pro 用户服务——**旧攻略「Gemini CLI 免费 1000 请求/天」是历史遗产，随 CLI 一起失效**。
- **Antigravity CLI 免费档**：社区口径极度收紧（有称个人档 ~20 agent 请求/天，单源低置信）；与 Google AI Pro 订阅不共享配额池。
- **API 免费层（仍然活着，实查法）**：
  1. 登录 https://aistudio.google.com → Usage 区看当前项目各模型 RPM/RPD **实显值**（官方已改为动态限额、不公布静态表）；
  2. 社区实测口径：Flash 系约几百~1000/天、Pro 系约 100/天甚至更低、preview/experimental 更紧；
  3. RPD 太平洋时间午夜重置（UTC-8）。
- **活法**：AI Studio API 免费层仍是海外免费主力；CLI 编程场景换 Antigravity 体验或直接用 API Key + 开源 Agent 框架。
- **未付费服务**：Google 可用提交内容和生成回复来改进产品及机器学习技术，也可能由人工审阅。避免提交私人代码、个人信息或其他机密内容。
- **按付费服务处理的条件**：Gemini API 看调用项目是否关联有效的 Cloud Billing 账号。AI Studio 看当前账号是否能访问这类项目，或是否为 Workspace 企业账号。付费数据条款下，Google 不用提示词和回复改进产品，但可为安全、滥用防控或法定义务短期记录。[Google 付费数据条款](https://aistudio.google.com/docs/terms#data-use-paid)
- **地区例外**：位于欧洲经济区、瑞士或英国时，即使使用 AI Studio 或 Gemini API 免费额度，数据用途也按付费服务条款处理。[Google 官方数据用途条款](https://aistudio.google.com/docs/terms#data-use-unpaid)

## 2. Groq 免费档

gpt-oss-120b 的公开上限为 20 万 Token/天，另有每分钟 30 次、8,000 Token 和每天 1,000 次的限制。按 30 天计最多 600 万 Token，组织的实际限额见控制台。[官方免费档限额](https://console.groq.com/docs/rate-limits)

**训练与留存**：Groq 表示不会用客户数据为自己训练模型。普通推理默认不保留输入和输出，排障或调查滥用时可能记录最多 30 天，法律要求时可更久。批处理、微调等功能另有留存规则。使用量元数据始终记录，组织管理员可在控制台启用零数据留存（ZDR）。[Groq Trust Center](https://trust.groq.com/faq?s=9pcm46fyh5sypzqgtfto) · [Groq 留存与数据控制](https://console.groq.com/docs/your-data)

<a href="../platform/groq.html">查看 Groq 的额度与使用规则</a>

## 3. Cerebras——永久免费层已死，现在是 $5 体验金

- **2026-07 改版**：取消「每天 100 万 tokens 永久免费」，改为 **Free Trial：注册送 $5 一次性 credits**（官网原文直核）。
- **限速（第三方口径，中）**：约 5 RPM / 30K TPM / ~100 万 tokens/日（gpt-oss-120b 等）；Developer 档充 $10 起，速率 10×。
- **绑卡与扣费**：Free Trial 注册**不要求信用卡**（官方页未列支付步骤即发放）；$5 用完即止——**未见自动扣费机制**（体验金性质，非订阅）。想续力再手动充 $10 进 Developer 档。
- **实查**：https://cloud.cerebras.ai 控制台看 credits 余额与限速页。
- **活法**：$5 按 gpt-oss-120b 价格能跑几千万 token 输入，够把一个项目代码库完整索引几轮；当一次性「深度审计基金」用。

## 4. Mistral Studio 与 Vibe

免费方案提供 Studio 和 Vibe 用量；创建 API Key 和调用 API 需要启用按量计费。工作区可查看当前限额。[Mistral 官方用量说明](https://docs.mistral.ai/admin/billing-usage/usage-limits)

<a href="../platform/mistral.html">查看 Mistral 的额度与使用规则</a>

## 5. Cohere——老实的幸存者

- **Trial Key 政策至今未变（verified 口径）**：注册送 Trial Key、**无需信用卡、每月 1000 次调用、Chat 端点按模型限速**，每月自动重置。官方 FAQ 原文口径。
- **活法**：1000 次/月适合「月度批处理一个明确任务」（如每月跑一次全库文档摘要），Command 系模型质量在线；商用再升 Production。

<a href="../platform/cohere.html">查看 Cohere 的额度与使用规则</a>

## 6. OpenRouter——免费模型聚合，按累计购买金额区分调用上限

- **规则（官方 FAQ/Limits 口径）**：`:free` 结尾模型限额取决于**累计充值金额**：
  - 未充值/累计 <$10：**50 次/天**（20 req/min）
  - **累计充值 ≥$10：解锁 1000 次/天**（20 req/min 不变）
  - $10 是正常买的可用额度（付费模型也能花），不是「门票费」；超限返回 429。
- **历史**：免费层曾 200 次/天 → 砍到 50 次/天 → 充值解锁机制。
- ⚠️ 免费模型请求可能带「数据用于训练」条款；到顶还可能被额外限流。玩法：充 $10 一次性解锁 1000/天，把 :free 模型池当「多厂商免费轮换层」，按天轮换不同厂商的免费档。

<a href="../platform/openrouter.html">查看 OpenRouter 的额度与使用规则</a>

## 7. 生存优先级总表

| 平台 | 现行免费形态 | 量级 | 最优用法 |
|---|---|---|---|
| Gemini API | 限速免费层（动态） | Flash 系数百~1000/天，Pro 系~100/天 | 日常对话+夜间批任务 |
| Antigravity CLI（原 Gemini CLI） | 免费档极紧 | 社区口径~20 agent 请求/天（低置信） | 体验为主，量活走 API 免费层 |
| Cohere | Trial Key | 1000 次/月 | 每月一次的批处理 |
| OpenRouter | :free 池 | 50/天，充 $10→1000/天 | 多厂商免费轮换 |
| Cerebras | $5 体验金 | ~1M tokens/日限速 | 一次性深度审计 |
| Groq | 限速免费层 | gpt-oss-120b 每天 20 万 Token | 低延迟原型 |
| Mistral | Studio / Vibe 免费档 | 工作区月上限 | 客户端体验 |

**三条生存法则**：① 静态数字一律以控制台实显为准（海外已全面动态化）；② 提交敏感数据前，按使用的产品、项目和地区分别确认训练用途、留存期限和功能例外；③ 把「每日限速」当节奏而不是障碍——多平台轮换，每个平台跑当日最适合它的一段任务。

Gemini 与 Groq 的数据用途条款核对于 2026-11-27。

---
**核实于 2026-10-27**。来源列表：
- Gemini 速率限制页：https://ai.google.dev/gemini-api/docs/rate-limits ｜ CLI→Antigravity 过渡（官方博客）：https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli ｜ 社区实领收缩：https://github.com/google-gemini/gemini-cli/issues/4300 、/issues/10513 、过渡讨论 /discussions/27274
- Cerebras：https://www.cerebras.ai/inference （官网直核 $5 体验金）｜ 第三方限速：pricepertoken.com
- Mistral 现状：https://docs.mistral.ai/admin/overview + Reddit r/MistralAI（403 tier_not_allowed 口径）
- Cohere Trial：官方 FAQ（每月 1000 次口径）+ dashboard.cohere.com/api-keys
- OpenRouter：官方 FAQ/Limits 口径（openrouter.ai/docs）+ CSDN 政策调整解读（2026）：<span style="overflow-wrap:anywhere">https://blog.csdn.net/weixin_41287260/article/details/159652183</span>
