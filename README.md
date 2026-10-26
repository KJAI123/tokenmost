# tokenmost.com

五层来源 AI token 折扣情报站：大模型官方（国内）/ Agent 平台 / 算力 / Token 中间商 / 大模型官方（海外）。

## 三层信息结构

| 层 | 内容 | 变化频率 | 载体 |
|---|---|---|---|
| 导航层 | 五类来源的直达入口（hao123 式） | 几乎不变 | sites.json |
| 时效层 | 折扣情报 + 折扣码（带验证时间戳） | 每天变 | deals.json |
| 个人层 | 账号库（本地 localStorage，不联网） | 用户自己 | 浏览器 |

关于「一键登录托管」的诚实边界：网页无法跨站自动填密码（浏览器安全模型）。MVP 用本地账号库 + 直达登录链接 + 指引配合浏览器密码管理器实现「准一键」；真·一键登录是二期浏览器扩展的活。折扣码卡片支持一键复制。

## 文件树

```
tokenmost/
├── index.html      # 全站（导航+卡片流+账号库抽屉）
├── sites.json      # hao123 导航数据（五层）
├── deals.json      # 折扣情报+折扣码
├── robots.txt
├── sitemap.xml
└── README.md
```

## 本地预览

    python3 -m http.server 8000

（file:// 协议无法 fetch JSON，必须走 HTTP）

## 部署

GitHub push → Cloudflare Pages（构建命令留空，输出目录 `/`）→ 绑定 tokenmost.com

## 每日 30 分钟维护流程

1. deals.json 重验 10 条 → verified_at 改今天
2. 新羊毛加草稿条目（published:false）
3. 折扣码有真实来源才填 coupon 字段（填真码时删掉 placeholder 标记）
4. 有上下架变动时同步 rss.xml（当前 12 条 published 与 RSS 一一对应）
5. git push 全站自动更新

## 数据契约

- sites.json：稳定入口层，很少改。可选 `api` 字段 `{base_url, model, env}`——配置了即可生成「⚡ 一键接入」代码（cURL/Python/Node/客户端配置），字段均可在面板中编辑，端点与模型名以官方文档为准
- deals.json：五层 category 对齐 sites 的 layer key；deal 的 provider 通过首词匹配关联 sites 条目（如「硅基流动」↔「硅基流动 SiliconFlow」）。可选 `deadline` 字段（ISO 日期）显示截止提醒，free_tier/price_low 无截止时显示「长期有效」；`placeholder:true` 标记占位示例码——卡片禁用复制并显示「示例码」角标，不与真实码同权展示
- notes 字段以 `TODO` 或 `⚠️` 开头的内容视为维护者备注，不在卡片上展示
- coupon 字段存在时卡片自动出现「复制」按钮（placeholder 除外）
- 账号库纯 localStorage（key: `tm_vault_v1`），无后端
- 「已领」标记纯 localStorage（key: `tm_claimed_v1`），配合「⭐ 已领」筛选 chip

## 一键接入（v0.2 核心特性）

羊毛卡片的「⚡ 接入」按钮：选平台 → 面板预填 base_url / 模型名 / KEY 环境变量名 → 一键生成 cURL、Python、Node.js 或客户端（Cherry Studio/ChatBox/Cline 等）配置，复制即跑通第一条 API。KEY 用环境变量传递，本站不收集任何密钥。

## ⚠️ 上线前两件事（交付纪律）

1. **替换占位折扣码**——`SILICON-MOST` 是演示复制按钮 UI 的假码（已加 `placeholder:true` 技术闸：复制禁用 + 「示例码 · 非真实优惠」角标，不会被当真实优惠发布），拿到真实码后仍必须替换并删除 placeholder 标记
2. **重验全部 verified 条目的具体数额**

（2026-10-27 老板拍板：邮箱订阅相关功能——Brevo 表单、mailto 兜底/纠错——**全部砍除，不再回加**，站内联系方式仅保留 RSS。）

折扣码的真实来源：Linux.do 的福利帖、各中间商公众号活动、官方 Agent 平台的邀请裂变——这是初期人肉收集的主战场，收到一条填一条 coupon 字段。

账号库的安全声明不能删——它给了用户存敏感信息的信任前提（本地 + 不上传），删了这套说辞，出事就是站方的责任。

## 二期路线

- 浏览器扩展（Chrome Extension 注入各平台登录页 + Bitwarden 类密码填充）实现真·一键登录
- usage API 轮询做额度监控——账号库从「记事本」进化成「面板」
