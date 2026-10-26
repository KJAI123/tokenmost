# 智谱 BigModel — 调研发现

- **核实时间**: 2026-10-27
- **核实方式**: WebSearch 多源交叉（官方定价文档 + 第三方汇总）
- **数据可信度**: 高（赠送额度与免费模型双源一致；具体模型价格以官方页为准）

## 结论（可直接进 deals.json）

新用户注册送 **2000 万 Tokens 体验包**（代金券制，通常约 1 个月有效）；**GLM-4-Flash** 等模型长期免费调用；另有 GLM Coding Plan 低至 20 元/月（适配 Claude Code / Cline）。

## 明细

| 项目 | 内容 |
|---|---|
| 注册赠送 | 2000 万 Tokens 体验包，代金券有效期约 1 个月 |
| 免费模型 | GLM-4-Flash（2024 年 0.1 元/M 起，后转长期免费）、GLM-Z1 系等；免费清单以控制台为准 |
| Token 换算 | GLM 系列与汉字约 1:1.6（官方文档） |
| 付费亮点 | GLM Coding Plan 20 元/月起 |

## 来源

- 官方定价: https://docs.bigmodel.cn/cn/guide/start/pricing
- 官方活动页: https://docs.bigmodel.cn/cn/update/promotion
- 第三方汇总: 网易《2026 免费大模型 API 盘点》 https://www.163.com/dy/article/KO5TL2AE05314EKW.html
- 社区维护清单: https://github.com/guihuashaoxiang/FreeLLM-API-KeyHub

## 待办

- [x] ~~确认注册赠送当前形态~~ 采集器首轮已核实：注册礼包 2500 万 + 邀请机制（双方各 2000 万，月上限 10 人 = 2 亿 Tokens/月），见下
- [ ] GLM-5.3 系列当前单价已由采集器抓到（GLM-5 输入 4–6 元/M），可做站内比价

## 采集器补充发现（2026-10-27 首轮 harvest，来源同官方活动页）

- 邀请有礼：邀请人与被邀请人**各得 2000 万 GLM-4.5-Air Tokens**（刊例价 58 元），被邀请人额外得 **2500 万新客礼包**；每人每月最多成功邀请 10 位，**月累计最高 2 亿 Tokens 免费额度**
- 当日定价表实测：GLM-4-Flash-250414 与 GLM-Z1-Flash 标注「免费」；GLM-5 输入 4–6 元/M、输出 18–22 元/M（输入 ≥32K 档）
- 注意：智谱定价表大量条目标注「限时免费」，时效性敏感，harvest 高频盯防对象
