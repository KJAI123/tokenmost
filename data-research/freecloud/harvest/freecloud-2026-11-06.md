# freecloud 采集快照 2026-11-06

- 采集时间: 2026-11-06T15:52:20Z（pagesift 内核·零 LLM 参与·遵守 robots.txt·两次观测确认制）
- 源数: 42 | 🔔变化: render-pricing | 👀观察中: 无 | 🌱首跑基线: 25 | 失败: 无

##    InstaBox 定价（Agent 云电脑·文章样例主角）（instabox-pricing）
- 状态: ok | https://instabox.sh/pricing
- 🔎 **1 MiB (`truncated`), and bytes that are not UTF-8 become U+FFFD (** `output fail with a broken pipe. Exec output is UTF-8 text: without streaming each stream is cut at 1 MiB (`truncated`), and bytes that are not UTF-8 become U+FFFD (`invalidUtf8`), so read files with `GET /v1/machines/{id}/files/content` or `instabox pull`/`cp`, no`
- 🔎 **4 vCPUs / 8 GiB by default, a 16 GiB root disk (8 GiB on `herdr` an** `r. - Machine: a Firecracker microVM, Debian 13 (trixie) amd64 (`ci`: Ubuntu 24.04), kernel 6.18.60, 4 vCPUs / 8 GiB by default, a 16 GiB root disk (8 GiB on `herdr` and `orca`) and a 20 GiB persistent disk at `/data` (home is `/data/home`). Python 3.13 with `python3`
- 🔎 **20 GiB persistent disk at `/data` (home is `/data/home`)** `kernel 6.18.60, 4 vCPUs / 8 GiB by default, a 16 GiB root disk (8 GiB on `herdr` and `orca`) and a 20 GiB persistent disk at `/data` (home is `/data/home`). Python 3.13 with `python3 -m venv` and pip on every template but `ci`, which has Python 3.12 with`
- 🔎 **1 GiB on 2/4, ~2 GiB on 4/8)** `10 days, in snapshots; your own `TMPDIR` is kept) and `/tmp` is capped at a quarter of guest RAM (~1 GiB on 2/4, ~2 GiB on 4/8). Older machines (`echo $TMPDIR` empty): `/tmp` is about half guest RAM (~2 GiB on 2/4, ~4 GiB on 4/`
- 🔎 **2 GiB on 2/4, ~4 GiB on 4/8); for big staging set `TMPDIR=$HOME/t** `GiB on 2/4, ~2 GiB on 4/8). Older machines (`echo $TMPDIR` empty): `/tmp` is about half guest RAM (~2 GiB on 2/4, ~4 GiB on 4/8); for big staging set `TMPDIR=$HOME/tmp` (home is `/data/home`; on `agent-browser`, `universal` and `t3` the top of `/data` is the user's`
- 🔎 **4 GiB (2/4: 4 GiB), listed in `/etc/fstab` so it stays on across ** `e size. - Swap: every machine gets `/data/swapfile` at its first boot, the size of its memory up to 4 GiB (2/4: 4 GiB), listed in `/etc/fstab` so it stays on across stop and start; it is skipped (and the guest agent logs why) when `/data` would keep under 1 GiB, or`
- 🔎 **1 GiB, or a tenth of the disk, free** `n across stop and start; it is skipped (and the guest agent logs why) when `/data` would keep under 1 GiB, or a tenth of the disk, free. `swapon`, `swapoff` and `mkswap` are on the user PATH (changing swap takes `sudo`). Removed (`sudo`
- 🔎 **20 GiB by default; at create it comes with the size, so leave `per** `topped: resume it, then stop it, which is what `--restart` does). - Disk: one per machine, `/data`, 20 GiB by default; at create it comes with the size, so leave `persistentDiskGiB` out (another size is `400 spec_not_allowed`; `diskGiB` is the TypeScript SDK option`
- 🔎 **1024 GiB; it grows while running (no restart) or at the next start, ** `x resize <machine> --disk N [--restart]` or `PATCH /v1/machines/{id}` `{"persistentDiskGiB": N}`: 1-1024 GiB; it grows while running (no restart) or at the next start, and shrinks only while stopped when the data plus 10% (at least 1 GiB) fits (else `409 disk_too_smal`
- 🔎 **1 GiB) fits (else `409 disk_too_small`); at most 200 GiB on Pro, ** `(no restart) or at the next start, and shrinks only while stopped when the data plus 10% (at least 1 GiB) fits (else `409 disk_too_small`); at most 200 GiB on Pro, 500 GiB on Builder, 1024 GiB on Team and Enterprise (`429 quota_exceeded`). The system disk is the t`

##    E2B 定价（Agent 沙盒）（e2b-pricing）
- 状态: ok | https://e2b.dev/pricing
- 🔎 **credits (+usage costs)** `More. Free Hobby tier, and paid upgrades to cover all needs. Separate usage costs. FREE /$100 in credits (+usage costs) See our cost calculator - $100 one-time usage credit - Sessions up to 1 hour - 20 concurrent sand`
- 🔎 **credit** `usage costs. FREE /$100 in credits (+usage costs) See our cost calculator - $100 one-time usage credit - Sessions up to 1 hour - 20 concurrent sandboxes20 concurrent sandboxesThe maximum number of sandb`
- 🔎 **/month (+usage costs)** `x CPU and RAM [Start for Free](https://console.e2b.dev/sign-up?signup_source=pricing_hobby) $150 /month (+usage costs) See our cost calculator - Everything in Hobby, usage billed by the second - Sessions up to 24 hou`
- 🔎 **/mo** `an Monthly Cost Usage Cost $166 Pro Plan Base $150 Concurrency Addon $0 Total Monthly $316 /mo Max Concurrent Sandboxes100 Enterprise starts at a $2,000/mo commit, 500 concurrent included. ##`
- 🔎 **/mo commit, 500 concurrent included** `ency Addon $0 Total Monthly $316 /mo Max Concurrent Sandboxes100 Enterprise starts at a $2,000/mo commit, 500 concurrent included. ### Let us know if you need more powerful compute. If you don't see convenient times, please ema`
- 🔎 **sandbox** `sts) See our cost calculator - $100 one-time usage credit - Sessions up to 1 hour - 20 concurrent sandboxes20 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sa`
- 🔎 **sandbox** `ulator - $100 one-time usage credit - Sessions up to 1 hour - 20 concurrent sandboxes20 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sandbox CPU and RAM [Sta`
- 🔎 **sandbox** `redit - Sessions up to 1 hour - 20 concurrent sandboxes20 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sandbox CPU and RAM [Start for Free](https://console.e2`
- 🔎 **sandbox** `oxes20 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sandbox CPU and RAM [Start for Free](https://console.e2b.dev/sign-up?signup_source=pricing_hobby) $150 /`
- 🔎 **sandbox** `lator - Everything in Hobby, usage billed by the second - Sessions up to 24 hours - 100 concurrent sandboxes, expandable to 1,100 - Custom sandbox CPU and RAM [Choose Pro](https://console.e2b.dev/sign-up?s`

##    Daytona 定价（Agent 沙盒）（daytona-pricing）
- 状态: ok | https://daytona.io/pricing
- 🔎 **12GB GDDR6** `them down just as fast. Use what you need, when you need it. $200 in free compute included. GPU 12GB GDDR6 GPU 16-CORE GPU 16-CORE GPU 8-CORE GPU 32-CORE GPU 12GB GDDR6 Compute vCPU $0.0504/h`
- 🔎 **12GB GDDR6** `ree compute included. GPU 12GB GDDR6 GPU 16-CORE GPU 16-CORE GPU 8-CORE GPU 32-CORE GPU 12GB GDDR6 Compute vCPU $0.0504/h GPU ### Preemptible ($/hour) Nvidia B300 $4.08/h Nvidia B200 $3.59/`
- 🔎 **12GB GDDR6** `t them down just as fast. Use what you need, when you need it. $200 in free compute included. GPU 12GB GDDR6 GPU 16-CORE GPU 16-CORE GPU 8-CORE GPU 32-CORE GPU 12GB GDDR6 Compute vCPU $0.0504/h`
- 🔎 **12GB GDDR6** `them down just as fast. Use what you need, when you need it. $200 in free compute included. GPU 12GB GDDR6 GPU 16-CORE GPU 16-CORE GPU 8-CORE GPU 32-CORE GPU 12GB GDDR6 All billing is calculated`
- 🔎 **12GB GDDR6** `ree compute included. GPU 12GB GDDR6 GPU 16-CORE GPU 16-CORE GPU 8-CORE GPU 32-CORE GPU 12GB GDDR6 All billing is calculated per second. All billing is calculated per second. Sign up for a free t`
- 🔎 **free trial - no credit card required** `GDDR6 All billing is calculated per second. All billing is calculated per second. Sign up for a free trial - no credit card required Sign up for a free trial - no credit card required Pay as you go with usage-based pricing Pay as`
- 🔎 **free trial - no credit card required** `illing is calculated per second. Sign up for a free trial - no credit card required Sign up for a free trial - no credit card required Pay as you go with usage-based pricing Pay as you go with usage-based pricing Unlock volume disc`
- 🔎 **credit card required** `ing is calculated per second. All billing is calculated per second. Sign up for a free trial - no credit card required Sign up for a free trial - no credit card required Pay as you go with usage-based pricing Pay as`
- 🔎 **credit card required** `ated per second. Sign up for a free trial - no credit card required Sign up for a free trial - no credit card required Pay as you go with usage-based pricing Pay as you go with usage-based pricing Unlock volume disc`
- 🔎 **credits for free** `Unlock volume discounts as you scale ##### Start-ups Daytona supports startups with up to $50k in credits for free. ##### Enterprise Designed for businesses that need larger limits, SSO, audit logs, or BYOC`

##    Modal 定价（每月免费金）（modal-pricing）
- 状态: ok | https://modal.com/pricing
- 🔎 **80 GB $ / sec** `c - Nvidia H200 SXM $ / sec - Nvidia H100 SXM5 $ / sec - Nvidia RTX PRO 6000 $ / sec - Nvidia A100, 80 GB $ / sec - Nvidia A100, 40 GB $ / sec - Nvidia L40S $ / sec - Nvidia A10 $ / sec - Nvidia L4 $ / sec - Nvidi`
- 🔎 **40 GB $ / sec** `Nvidia H100 SXM5 $ / sec - Nvidia RTX PRO 6000 $ / sec - Nvidia A100, 80 GB $ / sec - Nvidia A100, 40 GB $ / sec - Nvidia L40S $ / sec - Nvidia A10 $ / sec - Nvidia L4 $ / sec - Nvidia T4 $ / sec Physical core (`
- 🔎 **2 vCPU equivalent)** `- Nvidia L40S $ / sec - Nvidia A10 $ / sec - Nvidia L4 $ / sec - Nvidia T4 $ / sec Physical core (2 vCPU equivalent) *minimum of 0.125 cores per container *includes 1 TiB / mo free ## Pricing plans ### Starter B`
- 🔎 **2 vCPU equivalent)** `ptible-functions) rates of 3x list price. ### Compute costs CPU (non-preemptible) Physical core (2 vCPU equivalent) $ / core / sec *minimum of 0.125 cores per container Memory (non-preemptible) $ / GiB / sec ##`
- 🔎 **free credits** `### Starter Built for small teams and independent developers looking to level up. - $30 / month free credits - 3 workspace seats included - 100 containers + 10 GPU concurrency - Scheduled and Web Functions (l`
- 🔎 **free credits** `ss ### Team Built for startups and larger organizations looking to scale quickly. - $100 / month free credits - Unlimited seats - 5000 containers + 50 GPU concurrency - Unlimited Scheduled Functions - Custom d`
- 🔎 **credits** `Starter Built for small teams and independent developers looking to level up. - $30 / month free credits - 3 workspace seats included - 100 containers + 10 GPU concurrency - Scheduled and Web Functions (l`
- 🔎 **credits** `## Team Built for startups and larger organizations looking to scale quickly. - $100 / month free credits - Unlimited seats - 5000 containers + 50 GPU concurrency - Unlimited Scheduled Functions - Custom d`
- 🔎 **Credits and variable costs |  |  |  |** `--- | --- | | ### Workspace | | | | | Number of seats | Up to 3 | Unlimited | Unlimited | | ### Credits and variable costs | | | | | Included compute | $30 / month | $100 / month | Custom | | Included network egress | 1 TiB / mont`
- 🔎 **credits?** `billing? - ### How should I estimate the total cost of Modal Sandboxes? - ### Do I need to purchase credits? - ### Can I add more than three team members on the starter plan? - ### Can I use my AWS, GCP, or A`

## 🌱 Ona 定价（Gitpod 改名，云 IDE 免费 credits）（ona-pricing）
- 状态: ok | https://ona.com/pricing
- ⚠️ 0 命中——页面可能 JS 渲染或改版，需人工核 pattern

## 🌱 Replit 定价（云 IDE+Agent）（replit-pricing）
- 状态: ok | https://replit.com/pricing
- 🔎 **credits work?** `istakes. ## Frequently asked questions What are all the features included in these plans? How do credits work? What happens when I run out of credits? What comes with my subscription? What plan is best for m`
- 🔎 **credits?** `are all the features included in these plans? How do credits work? What happens when I run out of credits? What comes with my subscription? What plan is best for me? What is Effort-Based Pricing (pay-as-`
- 🔎 **credit card payments?** `ol what I spend on Replit? How can I see how much I'm spending? Do you offer invoicing instead of credit card payments? Do you offer annual plans at a discount? Still have questions?You can see more details in our [Bi`
- 🔎 **Agent** `cated premium support and much more *Prices are subject to tax depending on your location. Replit Agent is powered by large language models. While it can produce powerful results, its behavior is probabi`

## 🌱 bolt.new（StackBlitz 旗下 AI 全栈云开发）（bolt-new）
- 状态: ok | https://bolt.new/
- 🔎 **free** `age/personas/students.png) ## Ready to build something amazing? Try it out and start building for free`

## 🌱 Firebase Studio（原 Project IDX，Google 免费 cloud IDE）（firebase-studio）
- 状态: ok | https://firebase.studio/
- 🔎 **workspace** `The full stack AI workspace Firebase Studio accelerates your entire development lifecycle with AI agents. Build backends, fron`
- 🔎 **workspace** `. You can also customize your environment with Nix. Firebase Studio is currently available with 3 workspaces at no cost during preview. Members of the [Google Developer Program](https://accounts.google.com/A`
- 🔎 **workspace** `aign%3DFY25-Q2-firebasestudio_nextlaunch%26utm_content%3Dquickstart_gdp%26utm_term%3D-)get up to 30 workspaces. AI powered ## Build with in Firebase Work quickly and efficiently with Gemini in Firebase. Com`
- 🔎 **workspace** `nd work together Provide a URL for your early testers to preview your app and give feedback. Share workspaces with other team members to contribute to the same project at the same time. Enable everyone to wor`
- 🔎 **workspace** `t the same time. Enable everyone to work together, whether they can code or not. ![Firebase Studio workspace](https://rstr.in/google/firebase-studio/-LzIMPuLhOu) End-to-end testing ## Optimize your full-sta`
- 🔎 **Gemini** `)get up to 30 workspaces. AI powered ## Build with in Firebase Work quickly and efficiently with Gemini in Firebase. Complete a variety of tasks like coding, debugging, testing, refactoring, explaining,`

## 🌱 StackBlitz 定价（云 IDE 免费档）（stackblitz-pricing）
- 状态: ok | https://stackblitz.com/pricing
- 🔎 **free** `ojects, you do need a GitHub account to save your work or collaborate with others. You can create a free GitHub account [on their website here](https://github.com/). What is included in the free Personal`
- 🔎 **free** `create a free GitHub account [on their website here](https://github.com/). What is included in the free Personal plan? The free Personal plan includes unlimited public StackBlitz projects and Github repo`
- 🔎 **free** `ount [on their website here](https://github.com/). What is included in the free Personal plan? The free Personal plan includes unlimited public StackBlitz projects and Github repositories. If you need to`
- 🔎 **free** `ion are automatically synced to your StackBlitz Teams account. You can change individual members to free or paid users depending on what they need to access. Free users can access and edit all public proj`

## 🌱 Browserbase 定价（Agent 浏览器沙盒）（browserbase-pricing）
- 状态: ok | https://www.browserbase.com/pricing
- 🔎 **Free Plan** `rottling as you build, billed at your plan’s rate. And as always, you can get started for free. ## Free Plan $0/mo Get started with Browserbase. Explore and prototype ideas. Infrastructure - 3concurrent b`
- 🔎 **/mo** `ou build, billed at your plan’s rate. And as always, you can get started for free. ## Free Plan $0/mo Get started with Browserbase. Explore and prototype ideas. Infrastructure - 3concurrent browsers`
- 🔎 **/mo** `s - 15minutes /session Capabilities - Models$5 in tokens - Runtimeincluded ## Developer Plan $20/mo Build and test real workflows. Prepare for production. Infrastructure - 25concurrent browsers -`
- 🔎 **/mo** `included Capabilities - Runtimeincluded - Auto captcha solving MOST POPULAR ## Startup Plan $99/mo Run in production with room to grow and scale usage. Infrastructure - 100concurrent browsers - 5`
- 🔎 **/models): your Browserbase API key gives access to ma** `on Browserbase for faster & more secure execution - [**Model Gateway**](https://www.browserbase.com/models): your Browserbase API key gives access to major models via Stagehand and unified billing. ### What kinds of use cases do companies use Browserb`
- 🔎 **free** `caps or throttling as you build, billed at your plan’s rate. And as always, you can get started for free. ## Free Plan $0/mo Get started with Browserbase. Explore and prototype ideas. Infrastructure`
- 🔎 **hours** `| --- | --- | --- | | Infrastructure | | | | | | Concurrency | 3 | 25 | 100 | 250+ | | Browser hours | 1 | 100 then $0.12/browser hr | 500 then $0.10/browser hr | Usage-based | | Agent runs | 3 | 15 |`
- 🔎 **hours** `its? A browser hour goes further than you think. A typical web scrape runs in under 2 minutes. 100 hours is roughly 3,000 page-level tasks. Teams that ship use Browserbase. ## FAQs ### What does Browse`
- 🔎 **concurrent** `## Free Plan $0/mo Get started with Browserbase. Explore and prototype ideas. Infrastructure - 3concurrent browsers - 1browser hour - 3Agent runs included - 1,000Search calls - 1,000Fetch calls - 15minutes`
- 🔎 **concurrent** `Developer Plan $20/mo Build and test real workflows. Prepare for production. Infrastructure - 25concurrent browsers - 15Agent runs included Capabilities - Runtimeincluded - Auto captcha solving MOST POPU`

## 🌱 Hyperbrowser 定价（Agent 浏览器沙盒）（hyperbrowser-pricing）
- 状态: ok | https://hyperbrowser.ai/pricing
- 🔎 **free trial for paid plans?** `and are prorated. Downgrades take effect at the end of your current billing cycle. ### Is there a free trial for paid plans? The Free plan gives you 5,000 credits to test the service. For Enterprise plans, we offer a 14-day`
- 🔎 **Free plan gives you 5,000 credits to test the service** `ke effect at the end of your current billing cycle. ### Is there a free trial for paid plans? The Free plan gives you 5,000 credits to test the service. For Enterprise plans, we offer a 14-day trial with full access to all features. ### What payment`
- 🔎 **credits for browsers, sandboxes, web data, and agents** `# Pay only for what you use. Each plan includes credits for browsers, sandboxes, web data, and agents. Choose your capacity, then use those credits across all four products. ## 5,000 credits. Try your`
- 🔎 **credits across all four products** `ncludes credits for browsers, sandboxes, web data, and agents. Choose your capacity, then use those credits across all four products. ## 5,000 credits. Try your first workflow. Enough for 50 browser hours or 5,000 fetched pages at`
- 🔎 **credits** `data, and agents. Choose your capacity, then use those credits across all four products. ## 5,000 credits. Try your first workflow. Enough for 50 browser hours or 5,000 fetched pages at base rates. ## Ch`
- 🔎 **credits = $1 in usage** `rkflow. Enough for 50 browser hours or 5,000 fetched pages at base rates. ## Choose a plan 1,000 credits = $1 in usage ### Startup **$30** in usage included each month For scheduled jobs and small applications. 30,`
- 🔎 **credits for all four products** `# Startup **$30** in usage included each month For scheduled jobs and small applications. 30,000 credits for all four products - 25 concurrent sessions - 30 days of data retention - Automatic CAPTCHA solving - Basic stealth m`
- 🔎 **credits for all four products** `00** in usage included each month For applications running more browser sessions at once. 100,000 credits for all four products - 100 concurrent sessions - 30 days of data retention - Automatic CAPTCHA solving - Basic stealth`
- 🔎 **credit allocations for all four products** `Custom capacity. Volume pricing. For custom capacity, volume pricing, and premium support. Custom credit allocations for all four products - 1,000+ concurrent sessions - 180+ days of data retention - Automatic CAPTCHA solving - Ultra ste`
- 🔎 **credits included** `PTCHA solving - Ultra stealth mode - Premium residential proxies ### Free **$0** to start · 5,000 credits included Paid plans support additional credit purchases when your included balance runs out. ## Usage rate`

## 🌱 Steel 定价（开源 Agent 浏览器云）（steel-pricing）
- 状态: ok | https://steel.dev/pricing
- 🔎 **free** `# Pricing Start for free and pay only for what runs. Move up when your agents go to production. ## Compare plans Every rat`

## 🌱 Serv00（波兰免费主机·白嫖圈热门）（serv00-home）
- 状态: ok | https://serv00.com/
- 🔎 **3 GB for free, no adverts, no hooks** `# Revolutionary hosting for FREE! 3 GB for free, no adverts, no hooks Check our offer [Register account](https://www.serv00.com/register-account/) [DONATE](https://buym`
- 🔎 **3 GB of SSD disk space**, unlimited data transfer, and support f** `ith completely free access**. **serv00.com** is an innovative free web hosting platform offering **3 GB of SSD disk space**, unlimited data transfer, and support for up to 100 websites and 16 databases – **all without ads or fees for the user**. Account registrat`
- 🔎 **3 GB Storage** `arantees lightning-fast page loading and smooth application performance even under heavy load. ### 3 GB Storage **3 GB of free SSD storage** for your websites and applications. High read and write performance e`
- 🔎 **3 GB of free SSD storage** for your websites and applications** `ng-fast page loading and smooth application performance even under heavy load. ### 3 GB Storage **3 GB of free SSD storage** for your websites and applications. High read and write performance ensures smooth operation even under heavy load. ### Forum support`
- 🔎 **3 GB of fast SSD storage**, unlimited data transfer, and support** `**. ## Why **serv00** Why choose **serv00.com**? Because we offer completely free hosting with **3 GB of fast SSD storage**, unlimited data transfer, and support for up to 100 websites and 16 databases – **all without ads or hidden fees**. Our intuitive **Devil`
- 🔎 **3 GB** `ng - Remote database access - Fast SSD drives - No ads - Price ### **serv00.com** FREE - Storage 3 GB - Monthly transfer **unlimited** - Websites 100 - MySQL databases 10 - PostgreSQL databases 3 - Mon`
- 🔎 **200 GB**** `ttps://www.serv00.com/register-account/) ### host**UNO**.com START 1 - PREMIUM 4 - Storage **5 - 200 GB** - Monthly transfer **unlimited** - Websites **unlimited** - MySQL databases **unlimited** - Postgre`
- 🔎 **4 GB**** `P ports **15+** - PHP interpreters **4 - 160** - System processes **20 - 150** - RAM memory **512 - 4 GB** - Backups **7 - 14 Days** - Server placement **Warsaw, Poland** - Free subdomain **login.useruno.co`
- 🔎 **3 GB** `s What capacity will I have if I use it? The capacity of the hosting account on serv00 servers is 3 GB What PHP versions are supported on serv00? Our hosting accounts currently support the following P`
- 🔎 **transfer, and support for up to 100 websites and 16 databases – **al** `om** is an innovative free web hosting platform offering **3 GB of SSD disk space**, unlimited data transfer, and support for up to 100 websites and 16 databases – **all without ads or fees for the user**. Account registration is very simple and free, and today the pl`

## 🌱 EUserv（德国免费 IPv6 VPS 申领）（euserv-home）
- 状态: ok | https://www.euserv.com/en/
- 🔎 **per month if not displayed different, additional one time s** `dex.php) \*)\*\*)\*\*\*) All prices are included VAT depending on selected country, price tags are per month if not displayed different, additional one time setup fee may apply starting at 0,- EUR. Please watch full description, details and pricing of servic`

## 🌱 Scaleway 定价（法国云，免费档+试用）（scaleway-pricing）
- 状态: ok | https://www.scaleway.com/en/pricing/
- 🔎 **/model-as-a-service/)** `verless - Generative APIs - Dedicated Deployment [View pricing](https://www.scaleway.com/en/pricing/model-as-a-service/) ## Storage ### Storage Discover our versatile storage options: - Object Storage - Scaleway Glac`

## 🌱 UpCloud 定价（试用金）（upcloud-pricing）
- 状态: ok | https://www.upcloud.com/pricing/
- 🔎 **50 GB** `expensive than previous-generation while offering the same 99.99% SLA. #### Standard storage 10 – 50 GB #### Memory 1 – 16 GB #### CPU cores 1 – 4 - 45 second deployment - Standard performance SSD s`
- 🔎 **16 GB** `generation while offering the same 99.99% SLA. #### Standard storage 10 – 50 GB #### Memory 1 – 16 GB #### CPU cores 1 – 4 - 45 second deployment - Standard performance SSD storage - Previous-gen AM`
- 🔎 **1 GB | 1 | 250 Mbit/s | 10 GB | **€3/mo *** |** `lobal price | Memory | CPU cores | Bandwidth | Storage | Price | | --- | --- | --- | --- | --- | | 1 GB | 1 | 250 Mbit/s | 10 GB | **€3/mo *** | | 2 GB | 1 | 250 Mbit/s | 20 GB | **€6/mo** | | 2 GB | 2 | 250 Mbit/s | 30 GB | **€8/mo** | | 4 GB`
- 🔎 **2 GB | 1 | 250 Mbit/s | 20 GB | **€6/mo** |** `Storage | Price | | --- | --- | --- | --- | --- | | 1 GB | 1 | 250 Mbit/s | 10 GB | **€3/mo *** | | 2 GB | 1 | 250 Mbit/s | 20 GB | **€6/mo** | | 2 GB | 2 | 250 Mbit/s | 30 GB | **€8/mo** | | 4 GB | 1 | 250 Mbit/s | 30 GB | **€10/mo** | | 4 GB`
- 🔎 **2 GB | 2 | 250 Mbit/s | 30 GB | **€8/mo** |** `- | | 1 GB | 1 | 250 Mbit/s | 10 GB | **€3/mo *** | | 2 GB | 1 | 250 Mbit/s | 20 GB | **€6/mo** | | 2 GB | 2 | 250 Mbit/s | 30 GB | **€8/mo** | | 4 GB | 1 | 250 Mbit/s | 30 GB | **€10/mo** | | 4 GB | 2 | 500 Mbit/s | 30 GB | **€12/mo** | | 8 G`
- 🔎 **4 GB | 1 | 250 Mbit/s | 30 GB | **€10/mo** |** `*** | | 2 GB | 1 | 250 Mbit/s | 20 GB | **€6/mo** | | 2 GB | 2 | 250 Mbit/s | 30 GB | **€8/mo** | | 4 GB | 1 | 250 Mbit/s | 30 GB | **€10/mo** | | 4 GB | 2 | 500 Mbit/s | 30 GB | **€12/mo** | | 8 GB | 2 | 500 Mbit/s | 40 GB | **€18/mo** | | 8 G`
- 🔎 **4 GB | 2 | 500 Mbit/s | 30 GB | **€12/mo** |** `** | | 2 GB | 2 | 250 Mbit/s | 30 GB | **€8/mo** | | 4 GB | 1 | 250 Mbit/s | 30 GB | **€10/mo** | | 4 GB | 2 | 500 Mbit/s | 30 GB | **€12/mo** | | 8 GB | 2 | 500 Mbit/s | 40 GB | **€18/mo** | | 8 GB | 4 | 500 Mbit/s | 40 GB | **€20/mo** | | 16`
- 🔎 **8 GB | 2 | 500 Mbit/s | 40 GB | **€18/mo** |** `* | | 4 GB | 1 | 250 Mbit/s | 30 GB | **€10/mo** | | 4 GB | 2 | 500 Mbit/s | 30 GB | **€12/mo** | | 8 GB | 2 | 500 Mbit/s | 40 GB | **€18/mo** | | 8 GB | 4 | 500 Mbit/s | 40 GB | **€20/mo** | | 16 GB | 2 | 500 Mbit/s | 50 GB | **€24/mo** | | 16`
- 🔎 **8 GB | 4 | 500 Mbit/s | 40 GB | **€20/mo** |** `* | | 4 GB | 2 | 500 Mbit/s | 30 GB | **€12/mo** | | 8 GB | 2 | 500 Mbit/s | 40 GB | **€18/mo** | | 8 GB | 4 | 500 Mbit/s | 40 GB | **€20/mo** | | 16 GB | 2 | 500 Mbit/s | 50 GB | **€24/mo** | | 16 GB | 4 | 500 Mbit/s | 50 GB | **€28/mo** | Fe`
- 🔎 **16 GB | 2 | 500 Mbit/s | 50 GB | **€24/mo** |** `* | | 8 GB | 2 | 500 Mbit/s | 40 GB | **€18/mo** | | 8 GB | 4 | 500 Mbit/s | 40 GB | **€20/mo** | | 16 GB | 2 | 500 Mbit/s | 50 GB | **€24/mo** | | 16 GB | 4 | 500 Mbit/s | 50 GB | **€28/mo** | Features and services specific to Cloud Servers.`

## 🌱 DigitalOcean 定价（$200/60天 试用观察）（digitalocean-pricing）
- 状态: ok | https://www.digitalocean.com/pricing
- 🔎 **50 GiB** `- Standard tier: $0.15 per GiB-month - High performance tier: $0.30 per GiB-month - Starting from 50 GiB - Flat pricing across all supported regions ### Volumes Starting at Business-ready block storage`
- 🔎 **100 GiB bandwidth (overage $0** `ng is free. Inter-datacenter VPC peering is $0.01/GiB. - VPC NAT Gateway: $40.00 per node, includes 100 GiB bandwidth (overage $0.01/GiB), supports up to 500,000 connections. ### Uptime Starting at Automated endpoint alerts -`
- 🔎 **500 GiB / mo** `let - Industry leading bandwidth pricing, Droplets include free outbound data transfer, starting at 500 GiB / mo - Free DNS management - Free container registry with 1 repository and 500 MiB storage - Free cloud`
- 🔎 **500 MiB storage** `fer, starting at 500 GiB / mo - Free DNS management - Free container registry with 1 repository and 500 MiB storage - Free cloud firewalls - Collect metrics on visibility, monitor Droplet performance, and get free a`
- 🔎 **000 GiB-seconds per month for free with DigitalOcean Functions** `onitor Droplet performance, and get free alerts when problems arise in your infrastructure - Use 90,000 GiB-seconds per month for free with DigitalOcean Functions. There are no additional charges for function invocations ### Experience a 186% return on investme`
- 🔎 **free credits or after the credit expiration period** `spending exceeds an amount you specify. Your card will be charged only after you have utilized the free credits or after the credit expiration period. For example, if you received a $5 credit for 90 days, then that $5 credit is automatically applied`
- 🔎 **credits or after the credit expiration period** `ing exceeds an amount you specify. Your card will be charged only after you have utilized the free credits or after the credit expiration period. For example, if you received a $5 credit for 90 days, then that $5 credit is automatically applied`
- 🔎 **credit for 90 days, then that $5 credit is automatically applied t** `utilized the free credits or after the credit expiration period. For example, if you received a $5 credit for 90 days, then that $5 credit is automatically applied to your account. If you spend $3 in that timeframe, your card will not be charged. If you spend $10,`
- 🔎 **credit will be fully utilized, and your card will be charged only ** `account. If you spend $3 in that timeframe, your card will not be charged. If you spend $10, the $5 credit will be fully utilized, and your card will be charged only $5. Since the credit is valid for 90 days, you won't be able to use any remaining credit after the 9`
- 🔎 **credit is valid for 90 days, you won't be able to use any remainin** `u spend $10, the $5 credit will be fully utilized, and your card will be charged only $5. Since the credit is valid for 90 days, you won't be able to use any remaining credit after the 90-day period expires. We charge you for the underlying compute on which the 1-C`

## 🌱 Vercel 定价（Hobby 免费档）（vercel-pricing）
- 状态: ok | https://vercel.com/pricing
- 🔎 **1 GB / month included** `per 1M Custom 1K included per project $50 / month per 25K redirects Custom Blob Storage Size 1 GB / month included $0.023 per GB Custom Blob Simple Operations 10K / month included $0.40 per 1M Custom Blob Ad`
- 🔎 **10 GB / month included** `r 1M Custom Blob Advanced Operations 2K / month included $5 per 1M Custom Blob Data Transfer 10 GB / month included Included in Flat Rate CDN Custom Image Optimization Transformation 5K / month included Startin`
- 🔎 **360 GB-hrs / month included** `ctive CPU 4 hours / month included Starting at $0.128 per hour Custom Fluid Provisioned Memory 360 GB-hrs / month included Starting at $0.0106 per GB-hr Custom Function Invocations 1M / month included Starting at $0.6`
- 🔎 **420 GB-hrs / month included** `ive CPU 5 hours / month included Starting at $0.128 per hour Custom Sandbox Provisioned Memory 420 GB-hrs / month included Starting at $0.0212 per GB-hr Custom Sandbox Creations 5K / month included Starting at $0.60 p`
- 🔎 **20 GB / month included** `ons 5K / month included Starting at $0.60 per 1,000,000 creations Custom Sandbox Data Transfer 20 GB / month included Included in Flat Rate CDN Custom Concurrent Sandboxes 10 10K Custom Snapshot Storage 15 GB`
- 🔎 **15 GB** `cluded Included in Flat Rate CDN Custom Concurrent Sandboxes 10 10K Custom Snapshot Storage 15 GB Starting at $0.08 per GB-month Custom Drive Storage 15 GB (lifetime) included Starting at $0.0`
- 🔎 **15 GB (lifetime) included** `s 10 10K Custom Snapshot Storage 15 GB Starting at $0.08 per GB-month Custom Drive Storage 15 GB (lifetime) included Starting at $0.05 per GB-month Custom Drive Reads 30 GB / month included Starting at $0.0015 p`
- 🔎 **30 GB / month included** `tom Drive Storage 15 GB (lifetime) included Starting at $0.05 per GB-month Custom Drive Reads 30 GB / month included Starting at $0.0015 per GB Custom Drive Writes 30 GB / month included Starting at $0.004 per G`
- 🔎 **30 GB / month included** `nth Custom Drive Reads 30 GB / month included Starting at $0.0015 per GB Custom Drive Writes 30 GB / month included Starting at $0.004 per GB Custom Daemons Active CPU 5 hours / month included Starting at $0.12`
- 🔎 **420 GB-hrs / month included** `ive CPU 5 hours / month included Starting at $0.128 per hour Custom Daemons Provisioned Memory 420 GB-hrs / month included Starting at $0.0212 per GB-hr Custom Workflow Events 50K events / month included $20 per 1,000`

## 🌱 Netlify 定价（免费 100GB 带宽档）（netlify-pricing）
- 状态: ok | https://www.netlify.com/pricing/
- 🔎 **10vCPUs), 6x more memory (36GB), and 4x higher concurrency than the** `on limits, increase memory, or set a custom AWS region. | | | | | | 5x faster processing power (10vCPUs), 6x more memory (36GB), and 4x higher concurrency than the standard build environment. | | | | | | 99.99% uptime SLA | | | | | | Preserve deploys olde`
- 🔎 **always free, with hard monthly limits that cannot be exceeded** `nts-and-billing/billing/billing-for-credit-based-plans/configure-auto-recharge/). The free plan is always free, with hard monthly limits that cannot be exceeded or incur any costs. Paid plans have spend control using the auto recharge setting for credits, whic`
- 🔎 **free plan is always free, with hard monthly limits that cannot be exc** `/manage/accounts-and-billing/billing/billing-for-credit-based-plans/configure-auto-recharge/). The free plan is always free, with hard monthly limits that cannot be exceeded or incur any costs. Paid plans have spend control using the auto recharge setting for credits,`
- 🔎 **credit limit / month** `& images with Blob storage - Firewall Traffic Rules & basic rate limiting - Global CDN - 300 credit limit / month - ## Personal $9$12$15[See pricing in your dashboard](https://app.netlify.com/teams/~/billing/g`
- 🔎 **credits / month** `Free, plus: - Smart secret detection - 1-day observability - Priority email support - 1,000 credits / month - ## Pro $20$20$25[See pricing in your dashboard](https://app.netlify.com/teams/~/billing/gener`
- 🔎 **credits** `lds - SSO & SCIM - Log drains - Organization management - 24/7 dedicated support ### Usage credits Flexible plans to optimize your usage A production deploy is the version of your project pushed t`
- 🔎 **credit-based pricing accounts, new projects start private by defau** `e your usage A production deploy is the version of your project pushed to your main domain. On new credit-based pricing accounts, new projects start private by default and become publicly accessible only when you choose to publish. Also includes: Unlimited Deploy P`
- 🔎 **credits | Usage credits |  |  |  |** `Edge functions. | | | | | | | --- | --- | --- | --- | --- | | Features | | | | | | Usage credits | Usage credits | | | | | Includes usage credits for production deploys, compute, form submissions, bandwidth, and web requ`
- 🔎 **credits for production deploys, compute, form submissions, bandwidt** `| --- | --- | | Features | | | | | | Usage credits | Usage credits | | | | | Includes usage credits for production deploys, compute, form submissions, bandwidth, and web requests. | 300 credit limit | 1,000 credits included | Starting with 3,000 credits per m`
- 🔎 **credit limit | 1,000 credits included | Starting with 3,000 credit** `usage credits for production deploys, compute, form submissions, bandwidth, and web requests. | 300 credit limit | 1,000 credits included | Starting with 3,000 credits per month, choose a Pro tier up to 20,000 credits per month. | Custom | | Additional credits are a`

## 🌱 Deno Deploy（免费层）（deno-deploy）
- 状态: ok | https://deno.com/deploy
- 🔎 **free tier, and gracefully scale up or down as needed, automatically** `t times than lambda functions or virtual machines. #### Elastic scalability Start with a generous free tier, and gracefully scale up or down as needed, automatically. #### Runs on Deno Deno Deploy runs on Deno under the hood, so you get better speed and security,`
- 🔎 **free** `t times than lambda functions or virtual machines. #### Elastic scalability Start with a generous free tier, and gracefully scale up or down as needed, automatically. #### Runs on Deno Deno Deploy run`
- 🔎 **free** `r the hood, so you get better speed and security, with full Node and npm compatibility. It's like a free upgrade. `Deno Deploy`![Deno Deploy egg logo](https://deno.com/logos/deploy/mark.svg?__frsh_c=ba3b`

## 🌱 Val Town 定价（免费云函数）（valtown-pricing）
- 状态: ok | https://val.town/pricing
- 🔎 **credit / mo** `Save $50 (2 months free) [Subscribe](https://www.val.town/checkout/yearly) - **$10** Townie (AI) credit / mo - **10** custom domains - **1 minute** cron intervals - **10 min** wall clock time / run - **2,000*`
- 🔎 **credit / mo** `hs free) [Contact us](mailto:business@val.town) - Everything in Pro, plus: - **$100** Townie (AI) credit / mo - **Unlimited** custom domains - **5 million** runs / day - **Team accounts** - **Val Town Access**`
- 🔎 **credit** `[Talk to us](mailto:business@val.town) - Everything in Business, plus: - **Flexible** Townie (AI) credit - **No limits** - **Log export** - **SOC 2** - **Custom Support** See also our [Limits](https://ww`
- 🔎 **/mo** `tion - **100,000** runs / day - **Email** yourself Pro For professionals and solopreneurs **$21**/mo Save $50 (2 months free) [Subscribe](https://www.val.town/checkout/yearly) - **$10** Townie (AI)`
- 🔎 **/mo** `day - **Email** anyone Business For collaboration and production use **Starting from** **$167**/mo Save $400 (2 months free) [Contact us](mailto:business@val.town) - Everything in Pro, plus: - **`
- 🔎 **free** `# Pricing 2 months free Free Start using Val Town today **$0** [Sign up](https://www.val.town/auth/signup) - **MCP** i`
- 🔎 **free** `/ day - **Email** yourself Pro For professionals and solopreneurs **$21**/mo Save $50 (2 months free) [Subscribe](https://www.val.town/checkout/yearly) - **$10** Townie (AI) credit / mo - **10** cus`
- 🔎 **free** `usiness For collaboration and production use **Starting from** **$167**/mo Save $400 (2 months free) [Contact us](mailto:business@val.town) - Everything in Pro, plus: - **$100** Townie (AI) credit`
- 🔎 **runs** `*1 min** wall clock time / run - **Unlimited** public vals - **3 days** log retention - **100,000** runs / day - **Email** yourself Pro For professionals and solopreneurs **$21**/mo Save $50 (2 months`
- 🔎 **runs** `10 min** wall clock time / run - **2,000** private vals - **10 days** log retention - **1,000,000** runs / day - **Email** anyone Business For collaboration and production use **Starting from** **$16`

## 🌱 Northflank 定价（免费 sandbox 服务）（northflank-pricing）
- 状态: ok | https://northflank.com/pricing
- 🔎 **12 vCPU and 48 GB** `jobs, and 1 database - Up to $20/mo of resources on Northflank Cloud - 1 BYOC cluster, up to 12 vCPU and 48 GB - Always on, no sleeping 2. ## Pay as you go Usage-based From $0.01667 per vCPU hour`
- 🔎 **140 MiB/s per disk included | $7** `on and service volumes | $0.11657/ GiB / month | Not billed | | Additional IOPSFirst 3,000 IOPS and 140 MiB/s per disk included | $7.37/ 1,000 IOPS / month | Not billed | | Additional throughputFirst 3,000 IOPS and 140 MiB/s per dis`
- 🔎 **140 MiB/s per disk included | $5** `isk included | $7.37/ 1,000 IOPS / month | Not billed | | Additional throughputFirst 3,000 IOPS and 140 MiB/s per disk included | $5.85/ 100 MiB/s / month | Not billed | | Network egressIngress is free | $0.06/ GB | Not billed | | E`
- 🔎 **100 MiB/s / month | Not billed |** `nth | Not billed | | Additional throughputFirst 3,000 IOPS and 140 MiB/s per disk included | $5.85/ 100 MiB/s / month | Not billed | | Network egressIngress is free | $0.06/ GB | Not billed | | Egress gatewayDedicated IP | $15.00/ g`
- 🔎 **5 vCPU · 1 GB | 0** `Memory | Per hour | Per month | | --- | --- | --- | --- | --- | | nf-compute-50Recommended for dev0.5 vCPU · 1 GB | 0.5 vCPU | 1 GB | $0.01667 | $12.00 | | nf-compute-100-2Most popular1 vCPU · 2 GB | 1 vCPU | 2 GB | $`
- 🔎 **5 vCPU | 1 GB | $0** `| Per month | | --- | --- | --- | --- | --- | | nf-compute-50Recommended for dev0.5 vCPU · 1 GB | 0.5 vCPU | 1 GB | $0.01667 | $12.00 | | nf-compute-100-2Most popular1 vCPU · 2 GB | 1 vCPU | 2 GB | $0.03333 | $24.00 |`
- 🔎 **2 GB | 1 vCPU | 2 GB | $0** `r dev0.5 vCPU · 1 GB | 0.5 vCPU | 1 GB | $0.01667 | $12.00 | | nf-compute-100-2Most popular1 vCPU · 2 GB | 1 vCPU | 2 GB | $0.03333 | $24.00 | | nf-compute-200Production2 vCPU · 4 GB | 2 vCPU | 4 GB | $0.06667 | $48.00 | | nf`
- 🔎 **4 GB | 2 vCPU | 4 GB | $0** `2Most popular1 vCPU · 2 GB | 1 vCPU | 2 GB | $0.03333 | $24.00 | | nf-compute-200Production2 vCPU · 4 GB | 2 vCPU | 4 GB | $0.06667 | $48.00 | | nf-compute-400Scale4 vCPU · 8 GB | 4 vCPU | 8 GB | $0.13 | $96.00 | | nf-compute`
- 🔎 **8 GB | 4 vCPU | 8 GB | $0** `pute-200Production2 vCPU · 4 GB | 2 vCPU | 4 GB | $0.06667 | $48.00 | | nf-compute-400Scale4 vCPU · 8 GB | 4 vCPU | 8 GB | $0.13 | $96.00 | | nf-compute-800-168 vCPU · 16 GB | 8 vCPU | 16 GB | $0.27 | $192.00 | ### GPUs on N`
- 🔎 **168 vCPU · 16 GB | 8 vCPU | 16 GB | $0** `7 | $48.00 | | nf-compute-400Scale4 vCPU · 8 GB | 4 vCPU | 8 GB | $0.13 | $96.00 | | nf-compute-800-168 vCPU · 16 GB | 8 vCPU | 16 GB | $0.27 | $192.00 | ### GPUs on Northflank Cloud Run a sandbox with a GPU and multi-read-write storage`

## 🌱 Google Colab FAQ（免费档 GPU/runtime 口径）（colab-faq）
- 状态: ok | https://research.google.com/colaboratory/faq.html
- 🔎 **free trial of a Google One plan (such as a promotional or extended fre** `benefits are available to paid Google AI plan subscribers. However, they are not included during a free trial of a Google One plan (such as a promotional or extended free trial). Additionally, Google AI plan benefits are only honored in countries where Colab offers its`
- 🔎 **transferable between Google products** `y to retroactively move the subscription to a different account. No. SheerID verifications are not transferable between Google products. If you have verified with SheerID for another Google product (Google One, YouTube Premium, etc), y`
- 🔎 **idle for a while, and have a maximum lifetime enforced** `. Code is executed in a virtual machine private to your account. Virtual machines are deleted when idle for a while, and have a maximum lifetime enforced by the Colab service. You can download any Colab notebook that you’ve created from Google Drive fo`
- 🔎 **idle timeout periods, maximum VM lifetime, GPU types a** `by not providing guaranteed or unlimited resources. This means that overall usage limits as well as idle timeout periods, maximum VM lifetime, GPU types available, and other factors vary over time. Colab does not publish these limits, in part because the`
- 🔎 **idle** `hat_types_of_gpus) Colab. Colab prioritizes interactive compute. Runtimes will time out if you are idle. In the version of Colab that is free of charge notebooks can run for at most 12 hours, depending`
- 🔎 **Idle timeouts only apply if code execution terminates** `ab Pro+ supports continuous code execution for up to 24 hours if you have sufficient compute units. Idle timeouts only apply if code execution terminates. You can fully relax any runtime limits and idle timeouts by purchasing a dedicated VM at [GCP Mar`
- 🔎 **idle timeouts by purchasing a dedicated VM at [GCP Mar** `Idle timeouts only apply if code execution terminates. You can fully relax any runtime limits and idle timeouts by purchasing a dedicated VM at [GCP Marketplace](https://research.google.com/colaboratory/marketplace.html?utm_source=faq&utm_medium=link&u`
- 🔎 **free** `# The Basics Colab is a hosted Jupyter Notebook service that requires no setup to use and provides free of charge access to computing resources, including GPUs and TPUs. Colab is especially well suited t`
- 🔎 **free** `s. Colab is especially well suited to machine learning, data science, and education. Yes. Colab is free of charge to use. In order to provide access to as many students and under-resourced groups around`
- 🔎 **free** `, and usage limits sometimes fluctuate. This is necessary for Colab to be able to provide resources free of charge. For more details, see Resource Limits. Colab managed runtimes prohibit abusive actions`

## 🌱 Lightning AI 定价（每月免费 credits）（lightning-pricing）
- 状态: ok | https://lightning.ai/pricing
- 🔎 **600096 GB$4** `No restrictions in Pro or higher. - T416 GB$0.55/hr - L424 GB$0.79/hr - L40S48 GB$3.54/hr - RTXP 600096 GB$4.64/hr - A10040 GB$2.19/hr - H10080 GB$5.45/hr - H200141 GB$4.50/hr Billed by the second. Free hour`
- 🔎 **50GB of persistent storage** `htning.ai/lightning-coin.svg)Up to 30 credits to start - Up to 2 seats - Up to 2 concurrent GPUs - 50GB of persistent storage - Pay as you go - 32 core CPUs - Single GPUs - 1 free Studio with 4 hour restarts - Up to 80% off`
- 🔎 **200GB of persistent storage** `ightning-coin.svg)240 annual credits100 annual credits - Up to 5 seats - Up to 6 concurrent GPUs - 200GB of persistent storage - All Free features - 64 core CPUs - Multi GPUs - 1 free 24/7 Studio - Connect your S3 buckets - D`
- 🔎 **2TB of persistent storage** `a.lightning.ai/lightning-coin.svg)600 annual credits - Up to 10 seats - Up to 12 concurrent GPUs - 2TB of persistent storage - All Pro features - 96 core CPUs - Full-node GPUs - Multi-node training - Use via AWS marketplace`
- 🔎 **1 TB stored, moved out once** `not to use it. The bill is set by what you keep, not how hard your team works. ### Base case — 1 TB stored, moved out once No per-movement charge to forecast, no penalty for iterating — the bill is set by what you store,`
- 🔎 **024 GB | $0** `te | Lightning | AWS/mo | Lightning/mo | | --- | --- | --- | --- | --- | --- | | Object storage | 1,024 GB | $0.023/GB-mo | $0.10/GB-mo | $23.55 | $102.40 | | PUT / COPY / POST / LIST | 100,000 | $0.005/1K | Inc`
- 🔎 **024 GB | $0** `GET / SELECT / other | 1,000,000 | $0.0004/1K | Included | $0.40 | $0.00 | | Egress — data out | 1,024 GB | $0.09/GB | Included | $92.16 | $0.00 | | Total monthly | | $116.61 | $102.40 | | | **Storage** $0`
- 🔎 **1 TB dataset in every row; a move is the full TB leaving storage** `$485.25 | $102.40 | Save 79% | | Heavy experimentation | 10 | $946.05 | $102.40 | Save 89% | Same 1 TB dataset in every row; a move is the full TB leaving storage. US-East, 1 TB = 1,024 GB. AWS S3 Standard vs. Lightning storage, public list rates. ## You have t`
- 🔎 **1 TB = 1,024 GB** `02.40 | Save 89% | Same 1 TB dataset in every row; a move is the full TB leaving storage. US-East, 1 TB = 1,024 GB. AWS S3 Standard vs. Lightning storage, public list rates. ## You have to try it to believe it. 4`
- 🔎 **free tier with 50* free GPU hours** `# Get up to 50 free GPU hours. Then pay-as-you-go. Start on the free tier with 50* free GPU hours. Pay as you go for more hours. Upgrade for enterprise features like bring your own cloud, use your`

## 🌱 Paperspace 定价（DO 旗下，Gradient 免费档现状）（paperspace-pricing）
- 状态: ok | https://www.paperspace.com/pricing
- 🔎 **5GB storage** `n.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-check-small.svg) 5GB storage - ![](https://cdn.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-ch`
- 🔎 **50GB storage** `n.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-check-small.svg) 50GB storage - ![](https://cdn.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-ch`
- 🔎 **10GB Persistent Storage included ($0** `n.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-check-small.svg) 10GB Persistent Storage included ($0.29/GB overage) - ![](https://cdn.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a9903700`
- 🔎 **500GB Persistent Storage included ($0** `n.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-check-small.svg) 500GB Persistent Storage included ($0.29/GB overage) - ![](https://cdn.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a9903700`
- 🔎 **15GB storage** `n.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-check-small.svg) 15GB storage - ![](https://cdn.prod.website-files.com/5eaa1464031f7c15343019ee/5eaa14654a99037004326d7c_icon-ch`
- 🔎 **90GB RAM** `a.avif) #### Servers & Desktops # H100 NewLy Available $ # 3.09 / hour - NVIDIA A100 GPU - 90GB RAM - 12 vCPU $ # 2.24* / hour - NVIDIA HGX H100 GPU - 256 GB RAM - 20 vCPU Multi-GPU types: 8x`
- 🔎 **12 vCPU** `## Servers & Desktops # H100 NewLy Available $ # 3.09 / hour - NVIDIA A100 GPU - 90GB RAM - 12 vCPU $ # 2.24* / hour - NVIDIA HGX H100 GPU - 256 GB RAM - 20 vCPU Multi-GPU types: 8x [Create](h`
- 🔎 **256 GB RAM** `# 3.09 / hour - NVIDIA A100 GPU - 90GB RAM - 12 vCPU $ # 2.24* / hour - NVIDIA HGX H100 GPU - 256 GB RAM - 20 vCPU Multi-GPU types: 8x [Create](https://console.paperspace.com/signup?core=true) # A100-`
- 🔎 **20 vCPU** `r - NVIDIA A100 GPU - 90GB RAM - 12 vCPU $ # 2.24* / hour - NVIDIA HGX H100 GPU - 256 GB RAM - 20 vCPU Multi-GPU types: 8x [Create](https://console.paperspace.com/signup?core=true) # A100-80G $ #`
- 🔎 **90GB RAM** `://console.paperspace.com/signup?core=true) # A100-80G $ # 1.15\*\* / hour - NVIDIA A100 GPU - 90GB RAM - 12 vCPU Multi-GPU types: 8x [Create](https://console.paperspace.com/signup?core=true) # A4000`

## 🌱 Replicate 定价（免费额度收回观察）（replicate-pricing）
- 状态: ok | https://replicate.com/pricing
- 🔎 **2GB** `e model's version list. #### Hardware pricing **GPU** \- **CPU** 1x **GPU RAM** \- **RAM** 2GB **GPU** \- **CPU** 4x **GPU RAM** \- **RAM** 8GB **GPU** 1x **CPU** 10x **GPU RAM** 8`
- 🔎 **8GB** `\- **CPU** 1x **GPU RAM** \- **RAM** 2GB **GPU** \- **CPU** 4x **GPU RAM** \- **RAM** 8GB **GPU** 1x **CPU** 10x **GPU RAM** 80GB **RAM** 144GB **GPU** 2x **CPU** 20x **GPU RAM`
- 🔎 **80GB** `B **GPU** \- **CPU** 4x **GPU RAM** \- **RAM** 8GB **GPU** 1x **CPU** 10x **GPU RAM** 80GB **RAM** 144GB **GPU** 2x **CPU** 20x **GPU RAM** 160GB **RAM** 288GB **GPU** 1x **CPU*`
- 🔎 **144GB** `**CPU** 4x **GPU RAM** \- **RAM** 8GB **GPU** 1x **CPU** 10x **GPU RAM** 80GB **RAM** 144GB **GPU** 2x **CPU** 20x **GPU RAM** 160GB **RAM** 288GB **GPU** 1x **CPU** 13x **GPU RA`
- 🔎 **160GB** `GPU** 1x **CPU** 10x **GPU RAM** 80GB **RAM** 144GB **GPU** 2x **CPU** 20x **GPU RAM** 160GB **RAM** 288GB **GPU** 1x **CPU** 13x **GPU RAM** 80GB **RAM** 144GB **GPU** 1x **CPU**`
- 🔎 **288GB** `** 10x **GPU RAM** 80GB **RAM** 144GB **GPU** 2x **CPU** 20x **GPU RAM** 160GB **RAM** 288GB **GPU** 1x **CPU** 13x **GPU RAM** 80GB **RAM** 144GB **GPU** 1x **CPU** 10x **GPU RAM`
- 🔎 **80GB** `PU** 2x **CPU** 20x **GPU RAM** 160GB **RAM** 288GB **GPU** 1x **CPU** 13x **GPU RAM** 80GB **RAM** 144GB **GPU** 1x **CPU** 10x **GPU RAM** 48GB **RAM** 65GB **GPU** 2x **CPU**`
- 🔎 **144GB** `** 20x **GPU RAM** 160GB **RAM** 288GB **GPU** 1x **CPU** 13x **GPU RAM** 80GB **RAM** 144GB **GPU** 1x **CPU** 10x **GPU RAM** 48GB **RAM** 65GB **GPU** 2x **CPU** 20x **GPU RAM*`
- 🔎 **48GB** `GPU** 1x **CPU** 13x **GPU RAM** 80GB **RAM** 144GB **GPU** 1x **CPU** 10x **GPU RAM** 48GB **RAM** 65GB **GPU** 2x **CPU** 20x **GPU RAM** 96GB **RAM** 144GB **GPU** 1x **CPU**`
- 🔎 **65GB** `U** 13x **GPU RAM** 80GB **RAM** 144GB **GPU** 1x **CPU** 10x **GPU RAM** 48GB **RAM** 65GB **GPU** 2x **CPU** 20x **GPU RAM** 96GB **RAM** 144GB **GPU** 1x **CPU** 4x **GPU RAM*`

## 🌱 fal.ai 定价（生成式 AI 云免费额度）（fal-pricing）
- 状态: ok | https://fal.ai/pricing
- 🔎 **288 GB** `ively priced GPU fleet, as low as $2.49/hr for H100. GPU VRAM List Price As low as B300 VRAM 288 GB List Price $12.99/h As low as $5.99/h GB200 VRAM 192 GB List Price $9.99/h As low as $5.`
- 🔎 **192 GB** `List Price As low as B300 VRAM 288 GB List Price $12.99/h As low as $5.99/h GB200 VRAM 192 GB List Price $9.99/h As low as $5.89/h B200 VRAM 192 GB List Price $7.99/h As low as $5.49`
- 🔎 **192 GB** `99/h As low as $5.99/h GB200 VRAM 192 GB List Price $9.99/h As low as $5.89/h B200 VRAM 192 GB List Price $7.99/h As low as $5.49/h H200 VRAM 141 GB List Price $6.00/h As low as $2.99`
- 🔎 **141 GB** `.99/h As low as $5.89/h B200 VRAM 192 GB List Price $7.99/h As low as $5.49/h H200 VRAM 141 GB List Price $6.00/h As low as $2.99/h H100 VRAM 80 GB List Price $4.50/h As low as $2.49/`
- 🔎 **80 GB** `.99/h As low as $5.49/h H200 VRAM 141 GB List Price $6.00/h As low as $2.99/h H100 VRAM 80 GB List Price $4.50/h As low as $2.49/h RTX PRO 6000 VRAM 96 GB List Price $4.00/h As low as`
- 🔎 **96 GB** `As low as $2.99/h H100 VRAM 80 GB List Price $4.50/h As low as $2.49/h RTX PRO 6000 VRAM 96 GB List Price $4.00/h As low as $1.99/h ## Model APIs Pricing ### Video Models Video models are`
- 🔎 **credits, depending on the model** `05 Units per $1 20 1000 characters ### 3D Models 3D models are billed in units, generations, or credits, depending on the model. The table shows the price per unit and the approximate units per $1. Model Unit Price Units pe`
- 🔎 **credits** `nits per $1 12.5 generations Unit generations Price $0.02 Units per $1 50 generations Unit credits Price $0.01 Units per $1 100 credits Unit credits Price $0.01 Units per $1 100 credits U`
- 🔎 **credits** `rations Price $0.02 Units per $1 50 generations Unit credits Price $0.01 Units per $1 100 credits Unit credits Price $0.01 Units per $1 100 credits Unit credits Price $0.01 Units per $1`
- 🔎 **credits** `$0.02 Units per $1 50 generations Unit credits Price $0.01 Units per $1 100 credits Unit credits Price $0.01 Units per $1 100 credits Unit credits Price $0.01 Units per $1 100 credits U`

## 🌱 LowEndBox RSS（免费 VPS 帖聚合雷达）（lowendbox-feed）
- 状态: ok | https://lowendbox.com/feed/
- 🔎 **4GB VPS for Only $3** `from $17.99/Year! appeared first on LowEndBox . - [Cheap VPS Deals in Toronto from EnderHost! Get a 4GB VPS for Only $3.84/Month!](https://lowendbox.com/blog/cheap-vps-deals-in-toronto-from-enderhost-get-a-4gb-vps-for-o`
- 🔎 **4gb-vps-for-only-3-84-month/) — Mon, 02 Nov 2026 12:00:00 +0000** `S for Only $3.84/Month!](https://lowendbox.com/blog/cheap-vps-deals-in-toronto-from-enderhost-get-a-4gb-vps-for-only-3-84-month/) — Mon, 02 Nov 2026 12:00:00 +0000 EnderHost has some wonderful deals in Toronto, Canada for us! Cheap pricing from a quality provid`
- 🔎 **4GB VPS for Only $3** `ider with a lot to offer. Check this out! The post Cheap VPS Deals in Toronto from EnderHost! Get a 4GB VPS for Only $3.84/Month! appeared first on LowEndBox . - [RackNerd’s Fall Giveaway Has Started! Win a Meta Quest 3`
- 🔎 **100GB Plan Only $8** `t on LowEndBox . - [Mango Mail Halloween Sale: Up to 40% Perfect Off on High Quality Email Hosting! 100GB Plan Only $8.70/Month!](https://lowendbox.com/blog/mango-mail-halloween-sale-up-to-40-perfect-off-on-high-qualit`
- 🔎 **100gb-plan-only-8-70-month/) — Fri, 30 Oct 2026 11:00:17 +0000** `s://lowendbox.com/blog/mango-mail-halloween-sale-up-to-40-perfect-off-on-high-quality-email-hosting-100gb-plan-only-8-70-month/) — Fri, 30 Oct 2026 11:00:17 +0000 It's Halloween and Mango Mail is celebrating with up to 40% percent OFF! This makes our 100GB pla`
- 🔎 **100GB plan only $8** `:17 +0000 It's Halloween and Mango Mail is celebrating with up to 40% percent OFF! This makes our 100GB plan only $8.70/mo. We're excited to let the community know and have them take advantage of the reduced prices.`
- 🔎 **100GB Plan Only $8** `tion ends. The post Mango Mail Halloween Sale: Up to 40% Perfect Off on High Quality Email Hosting! 100GB Plan Only $8.70/Month! appeared first on LowEndBox . - [Proton Unleashes Massive Footgun and Horrifies Its User`
- 🔎 **2GB VPS for only $16** `from ServerHost! No tricks here, just a wonderful treat: $500 in cold hard cash! Plus you can get a 2GB VPS for only $16.99/YEAR or a 4GB VPS for only $27.99/YEAR! Wow! The post 🎃 Did You Get Your 10 Bonus Entries in Ser`
- 🔎 **4GB VPS for only $27** `ust a wonderful treat: $500 in cold hard cash! Plus you can get a 2GB VPS for only $16.99/YEAR or a 4GB VPS for only $27.99/YEAR! Wow! The post 🎃 Did You Get Your 10 Bonus Entries in ServerHost&#8217;s $500 Giveaway Yet?`
- 🔎 **2GB VPS!](https://lowendbox** `on LowEndBox . - [Get Cheap Hosting in LA, NY or Atlanta from FlipperHost – Only $29.99/Year for a 2GB VPS!](https://lowendbox.com/blog/get-cheap-hosting-in-la-ny-or-atlanta-from-flipperhost-only-29-99-year-for-a-2gb-vps/) — M`

## 🌱 百度智能云免费试用（baidu-free）
- 状态: ok | https://cloud.baidu.com/campaign/free/index.html
- 🔎 **免费试用馆** `A6%86-pc%E5%A4%B4%E5%9B%BE.png) [新客特惠专场](https://cloud.baidu.com/campaign/experience/index.html) 企业免费试用馆 200+热销AI 基础云及企业应用产品0元试用 新客先领券 体验惠更多 新客先领券 再购买活动商品 实惠加倍 - 400元新用户专享券 50减20 100减50 500减130 800`
- 🔎 **免费额度** `TTPDNS 避免使用DNS所带来的域名劫持及域名更新生效不及时等问题 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 全网域名解析 300万次月免费额度 *![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)*`
- 🔎 **免费试用** `管理 ITM 智能管理接入域名流量，帮助用户策略化分配流量、高效利用带宽资源 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 流量智能调度 30天免费试用 *![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)*`
- 🔎 **免费额度** `LS 实时日志分析服务，轻松应对服务运维管理、商业趋势洞察、安全监控审计等 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 日志收集 500MB月免费额度 *![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)*`
- 🔎 **免费试用）** `度效率云服务 基于百度多年软件工程实践自主开发的DevOps解决方案 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 一站式服务 按用户计费（当前免费试用） *![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)*`
- 🔎 **免费试用）**** `2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)* 自定义看板、可视化报表 价格查询中 **¥** **按用户计费（当前免费试用）** 立即试用 通用文字识别标准版 对图片中的文字进行检测和识别，支持中、英、法、俄等10种语言 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 多`
- 🔎 **赠送50分钟机器人通话费用** `智能外呼 拟人的完成和客户语音交互，挖掘客户意图，高效准确地锁定意向客户 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 意向客户筛选 试用30天赠送50分钟机器人通话费用 *![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)*`
- 🔎 **流量调度服务 [产品详情 >](https://ai** `84%E5%8B%BE.svg)* 支持尺寸、数量等参数自定义设置 价格查询中 **¥** **免费体验** 立即试用 智能云解析 DNS 提供稳定、高效、安全灵活的内网和公网DNS解析以及流量调度服务 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 域名解析 公网DNS服务基础版 *![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733`
- 🔎 **流量调度稳定可靠** `*![](https://bj.bcebos.com/bce-cdn/2023-8/1692587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)* 流量调度稳定可靠 价格查询中 **¥** **免费体验** 立即试用 通用文字识别标准版 对图片中的文字进行检测和识别，支持中、英、法、俄等10种语言 [产品详情 >](https://ai.baidu.c`
- 🔎 **流量统计** `92587733426/%E9%BB%91%E8%89%B2%E7%9A%84%E5%8B%BE.svg)* 监测预警各类危险、违规行为 价格查询中 **¥** **免费体验** 立即试用 人流量统计 统计图像中的人体个数和流动趋势，以头肩为主要识别目标统计人数 [产品详情 >](https://ai.baidu.com/tech/ocr/general) 安防监测 5万次 有效期1年 *`

##    Oracle Cloud 免费层（Always Free 白嫖之王）（oracle-free）
- 状态: ok | https://www.oracle.com/cloud/free/
- 🔎 **Always Free Services in your Free Tier account** `*** You’ll have 30 days to use it to test your applications on all OCI services, in addition to Always Free Services in your Free Tier account. - #### 2 At any time during or after the 30-day period,* switch to a **Pay As You Go** account`
- 🔎 **Always Free Services** `tch to a **Pay As You Go** account. Pay only for services that exceed the monthly free amounts from Always Free Services. - #### 3 If you do nothing after 30 days, you’ll continue to get Always Free Services in your`
- 🔎 **Always Free Services in your Free Tier account** `nts from Always Free Services. - #### 3 If you do nothing after 30 days, you’ll continue to get Always Free Services in your Free Tier account. ## Oracle Cloud Free Tier Get cloud credits and start using Oracle Cloud services. #### Service`
- 🔎 **Always Free services and a Free Trial with US$300 of free cre** `Oracle Cloud Free Tier allows you to sign up for an Oracle Cloud account which provides a number of Always Free services and a Free Trial with US$300 of free credit to use on all eligible Oracle Cloud Infrastructure services for up to 30 days. The Always Free s`
- 🔎 **Always Free services are available for an unlimited period of** `0 of free credit to use on all eligible Oracle Cloud Infrastructure services for up to 30 days. The Always Free services are available for an unlimited period of time. The Free Trial services may be used until your US$300 of free credits are consumed or the 30`
- 🔎 **Always Free services are part of Oracle Cloud Free Tier** `il your US$300 of free credits are consumed or the 30 days has expired, whichever comes first. - Always Free services are part of Oracle Cloud Free Tier. Always Free services are available for an unlimited time. Some limitations apply. As new Always Fr`
- 🔎 **Always Free services are available for an unlimited time** `s has expired, whichever comes first. - Always Free services are part of Oracle Cloud Free Tier. Always Free services are available for an unlimited time. Some limitations apply. As new Always Free services become available, you will automatically be ab`
- 🔎 **Always Free services become available, you will automatically** `Free Tier. Always Free services are available for an unlimited time. Some limitations apply. As new Always Free services become available, you will automatically be able to use those as well. The following services are available as Always Free: - HeatW`
- 🔎 **Always Free:** `, you will automatically be able to use those as well. The following services are available as Always Free: - HeatWave - AMD-based Compute - Arm-based Ampere A1 Compute - Block Volume - O`
- 🔎 **Always Free account is permitted per person** `cle Sales team can help you sign up for Oracle Cloud Free Tier. - One Oracle Cloud Free Trial or Always Free account is permitted per person. Please note: - Creating or attempting to create multiple free accounts is prohibited. - Al`

##    Google Cloud 免费层（google-free）
- 状态: ok | https://cloud.google.com/free
- 🔎 **5 GB-months Standard Storage** `Cloud Storage Best-in-class performance, reliability, and pricing for all your storage needs. 5 GB-months Standard Storage - BigQuery Fully managed, petabyte scale, analytics data warehouse. 1 TB queries per month`
- 🔎 **1 TB queries per month** `-months Standard Storage - BigQuery Fully managed, petabyte scale, analytics data warehouse. 1 TB queries per month - Cloud Run A fully managed environment to run stateless containers, build apps, or host and de`
- 🔎 **1 GB storage** `restore NoSQL document database that simplifies storing, syncing, and querying data for apps. 1 GB storage - Pub/Sub A global service for real-time and reliable messaging and streaming data. 10 GB me`
- 🔎 **10 GB messages per month** `storage - Pub/Sub A global service for real-time and reliable messaging and streaming data. 10 GB messages per month - Cloud Run functions A serverless environment to build and connect cloud services with code.`
- 🔎 **5 GB of persistent disk storage** `Online development and operations environment accessible anywhere with your browser. Includes 5 GB of persistent disk storage - Workload Manager Rule-based validation service for evaluating your workloads running on Googl`
- 🔎 **100 GiB of CDC data from eligible first-party sources per month** `m Reliably replicates data across your databases and applications with minimal latency. Up to 100 GiB of CDC data from eligible first-party sources per month. - Application Integration A fully managed, no-code integration platform for enterprise applica`
- 🔎 **20 GiB of data processed per month** `integration platform for enterprise applications and data. Up to 400 integration executions and 20 GiB of data processed per month - Artifact Registry A secure storage registry for container images and language packages. 0.`
- 🔎 **0.5 GB of storage per month** `th - Artifact Registry A secure storage registry for container images and language packages. 0.5 GB of storage per month #### Explore more offers from Google Cloud | OFFER | KEY BENEFITS | | --- | --- | | ##### Gemini`
- 🔎 **8 vCPU Enterprise Plus instance, 64 GB of memory, and 100 GB of st** `SQL Free Trial Instance Start a 30-day [Cloud SQL](https://cloud.google.com/sql) free trial with an 8 vCPU Enterprise Plus instance, 64 GB of memory, and 100 GB of storage. Plus, new Google Cloud customers get [$300 in free credits](https://docs.cloud.google.com/sql`
- 🔎 **10 GB of storage at no cost** `ner Free Trial Create a 90-day [Spanner](https://cloud.google.com/spanner) free trial instance with 10 GB of storage at no cost. Plus, new Google Cloud customers get [$300 in free credits](https://console.cloud.google.com/freet`

##    AWS Free Tier（aws-free）
- 状态: ok | https://aws.amazon.com/free/
- 🔎 **Always free** `te the service, and any eligible credits automatically apply to usage beyond the trial limits. ### Always free ![Illustration of a document, gear, and cloud with code symbols, representing cloud-based coding o`
- 🔎 **always free within monthly usage limits on both the Free and ** `vices-gear-document-icon-560x258.3d9731b98f2f92c30d61d8bf5b6f4af42ec9d06e.png) 30+ AWS services are always free within monthly usage limits on both the Free and Paid plans. If you go beyond these limits or access paid features, credits are automatically applied`
- 🔎 **Free Tier Categories** `- [Overview](https://aws.amazon.com/free/?p=ft&z=subnav&loc=2) - Free Tier Categories - Featured Offers for Business - [Terms and Conditions](https://aws.amazon.com/free/terms/?p=ft&z=s`
- 🔎 **Free Tier** `ness - [Terms and Conditions](https://aws.amazon.com/free/terms/?p=ft&z=subnav&loc=6) - More # AWS Free Tier Get started for free with up to $200 in credits [Create a free account](https://signin.aws.amazon`
- 🔎 **Free Tier account, you get $100 in credits immediately** `mazon.com/console/home/) ## Get up to $200 in credits for new customers When you create a new AWS Free Tier account, you get $100 in credits immediately. As you explore key services, you can earn up to $100 more. That's up to $200 over 6 months to buil`
- 🔎 **Free plan** `0 over 6 months to build, break things, and experiment with no charges and no surprise bills on the Free plan. The account closes on its own 6 months after you open it or when your credits run out, whichever c`
- 🔎 **free plan to get started, paid plan to scale** `bf42784e3b9c3a5e4b387d48cb10b00f.png) ## Compare the plans Choose the plan that fits your needs — free plan to get started, paid plan to scale. | Benefits | Free plan | Paid plan | | --- | --- | --- | | Receive up to $200 USD free credits |`
- 🔎 **Free plan | Paid plan |** `Choose the plan that fits your needs — free plan to get started, paid plan to scale. | Benefits | Free plan | Paid plan | | --- | --- | --- | | Receive up to $200 USD free credits | ✔ | ✔ | | Free usage of select services`
- 🔎 **free credits | ✔ | ✔ |** `d plan to scale. | Benefits | Free plan | Paid plan | | --- | --- | --- | | Receive up to $200 USD free credits | ✔ | ✔ | | Free usage of select services | ✔ | ✔ | | Access to all AWS services | ✖ Limited to select servic`
- 🔎 **Free plan** `e learning for every data scientist and developer. Learn more ## Learn more about our offers ### Free plan ![Missing alt text value](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/dev`

##    Azure 免费服务（azure-free）
- 状态: ok | https://azure.microsoft.com/en-us/pricing/free-services
- 🔎 **always free to all Azure customers, and some are free for 12 ** `n to life with free services. These services are free up to the specified monthly amounts. Some are always free to all Azure customers, and some are free for 12 months to new customers only. [Get started with Azure](https://azure.microsoft.com/en-us/pricing/pu`
- 🔎 **12 months** `o the specified monthly amounts. Some are always free to all Azure customers, and some are free for 12 months to new customers only. [Get started with Azure](https://azure.microsoft.com/en-us/pricing/purchase`
- 🔎 **12 months** `//azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=free-services) 1. [*] *12 months free services is available only to new customers who have not previously had an Azure account or re`
- 🔎 **12 months** `ervices is available only to new customers who have not previously had an Azure account or received 12 months of free services. It is not currently available to customers who sign up directly for pay as you go`
- 🔎 **12 months** `India. Customers who try Azure free must move to pay as you go within 30 days to continue receiving 12 months free services. [![](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/acom_social_icon`
- 🔎 **free services** `[Sign in](https://portal.azure.com/) # Explore free Azure services Bring your vision to life with free services. These services are free up to the specified monthly amounts. Some are always free to all Azure cus`
- 🔎 **free services** `crosoft.com/en-us/pricing/purchase-options/azure-account?icid=free-services) 1. [*] *12 months free services is available only to new customers who have not previously had an Azure account or received 12 mont`
- 🔎 **free services** `ailable only to new customers who have not previously had an Azure account or received 12 months of free services. It is not currently available to customers who sign up directly for pay as you go in China and Ind`
- 🔎 **free services** `tomers who try Azure free must move to pay as you go within 30 days to continue receiving 12 months free services. [![](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/acom_social_icon_azure) Explor`

##    Fly.io 定价（免费层收缩观察）（fly-pricing）
- 状态: ok | https://fly.io/pricing
- 🔎 **1GB | $0** `ed-cpu-1x · 256MB | $0.0030 | $2.19 | | shared-cpu-2x · 512MB | $0.0061 | $4.39 | | shared-cpu-4x · 1GB | $0.0122 | $8.78 | | shared-cpu-6x · 1.5GB | $0.0183 | $13.16 | | shared-cpu-8x · 2GB | $0.0244 | $17.5`
- 🔎 **1.5GB | $0** `ared-cpu-2x · 512MB | $0.0061 | $4.39 | | shared-cpu-4x · 1GB | $0.0122 | $8.78 | | shared-cpu-6x · 1.5GB | $0.0183 | $13.16 | | shared-cpu-8x · 2GB | $0.0244 | $17.55 | | performance-1x · 2GB | $0.0458 | $33.0`
- 🔎 **2GB | $0** `red-cpu-4x · 1GB | $0.0122 | $8.78 | | shared-cpu-6x · 1.5GB | $0.0183 | $13.16 | | shared-cpu-8x · 2GB | $0.0244 | $17.55 | | performance-1x · 2GB | $0.0458 | $33.00 | | performance-2x · 4GB | $0.0917 | $66.`
- 🔎 **2GB | $0** `d-cpu-6x · 1.5GB | $0.0183 | $13.16 | | shared-cpu-8x · 2GB | $0.0244 | $17.55 | | performance-1x · 2GB | $0.0458 | $33.00 | | performance-2x · 4GB | $0.0917 | $66.00 | | performance-4x · 8GB | $0.1833 | $132`
- 🔎 **4GB | $0** `ed-cpu-8x · 2GB | $0.0244 | $17.55 | | performance-1x · 2GB | $0.0458 | $33.00 | | performance-2x · 4GB | $0.0917 | $66.00 | | performance-4x · 8GB | $0.1833 | $132.01 | | performance-6x · 12GB | $0.2750 | $1`
- 🔎 **8GB | $0** `rmance-1x · 2GB | $0.0458 | $33.00 | | performance-2x · 4GB | $0.0917 | $66.00 | | performance-4x · 8GB | $0.1833 | $132.01 | | performance-6x · 12GB | $0.2750 | $198.01 | | performance-8x · 16GB | $0.3667 |`
- 🔎 **12GB | $0** `mance-2x · 4GB | $0.0917 | $66.00 | | performance-4x · 8GB | $0.1833 | $132.01 | | performance-6x · 12GB | $0.2750 | $198.01 | | performance-8x · 16GB | $0.3667 | $264.01 | | performance-10x · 20GB | $0.4584 |`
- 🔎 **16GB | $0** `nce-4x · 8GB | $0.1833 | $132.01 | | performance-6x · 12GB | $0.2750 | $198.01 | | performance-8x · 16GB | $0.3667 | $264.01 | | performance-10x · 20GB | $0.4584 | $330.01 | | performance-12x · 24GB | $0.5500`
- 🔎 **20GB | $0** `e-6x · 12GB | $0.2750 | $198.01 | | performance-8x · 16GB | $0.3667 | $264.01 | | performance-10x · 20GB | $0.4584 | $330.01 | | performance-12x · 24GB | $0.5500 | $396.02 | | performance-14x · 28GB | $0.6417`
- 🔎 **24GB | $0** `-8x · 16GB | $0.3667 | $264.01 | | performance-10x · 20GB | $0.4584 | $330.01 | | performance-12x · 24GB | $0.5500 | $396.02 | | performance-14x · 28GB | $0.6417 | $462.02 | | performance-16x · 32GB | $0.7334`

## 🔔 Render 定价（免费 Web 服务）（render-pricing）
- 状态: ok | https://render.com/pricing
- 🔎 **5 GB of bandwidth included** `Get in touch](https://render.com/contact) - Connect your repo, and go - Deploy up to 25 services - 5 GB of bandwidth included - Single-service previews - Global regions & CDN - Custom domains - Firewall & DDoS mitigation - Da`
- 🔎 **25 GB bandwidth included** `tigation - Database PITR - Chat support - All Hobby features, plus: - Unlimited seats & services - 25 GB bandwidth included - Full-stack previews - Horizontal autoscaling - Isolated environments - OIDC authentication - AWS`
- 🔎 **1 TB of bandwidth included** `ation - AWS Private Links - Workspace audit logs - All Pro features, plus: - Multiple workspaces - 1 TB of bandwidth included - Extended metrics retention - Inbound IP rules - HIPAA-compliant workspaces - SAML SSO & SCIM - Ad`
- 🔎 **2 GB RAM | 1c-2g |** `| --- | --- | --- | | Less than 1 CPU | $7/month | 512 MB RAM | 0.5c-512mb | | 1 CPU | $25/month | 2 GB RAM | 1c-2g | | 2 CPU | $85/month | 4 GB RAM | 2c-4g | | 2 CPU | $135/month | 8 GB RAM | 2c-8g | | 2 CPU | $200/m`
- 🔎 **4 GB RAM | 2c-4g |** `$7/month | 512 MB RAM | 0.5c-512mb | | 1 CPU | $25/month | 2 GB RAM | 1c-2g | | 2 CPU | $85/month | 4 GB RAM | 2c-4g | | 2 CPU | $135/month | 8 GB RAM | 2c-8g | | 2 CPU | $200/month | 16 GB RAM | 2c-16g | | 4 CPU | $17`
- 🔎 **8 GB RAM | 2c-8g |** `PU | $25/month | 2 GB RAM | 1c-2g | | 2 CPU | $85/month | 4 GB RAM | 2c-4g | | 2 CPU | $135/month | 8 GB RAM | 2c-8g | | 2 CPU | $200/month | 16 GB RAM | 2c-16g | | 4 CPU | $175/month | 8 GB RAM | 4c-8g | | 4 CPU | $22`
- 🔎 **16 GB RAM | 2c-16g |** `U | $85/month | 4 GB RAM | 2c-4g | | 2 CPU | $135/month | 8 GB RAM | 2c-8g | | 2 CPU | $200/month | 16 GB RAM | 2c-16g | | 4 CPU | $175/month | 8 GB RAM | 4c-8g | | 4 CPU | $225/month | 16 GB RAM | 4c-16g | | 4 CPU | $35`
- 🔎 **8 GB RAM | 4c-8g |** `$135/month | 8 GB RAM | 2c-8g | | 2 CPU | $200/month | 16 GB RAM | 2c-16g | | 4 CPU | $175/month | 8 GB RAM | 4c-8g | | 4 CPU | $225/month | 16 GB RAM | 4c-16g | | 4 CPU | $350/month | 32 GB RAM | 4c-32g | | 8 CPU | $`
- 🔎 **16 GB RAM | 4c-16g |** `$200/month | 16 GB RAM | 2c-16g | | 4 CPU | $175/month | 8 GB RAM | 4c-8g | | 4 CPU | $225/month | 16 GB RAM | 4c-16g | | 4 CPU | $350/month | 32 GB RAM | 4c-32g | | 8 CPU | $300/month | 16 GB RAM | 8c-16g | | 8 CPU | $`
- 🔎 **32 GB RAM | 4c-32g |** `$175/month | 8 GB RAM | 4c-8g | | 4 CPU | $225/month | 16 GB RAM | 4c-16g | | 4 CPU | $350/month | 32 GB RAM | 4c-32g | | 8 CPU | $300/month | 16 GB RAM | 8c-16g | | 8 CPU | $450/month | 32 GB RAM | 8c-32g | | 8 CPU | $`

##    Koyeb 定价（免费层）（koyeb-pricing）
- 状态: ok | https://www.koyeb.com/pricing
- 🔎 **48GB** `ing, secure VMs on top of high-performance bare metal servers. /Popular instances RTX-A6000 vRAM 48GB vRAM 48GB $0.75 /hour $0.000208 /sec L40S vRAM 48GB vRAM 48GB $1.20 /hour $0.000333 /sec A`
- 🔎 **48GB** `VMs on top of high-performance bare metal servers. /Popular instances RTX-A6000 vRAM 48GB vRAM 48GB $0.75 /hour $0.000208 /sec L40S vRAM 48GB vRAM 48GB $1.20 /hour $0.000333 /sec A100 vRAM 8`
- 🔎 **48GB** `vers. /Popular instances RTX-A6000 vRAM 48GB vRAM 48GB $0.75 /hour $0.000208 /sec L40S vRAM 48GB vRAM 48GB $1.20 /hour $0.000333 /sec A100 vRAM 80GB vRAM 80GB $1.60 /hour $0.000444 /sec A`
- 🔎 **48GB** `ular instances RTX-A6000 vRAM 48GB vRAM 48GB $0.75 /hour $0.000208 /sec L40S vRAM 48GB vRAM 48GB $1.20 /hour $0.000333 /sec A100 vRAM 80GB vRAM 80GB $1.60 /hour $0.000444 /sec Autoscaling`
- 🔎 **80GB** `B $0.75 /hour $0.000208 /sec L40S vRAM 48GB vRAM 48GB $1.20 /hour $0.000333 /sec A100 vRAM 80GB vRAM 80GB $1.60 /hour $0.000444 /sec Autoscaling Scale-to-Zero Per second billing Get starte`
- 🔎 **80GB** `our $0.000208 /sec L40S vRAM 48GB vRAM 48GB $1.20 /hour $0.000333 /sec A100 vRAM 80GB vRAM 80GB $1.60 /hour $0.000444 /sec Autoscaling Scale-to-Zero Per second billing Get started Trusted`
- 🔎 **44GB** `g a GitHub repository or pre-built container Price per RTX-4000-SFF-ADA $0.50 /hr vCPU 6 RAM 44GB Disk 240GB L4 $0.70 /hr vCPU 6 RAM 32GB Disk 160GB RTX-A6000 $0.75 /hr vCPU 6 RAM 6`
- 🔎 **240GB** `epository or pre-built container Price per RTX-4000-SFF-ADA $0.50 /hr vCPU 6 RAM 44GB Disk 240GB L4 $0.70 /hr vCPU 6 RAM 32GB Disk 160GB RTX-A6000 $0.75 /hr vCPU 6 RAM 64GB Disk 16`
- 🔎 **32GB** `ice per RTX-4000-SFF-ADA $0.50 /hr vCPU 6 RAM 44GB Disk 240GB L4 $0.70 /hr vCPU 6 RAM 32GB Disk 160GB RTX-A6000 $0.75 /hr vCPU 6 RAM 64GB Disk 160GB L40S $1.20 /hr vCPU 15 RAM`
- 🔎 **160GB** `-4000-SFF-ADA $0.50 /hr vCPU 6 RAM 44GB Disk 240GB L4 $0.70 /hr vCPU 6 RAM 32GB Disk 160GB RTX-A6000 $0.75 /hr vCPU 6 RAM 64GB Disk 160GB L40S $1.20 /hr vCPU 15 RAM 64GB Disk`

##    Railway 定价（试用金观察）（railway-pricing）
- 状态: ok | https://railway.com/pricing
- 🔎 **1 vCPU / 0** `small apps on Railway - Start with a 30-day free trial with $5 credits, then $1 per month - Up to 1 vCPU / 0.5 GB RAM per service - 0.5 GB of volume storage - Community support No credit card required ### H`
- 🔎 **5 GB RAM per service** `on Railway - Start with a 30-day free trial with $5 credits, then $1 per month - Up to 1 vCPU / 0.5 GB RAM per service - 0.5 GB of volume storage - Community support No credit card required ### Hobby $5minimum usage`
- 🔎 **0.5 GB of volume storage** `th a 30-day free trial with $5 credits, then $1 per month - Up to 1 vCPU / 0.5 GB RAM per service - 0.5 GB of volume storage - Community support No credit card required ### Hobby $5minimum usage For hobbyist developers b`
- 🔎 **48 vCPU / 48 GB RAM per service** `hly usage credits - After credits are used, you'll only be charged for extra resource usage - Up to 48 vCPU / 48 GB RAM per service - Up to 5 replicas, at 8 vCPU / 8 GB RAM per replica - Up to 5 GB storage - Single developer worksp`
- 🔎 **8 vCPU / 8 GB RAM per replica** `be charged for extra resource usage - Up to 48 vCPU / 48 GB RAM per service - Up to 5 replicas, at 8 vCPU / 8 GB RAM per replica - Up to 5 GB storage - Single developer workspace - Community support - 99.9% Availability Target -`
- 🔎 **5 GB storage** `Up to 48 vCPU / 48 GB RAM per service - Up to 5 replicas, at 8 vCPU / 8 GB RAM per replica - Up to 5 GB storage - Single developer workspace - Community support - 99.9% Availability Target - 7-Day Log History -`
- 🔎 **000 vCPU / 1 TB RAM per service** `y usage credits - After credits are used, you'll only be charged for extra resource usage - Up to 1,000 vCPU / 1 TB RAM per service - Up to 42 replicas, at 24 vCPU / 24 GB RAM per replica - Up to 1 TB storage - Unlimited workspace`
- 🔎 **24 vCPU / 24 GB RAM per replica** `charged for extra resource usage - Up to 1,000 vCPU / 1 TB RAM per service - Up to 42 replicas, at 24 vCPU / 24 GB RAM per replica - Up to 1 TB storage - Unlimited workspace seats included - Railway Support - 99.99% Availability T`
- 🔎 **1 TB storage** `o 1,000 vCPU / 1 TB RAM per service - Up to 42 replicas, at 24 vCPU / 24 GB RAM per replica - Up to 1 TB storage - Unlimited workspace seats included - Railway Support - 99.99% Availability Target - 30-Day Log Hi`
- 🔎 **400 vCPU / 2,4 TB RAM per service** `.999% Availability Target - Highest compute limits - Dedicated VMs - Bring your own cloud - Up to 2,400 vCPU / 2,4 TB RAM per service - Up to 50 replicas, at 48 vCPU / 48 GB RAM per service Memory $0.00000386 per GB / sec CPU $0.`

##    GitHub Codespaces（免费 120 core-hours/月）（codespaces-pricing）
- 状态: ok | https://github.com/features/codespaces
- 🔎 **15 GB of storage each month** `l provide users in the free plan 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month. See how it's balanced on the billing page. #### Is Codespaces available for teams and companies?`
- 🔎 **free plan 120 core hours or 60 hours of run time on a 2 core codespac** `ee the next question) for their private and internal repositories. GitHub will provide users in the free plan 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month. See how it's balanced on the billing page. #### Is Codespaces`
- 🔎 **free monthly usage** `e for open source maintainers? Codespaces provides both maintainers and contributors with generous free monthly usage.`
- 🔎 **core hours** `estion) for their private and internal repositories. GitHub will provide users in the free plan 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month. See how it's balan`
- 🔎 **120** `t question) for their private and internal repositories. GitHub will provide users in the free plan 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month. See how`
- 🔎 **free** `who pays for the user's codespace. All personal (individual) GitHub.com accounts include a quota of free usage each month, which organizations can enable (see the next question) for their private and inte`
- 🔎 **free** `ee the next question) for their private and internal repositories. GitHub will provide users in the free plan 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month`
- 🔎 **free** `able Codespaces in an organization in our docs. #### How much does Codespaces cost? Codespaces is free for individual use up to 60 hours a month and comes with simple, pay-as-you-go pricing after that.`
- 🔎 **free** `ice anytime, from any machine via LinkedIn. These courses will be unlocked on LinkedIn Learning for free through Feb. 2023. Learn more about LinkedIn Learning and GitHub Codespaces here. #### How do I en`
- 🔎 **free** `### How do I enable Codespaces on GitHub? Codespaces is on by default for developers with a GitHub free account. If you belong to an organization, there may be a policy that prevents cloning—but if you c`

##    Cloudflare Workers 定价（免费 10 万请求/天）（cloudflare-workers）
- 状态: ok | https://developers.cloudflare.com/workers/platform/pricing/
- 🔎 **1 GB | 1 GB, + $0** `$5.00/million | | List requests | 1,000 / day | 1 million/month, + $5.00/million | | Stored data | 1 GB | 1 GB, + $0.50/ GB-month | | Namespaces | 1,000 | Unlimited, with a default limit of 1,000. First 1,000 include`
- 🔎 **1 GB-month | 1 GB-month included + $0** `lliseconds included per month + $0.02 per additional million CPU milliseconds | | Storage (GB-mo) | 1 GB-month | 1 GB-month included + $0.20/ GB-month | | Steps | 3,000 per day | 500,000 included per month + $0.80/ additional 100,000 per`
- 🔎 **5 GB (total) | First 5 GB included + $0** `,000 / day | First 50 million / month included + $1.00 / million rows | | Storage (per GB stored) | 5 GB (total) | First 5 GB included + $0.75 / GB-mo | | Databases | 10 | First 100,000 included + $0.10 per additional database per month. |`
- 🔎 **000 GB-s of billable compute duration is rounded up to 1,000,000 G** `is rounded up to the next billable unit before the corresponding rate is applied. For example, 500,000 GB-s of billable compute duration is rounded up to 1,000,000 GB-s and billed accordingly. | | Free plan | Paid plan | | --- | --- | --- | | Requests | 100,000 /`
- 🔎 **000 GB-s / day | 400,000 GB-s / month, + $12** `ncludes HTTP requests, RPC sessions1, WebSocket messages2, and alarm invocations | | Duration3 | 13,000 GB-s / day | 400,000 GB-s / month, + $12.50/million GB-s4,5 | Footnotes 1 Each [RPC session](https://developers.cloudflare.com/workers/run`
- 🔎 **5 GB (total) | 5 GB-month, + $0** `| 100,000 / day | First 50 million / month included + $1.00 / million rows | | SQL Stored data 5 | 5 GB (total) | 5 GB-month, + $0.20/ GB-month | Footnotes 1 Rows read and rows written included limits and rates match [D1 pricing`
- 🔎 **1 GB, + $0** `3 | 1 million, + $1.00/million | | Delete requests4 | 1 million, + $1.00/million | | Stored data5 | 1 GB, + $0.20/ GB-month | Footnotes 1 A request unit is defined as 4 KB of data read or written. A request t`
- 🔎 **10 GB-month / month | $0** `. | | Free | Standard storage | Infrequent Access storage | | --- | --- | --- | --- | | Storage | 10 GB-month / month | $0.015 / GB-month | $0.01 / GB-month | | Class A Operations | 1 million requests / month | $4.50 / mil`
- 🔎 **25 GiB-hours/month included +$0** `Memory | CPU | Disk | | --- | --- | --- | --- | | **Free** | N/A | N/A | N/A | | **Workers Paid** | 25 GiB-hours/month included +$0.0000025 per additional GiB-second | 375 vCPU-minutes/month \+ $0.000020 per additional vCPU-second`
- 🔎 **375 vCPU-minutes/month \+ $0** `/A | N/A | | **Workers Paid** | 25 GiB-hours/month included +$0.0000025 per additional GiB-second | 375 vCPU-minutes/month \+ $0.000020 per additional vCPU-second | 200 GB-hours/month +$0.00000007 per additional GB-second | You`

##    HuggingFace 定价（Spaces 免费 CPU 档）（hf-spaces）
- 状态: ok | https://huggingface.co/pricing
- 🔎 **500TB? [Contact sales](https://huggingface** `DN included at no extra cost. AWS S3 $23 Backblaze Overdrive $15 HF Hub $8–12 Need more than 500TB? [Contact sales](https://huggingface.co/contact/sales) for custom pricing. Base $12 /TB/mo Public repositories $18 /TB/mo Private r`
- 🔎 **50TB+ -20%** `ales) for custom pricing. Base $12 /TB/mo Public repositories $18 /TB/mo Private repositories 50TB+ -20% $10 /TB/mo Public repositories $16 /TB/mo Private repositories 200TB+ -25% $9 /TB/mo Public`
- 🔎 **200TB+ -25%** `rivate repositories 50TB+ -20% $10 /TB/mo Public repositories $16 /TB/mo Private repositories 200TB+ -25% $9 /TB/mo Public repositories $14 /TB/mo Private repositories 500TB+ -33% $8 /TB/mo Public r`
- 🔎 **500TB+ -33%** `rivate repositories 200TB+ -25% $9 /TB/mo Public repositories $14 /TB/mo Private repositories 500TB+ -33% $8 /TB/mo Public repositories $12 /TB/mo Private repositories Hub ## Explore, experiment, col`
- 🔎 **2 vCPU | 16 GB | - | - | FREE |** `celerator | VRAM | Hourly price Monthly price | | --- | --- | --- | --- | --- | --- | | CPU Basic | 2 vCPU | 16 GB | - | - | FREE | | CPU Upgrade | 8 vCPU | 32 GB | - | - | $0.03 $22 | | ZeroGPU | dynamic | dynamic | Nvidia RTX Pro`
- 🔎 **8 vCPU | 32 GB | - | - | $0** `| --- | --- | --- | --- | --- | --- | | CPU Basic | 2 vCPU | 16 GB | - | - | FREE | | CPU Upgrade | 8 vCPU | 32 GB | - | - | $0.03 $22 | | ZeroGPU | dynamic | dynamic | Nvidia RTX Pro 6000 Blackwell | up to 96 GB | FREE | | Nvi`
- 🔎 **96 GB | FREE |** `| 32 GB | - | - | $0.03 $22 | | ZeroGPU | dynamic | dynamic | Nvidia RTX Pro 6000 Blackwell | up to 96 GB | FREE | | Nvidia T4 - small | 4 vCPU | 15 GB | Nvidia T4 | 16 GB | $0.40 $288 | | Nvidia T4 - medium | 8 vC`
- 🔎 **4 vCPU | 15 GB | Nvidia T4 | 16 GB | $0** `PU | dynamic | dynamic | Nvidia RTX Pro 6000 Blackwell | up to 96 GB | FREE | | Nvidia T4 - small | 4 vCPU | 15 GB | Nvidia T4 | 16 GB | $0.40 $288 | | Nvidia T4 - medium | 8 vCPU | 30 GB | Nvidia T4 | 16 GB | $0.60 $432 | | 1x Nvidia L4 |`
- 🔎 **8 vCPU | 30 GB | Nvidia T4 | 16 GB | $0** `EE | | Nvidia T4 - small | 4 vCPU | 15 GB | Nvidia T4 | 16 GB | $0.40 $288 | | Nvidia T4 - medium | 8 vCPU | 30 GB | Nvidia T4 | 16 GB | $0.60 $432 | | 1x Nvidia L4 | 8 vCPU | 30 GB | Nvidia L4 | 24 GB | $0.80 $576 | | 4x Nvidia L4 | 48 vC`
- 🔎 **8 vCPU | 30 GB | Nvidia L4 | 24 GB | $0** `40 $288 | | Nvidia T4 - medium | 8 vCPU | 30 GB | Nvidia T4 | 16 GB | $0.60 $432 | | 1x Nvidia L4 | 8 vCPU | 30 GB | Nvidia L4 | 24 GB | $0.80 $576 | | 4x Nvidia L4 | 48 vCPU | 186 GB | Nvidia L4 | 96 GB | $3.80 $2,736 | | 1x Nvidia L40S |`

##    Kaggle Notebooks（每周 30h 免费 GPU）（kaggle-notebooks）
- 状态: ok | https://www.kaggle.com/docs/notebooks
- 🔎 **20 GBs of output from a Notebook may be saved to disk in /kaggle/w** `s. If you don’t, you risk consequences for rule-breaking in the Competition. #### Notebooks Up to 20 GBs of output from a Notebook may be saved to disk in /kaggle/working. This data is saved automatically and you can then reuse that data in any future Notebook: ju`
- 🔎 **transferable and cannot be exchanged for cash or any other goods or ** `le may terminate the extra GPU hours for their linked Kaggle account. - The extra GPU hours are non-transferable and cannot be exchanged for cash or any other goods or services. - The use of Kaggle's GPU resources is subject to Kaggle's Terms of Use and other applicab`
- 🔎 **idle time for your interactive session** `el Skylake CPUs. CPU Specifications While editing a Notebook, you are provided with 20 minutes of idle time for your interactive session. If the code is not modified or executed in that time the current interactive session will end. If`
- 🔎 **suspend the Promotion at any time, with or without notice** `Account via the settings page at any time. **Legal Terms** - Kaggle reserves the right to end or suspend the Promotion at any time, with or without notice, at its sole discretion. The end date of the Promotion may not be publicly announced and can occur`
- 🔎 **/modify-project) GCP account to query any data that i** `-118720642.1583860775) but requires a [billing-enabled](https://cloud.google.com/billing/docs/how-to/modify-project) GCP account to query any data that isn’t publicly released by BigQuery. You should carefully review the prices of BigQuery before trying`
- 🔎 **per month)** `are able to use the storage space for any type of data and only pay for used storage space (per GB per month). Google Cloud Storage is a paid service and requires a [billing-enabled](https://cloud.google.com/`
- 🔎 **/modify-project) GCP account** `rage is a paid service and requires a [billing-enabled](https://cloud.google.com/billing/docs/how-to/modify-project) GCP account. You should carefully review the prices of GCS before trying the integration in Kaggle Notebooks, a`
- 🔎 **/modify-project) GCP account** `toML is a paid service and requires a [billing-enabled](https://cloud.google.com/billing/docs/how-to/modify-project) GCP account. You should carefully review the prices of AutoML before trying the integration in Kaggle Notebooks`
- 🔎 **GPU** `nstalled packages, the ability to mount versioned data sources, customizable compute resources like GPUs, and more. #### Notebook Versions and Containers When you create a Notebook version using 'Save`
- 🔎 **GPU** `still need to have internet disabled to be submitted into select competitions. ##### Adding a free GPU You can add a single NVIDIA Tesla P100 to your Notebook for free. GPU environments have lower CPU`

##    阿里云免费试用（aliyun-free）
- 状态: ok | https://free.aliyun.com
- 🔎 **免费试用** `# 免费试用 立即领用云产品，开启云上实践之旅 试用规则 [我的试用](https://usercenter2.aliyun.com/home/myfreetier) 170+云产品免费试用 每款产品均`
- 🔎 **免费试用** `# 免费试用 立即领用云产品，开启云上实践之旅 试用规则 [我的试用](https://usercenter2.aliyun.com/home/myfreetier) 170+云产品免费试用 每款产品均可独立试用，互不影响资格 先试后买更优惠 试用结束后仍可享受新用户优惠价格 非预期费用可退 非预期费用支持退款，安心试用 可试用人群 产品筛选 类目筛选 清除筛选 可试`
- 🔎 **免费试用？** `个人开发者适用 ### 企业客户适用 *核心业务场景组合*，助力开发者普惠上云 阿里云产品赋能多种场景，助力开发者无忧用云 活动规则 阿里云产品赋能多种场景 活动规则 常见问题 什么是免费试用？ 免费试用旨在面向产品新用户，提供一定时间段内或一定额度内免费的阿里云产品。试用服务可以在指定的时间段内免费使用；额度限定的产品可在指定额度内免费使用。有关免费提供的服务和相应的限制，在试用产品卡片`
- 🔎 **免费试用旨在面向产品新用户，提供一定时间段内或一定额度内免费的阿里云产品** `### 企业客户适用 *核心业务场景组合*，助力开发者普惠上云 阿里云产品赋能多种场景，助力开发者无忧用云 活动规则 阿里云产品赋能多种场景 活动规则 常见问题 什么是免费试用？ 免费试用旨在面向产品新用户，提供一定时间段内或一定额度内免费的阿里云产品。试用服务可以在指定的时间段内免费使用；额度限定的产品可在指定额度内免费使用。有关免费提供的服务和相应的限制，在试用产品卡片中有详细说明。 为什么我无法享受试用优惠？ 请查看产品试用规则，如符合条`
- 🔎 **免费试用活动** `过相关产品，如有过试用或购买记录则无法再试用；（3）建议检查下是否因为有同人账号已经参与过活动，导致对应账号无法领取试用；（4）您需要从试用中心页面开通产品才能享受使用权益，从其他开通页面进入无法参与免费试用活动。 可以延长试用时间吗？ 每个账号只有一次试用权益，且试用时间无法延长。如有需要可购买产品；如不想继续使用，请及时清理资源，避免产生可能的扣费。 试用产品到期后数据是否会保留？ 到期后数据会保`
- 🔎 **免费试用** `会被释放，数据会被清理，请提前做好备份。 [阅读更多](https://help.aliyun.com/document_detail/612761.html) 更多服务 云市场SaaS和API免费试用 近万款热销产品最长免费试用180天，每月更新！ 权益中心 用云无忧，普惠好价，99 计划助力快速上云 云大使官方推荐返现计划 推荐新用户下单得现金奖励，最高返佣35%`
- 🔎 **免费试用180天，每月更新！** `做好备份。 [阅读更多](https://help.aliyun.com/document_detail/612761.html) 更多服务 云市场SaaS和API免费试用 近万款热销产品最长免费试用180天，每月更新！ 权益中心 用云无忧，普惠好价，99 计划助力快速上云 云大使官方推荐返现计划 推荐新用户下单得现金奖励，最高返佣35%`
- 🔎 **每月更新！** `读更多](https://help.aliyun.com/document_detail/612761.html) 更多服务 云市场SaaS和API免费试用 近万款热销产品最长免费试用180天，每月更新！ 权益中心 用云无忧，普惠好价，99 计划助力快速上云 云大使官方推荐返现计划 推荐新用户下单得现金奖励，最高返佣35%`
- 🔎 **云服务器** `惠 试用结束后仍可享受新用户优惠价格 非预期费用可退 非预期费用支持退款，安心试用 可试用人群 产品筛选 类目筛选 清除筛选 可试用人群 企业认证个人认证 产品类别 *长效普惠的云服务器*，助力业务创新提速 网站搭建、小程序开发、游戏加速等多场景精准适配，快速部署、极简体验 活动规则 网站搭建、小程序开发、游戏加速等多场景精准适配，快速部署、极简体验 活动规则 ### 个人`
- 🔎 **试用** `# 免费试用 立即领用云产品，开启云上实践之旅 试用规则 [我的试用](https://usercenter2.aliyun.com/home/myfreetier) 170+云产品免费试用 每款产品均可独立试用，互不影响资格 先试后买更优惠`
