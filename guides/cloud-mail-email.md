# 0 元搭「无限邮箱」攻略：一个域名收无限独立邮箱（Cloudflare + cloud-mail 自部署）

> 核实于 2026-11-11 ｜ 难度：★★☆ ｜ 特点：收信完全 0 元、每平台一个独立邮箱防泄漏溯源、Catch-all 全收任意前缀

## 能拿到什么

薅羊毛刚需工具：批量注册各平台账号时，用**一个域名开出无数个独立邮箱地址**——`github@你的域名`、`shopping@你的域名`、`netflix@你的域名`，每个地址独立收件箱互不干扰。哪个平台开始给你发垃圾邮件，就知道是谁泄漏的。

比 Gmail 的 `+号` 别名强：很多网站注册时**拒绝带 `+` 的邮箱**，独立域名造的地址看起来就是正常邮箱，无此问题。

整套系统跑在 Cloudflare 免费资源上（Worker + D1 + KV + Email Routing），**不需要买服务器，收信 0 元**。开源项目：`github.com/maillab/cloud-mail`。

## 前置条件

1. Cloudflare 账号（免费版够用）
2. 一个域名（免费二级域名也行，但**发信**需要自有顶级域名，见下文限制）
3. 本机 Node.js + pnpm + Wrangler CLI

## 部署八步（实测口径）

1. **域名托管到 Cloudflare**：NS 改到 Cloudflare，等状态 Active（免费二级域名实测顺畅无卡点）。
2. **部署 Worker**：`git clone https://github.com/maillab/cloud-mail.git` → **⚠️ 进 `mail-worker/` 手动跑 `pnpm install`**（README 只装前端依赖，跳过这步 `wrangler deploy` 会报 `drizzle-orm` 解析失败）→ 配好 `wrangler.toml`（绑定名必须叫 `db`/`kv`，vars 里 `domain`/`admin`/`jwt_secret` 一个不能错）→ `npx wrangler deploy`。
3. **建 D1/KV/R2 并绑定**：D1 建库绑 `db`；KV 建命名空间绑 `kv`；R2 附件功能可选绑 `r2`（R2 要进 Billing 确认订阅，免费 10GB/月但**可能需要绑卡**）。
4. **环境变量**：Worker Settings → Variables，`domain` 是 JSON 数组格式 `["xxx.ccwu.cc"]`；`jwt_secret` 建议 32+ 字符随机串。
5. **绑自定义域名并初始化**：Worker → Domains 加 `mail.你的域名`，浏览器访问 `https://mail.你的域名/api/init/<jwt_secret>`，返回 `success` 才算建表成功（返回 Database not initialized = secret 不匹配）。
6. **打开收信通道**：Cloudflare → 域名 → Email Routing → 路由规则设 **Catch-all → 转发到 cloud-mail Worker**；确认 Trigger Events 出现 `*@你的域名`。
7. **注册管理员**：访问 `/login` 注册第一个账号（自动成为管理员），**立刻去系统设置关闭「开放注册」**。
8. **收信实测**：从 Gmail 发一封到任意 `test@你的域名`，60 秒内入库可见。

## ⚠️ 关键坑（文档没写的四处）

1. **`noRecipient` 默认坑**：KV 设置里默认 `1` = 收件人不存在直接 reject，**邮件凭空消失不留痕迹**。想要「任意前缀照单全收」（无限邮箱的核心），把 `noRecipient` 改为 `0`；或先在前端把要用的地址创建好。
2. **Worker 后端依赖要手动装**（见第 2 步）。
3. **Wrangler OAuth 授权**：Windows 非交互环境常超时，重跑一次命令、浏览器点允许即可。
4. **Email Routing API 的 `name` 字段传完整域名会报错**，留空才正常。

## 发信要钱（收信免费）

| 方案 | 费用 | 条件 |
| --- | --- | --- |
| Resend + 自有域名 | 域名 ~$10/年 | ⚠️ 拒绝免费公共域名池（实测报 "We don't allow free public domains"） |
| Cloudflare Email Sending | Workers Paid $5/月 | Free 计划直接锁（报 `email.sending_disabled`） |
| 其他 SMTP/API 服务 | 各家免费额度 | 看域名策略 |

**纯白嫖结论：收信无限免费；发信要么花域名钱（推荐，$10/年 顺带解决公共域名问题），要么 $5/月订阅。**

## 附：参数速查

- 邮箱前缀最短长度：`minEmailPrefix`（默认 1，可改长防乱注册）
- 多邮箱开关：`manyEmail` / `addEmail`（0=允许）
- 初始化：`/api/init/<jwt_secret>` → success
- 收信延迟：< 60 秒
