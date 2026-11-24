# FreeLLMAPI 实测：本地免费路由与 NVIDIA 接入

2026-11-21：三家提供方共五次真实调用通过：OVH、Kilo 与使用本机 Key 的 NVIDIA。

FreeLLMAPI 在本机转发请求，免费额度由各上游提供。11 月 21 日实测的 OVH 和 Kilo 通道可免 Key，NVIDIA 通道需自备 Key。可用模型、额度和限速以各上游规则为准。

## 实测结果

使用项目源码服务，独立数据库，仅监听本机；前三次使用免 Key 通道，后两次只启用 NVIDIA Key；没有绑定支付方式。

- 普通生成：OVH / Llama 3.3 70B，HTTP 200，17+25 回答 42；本次 1.796 秒。
- 流式生成：Kilo / Auto Free，回答 42 并收到结束标记；本次 1.963 秒，响应报告 cost=0。
- 默认 auto：路由至 OVH / Qwen3.8 27B，HTTP 200，回答 `ROUTER_OK`；本次 1.781 秒。

- NVIDIA 普通生成：Nemotron 3.5 Lightning，HTTP 200，回答 42；本次 2.003 秒。
- NVIDIA 流式生成：同模型返回 42 并收到结束标记；本次 1.487 秒。流式用量字段标记为估计值。

这是五次短请求的结果，不代表长期速度或全部模型可用。未测试故障切换、长上下文、桌面安装包或整月额度。模型身份依据上游响应与路由记录，未做独立模型指纹验证。

## 一个真实遇到的目录过期问题

NVIDIA 的 GPT-OSS 20B 请求返回 HTTP 410，错误说明该模型已于 2026-11-18 停服，月度目录仍保留该条目。本轮已把它排除在本机 Key 使用范围外，改测当前官网列出的 Nemotron Lightning。接入时从本地 `/v1/models` 读取统一模型 ID；原厂 ID 或另一个提供方的简称不一定等价。

## “74 亿/月”怎么理解

它是路由软件。多个平台各自提供免费层，路由器帮助选择和切换；填一把 NVIDIA Key 只能使用对应 NVIDIA 权限。

原笔记为 74 亿/月、34 家、635 端点；11 月 21 日项目仓库的宣传已改为约 101 亿/月、87 家、1,313 端点。这些是项目汇总口径，TokenMost 没有实测全部容量，也不把它计入额外到账额度。免费版目录约滞后最新目录 30 天。

## 接入步骤

1. 从项目官方 Releases 选择匹配系统的桌面版本，或按官方文档自托管。
2. 先使用目录内支持匿名的通道，在试验场发一条简单请求；本轮 OVH 和 Kilo 已测试。
3. 需要 NVIDIA 时，进入官方 build.nvidia.com，完成账号、开发者计划及手机短信验证，在官方页面生成 Key。
4. 在本机 FreeLLMAPI 的 Keys 页面添加 NVIDIA Key；模型和余量以自己的账号为准。
5. 在本机界面取得统一 API Key。客户端指向实际本地地址并使用 model=auto；服务端默认端口 3001，桌面版以实际显示地址为准。

NVIDIA 当前要求先完成手机短信验证，才能生成 API Key。本轮账号页面显示最高 40 请求/分钟；已用短期 Key 测通上述模型，没有固定 Token 月赠额可折算。

## 来源与复现边界

- [FreeLLMAPI 项目仓库](https://github.com/tashfeenahmed/freellmapi)
- [NVIDIA 官方 API Quickstart](https://docs.api.nvidia.com/nim/docs/api-quickstart)
- [Kilo 官方匿名调用规则](https://kilo.ai/docs/gateway/authentication)
- [OVH 官方接入说明](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-endpoints-getting-started)
- [本轮脱敏调用记录 JSON](https://tokenmost.com/guides/freellmapi-smoke-20261121.json)

源码版本：`7ad9097fd9d83bc3e1af0f925ea813a913b18dde`；免费目录 monthly v2026.11.19。各提供方限额、适用地区与数据规则独立生效，适合按项目说明做个人测试。
