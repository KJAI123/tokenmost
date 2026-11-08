# 公众号源接入 freecloud 线 — TK 调研与推荐

核实时间：2026-11-08（本机脚本直抓 + 搜狗微信搜索 + webReader 服务端通道，零 LLM token）
结论可信度：A（全部一手实测，来源URL见各条）

## 结论（先看这行）

**首推「数字生命斯派克」入公众号雷达名册，接入位置=发现雷达轨（weixin_state.json + weixin_pipeline.py QUERIES），freecloud_sources.json 不加 mp.weixin/sogou URL 源**——mp.weixin 文章页与 weixin.sogou.com 的 robots 对通用 UA 均为全站 Disallow（2026-11-08 实测全文），pagesift 内核的 freecloud_harvest 必拒（同 huawei-free 先例），且搜狗结果页 token 轮转会让指纹 diff 常态误报。

## 一、盘点（应 freecloud 线咨询）

- 名册实况：weixin_state.json accounts 共 **15 号**（任务书说 13 已过时；weixin_accounts.json 是 state 的导出物，管线每轮重写）。
- 关键词扫描（免费服务器/白嫖/VPS/云服务器/云电脑/算力/free，weixin_state.json seen 109 条 + weixin_articles.json 40 条）：**名册内无一持续产出云服务器主题**。唯一擦边：「职场向上生长力」2026-11-01《全网最全!2026深度学习GPU算力"白嫖"资源地图》(via 搜狗:算力 白嫖，GPU 训练算力向，非云服务器/云电脑)。
- 未归因强相关历史标题（供溯源）：「别再乱买 Token 了：免费 Agent/服务器/模型额度清单」(10-28)、「保姆级教程：腾讯版小龙虾…算力,云服务器统统白嫖」(11-01)、「赛博0元购：全球 AI 算力白嫖终极版图」(11-01)。

## 二、候选推荐（按价值排序）

### 首推：数字生命斯派克

- 定位一句话：Agent 实操 + 白嫖云资源（云电脑/云服务器），freecloud 立项样例作者，与 freecloud 线定位完全重合，且横跨 token 线素材。
- 证据（核实时间 2026-11-08）：
  - 《免费 4 核 8G 云电脑，我把 Agent 搬进去了》2026-10-25，https://mp.weixin.qq.com/s/qMabG5jASD-QcFx41Y14qg ——本机直抓 HTTP 200/3.5MB/js_content 全文无验证墙；webReader 服务端通道亦全文可达（副标题：免费档 4核8G Linux 云电脑，跑 Docker/开浏览器/接 Agent）。内容=InstaBox 免费档实操，与 freecloud/findings/2026-11-06-instabox.md 互证。
  - 《Hy4 开源 770B，腾讯在发布稿里写了幻觉率》2026-11-05 ——搜狗 type=2 归因。
  - 《腾讯云又送 token 了，教你怎么领取》2026-11-06 ——搜狗 type=2 归因（token 线素材，双线价值）。
  - 活跃度：10-25 / 11-05 / 11-06 三文，周更级。
- 可抓性实测：mp.weixin 文章页静态可抓（200，无验证墙）；搜狗 type=2 文章搜索可索引归因（3/3 成功）；**搜狗 type=1 号名搜索无收录**（返回 10KB 空结果页）——按号监控只能走 type=2 关键词轮询，不能走号主页。

### 次推：小6玩AI

- 定位一句话：AI 工具实操测评号，云电脑专题已成系列。
- 证据（核实时间 2026-11-08）：
  - 《白嫖一台 AI 云电脑，Box 免费开箱》2026-11-07 ——搜狗 type=2 归因+解析直达直抓 200（正文含 云电脑/免费/8G/Box 关键词，即 InstaBox 同款免费档题材，与 T1 盯防的 instabox-pricing 呼应）。
  - 《3款国产AI助理带云电脑：谁更值得用》2026-11-02 ——搜狗 type=2 归因。
  - 《腾讯AI同传免费了！5个场景马上能用》2026-10-27 ——搜狗 type=2 归因。
- 可抓性实测：mp.weixin 直抓 200；搜狗 type=2 归因成功。

### 观察位（不入名册，靠主题词自然覆盖）

- 赛博尝鲜局：2026-11-05《白嫖 4 核 8G 服务器：千问云电脑免费开，有人连跑 7 天没停》——**自带新线索：千问云电脑免费档**（疑似阿里官方渠道，建议 freecloud 线定位官方页核实，可成 T1 候选）。
- AI工具漫谈（10-25 InstaBox 注册教程）、星标值得看（10-26《2026个人云Agent横评》）、推广月月（10-26 云电脑+一年期 VPS）：单篇相关，暂不盯。
- 秀彬的AI笔记 / 萝卜AI笔记 / 马小帮：OpenClaw 免费云服务器教程类，最新 2026-03 已过一月时效线，不设盯防。

## 三、接线方案（推荐雷达轨，附 JSON）

### A. 首选：发现雷达轨（改动最小，机制已跑通）

1. `data-research/weixin_state.json`（TK 权限文件）accounts 段加一行——**注意必须写 state，weixin_accounts.json 会被管线每轮从 state 重写**：

```json
"数字生命斯派克": {
  "last_title": "腾讯云又送 token 了,教你怎么领取",
  "last_seen": "2026-11-08 05:00 UTC"
}
```

2. 同文件 seeds 段追加样例文 URL（滚雪球自增长，轮换抓取保持该号热度）：

```json
"https://mp.weixin.qq.com/s/qMabG5jASD-QcFx41Y14qg"
```

3. `tools/weixin_pipeline.py` QUERIES 追加两个 freecloud 主题词（已实测各出强相关新文；管线 16 词轮换自动消化）：

```python
QUERIES = [...现有16词..., "免费 云电脑", "免费 云服务器"]
```

注：任务书提到的 weixin_channels 配置不存在；发现雷达的实际形态=weixin_pipeline.py QUERIES + weixin_state.json（accounts/seeds/seen）。

### B. freecloud_sources.json 留痕条目（可选，disabled 不参与采集）

若主会话希望在 freecloud 源表留痕便于审计，加一条 disabled 记录性源（**勿用活跃状态**，理由见合规段）：

```json
{
  "id": "weixin-sogou-freecloud-radar",
  "name": "搜狗微信查询位（云电脑/云服务器新文雷达，由 weixin_pipeline 代跑）",
  "url": "https://weixin.sogou.com/weixin?type=2&query=云电脑 免费 Agent",
  "patterns": ["云电脑", "云服务器", "免费", "沙盒", "InstaBox", "白嫖"],
  "disabled": true,
  "disabled_reason": "2026-11-08 TK 定性：weixin.sogou.com robots 对 * 全站 Disallow（pagesift 必拒）+ 结果页 token 轮转致指纹 diff 常态误报 → 由 weixin_pipeline（低频查询+seen 去重）代盯，本条仅留痕",
  "note": "TK 推荐 freecloud 公众号源：首推号=数字生命斯派克（10-25 InstaBox 文已直核），次推=小6玩AI（11-07 Box 免费开箱）；该查询位实测一次命中 6 号 6 篇强相关"
}
```

### C. 不推荐（明确排除）

- mp.weixin 文章 URL 直接进 freecloud_sources.json 当活跃源：①robots `Disallow: /` → pagesift 拒抓（同 huawei-free 先例）；②文章页静态不变，diff 无监控价值。
- 以搜狗 type=1 号主页当源：斯派克未被 type=1 收录（空结果页），不可行。

## 四、合规诚实修正（2026-11-08 实测两站 robots 全文）

- weixin.sogou.com/robots.txt：17 个具名蜘蛛组（Sogou web/inst/spider2/blog/News/Orion/Jike/360spider/YoudaoBot/EtaoSpider/YisouSpider 等）各 Disallow `/weixin?` 等 + **`User-agent: * / Disallow: /`，全文 0 条 Allow**——旧记录「搜狗 robots 仅限制其自家蜘蛛」只读到具名组，结论过时，本条为修正。
- mp.weixin.qq.com/robots.txt：`User-agent: * / Disallow: /`，仅 Allow 登录页/debug/qa/wiki/cgi-bin/wx/webpoc/小程序落地页——文章页 /s/ 在禁止之列。
- 影响判定：①既有 weixin 管线（weixin_discover/weixin_pipeline 的本机直连查询与文章直抓）属老板既定实践（低频、公开页、无私密数据、限速 2.5s+），是否收敛（改走 webReader 服务端通道或人工）提请老板复核，TK 不擅自变更既有管线；②pagesift 通道（freecloud_harvest）对两站必拒，故 freecloud_sources.json 不可行；③webReader 服务端通道实测可抓全文（2026-11-08 斯派克样例文验证），为文章级核实的合规替代。
- 红线执行情况：本轮未绕任何反爬，未碰登录后内容与个人数据；所有请求限速 ≥2s；搜狗 antispider 未触发。

## 五、本轮零 token 账目

全程 4 组 python 脚本（robots×3、mp.weixin 直抓×4、搜狗 type=1/2×7+/link 解析×3、候选池扫描×1）+ webReader×1，无 LLM 调研开销。新增可沉淀模式：搜狗新版账号字段=`<span class="all-time-y2">号名</span>`（旧正则 copy_under 已失效——weixin_discover.py/weixin_pipeline.py 的 account 提取需按此修复，归属主会话裁决）。
