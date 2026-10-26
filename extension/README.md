# TokenMost 羊毛助手（Chrome 扩展 MVP）

真·一键登录的落地形态：账号托管在本机 + 在各平台官方登录页一键填充。**不做也不允许**自动注册、多号批量、验证码绕过——只帮你填你自己的账号密码（定位同密码管理器）。

## 安装（免上架，加载已解压）

1. Chrome / Edge 打开 `chrome://extensions`
2. 右上角开「开发者模式」→「加载已解压的扩展程序」→ 选本目录（`extension/`）

## 使用

1. **配置站点**：popup 底部把站点地址改成你的部署地址（如 `https://xxx.github.io/tokenmost`），保存后「今日羊毛」自动显示最新 3 条
2. **添加托管**：选平台 + 手机号/邮箱 + 密码（密码可留空，仅存本机 `chrome.storage.local`）
3. **一键填充**：先在浏览器打开该平台官方登录页 → 点扩展 → 该账号条目「✍️ 填充本页」→ 账号密码自动填入，检查后手动点登录
4. **导入**：tokenmost 网站账号库「导出备份」的 json 可直接导入（不带密码，导入后逐个补）

## 安全边界（务必读）

- 密码**仅存本机**（chrome.storage.local），不上传、不同步、**不加密**——公共设备勿用；高敏感账号请用 Bitwarden 等专业密码管理器
- 扩展只在「你点击填充」时向当前页注入脚本（activeTab 权限），无后台常驻、不读其他页面、不发起任何网络请求（拉取你自己站点的 deals/sites json 除外）
- 合规红线：仅填充本人账号；不支持也不提供批量注册/接码/验证码绕过

## 文件

- `manifest.json` MV3（permissions: storage/activeTab/scripting/clipboardWrite）
- `popup.html/js` 面板（今日羊毛 + 托管列表 + 添加/导入/配置）
- `fill-core.js` 填充引擎（启发式定位账号/密码框，React 受控组件兼容）——popup 与注入共用一份
- `test-login.html` 回归页（本地 `python3 -m http.server` 后访问 `/extension/test-login.html` 验证填充）

## 已知限制（MVP）

- 填充依赖登录页有可见密码框；短信验证码登录模式会提示「先切到密码登录」
- 密码框启发式：取页面第一个可见密码框，账号框按 name/id/placeholder 关键词匹配，兜底取密码框前最后一个文本框——冷门布局可能填错位置，永远让用户确认后再点登录
