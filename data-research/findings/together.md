# Together AI — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch（Together 官方模型页 + LiteML/TrueFoundry 定价追踪，2026-10 数据）
- **数据可信度**: 中高（官方模型页存在 + 第三方定价追踪一致；定价页原文未逐字直核）

## 结论（与主数据互证）

**与主数据一致**。deals.json `together-free`「Prism-ML/Ternary-Bonsai-27B 输入输出全免费；together/Tev1-4B-experimental 输出免费」逐项核实成立。

## 明细

| 项目 | 主数据 | 独立核实 | 结论 |
|---|---|---|---|
| Ternary-Bonsai-27B | 输入输出全免费 | LiteML 定价追踪（2026-10）：input/output 均 free；256K 上下文 | ✅ |
| Tev1-4B-experimental | 输出免费 | 官方模型页：Output/1M Free（Input $0.04/1M 收费） | ✅（主数据只主张输出免费，无出入） |

背景：Bonsai 系列权重 Apache 2.0 开源可自部署；Together 同期其他模型（Kimi K3 $3/$15 等）均收费——免费款属厂商推广位，**清单变动风险高，适合 harvest 盯防**。

## 来源

- 官方模型页: https://www.together.ai/models/prism-ml-ternary-bonsai-27b
- 定价追踪: https://models.litellm.ai/providers/together_ai

## 待办

- [ ] 建议将 together.ai 模型/定价页纳入 harvest_sources.json（免费推广位变动快）
- [x] 互证结论：与主数据一致（verify_by:search，2026-10-27）
