# 部署指南（GitHub → Cloudflare Pages）

本仓库已 `git init` 并提交，随时可推。全程约 5 分钟。

## 1. 推到 GitHub（老板操作，约 1 分钟）

```bash
cd tokenmost/

# 方式 A：装了 gh CLI（推荐，自动建仓库）
brew install gh && gh auth login
gh repo create tokenmost --public --source=. --push

# 方式 B：网页建仓后手动推
#   1. 打开 https://github.com/new ，名称 tokenmost，Public，其余默认
#   2. 复制仓库地址后：
git remote add origin git@github.com:<你的用户名>/tokenmost.git
git push -u origin main
```

## 2. 接 Cloudflare Pages（老板操作，约 3 分钟）

1. 打开 https://dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. 授权并选中 `tokenmost` 仓库
3. 构建设置：
   - Framework preset: **None**
   - **Build command: 留空**
   - **Build output directory: `/`**
4. Save and Deploy —— 默认得到 `tokenmost.pages.dev`
5. 绑定主域：Pages 项目 → **Custom domains** → **Set up a domain** → 填 `tokenmost.com`（域名 DNS 在 Cloudflare 托管时自动加 CNAME，零配置）

## 3. 之后每次更新

```bash
# 改完 deals.json / sites.json / index.html 后：
git add -A && git commit -m "情报更新 YYYY-MM-DD" && git push
```

Cloudflare Pages 自动构建，约 1 分钟后全站生效。

## 上线检查单（推送前最后一眼）

- [ ] deals.json 里无 `placeholder:true` 的真实化折扣码（占位码有技术闸，可带占位上线，见 README）
- [ ] `verified_at` 全部刷新为当日
- [ ] rss.xml 条目数与 deals.json `published:true` 一一对应
- [ ] 免责声明在页脚（勿删）
