# GEO 账号扩张探查 — 6 开发者社区注册页实测

> 探查日期：2026-11-19 23:31–23:48（9223 无头 Chrome for Testing 158，全新 profile 无登录态）
> 方法：开注册页 → CDP 读 DOM 表单/验证方式/第三方登录 → 截图 → 关标签。**未提交任何注册动作**（待老板确认后执行）。
> 截图：`/tmp/geo-*.png`

## 总结论（先看这个）

| 平台 | 注册验证 | 自动化判定 |
|---|---|---|
| 博客园 | 邮箱 + **+86 手机号（表单硬性字段）** + invisible reCAPTCHA | **需要老板手机码**（门槛最高：手机+谷歌盾双卡） |
| 51CTO | 手机号 + 阿里云滑块(nc_1) + **短信验证码** | **需要老板手机码**（且 www 主站被 EdgeOne 拦，走 home 子域） |
| 思否 SegmentFault | 手机号 + **短信验证码** | **需要老板手机码** |
| 开源中国 OSCHINA | 手机号 + **短信验证码**（未注册手机验证后自动注册） | **需要老板手机码** |
| 腾讯云开发者社区 | 微信扫码(默认) / 邮箱路径**仍要 +86 手机短信码 | **需要老板手机码**，深绑腾讯生态 |
| 阿里云开发者社区 | 扫码(阿里云APP/支付宝/钉钉) / 账号路径 **+86 手机+短信码 | **需要老板手机码**，深绑阿里生态 |

**结论：6 家无一"纯邮箱可自动注册"。全部要 +86 手机短信码 → 全部走老板确认流程。**
唯一潜在旁路（未验证）：开源中国、博客园、51CTO 支持 GitHub 第三方登录，若用 GitHub OAuth 首登后只需绑邮箱即可建号，可绕开国内手机号——但三家的"第三方首登是否强制绑手机"未实测（涉及真实 OAuth 动作，待老板点头再试）。

---

## 1. 博客园 cnblogs.com

- 注册 URL：`https://account.cnblogs.com/signup?returnUrl=https%3A%2F%2Fwww.cnblogs.com%2F`（入口：登录页底部"立即注册"）
- 表单字段（Angular Material，DOM 实测）：
  - `autocomplete=email — 邮箱
  - `tel-country-code — 国码，固定显示 **+86
  - `tel-national — "请输入中国内地的手机号
  - `nickname — 昵称
  - `password ×2（new-password）— 密码 / 确认密码
- 验证方式：**invisible reCAPTCHA ×2（recaptcha.net，sitekey 6LfFqK0U… / 6Lci1a0U…）**，提交时静默触发，风险分高会弹图片挑战。页面未见邮箱验证链接字段（注册后是否发验证邮件未测，不提交不知道）。
- 第三方登录（登录页实测）：**微信、QQ、GitHub。
- 截图：`/tmp/geo-cnblogs-signup.png（注册表单）、/tmp/geo-cnblogs-signin.png（登录页）
- 判定：**手机号是表单必填项 → 老板手机码 + reCAPTCHA 双重门槛。自动化难度：高。

## 2. 51CTO

- ⚠️ 首要障碍：`https://www.51cto.com/ 被 **Tencent Cloud EdgeOne 567 硬拦截（"请求已被站点的安全策略拦截，IP 级别，等了多轮不解除；截图 `/tmp/geo-51cto-home.png（请求 ID 7046654044165748907）。`login.51cto.com 不存在（NXDOMAIN）。
- ✅ 可用通道：**`https://home.51cto.com/（51CTO 账号通行证，老门户，未被拦）
  - 注册 URL：`https://home.51cto.com/user/register?regtype=mobile（登录页"手机号注册链接直达）
- 表单字段（DOM 实测）：
  - `registerName — "请输入11位手机号
  - `nc_1_captcha_input — **阿里云 NoCaptcha 滑块（点"立即注册后出现）
  - `verify_code — 短信验证码
  - `username — 用户名；`password — 密码；`checkbox — 同意《51CTO服务条款》《隐私协议》；`commit — 提交
- 第三方：**微信 / QQ / 微博 / GitHub 四图标（实测 QQ 走 `home.51cto.com/third-party/auth?type=qq）
- 截图：`/tmp/geo-51cto-signup.png
- 判定：**手机短信码 + 滑块 → 老板手机码。注意自动化全程只能走 home.51cto.com，www 域对本机 IP 已拉黑。

## 3. 思否 SegmentFault

- 注册 URL：`https://segmentfault.com/user/register（直接可达；`/login 是 404，登录在 `https://segmentfault.com/user/login）
- 表单字段（DOM 实测）：
  - `name — 你的名字
  - `phone — 手机号
  - 短信验证码 + 获取验证码按钮（无 name/id，input-group）
- 验证方式：**短信验证码（点获取验证码时含前端 captcha 元素，class*="captcha 命中）
- 第三方（登录页实测）：**微信登录（唯一）；登录方式 = 手机+验证码 / 免密码 / 密码。登录页明示 **"新手机号将自动注册**（注册登录同一条通道）。
- 截图：`/tmp/geo-sf-signup.png（注册）、/tmp/geo-sf-login.png（登录页）
- 判定：**手机短信码 → 老板手机码。流程最简单的一家（3 个字段）。

## 4. 开源中国 OSCHINA

- 注册 URL：`https://www.oschina.net/home/login（首页"注册按钮即指向登录页，登录注册合一）
- 表单字段（DOM 实测，Ant Design）：
  - 免密登录 tab：`form_item_mobile — 手机号码 + `form_item_code — 短信验证码 + 发送验证码
  - 密码登录 tab：`form_item_account — 手机号/用户名/邮箱 + `form_item_password — 密码
  - 两个 checkbox（同意《服务条例》《隐私声明）
  - 提交按钮文案即 **"登录/注册
- 验证方式：**短信验证码（发送时含 captcha 元素）；**"未注册的手机号码在验证后将自动登录** = 手机号即注册。
- 第三方：**Gitee 独立大按钮（使用Gitee登录）+ 微信 / QQ / GitHub 三图标。
- 截图：`/tmp/geo-oschina-signup.png、首页 `/tmp/geo-oschina-home.png
- 判定：**手机短信码 → 老板手机码。Gitee OAuth 是潜在旁路（Gitee 本身注册也要手机号，除非已有 Gitee 账号）。

## 5. 腾讯云开发者社区

- 社区首页 `https://cloud.tencent.com/developer：登录/注册按钮（JS 弹统一账号面板）+ **"邀请作者入驻 → `https://cloud.tencent.com/developer/support-plan-invitation = **自媒体同步曝光计划**（社区作者入驻的正式通道：需先有腾讯云账号 → 经邀请链接提交计划申请 → 审核通过；邀请双方得 30/100/180 元代金券，榜单可查）。
- 注册 URL：`https://cloud.tencent.com/register
- 注册方式（DOM+截图实测）：
  - **微信扫码注册（默认 tab，open.weixin.qq.com qrconnect iframe，appid wxca396cd1df083b9d）
  - **邮箱注册 tab：email + password + confirmPassword + **phoneNumber（+86，请输入验证码）→ **邮箱路径也强制 +86 手机短信码
  - 其他注册方式：**QQ、企业微信、小程序公众号 —— 全部腾讯生态内闭环
- 登录页 `https://cloud.tencent.com/login：微信（默认）/**企业微信** 扫码 + 其他：QQ / 小程序公众号 / 子用户 / 通行密钥 / 邮箱登录。
- 截图：`/tmp/geo-tc-signup.png（注册，微信扫码+QQ/企微/小程序公众号）、/tmp/geo-tc-login.png、/tmp/geo-tc-invite.png（入驻计划页）
- 判定：**需要老板手机码（任何路径）+ 微信生态强绑定。入驻社区另有内容审核关（计划申请要过审）。

## 6. 阿里云开发者社区

- 社区首页 `https://developer.aliyun.com：注册直达 `https://account.aliyun.com/register/qr_register.htm?oauth_callback=https%3A%2F%2Fdeveloper.aliyun.com%2F；创作者入驻 = **创作者中心 `https://developer.aliyun.com/creatorcenter/home（登录后可见权益）。
- 注册页（DOM+截图实测）：
  - 左侧：**扫码注册 — 用 阿里云APP / 支付宝 / 钉钉 扫；**其他方式图标：**支付宝、淘宝、(橙)旗下 App、**微博、钉钉 —— 深绑阿里生态
  - 右侧账号表单（passport.aliyun.com iframe，OOPIF 上下文内实测）：
    - `mobile — **+86 手机号（请输入）
    - `mobileCode — 短信验证码 + 获取验证码
    - `agreement — checkbox（用户协议、隐私政策、产品服务协议）
    - 立即注册按钮；初始态未见滑块（点击获取验证码后可能触发 nocaptcha，未实测）
- 登录页 `https://account.aliyun.com/login/login.htm：扫码（阿里云APP/支付宝/钉钉）+ 其他方式：账密登录 / 手机号登录 / 通行密钥 / RAM 登录。
- 截图：`/tmp/geo-ali-signup.png（一屏全见：扫码+图标+手机表单）、/tmp/geo-ali-login.png
- 判定：**需要老板手机码。淘宝/支付宝一键是登录通道（扫码授权），不是绕开手机号的注册通道。

---

## 老板决策清单

1. **手机资源：6 家全部需要 +86 手机短信码。需要一个老板可控的国内手机号（接码平台风险自担，探查不代决定）。短信码有时效（60s–5min），执行时需老板在线转发或接码 API。
2. **执行顺序建议（按流程简单度）：思否（3 字段）→ 开源中国（手机即注册）→ 51CTO（home 域，滑块）→ 腾讯云（注册+入驻申请两步）→ 阿里云（注册+创作者中心两步）→ 博客园（reCAPTCHA，风险最高，放最后）。
3. **GitHub 旁路待验证：博客园/51CTO/开源中国 有 GitHub 登录；若 GitHub OAuth 首登允许只绑邮箱建号，可省手机号——需老板批准后用真 GitHub 账号试一次才知道。
4. **51CTO 注意：www 主站对本机 IP 已被 EdgeOne 拉黑（567），注册/发文章都走 home.51cto.com + app 子域，主站流量可能与发帖冲突。
5. 腾讯云"自媒体同步曝光计划**支持邀请链接裂变（30/100/180 元代金券激励），多账号矩阵可互相邀请。

## 覆盖度说明

- 全部实测基于 9223 无头 Chrome（Chrome for Testing 158.0.8127.18，全新 profile，无 cookie/登录态）。
- 所有探查标签已关闭，无僵尸标签；浏览器保持运行（127.0.0.1:9223）。
- 未提交任何注册表单、未点击任何发送验证码按钮（只读 DOM + 截图）。
- 思否注册页 body.innerText 仅 34 字符属正常（placeholder 不计入 innerText），表单实际渲染完整。
