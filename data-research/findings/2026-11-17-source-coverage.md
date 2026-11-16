# 2026-11-17 · 信源覆盖复核

优先补「官方页或候选已存在，权益未上架」的缺口。下列结论为公开文档核验，未逐个注册、充值或实际调用。

| 条目 | 核验依据与处理 |
|---|---|
| Kilo Gateway | [官方模型文档](https://kilo.ai/docs/gateway/models-and-providers)：已有采集和导航，补 Auto Free、模型变化和匿名限额。 |
| LLM7.io | [官方限额](https://docs.llm7.io/limits)：已有采集和导航，补 Free Token 24 小时使用上限并保留原始单位。 |
| Cloudflare Workers AI | [官方计费](https://developers.cloudflare.com/workers-ai/platform/pricing/)：采集已覆盖，补每天 Neurons；之前的 Workers HTTP 免费层独立保留。 |
| Hugging Face Inference Providers | [官方计费](https://huggingface.co/docs/inference-providers/pricing)：推理文档已采集，新增免费账户月配额，与 Spaces 公开托管分开。 |
| Vercel AI Gateway | [官方计费](https://vercel.com/docs/ai-gateway/pricing)：候选转公开；免费额度只用于合资格模型，买入额度后停止月免，未沿用历史「所有模型」表述。 |
| Atlassian Rovo Dev | [官方积分说明](https://support.atlassian.com/rovo/docs/view-your-rovo-dev-credit-usage/)：候选转公开；明确 Jira 站点启用条件。 |
| Lightning AI Studio | [官方定价](https://studio.lightning.ai/pricing/)：候选转云服务器专区；仅发布固定的免费基础 CPU Studio，GPU 小时随规格与资格变化，不合并宣传。 |
| GitHub Copilot Free | [官方用量计费](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing)：更正原条目，保留 2,000 次补全，聊天改用 AI Credits，移除由旧 50 次聊天推算的 Token 当量。 |

后续优先复核：讯飞星辰模型广场的 0 元档和实际限额（需官方控制台）；七牛云免费模型的当前可调用状态（需官方模型页）；千问云电脑的登录后入口与账号资格（公开网页证据不足）；OVHcloud AI Endpoints 候选（区分限时赠金与常设免费权益）。AIHOT 等聚合条目已经收录的，下一轮按优先级补官方直接证据，不重复发布。

补核已上架的 AIHOT 情报，保留原聚合链接，并加上官方原文：

- [Rime](https://www.rime.ai/pricing)：确认每月 $50，补无需绑卡、未用额度不结转及 Flex 超额计费条件。
- [LiveKit](https://docs.livekit.io/deploy/admin/quotas-and-limits/)：确认 Build 免费档每月 $2.50，补超额即停，去掉未由官方说明支持的「每月 1 日」口径。
- [ElevenLabs](https://elevenlabs.io/pricing)：确认每月 10,000 credits，补免费 TTS 的非商业使用和署名条件。
- [Zed](https://zed.dev/education)：确认学生计划 $10/月、为期 12 个月、之后自动降为 Free；不承诺具体模型长期可用。

清理采集覆盖：修复 `bailian-main`、`console-main`、`docs-main` 三组重名，共 18 个不同地址。旧的快照比较按 ID 覆盖同组前面的地址；改为独立 ID 后，各来源分别比较。旧快照按 URL 兼容，无需覆盖历史文件。
