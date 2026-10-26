# 部署指南（GitHub Pages 全自动，2026-10-27 老板拍板砍掉 Cloudflare）

> 全线只用 GitHub 一个平台：代码、每日自动同步、站点托管一站完成。仓库需 **Public**（Actions 与 Pages 对公共仓免费）。

## 1. 推到 GitHub（唯一手工步骤，约 2 分钟）

```bash
cd tokenmost/

# 方式 A：装了 gh CLI（推荐，自动建仓库）
brew install gh && gh auth login
gh repo create tokenmost --public --source=. --push

# 方式 B：网页建仓后手动推
#   1. https://github.com/new ，名称 tokenmost，Public，其余默认
#   2. 复制仓库地址后：
git remote add origin git@github.com:<你的用户名>/tokenmost.git
git push -u origin main
```

推上去之后两个工作流自动就位：
- **daily-sync**：每日北京 06:30 / 18:30 自动抓 32 个数据源 → 更新数据 → bot 自动提交
- **deploy-pages**：main 一有提交（含 bot 提交）自动发布全站

## 2. 打开 Pages（仓库里点两下）

repo **Settings → Pages → Build and deployment → Source 选「GitHub Actions」**。
之后 `https://<用户名>.github.io/tokenmost/` 就是线上站。

## 3. 绑主域 tokenmost.com（可选）

1. repo **Settings → Pages → Custom domain** 填 `tokenmost.com` → Add
2. 域名 DNS 加两条记录：
   - `@` A 记录：`185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`
   - `www` CNAME：`<用户名>.github.io`
3. 回 Pages 页勾选 **Enforce HTTPS**

## 4. 之后零操作

每日 2 次自动同步、自动发布；人工只剩每天看一眼 `review-queue.md`（约 5 分钟）。

## 上线检查单（推送前最后一眼）

- [ ] deals.json 里无 `placeholder:true` 的真实化折扣码（占位码有技术闸，可带占位上线，见 README）
- [ ] `verified_at` 全部刷新为当日
- [ ] rss.xml 与 deals.json `published:true` 一一对应（`python3 tools/check.py` 自动保证）
- [ ] 免责声明在页脚（勿删）；账号库安全声明勿删（含 API Key 仅本地承诺）
