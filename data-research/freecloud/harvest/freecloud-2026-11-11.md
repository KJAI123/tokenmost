# freecloud 采集快照 2026-11-11

- 采集时间: 2026-11-11T02:32:18Z（pagesift 内核·零 LLM 参与·遵守 robots.txt·两次观测确认制）
- 源数: 58 | 🔔变化: aws-free, railway-pricing | 👀观察中: himitsushell, gpunz | 🌱首跑基线: 0 | 失败: valtown-pricing, colab-faq, google-free, render-pricing, codespaces-pricing, hf-spaces, idrive-e2, replit-pricing, scaleway-pricing, shakticloud

##    InstaBox 定价（Agent 云电脑·文章样例主角）（instabox-pricing）
- 状态: ok | https://instabox.sh/pricing
- 🔎 **1 MiB (`truncated`), and bytes that are not UTF-8 become U+FFFD (** `output fail with a broken pipe. Exec output is UTF-8 text: without streaming each stream is cut at 1 MiB (`truncated`), and bytes that are not UTF-8 become U+FFFD (`invalidUtf8`), so read files with `GET /v1/machines/{id}/files/content` or `instabox pull`/`cp`, no`
- 🔎 **4 vCPUs / 8 GiB by default, a 16 GiB root disk (8 GiB on `herdr` an** `cker microVM, Debian 13 (trixie) amd64 (`ci`: Ubuntu 24.04; `omarchy`: Arch Linux), kernel 6.18.60, 4 vCPUs / 8 GiB by default, a 16 GiB root disk (8 GiB on `herdr` and `orca`, 24 GiB on `omarchy`) and a 20 GiB persistent disk at `/data` (home is `/data/home`). Pytho`
- 🔎 **24 GiB on `omarchy`) and a 20 GiB persistent disk at `/data` (home** `inux), kernel 6.18.60, 4 vCPUs / 8 GiB by default, a 16 GiB root disk (8 GiB on `herdr` and `orca`, 24 GiB on `omarchy`) and a 20 GiB persistent disk at `/data` (home is `/data/home`). Python 3.13 with `python3 -m venv` and pip on every template but `ci` (Python 3.1`
- 🔎 **1 GiB on 2/4, ~2 GiB on 4/8)** `10 days, in snapshots; your own `TMPDIR` is kept) and `/tmp` is capped at a quarter of guest RAM (~1 GiB on 2/4, ~2 GiB on 4/8). Older machines (`echo $TMPDIR` empty): `/tmp` is about half guest RAM (~2 GiB on 2/4, ~4 GiB on 4/`
- 🔎 **2 GiB on 2/4, ~4 GiB on 4/8); for big staging set `TMPDIR=$HOME/t** `GiB on 2/4, ~2 GiB on 4/8). Older machines (`echo $TMPDIR` empty): `/tmp` is about half guest RAM (~2 GiB on 2/4, ~4 GiB on 4/8); for big staging set `TMPDIR=$HOME/tmp` (home is `/data/home`; on `agent-browser`, `universal` and `t3` the top of `/data` is the user's`
- 🔎 **4 GiB (2/4: 4 GiB), listed in `/etc/fstab` so it stays on across ** `e size. - Swap: every machine gets `/data/swapfile` at its first boot, the size of its memory up to 4 GiB (2/4: 4 GiB), listed in `/etc/fstab` so it stays on across stop and start; it is skipped (and the guest agent logs why) when `/data` would keep under 1 GiB, or`
- 🔎 **1 GiB, or a tenth of the disk, free** `n across stop and start; it is skipped (and the guest agent logs why) when `/data` would keep under 1 GiB, or a tenth of the disk, free. `swapon`, `swapoff` and `mkswap` are on the user PATH (changing swap takes `sudo`). Removed (`sudo`
- 🔎 **20 GiB by default; at create it comes with the size, so leave `per** `topped: resume it, then stop it, which is what `--restart` does). - Disk: one per machine, `/data`, 20 GiB by default; at create it comes with the size, so leave `persistentDiskGiB` out (another size is `400 spec_not_allowed`; `diskGiB` is the TypeScript SDK option`
- 🔎 **1024 GiB; it grows while running (no restart) or at the next start, ** `x resize <machine> --disk N [--restart]` or `PATCH /v1/machines/{id}` `{"persistentDiskGiB": N}`: 1-1024 GiB; it grows while running (no restart) or at the next start, and shrinks only while stopped when the data plus 10% (at least 1 GiB) fits (else `409 disk_too_smal`
- 🔎 **1 GiB) fits (else `409 disk_too_small`); at most 200 GiB on Pro, ** `(no restart) or at the next start, and shrinks only while stopped when the data plus 10% (at least 1 GiB) fits (else `409 disk_too_small`); at most 200 GiB on Pro, 500 GiB on Builder, 1024 GiB on Team and Enterprise (`429 quota_exceeded`). The system disk is the t`

##    E2B 定价（Agent 沙盒）（e2b-pricing）
- 状态: ok | https://e2b.dev/pricing
- 🔎 **credits (+usage costs)** `More. Free Hobby tier, and paid upgrades to cover all needs. Separate usage costs. FREE /$100 in credits (+usage costs) See our cost calculator - $100 one-time usage credit - Sessions up to 1 hour - 10 concurrent sand`
- 🔎 **credit** `usage costs. FREE /$100 in credits (+usage costs) See our cost calculator - $100 one-time usage credit - Sessions up to 1 hour - 10 concurrent sandboxes10 concurrent sandboxesThe maximum number of sandb`
- 🔎 **/month (+usage costs)** `x CPU and RAM [Start for Free](https://console.e2b.dev/sign-up?signup_source=pricing_hobby) $150 /month (+usage costs) See our cost calculator - Everything in Hobby, usage billed by the second - Sessions up to 24 hou`
- 🔎 **/mo** `an Monthly Cost Usage Cost $166 Pro Plan Base $150 Concurrency Addon $0 Total Monthly $316 /mo Max Concurrent Sandboxes100 Enterprise starts at a $2,000/mo commit, 500 concurrent included. ##`
- 🔎 **/mo commit, 500 concurrent included** `ency Addon $0 Total Monthly $316 /mo Max Concurrent Sandboxes100 Enterprise starts at a $2,000/mo commit, 500 concurrent included. ### Let us know if you need more powerful compute. If you don't see convenient times, please ema`
- 🔎 **sandbox** `sts) See our cost calculator - $100 one-time usage credit - Sessions up to 1 hour - 10 concurrent sandboxes10 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sa`
- 🔎 **sandbox** `ulator - $100 one-time usage credit - Sessions up to 1 hour - 10 concurrent sandboxes10 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sandbox CPU and RAM [Sta`
- 🔎 **sandbox** `redit - Sessions up to 1 hour - 10 concurrent sandboxes10 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sandbox CPU and RAM [Start for Free](https://console.e2`
- 🔎 **sandbox** `oxes10 concurrent sandboxesThe maximum number of sandboxes that can run at the same time. - Default sandbox CPU and RAM [Start for Free](https://console.e2b.dev/sign-up?signup_source=pricing_hobby) $150 /`
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

##    Ona 定价（Gitpod 改名，云 IDE 免费 credits）（ona-pricing）
- 状态: ok | https://ona.com/pricing
- ⚠️ 0 命中——页面可能 JS 渲染或改版，需人工核 pattern

##    Replit 定价（云 IDE+Agent）（replit-pricing）
- 状态: error | https://replit.com/pricing
- ❌ ACCESS_BARRIER: the site returned an access barrier (generic block); pagesift does not bypass it

##    bolt.new（StackBlitz 旗下 AI 全栈云开发）（bolt-new）
- 状态: ok | https://bolt.new/
- 🔎 **free** `age/personas/students.png) ## Ready to build something amazing? Try it out and start building for free`

##    Firebase Studio（原 Project IDX，Google 免费 cloud IDE）（firebase-studio）
- 状态: ok | https://firebase.studio/
- 🔎 **workspace** `The full stack AI workspace Firebase Studio accelerates your entire development lifecycle with AI agents. Build backends, fron`
- 🔎 **workspace** `. You can also customize your environment with Nix. Firebase Studio is currently available with 3 workspaces at no cost during preview. Members of the [Google Developer Program](https://accounts.google.com/A`
- 🔎 **workspace** `aign%3DFY25-Q2-firebasestudio_nextlaunch%26utm_content%3Dquickstart_gdp%26utm_term%3D-)get up to 30 workspaces. AI powered ## Build with in Firebase Work quickly and efficiently with Gemini in Firebase. Com`
- 🔎 **workspace** `nd work together Provide a URL for your early testers to preview your app and give feedback. Share workspaces with other team members to contribute to the same project at the same time. Enable everyone to wor`
- 🔎 **workspace** `t the same time. Enable everyone to work together, whether they can code or not. ![Firebase Studio workspace](https://rstr.in/google/firebase-studio/-LzIMPuLhOu) End-to-end testing ## Optimize your full-sta`
- 🔎 **Gemini** `)get up to 30 workspaces. AI powered ## Build with in Firebase Work quickly and efficiently with Gemini in Firebase. Complete a variety of tasks like coding, debugging, testing, refactoring, explaining,`

##    StackBlitz 定价（云 IDE 免费档）（stackblitz-pricing）
- 状态: ok | https://stackblitz.com/pricing
- 🔎 **free** `ojects, you do need a GitHub account to save your work or collaborate with others. You can create a free GitHub account [on their website here](https://github.com/). What is included in the free Personal`
- 🔎 **free** `create a free GitHub account [on their website here](https://github.com/). What is included in the free Personal plan? The free Personal plan includes unlimited public StackBlitz projects and Github repo`
- 🔎 **free** `ount [on their website here](https://github.com/). What is included in the free Personal plan? The free Personal plan includes unlimited public StackBlitz projects and Github repositories. If you need to`
- 🔎 **free** `ion are automatically synced to your StackBlitz Teams account. You can change individual members to free or paid users depending on what they need to access. Free users can access and edit all public proj`

##    Browserbase 定价（Agent 浏览器沙盒）（browserbase-pricing）
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

##    Hyperbrowser 定价（Agent 浏览器沙盒）（hyperbrowser-pricing）
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

##    Steel 定价（开源 Agent 浏览器云）（steel-pricing）
- 状态: ok | https://steel.dev/pricing
- 🔎 **free** `# Pricing Start for free and pay only for what runs. Move up when your agents go to production. ## Compare plans Every rat`

##    Serv00（波兰免费主机·白嫖圈热门）（serv00-home）
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

##    EUserv（德国免费 IPv6 VPS 申领）（euserv-home）
- 状态: ok | https://www.euserv.com/en/
- 🔎 **per month if not displayed different, additional one time s** `dex.php) \*)\*\*)\*\*\*) All prices are included VAT depending on selected country, price tags are per month if not displayed different, additional one time setup fee may apply starting at 0,- EUR. Please watch full description, details and pricing of servic`

##    Scaleway 定价（法国云，免费档+试用）（scaleway-pricing）
- 状态: error | https://www.scaleway.com/en/pricing/
- ❌ ACCESS_BARRIER: the site returned an access barrier (generic block); pagesift does not bypass it

##    UpCloud 定价（试用金）（upcloud-pricing）
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

##    DigitalOcean 定价（$200/60天 试用观察）（digitalocean-pricing）
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

##    Vercel 定价（Hobby 免费档）（vercel-pricing）
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

##    Netlify 定价（免费 100GB 带宽档）（netlify-pricing）
- 状态: ok | https://www.netlify.com/pricing/
- 🔎 **10vCPUs), 6x more memory (36GB), and 4x higher concurrency than the** `on limits, increase memory, or set a custom AWS region. | | | | | | 5x faster processing power (10vCPUs), 6x more memory (36GB), and 4x higher concurrency than the standard build environment. | | | | | | 99.99% uptime SLA | | | | | | Preserve deploys olde`
- 🔎 **always free, with hard monthly limits that cannot be exceeded** `nts-and-billing/billing/billing-for-credit-based-plans/configure-auto-recharge/). The free plan is always free, with hard monthly limits that cannot be exceeded or incur any costs. Paid plans have spend control using the auto recharge setting for credits, whic`
- 🔎 **free plan is always free, with hard monthly limits that cannot be exc** `/manage/accounts-and-billing/billing/billing-for-credit-based-plans/configure-auto-recharge/). The free plan is always free, with hard monthly limits that cannot be exceeded or incur any costs. Paid plans have spend control using the auto recharge setting for credits,`
- 🔎 **credit limit / month** `& images with Blob storage - Firewall Traffic Rules & basic rate limiting - Global CDN - 300 credit limit / month - ## Personal $9[See pricing in your dashboard](https://app.netlify.com/teams/~/billing/general`
- 🔎 **credits / month** `Free, plus: - Smart secret detection - 1-day observability - Priority email support - 1,000 credits / month - ## Pro $20[See pricing in your dashboard](https://app.netlify.com/teams/~/billing/general#pla`
- 🔎 **credits** `lds - SSO & SCIM - Log drains - Organization management - 24/7 dedicated support ### Usage credits Flexible plans to optimize your usage A production deploy is the version of your project pushed t`
- 🔎 **credit-based pricing accounts, new projects start private by defau** `e your usage A production deploy is the version of your project pushed to your main domain. On new credit-based pricing accounts, new projects start private by default and become publicly accessible only when you choose to publish. Also includes: Unlimited Deploy P`
- 🔎 **credits | Usage credits |  |  |  |** `Edge functions. | | | | | | | --- | --- | --- | --- | --- | | Features | | | | | | Usage credits | Usage credits | | | | | Includes usage credits for production deploys, compute, form submissions, bandwidth, and web requ`
- 🔎 **credits for production deploys, compute, form submissions, bandwidt** `| --- | --- | | Features | | | | | | Usage credits | Usage credits | | | | | Includes usage credits for production deploys, compute, form submissions, bandwidth, and web requests. | 300 credit limit | 1,000 credits included | Starting with 3,000 credits per m`
- 🔎 **credit limit | 1,000 credits included | Starting with 3,000 credit** `usage credits for production deploys, compute, form submissions, bandwidth, and web requests. | 300 credit limit | 1,000 credits included | Starting with 3,000 credits per month, choose a Pro tier up to 20,000 credits per month. | Custom | | Additional credits are a`

##    Deno Deploy（免费层）（deno-deploy）
- 状态: ok | https://deno.com/deploy
- 🔎 **free tier, and gracefully scale up or down as needed, automatically** `t times than lambda functions or virtual machines. #### Elastic scalability Start with a generous free tier, and gracefully scale up or down as needed, automatically. #### Runs on Deno Deno Deploy runs on Deno under the hood, so you get better speed and security,`
- 🔎 **free** `t times than lambda functions or virtual machines. #### Elastic scalability Start with a generous free tier, and gracefully scale up or down as needed, automatically. #### Runs on Deno Deno Deploy run`
- 🔎 **free** `r the hood, so you get better speed and security, with full Node and npm compatibility. It's like a free upgrade. `Deno Deploy`![Deno Deploy egg logo](https://deno.com/logos/deploy/mark.svg?__frsh_c=e16f`

##    Val Town 定价（免费云函数）（valtown-pricing）
- 状态: error | https://val.town/pricing
- ❌ TIMEOUT: connect timeout

##    Northflank 定价（免费 sandbox 服务）（northflank-pricing）
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

##    Google Colab FAQ（免费档 GPU/runtime 口径）（colab-faq）
- 状态: error | https://research.google.com/colaboratory/faq.html
- ❌ TIMEOUT: connect timeout

##    Lightning AI 定价（每月免费 credits）（lightning-pricing）
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

##    Paperspace 定价（DO 旗下，Gradient 免费档现状）（paperspace-pricing）
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

##    Replicate 定价（免费额度收回观察）（replicate-pricing）
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

##    fal.ai 定价（生成式 AI 云免费额度）（fal-pricing）
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

##    LowEndBox RSS（免费 VPS 帖聚合雷达）（lowendbox-feed）
- 状态: ok | https://lowendbox.com/feed/
- 🔎 **4GB VPS!](https://lowendbox** `on LowEndBox . - [GenixNode: Amazing Low Prizes in 14 Locations Around the Globe! $2.39/Month for a 4GB VPS!](https://lowendbox.com/blog/genixnode-amazing-low-prizes-in-14-locations-around-the-globe-2-39-month-for-a-4gb-vps/) —`
- 🔎 **4gb-vps/) — Mon, 09 Nov 2026 12:00:26 +0000** `//lowendbox.com/blog/genixnode-amazing-low-prizes-in-14-locations-around-the-globe-2-39-month-for-a-4gb-vps/) — Mon, 09 Nov 2026 12:00:26 +0000 GenixNode is a VPS provider with deals in 14 different locations around the world. From Dallas to`
- 🔎 **4GB VPS! The post GenixNode: Amazing Low Prizes in 14 Locations** `want to be. Prices vary by location but prices start as low as $2.39/month on annual contract for a 4GB VPS! The post GenixNode: Amazing Low Prizes in 14 Locations Around the Globe! $2.39/Month for a 4GB VPS! appeared first on LowEndBox . - [BONUS CODE DROP for R`
- 🔎 **4GB VPS! appeared first on LowEndBox ** `4GB VPS! The post GenixNode: Amazing Low Prizes in 14 Locations Around the Globe! $2.39/Month for a 4GB VPS! appeared first on LowEndBox . - [BONUS CODE DROP for RackNerd’s Fall Giveaway! Win a Meta Quest 3, a Synology NAS, a Gaming Moni`
- 🔎 **4GB VPS with 1TB Bandwidth!](https://lowendbox** `appeared first on LowEndBox . - [Great Singapore Deals from Kainode! Starting at $5.99/Month for a 4GB VPS with 1TB Bandwidth!](https://lowendbox.com/blog/great-singapore-deals-from-kainode-starting-at-5-99-month-for-a-4gb-vps-with-1tb-bandwidth`
- 🔎 **4gb-vps-with-1tb-bandwidth/) — Sat, 07 Nov 2026 12:00:46 +0000** `dwidth!](https://lowendbox.com/blog/great-singapore-deals-from-kainode-starting-at-5-99-month-for-a-4gb-vps-with-1tb-bandwidth/) — Sat, 07 Nov 2026 12:00:46 +0000 Offers in Singapore are always popular. It's not easy to find a true "low end" provider there bec`
- 🔎 **4GB VPS for only $5** `k centers like Dallas or Amsterdam. But Kainode has brought us some good deals today: you can get a 4GB VPS for only $5.99/month! The post Great Singapore Deals from Kainode! Starting at $5.99/Month for a 4GB VPS with 1`
- 🔎 **4GB VPS with 1TB Bandwidth! appeared first on LowEndBox ** `PS for only $5.99/month! The post Great Singapore Deals from Kainode! Starting at $5.99/Month for a 4GB VPS with 1TB Bandwidth! appeared first on LowEndBox . - [Need Cheap, Quality Email Hosting? Check Out FranklyMail – and Their Special Offer Exclusively`
- 🔎 **4GB VPS for Only $3** `from $17.99/Year! appeared first on LowEndBox . - [Cheap VPS Deals in Toronto from EnderHost! Get a 4GB VPS for Only $3.84/Month!](https://lowendbox.com/blog/cheap-vps-deals-in-toronto-from-enderhost-get-a-4gb-vps-for-o`
- 🔎 **4gb-vps-for-only-3-84-month/) — Mon, 02 Nov 2026 12:00:00 +0000** `S for Only $3.84/Month!](https://lowendbox.com/blog/cheap-vps-deals-in-toronto-from-enderhost-get-a-4gb-vps-for-only-3-84-month/) — Mon, 02 Nov 2026 12:00:00 +0000 EnderHost has some wonderful deals in Toronto, Canada for us! Cheap pricing from a quality provid`

##    百度智能云免费试用（baidu-free）
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
- 状态: error | https://cloud.google.com/free
- ❌ TIMEOUT: connect timeout

## 🔔 AWS Free Tier（aws-free）
- 状态: ok | https://aws.amazon.com/free/
- 🔎 **Always free** `te the service, and any eligible credits automatically apply to usage beyond the trial limits. ### Always free ![Illustration of a document, gear, and cloud with code symbols, representing cloud-based coding o`
- 🔎 **always free within monthly usage limits on both the Free and ** `vices-gear-document-icon-560x258.3d9731b98f2f92c30d61d8bf5b6f4af42ec9d06e.png) 30+ AWS services are always free within monthly usage limits on both the Free and Paid plans. If you go beyond these limits or access paid features, credits are automatically applied`
- 🔎 **free tier at [www** `Please visit [www.amazonaws.cn](https://www.amazonaws.cn/?hd_gl_2109). Learn about the China region free tier at [www.amazonaws.cn/free](https://www.amazonaws.cn/free/?hd_gl_2109). - [Overview](https://aws.amazon.com`
- 🔎 **Free Tier Categories** `w.amazonaws.cn/free/?hd_gl_2109). - [Overview](https://aws.amazon.com/free/?p=ft&z=subnav&loc=2) - Free Tier Categories - Featured Offers for Business - [Terms and Conditions](https://aws.amazon.com/free/terms/?p=ft&z=s`
- 🔎 **Free Tier** `ness - [Terms and Conditions](https://aws.amazon.com/free/terms/?p=ft&z=subnav&loc=6) - More # AWS Free Tier Get started for free with up to $200 in credits [Create a free account](https://signin.aws.amazon`
- 🔎 **Free Tier account, you get $100 in credits immediately** `mazon.com/console/home/) ## Get up to $200 in credits for new customers When you create a new AWS Free Tier account, you get $100 in credits immediately. As you explore key services, you can earn up to $100 more. That's up to $200 over 6 months to buil`
- 🔎 **Free plan** `0 over 6 months to build, break things, and experiment with no charges and no surprise bills on the Free plan. The account closes on its own 6 months after you open it or when your credits run out, whichever c`
- 🔎 **free plan to get started, paid plan to scale** `bf42784e3b9c3a5e4b387d48cb10b00f.png) ## Compare the plans Choose the plan that fits your needs — free plan to get started, paid plan to scale. | Benefits | Free plan | Paid plan | | --- | --- | --- | | Receive up to $200 USD free credits |`
- 🔎 **Free plan | Paid plan |** `Choose the plan that fits your needs — free plan to get started, paid plan to scale. | Benefits | Free plan | Paid plan | | --- | --- | --- | | Receive up to $200 USD free credits | ✔ | ✔ | | Free usage of select services`
- 🔎 **free credits | ✔ | ✔ |** `d plan to scale. | Benefits | Free plan | Paid plan | | --- | --- | --- | | Receive up to $200 USD free credits | ✔ | ✔ | | Free usage of select services | ✔ | ✔ | | Access to all AWS services | ✖ Limited to select servic`

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

##    Render 定价（免费 Web 服务）（render-pricing）
- 状态: error | https://render.com/pricing
- ❌ TIMEOUT: connect timeout

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

## 🔔 Railway 定价（试用金观察）（railway-pricing）
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
- 状态: error | https://github.com/features/codespaces
- ❌ TIMEOUT: connect timeout

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
- 状态: error | https://huggingface.co/pricing
- ❌ TIMEOUT: connect timeout

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

##    Oracle Always Free 资源明细页（官方文档级口径）（oracle-alwaysfree-docs）
- 状态: ok | https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- 🔎 **500 OCPU hours and 9,000 GB hours per month for free for VM instance** `AMD processor. - **OCI Ampere A1 Compute instances (Arm processor):** All tenancies get the first 1,500 OCPU hours and 9,000 GB hours per month for free for VM instances using the VM.Standard.A1.Flex [shape](https://docs.oracle.com/iaas/Content/Compute/References/comp`
- 🔎 **2 OCPUs and 12 GB of memory** `acle.com/iaas/Content/Compute/References/arm.htm). For Always Free tenancies, this is equivalent to 2 OCPUs and 12 GB of memory. In regions with multiple availability domains: - You can create OCI Ampere A1 Compute instances`
- 🔎 **2 OCPUs total** `to each OCI Ampere A1 Compute instance, you can create one or two OCI Ampere A1 Compute instances, 2 OCPUs total. The minimum [boot volume](https://docs.oracle.com/iaas/Content/Block/Concepts/bootvolumes.htm) siz`
- 🔎 **47 GB, regardless of shape** `ume](https://docs.oracle.com/iaas/Content/Block/Concepts/bootvolumes.htm) size for each instance is 47 GB, regardless of shape. Your account comes with 200 GB of Always Free [block volume](https://docs.oracle.com/en-us/iaas/Co`
- 🔎 **200 GB of Always Free [block volume](https://docs** `epts/bootvolumes.htm) size for each instance is 47 GB, regardless of shape. Your account comes with 200 GB of Always Free [block volume](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm#blockvolume) storag`
- 🔎 **47 GB, you could provision two instances using the VM** `te the boot volumes for your compute instances. For example, using the default boot volume size of 47 GB, you could provision two instances using the VM.Standard.E2.1.Micro shape, and one OCI Ampere A1 Compute instance with 2 OCPUs or two OCI Ampere A1`
- 🔎 **2 OCPUs or two OCI Ampere A1 Compute instances with 1 OCPU each, an** `n two instances using the VM.Standard.E2.1.Micro shape, and one OCI Ampere A1 Compute instance with 2 OCPUs or two OCI Ampere A1 Compute instances with 1 OCPU each, and zero instances using the VM.Standard.E2.1.Micro shape. Many combinations are possible, depending o`
- 🔎 **1 GB** `* - **Processor:** 1/8th of an OCPU with the ability to use additional CPU resources - **Memory:** 1 GB - **Networking:** Includes one **VNIC** with one public IP address and up to 50 Mbps network bandwi`
- 🔎 **1 OCPU each (2 OCPUs total) that each use a portion of the resourc** `l of the Always Free OCPUs and memory to create a single instance, or create up to two instances of 1 OCPU each (2 OCPUs total) that each use a portion of the resources. - **Processor:** 2 OCPUs total, which you can allocate flexibly - **Memory:** 12 GB total, whic`
- 🔎 **2 OCPUs total, which you can allocate flexibly** `nstances of 1 OCPU each (2 OCPUs total) that each use a portion of the resources. - **Processor:** 2 OCPUs total, which you can allocate flexibly - **Memory:** 12 GB total, which you can allocate flexibly - **Networking:** The network bandwidth`

##    OpenShift Dev Spaces（红帽免费云 IDE 工作区）（openshift-workspaces）
- 状态: ok | https://workspaces.openshift.com/
- 🔎 **workspace** `![](https://workspaces.openshift.com/loader.svg) Loading Red Hat OpenShift Dev Spaces... To use Red Hat OpenShift Dev S`

##    paizaCloud（日本免费云 IDE）（paizacloud-free）
- 状态: ok | https://paiza.cloud/en/
- 🔎 **2GB, ディスク: 1GB CPU: 2Core, MEM: 2GB, Disk: 1GB** `ailable servers: 1 サーバservers （連続起動時間制限あり） (Limited continuous running time) - --- - CPU: 2コア, メモリ: 2GB, ディスク: 1GB CPU: 2Core, MEM: 2GB, Disk: 1GB - --- #### ライトプラン LITE plan ##### 980円/月～ $9.80/month - - 利用期間 Server Lifetime: **制限なし Unlimited`
- 🔎 **2GB, ディスク: 2GB CPU: 2Core, MEM: 2GB, Disk: 2GB** `ble servers: **3 サーバservers** （連続起動時間制限あり） (Limited continuous running time) - --- - CPU: 2コア, メモリ: 2GB, ディスク: 2GB CPU: 2Core, MEM: 2GB, Disk: 2GB - --- #### ベーシックプラン BASIC plan ##### 1,980円/月～ $19.80/month - - 利用期間 Server Lifetime: **制限なし Unl`
- 🔎 **2GB, ディスク: 4GB CPU: 2Core, MEM: 2GB, Disk: 4GB** `1 サーバservers + 3 サーバservers** （連続起動時間制限あり） (Limited continuous running time) - --- - CPU: 2コア, メモリ: 2GB, ディスク: 4GB CPU: 2Core, MEM: 2GB, Disk: 4GB - --- ## 仕様詳細 Specifications ### 一瞬で起動 Instant launch 開発環境(Linux)が立ち上がるまで約3秒。 3 seconds to launc`
- 🔎 **2GB** `nnection SSH接続も可能です。 You can connect to the server using SSH. ### リソース CPU: 2 core メモリ: Memory: 2GB ディスク: 1GB(フリープラン), 2GB(ライトプラン), 4GB(ベーシックプラン) Disk: 1GB(FREE), 2GB(LITE), 4GB(BASIC) ### OS Linu`
- 🔎 **1GB(フリープラン), 2GB(ライトプラン), 4GB(ベーシックプラン) Disk: 1GB(FREE), 2GB(LI** `SH接続も可能です。 You can connect to the server using SSH. ### リソース CPU: 2 core メモリ: Memory: 2GB ディスク: 1GB(フリープラン), 2GB(ライトプラン), 4GB(ベーシックプラン) Disk: 1GB(FREE), 2GB(LITE), 4GB(BASIC) ### OS Linux(Ubuntu 18.04) ### 開発環境 Development environments Web開発: Web developm`
- 🔎 **4GB(BASIC)** `2 core メモリ: Memory: 2GB ディスク: 1GB(フリープラン), 2GB(ライトプラン), 4GB(ベーシックプラン) Disk: 1GB(FREE), 2GB(LITE), 4GB(BASIC) ### OS Linux(Ubuntu 18.04) ### 開発環境 Development environments Web開発: Web development: LAMP, PHP,`
- 🔎 **FREE plan** `nvironment. I can also use the same environment without copying files. ## 料金体系 Pricing #### 無料プラン FREE plan ##### 無料 FREE - 利用期間 Server Lifetime: 24時間 24 Hours (同じサーバ環境を継続利用できる時間) (per 1 server) - 連続起動`
- 🔎 **/month -** `モリ: 2GB, ディスク: 1GB CPU: 2Core, MEM: 2GB, Disk: 1GB - --- #### ライトプラン LITE plan ##### 980円/月～ $9.80/month - - 利用期間 Server Lifetime: **制限なし Unlimited** - 連続起動時間 Running: ブラウザ開いている間 When you are online(open i`
- 🔎 **/month -** `B, ディスク: 2GB CPU: 2Core, MEM: 2GB, Disk: 2GB - --- #### ベーシックプラン BASIC plan ##### 1,980円/月～ $19.80/month - - 利用期間 Server Lifetime: **制限なし Unlimited** - 連続起動時間 Running: **常時起動 Always-On** - サービス公開制限 Publish`
- 🔎 **free** `can use them right away. You can also use the Linux shell and set up development environments more freely as well. ### サービスの公開、運用も可能！ポートフォリオとして最適 You can publish your service online! It's ideal for your`

##    Zoho Catalyst（免费云函数/Serverless）（zoho-catalyst）
- 状态: ok | https://catalyst.zoho.com/free-tier.html
- 🔎 **000 GB-seconds |** `ier limit | | --- | --- | --- | --- | | Functions | Function execution | $0.000016 / GB-second | 25,000 GB-seconds | | AppSail | Container runtime | $0.0013 / GB-minute | 900 GB-minutes | | Circuits | State transitio`
- 🔎 **900 GB-minutes |** `| $0.000016 / GB-second | 25,000 GB-seconds | | AppSail | Container runtime | $0.0013 / GB-minute | 900 GB-minutes | | Circuits | State transition | $0.00002 / state transition | 2,000 state transitions | ### CloudS`
- 🔎 **2 GB-days |** `| Monthly free tier limit | | --- | --- | --- | --- | | Data Store | Storage | $0.00072 / GB-days | 2 GB-days | | SELECT query | $0.00006 / request | 10,000 requests | | | INSERT row | $0.0001 / request | 5,000`
- 🔎 **2 GB-days |  |** `40K rows) | | | Truncate | $0.00002 / row | 10,000 rows | | | OLAP storage | $0.00072 / GB-days | 2 GB-days | | | OLAP fetch | $0.00008 / request | 10,000 rows | | | Stratus | File download | $0.0000004 / reque`
- 🔎 **5 GB |  |** `quests | | | File update | $0.000005 / request | 1,000 requests | | | File storage | $0.02 / GB | 5 GB | | | NoSQL | Insert | $0.0000013 / request | 5,000 requests | | Update | $0.0000012 / request | 5,000`
- 🔎 **1 GB |  |** `ts | | | Index Query | $0.00000035 / request | 5,000 requests | | | Table Storage | $0.005 / GB | 1 GB | | | Index Storage | $0.005 / GB | 1 GB | | | Cache | Cache GET | $0.00004 / request | 1,000 requests`
- 🔎 **1 GB |  |** `est | 5,000 requests | | | Table Storage | $0.005 / GB | 1 GB | | | Index Storage | $0.005 / GB | 1 GB | | | Cache | Cache GET | $0.00004 / request | 1,000 requests | | Cache PUT | $0.00006 / request | 5,00`
- 🔎 **2vCPU 4GB) | $0** `ion | Unit price | Monthly free tier limit | | --- | --- | --- | --- | | Frontend | Build & deploy (2vCPU 4GB) | $0.01 / GB-minutes | 12 GB-minutes | | Hosting: CDN Storage | $0.0001 / MB | 500 MB | | | Function in`
- 🔎 **12 GB-minutes |** `er limit | | --- | --- | --- | --- | | Frontend | Build & deploy (2vCPU 4GB) | $0.01 / GB-minutes | 12 GB-minutes | | Hosting: CDN Storage | $0.0001 / MB | 500 MB | | | Function invocations | $0.00016 / GB-second |`
- 🔎 **000 GB-seconds |  |** `osting: CDN Storage | $0.0001 / MB | 500 MB | | | Function invocations | $0.00016 / GB-second | 25,000 GB-seconds | | | CDN & origin requests | $0.000004 / request | 300,000 requests | | | ISR read | $0.0000003 / req`

##    Clever Cloud（法国 PaaS 免费额度）（clever-cloud）
- 状态: ok | https://clever.cloud/
- 🔎 **free** `. Deploy with the **Utmost Tools** [Ask for a demo](https://www.clever.cloud/contact/) [Try for free](https://api.clever-cloud.com/v2/sessions/signup) Cultivate developer efficiency. Safeguard every`
- 🔎 **trial** `adapt to your context. Whether you are a software publisher, a public sector organization, an industrial company, a digital services provider, or a healthcare business, Clever Cloud addresses your specifi`

##    Cloudflare Pages（免费静态托管 500 build/月）（cloudflare-pages）
- 状态: ok | https://developers.cloudflare.com/pages/
- 🔎 **Free plan)** `latform/limits/) Learn about limits that apply to your Pages project (500 deploys per month on the Free plan). ### [Framework guides](https://developers.cloudflare.com/pages/framework-guides/) Deploy popular`
- 🔎 **egress bandwidth fees associated with typical cloud storage servic** `udflare R2 Storage allows developers to store large amounts of unstructured data without the costly egress bandwidth fees associated with typical cloud storage services. D1 is Cloudflare’s native serverless database. Create a database by importing data or defining`
- 🔎 **per month on the Free plan)** `flare.com/pages/platform/limits/) Learn about limits that apply to your Pages project (500 deploys per month on the Free plan). ### [Framework guides](https://developers.cloudflare.com/pages/framework-guides/) Deploy popular`
- 🔎 **bandwidth** `R2 Storage allows developers to store large amounts of unstructured data without the costly egress bandwidth fees associated with typical cloud storage services. D1 is Cloudflare’s native serverless database`

## 👀 HimitsuShell（免费 Linux Shell 账号）（himitsushell）
- 状态: ok | https://himitsushell.com/
- 🔎 **credit** `rk Email & Technical Support Priority Support ![cards](https://himitsushell.com/img/paypal/debit_credit.svg) Powered by: ![paypal](https://himitsushell.com/img/paypal/wordmark_color.svg) Personal - $24`
- 🔎 **transfer iconv id ifconfig inotifyd insmod install ionice iorenice i** `ups gunzip halt hd head help hexedit host hostname httpd hwclock i2cdetect i2cdump i2cget i2cset i2ctransfer iconv id ifconfig inotifyd insmod install ionice iorenice iotop kill killall killall5 link linux32 ln logger login logname losetup ls lsattr lsmod lspci lsusb`
- 🔎 **transfer** `ntries. Please contact us by email, and we'll provide an alternative payment method, such as bank transfer. Can I use only the obfuscation engine? ![](https://himitsushell.com/img/plus.svg) Yes. See Himit`
- 🔎 **free** `Date Verification Provided as a Docker Image Download on GitHub Commercial Edition \+ 1 year of free updates (additional year $99) One-Time Purchase, No Expiration Commercial use allowed Everything`
- 🔎 **free** `nname dos2unix du echo egrep eject env expand factor fallocate false fgrep file find flock fmt fold free freeramdisk fsfreeze fstype fsync ftpget ftpput getconf getopt gpiodetect gpiofind gpioget gpioinfo`
- 🔎 **free** `dos2unix du echo egrep eject env expand factor fallocate false fgrep file find flock fmt fold free freeramdisk fsfreeze fstype fsync ftpget ftpput getconf getopt gpiodetect gpiofind gpioget gpioinfo gpio`
- 🔎 **free** `cho egrep eject env expand factor fallocate false fgrep file find flock fmt fold free freeramdisk fsfreeze fstype fsync ftpget ftpput getconf getopt gpiodetect gpiofind gpioget gpioinfo gpioset grep group`
- 🔎 **shell** `& Docker Containers Compile Features ![auditd analysis results for HimitsuShell](https://himitsushell.com/img/features_os.png?v=1794364308088) OS-Level Logging & Hooking Protection Executes shell scr`
- 🔎 **shell** `itsushell.com/img/features_os.png?v=1794364308088) OS-Level Logging & Hooking Protection Executes shell scripts using its own embedded shell interpreter instead of the system shell (e.g., /bin/bash). She`
- 🔎 **shell** `794364308088) OS-Level Logging & Hooking Protection Executes shell scripts using its own embedded shell interpreter instead of the system shell (e.g., /bin/bash). Shell scripts are not exposed even by OS`

##    iDrive E2 对象存储（1TB $40/yr 低价存储线）（idrive-e2）
- 状态: error | https://www.idrive.com/object-storage-e2/pricing
- ❌ ACCESS_BARRIER: the site returned an access barrier (aws_cloudfront block); pagesift does not bypass it

##    ShaktiCloud（Yotta GPU 云定价）（shakticloud）
- 状态: error | https://shakticloud.ai/pricing.html
- ❌ TIMEOUT: request deadline passed

##    Cloudzy（VPS/GPU/裸金属定价）（cloudzy）
- 状态: ok | https://cloudzy.com/pricing
- 🔎 **64 GB workhorse** `ered by EPYC CPUs, NVMe storage, 40 Gbps connections, and DDR5 memory. 10 sizes from a sandbox to a 64 GB workhorse. | Memory | vCPU | Transfer | Storage | Price | | | --- | --- | --- | --- | --- | --- | | 512 MB`
- 🔎 **1 vCPU | 1 TB · **40 Gbps** | 20 GB **NVMe** | $2** `mory | vCPU | Transfer | Storage | Price | | | --- | --- | --- | --- | --- | --- | | 512 MB DDR5 | 1 vCPU | 1 TB · **40 Gbps** | 20 GB **NVMe** | $2.48 /mo $4.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=0.5&os=ubuntu)14-day money-back |`
- 🔎 **1 GB DDR5 | 1 vCPU | 1 TB · **40 Gbps** | 25 GB **NVMe** | $3** `/mo $4.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=0.5&os=ubuntu)14-day money-back | | 1 GB DDR5 | 1 vCPU | 1 TB · **40 Gbps** | 25 GB **NVMe** | $3.48 /mo $6.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=1&os=ubuntu)14-day money-back | |`
- 🔎 **2 GB DDR5 | 1 vCPU | 3 TB · **40 Gbps** | 60 GB **NVMe** | $7** `48 /mo $6.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=1&os=ubuntu)14-day money-back | | 2 GB DDR5 | 1 vCPU | 3 TB · **40 Gbps** | 60 GB **NVMe** | $7.48 /mo $14.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=2&os=ubuntu)14-day money-back |`
- 🔎 **4 GB DDR5 Popular | 2 vCPU | 5 TB · **40 Gbps** | 120 GB **NVMe*** `8 /mo $14.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=2&os=ubuntu)14-day money-back | | 4 GB DDR5 Popular | 2 vCPU | 5 TB · **40 Gbps** | 120 GB **NVMe** | $14.48 /mo $28.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=4&os=ubuntu)14-day money-`
- 🔎 **8 GB DDR5 | 4 vCPU | 7 TB · **40 Gbps** | 240 GB **NVMe** | $26** `8 /mo $28.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=4&os=ubuntu)14-day money-back | | 8 GB DDR5 | 4 vCPU | 7 TB · **40 Gbps** | 240 GB **NVMe** | $26.48 /mo $52.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=8&os=ubuntu)14-day money-back |`
- 🔎 **12 GB DDR5 | 4 vCPU | 8 TB · **40 Gbps** | 300 GB **NVMe** | $34** `8 /mo $52.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=8&os=ubuntu)14-day money-back | | 12 GB DDR5 | 4 vCPU | 8 TB · **40 Gbps** | 300 GB **NVMe** | $34.98 /mo $69.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=12&os=ubuntu)14-day money-back |`
- 🔎 **16 GB DDR5 | 8 vCPU | 10 TB · **40 Gbps** | 350 GB **NVMe** | $49** `/mo $69.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=12&os=ubuntu)14-day money-back | | 16 GB DDR5 | 8 vCPU | 10 TB · **40 Gbps** | 350 GB **NVMe** | $49.98 /mo $99.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=16&os=ubuntu)14-day money-back |`
- 🔎 **24 GB DDR5 | 8 vCPU | 12 TB · **40 Gbps** | 450 GB **NVMe** | $69** `/mo $99.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=16&os=ubuntu)14-day money-back | | 24 GB DDR5 | 8 vCPU | 12 TB · **40 Gbps** | 450 GB **NVMe** | $69.98 /mo $139.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=24&os=ubuntu)14-day money-back`
- 🔎 **32 GB DDR5 | 12 vCPU | 12 TB · **40 Gbps** | 750 GB **NVMe** | $1** `/mo $139.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=24&os=ubuntu)14-day money-back | | 32 GB DDR5 | 12 vCPU | 12 TB · **40 Gbps** | 750 GB **NVMe** | $109.98 /mo $219.95 -50% | [Deploy](https://welcome.cloudzy.com/cart?ram=32&os=ubuntu)14-day money-bac`

##    阿里云百炼新人免费额度（官方帮助中心规则页）（aliyun-bailian-freequota）
- 状态: ok | https://help.aliyun.com/zh/model-studio/new-free-quota
- 🔎 **免费额度** `当您首次开通阿里云百炼时，平台会自动为您发放各模型的新人专属免费额度。 ## 规则说明 ### 有效期 免费额度的有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算（以较晚者为准）。额度到期或耗尽后，继续调用模型推理服务将[产生计费](htt`
- 🔎 **免费额度的有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算（以较晚者为准）** `当您首次开通阿里云百炼时，平台会自动为您发放各模型的新人专属免费额度。 ## 规则说明 ### 有效期 免费额度的有效期为 90 天，从开通阿里云百炼、模型发布或模型申请通过之日起计算（以较晚者为准）。额度到期或耗尽后，继续调用模型推理服务将[产生计费](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。 **重要`
- 🔎 **免费额度有效期可能不足90天；在此之后开通的用户有效期为90天** `ps://help.aliyun.com/zh/model-studio/billing-for-model-studio)。 **重要****2025年9月8日11点**前已开通阿里云百炼的用户，免费额度有效期可能不足90天；在此之后开通的用户有效期为90天。详情参考[阿里云百炼新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment`
- 🔎 **免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/n** `-for-model-studio)。 **重要****2025年9月8日11点**前已开通阿里云百炼的用户，免费额度有效期可能不足90天；在此之后开通的用户有效期为90天。详情参考[阿里云百炼新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment)。 免费额度过期后自动失效，不支持补发、延期或重置： - 额度有效期内是否使用均不会暂停计时； - 额度过期后，剩余部分自动作废`
- 🔎 **免费额度过期后自动失效，不支持补发、延期或重置：** `考[阿里云百炼新人免费额度有效期调整通知](https://help.aliyun.com/zh/model-studio/new-free-quota-validity-adjustment)。 免费额度过期后自动失效，不支持补发、延期或重置： - 额度有效期内是否使用均不会暂停计时； - 额度过期后，剩余部分自动作废，不会重新发放或延长； - 同一实名认证主体下重新注册账号，无法再次领取新人免费额度。 ### 适用范围 免费额度仅抵`
- 🔎 **免费额度** `费额度过期后自动失效，不支持补发、延期或重置： - 额度有效期内是否使用均不会暂停计时； - 额度过期后，剩余部分自动作废，不会重新发放或延长； - 同一实名认证主体下重新注册账号，无法再次领取新人免费额度。 ### 适用范围 免费额度仅抵扣模型**实时推理**（调用）产生的费用。 ### 注意事项 阿里云主账号与其RAM子账号共享免费额度。 > 例如：qwen-max的总免费额度为100万T`
- 🔎 **免费额度仅抵扣模型**实时推理**（调用）产生的费用** `延期或重置： - 额度有效期内是否使用均不会暂停计时； - 额度过期后，剩余部分自动作废，不会重新发放或延长； - 同一实名认证主体下重新注册账号，无法再次领取新人免费额度。 ### 适用范围 免费额度仅抵扣模型**实时推理**（调用）产生的费用。 ### 注意事项 阿里云主账号与其RAM子账号共享免费额度。 > 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，q`
- 🔎 **免费额度** `； - 同一实名认证主体下重新注册账号，无法再次领取新人免费额度。 ### 适用范围 免费额度仅抵扣模型**实时推理**（调用）产生的费用。 ### 注意事项 阿里云主账号与其RAM子账号共享免费额度。 > 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，qwen-max的剩余免费额度为70万Token。 不同模型（含同`
- 🔎 **免费额度为100万Token** `再次领取新人免费额度。 ### 适用范围 免费额度仅抵扣模型**实时推理**（调用）产生的费用。 ### 注意事项 阿里云主账号与其RAM子账号共享免费额度。 > 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，qwen-max的剩余免费额度为70万Token。 不同模型（含同一模型的不同快照版本）的免费额度相互独立，不互通、不共享。 -`
- 🔎 **免费额度为70万Token** `项 阿里云主账号与其RAM子账号共享免费额度。 > 例如：qwen-max的总免费额度为100万Token。主账号消耗了10万Token，RAM子账号消耗了20万Token，qwen-max的剩余免费额度为70万Token。 不同模型（含同一模型的不同快照版本）的免费额度相互独立，不互通、不共享。 - 每个模型均有独立的免费额度（通常为 100 万 Token），不能跨模型合并或转移使用。 - 带日期后缀的快照版本`

##    天翼云免费试用中心（运营商层）（ctyun-trial）
- 状态: ok | https://www.ctyun.cn/act/trial/central
- 🔎 **50GB** `dbc0fba11be7458eb037db363af8aa76.svg) 个人认证 云硬盘 高性能、高可靠、弹性扩展的块存储服务，适用于企业上云、云上虚拟化和数据库等场景 规格 通用型SSD 50GB 免费试用1个月 试用教程 试用教程 立即试用 立即试用 ![](https://ctyun-portal.gdoss.xstore.ctyun.cn/activity_media/b2847`
- 🔎 **100GB** `b2847d2c8ccc4f2bb7056a2ed14b792d.svg) 企业认证 云硬盘 高性能、高可靠、弹性扩展的块存储服务，适用于企业上云、云上虚拟化和数据库等场景 规格 通用型SSD 100GB 免费试用1个月 试用教程 试用教程 立即试用 立即试用 ![](https://ctyun-portal.gdoss.xstore.ctyun.cn/activity_media/dbc0f`
- 🔎 **200GB** `vity_media/dbc0fba11be7458eb037db363af8aa76.svg) 个人认证 云硬盘 具有更高的数据可靠性、更高的I/O吞吐能力和更加简单易用等特点 规格 高IO 200GB 免费试用1个月 试用教程 试用教程 立即试用 立即试用 ![](https://ctyun-portal.gdoss.xstore.ctyun.cn/activity_media/b2847`
- 🔎 **500GB** `vity_media/b2847d2c8ccc4f2bb7056a2ed14b792d.svg) 企业认证 云硬盘 具有更高的数据可靠性、更高的I/O吞吐能力和更加简单易用等特点 规格 高IO 500GB 免费试用1个月 试用教程 试用教程 立即试用 立即试用 学习与使用 ![](https://ctyun-portal-test.gdoss.xstore.ctyun.cn/activity`
- 🔎 **免费试用中心** `免费试用中心 注册并完成实名认证，最高可得2000元试用体验金，多款云产品免费试用， 快来开启云上之旅 免费试用 精选云产品免费试用，数量有限，领完为止 筛选条件 清除筛选条件 用户认证类型 企业认`
- 🔎 **免费试用， 快来开启云上之旅** `免费试用中心 注册并完成实名认证，最高可得2000元试用体验金，多款云产品免费试用， 快来开启云上之旅 免费试用 精选云产品免费试用，数量有限，领完为止 筛选条件 清除筛选条件 用户认证类型 企业认证个人认证 产品类别 计算存储网络人工智能安全及管理容器与中间件 ![](https:`
- 🔎 **免费试用** `免费试用中心 注册并完成实名认证，最高可得2000元试用体验金，多款云产品免费试用， 快来开启云上之旅 免费试用 精选云产品免费试用，数量有限，领完为止 筛选条件 清除筛选条件 用户认证类型 企业认证个人认证 产品类别 计算存储网络人工智能安全及管理容器与中间件 ![](https://ctyu`
- 🔎 **免费试用，数量有限，领完为止** `免费试用中心 注册并完成实名认证，最高可得2000元试用体验金，多款云产品免费试用， 快来开启云上之旅 免费试用 精选云产品免费试用，数量有限，领完为止 筛选条件 清除筛选条件 用户认证类型 企业认证个人认证 产品类别 计算存储网络人工智能安全及管理容器与中间件 ![](https://ctyun-portal.gdoss.xstore`
- 🔎 **免费试用7天** `14b792d.svg) 企业认证 经济型e实例 实例共享宿主机CPU，性价比更高，适用于对成本比较敏感、对性能抖动容忍度较高的场景 规格 4核8G 系统盘 60G 带宽 3Mbps 免费试用7天 试用教程 试用教程 立即试用 立即试用 ![](https://ctyun-portal.gdoss.xstore.ctyun.cn/activity_media/b2847d2c8ccc4f`
- 🔎 **免费试用7天** `) 企业认证 FS1飞腾通用型云主机-1C1G 搭载飞腾处理器，实例间无CPU争抢，适用于对安全、可控、合规有严格要求的核心业务场景 规格 1核1G 系统盘 40G 带宽 1Mbps 免费试用7天 试用教程 试用教程 立即试用 立即试用 ![](https://ctyun-portal.gdoss.xstore.ctyun.cn/activity_media/b2847d2c8ccc4f`

##    Atlas Cloud（GPU/Agent 云）（atlascloud）
- 状态: ok | https://www.atlascloud.ai
- 🔎 **free credits to start** `hrough one unified API alongside 300+ models, with pricing from $0.04 per image, 99.99% uptime, and free credits to start. [Explore](https://www.atlascloud.ai/models/nanobanana-2) Model Classification ![Nano Banana 2 R`
- 🔎 **free credits, 99** `, and infographics. On Atlas Cloud you reach it through one unified API alongside 300+ models, with free credits, 99.99% uptime, and no OpenAI organization verification required. [Explore](https://www.atlascloud.ai/`
- 🔎 **credits to start** `h one unified API alongside 300+ models, with pricing from $0.04 per image, 99.99% uptime, and free credits to start. [Explore](https://www.atlascloud.ai/models/nanobanana-2) Model Classification ![Nano Banana 2 R`
- 🔎 **credits, 99** `infographics. On Atlas Cloud you reach it through one unified API alongside 300+ models, with free credits, 99.99% uptime, and no OpenAI organization verification required. [Explore](https://www.atlascloud.ai/`
- 🔎 **Credit Card](https://www** `iding professional and efficient model services to empower the entire creative process. [Link Your Credit Card](https://www.atlascloud.ai/console/billing) ### Develop ![Develop](https://www.atlascloud.ai/_next/image?url=%`
- 🔎 **credit card required to start** `rt guide in the documentation. Most developers are making their first API call within 5 minutes. No credit card required to start. What AI models does Atlas Cloud support? Atlas Cloud supports 400+ models across every modality.`
- 🔎 **Transfer with Character Consistency](https://www** `925b.png&w=2048&q=75) Gemini Omni 1.2 Flash Text-to-Video $0.028/SEC$0.023/SEC ![Kling V3 Motion Transfer with Character Consistency](https://www.atlascloud.ai/_next/image?url=https%3A%2F%2Fstatic.atlascloud.ai%2Fuploads%2Fmodel-families%2F67670`
- 🔎 **Transfer motion while preserving character identity, guide generatio** `g V3.0 From Kuaishou, the Kling V3 API family supports text, image, and reference video workflows. Transfer motion while preserving character identity, guide generation with visual references, and edit videos through natural language commands. Atlas Cloud offers Stan`
- 🔎 **transfer** `ly for cinematic text-to-video and image-to-video creation, AI avatars, and reference-driven motion transfer. It supports flexible aspect ratios, enhanced dynamics, stable identity, and temporal consistency a`
- 🔎 **Transfer](https://www** `653b27119a.png&w=2048&q=75) Midjourney V8.2 Remove Background $0.086/PIC ![Midjourney V8.2 Style Transfer](https://www.atlascloud.ai/_next/image?url=https%3A%2F%2Fstatic.atlascloud.ai%2Fuploads%2Fmodels%2Fc131796f-f718`

## 👀 GPU.nz（新西兰 GPU 云定价）（gpunz）
- 状态: ok | https://gpu.nz/en/pricing
- 🔎 **8 GB+ | $0** `e | 30 minutes | 1 hour | A day (24 h) | | --- | --- | --- | --- | --- | | RTX 3060 Ti 8 GBGPU with 8 GB+ | $0.0011 | $0.034 | $0.067 | $1.61 | | Tesla V100 32 GBGPU with 24 GB+ | $0.0036 | $0.109 | $0.218 | $5`
- 🔎 **24 GB+ | $0** `| | RTX 3060 Ti 8 GBGPU with 8 GB+ | $0.0011 | $0.034 | $0.067 | $1.61 | | Tesla V100 32 GBGPU with 24 GB+ | $0.0036 | $0.109 | $0.218 | $5.23 | | GB10 128 GBGPU with 48 GB+ | $0.0083 | $0.248 | $0.496 | $11.90`
- 🔎 **48 GB+ | $0** `.61 | | Tesla V100 32 GBGPU with 24 GB+ | $0.0036 | $0.109 | $0.218 | $5.23 | | GB10 128 GBGPU with 48 GB+ | $0.0083 | $0.248 | $0.496 | $11.90 | | GB10 128 GBGPU with 80 GB+ | $0.0083 | $0.248 | $0.496 | $11.90`
- 🔎 **80 GB+ | $0** `| $5.23 | | GB10 128 GBGPU with 48 GB+ | $0.0083 | $0.248 | $0.496 | $11.90 | | GB10 128 GBGPU with 80 GB+ | $0.0083 | $0.248 | $0.496 | $11.90 | Prices and availability come from the live catalog and update au`
- 🔎 **288gb) | 288 GB | $21** `, $/h | Median, $/h | Servers | | --- | --- | --- | --- | --- | | [B300](https://gpu.nz/en/gpu/b300-288gb) | 288 GB | $21.88/h | $21.88/h | 1 | | [B200](https://gpu.nz/en/gpu/b200-180gb) | 180 GB | $11.02/h | $20.01/h | 2`
- 🔎 **180gb) | 180 GB | $11** `/gpu.nz/en/gpu/b300-288gb) | 288 GB | $21.88/h | $21.88/h | 1 | | [B200](https://gpu.nz/en/gpu/b200-180gb) | 180 GB | $11.02/h | $20.01/h | 21 | | [H200 SXM](https://gpu.nz/en/gpu/h200-141gb) | 141 GB | $5.83/h | $8.99/h`
- 🔎 **141gb) | 141 GB | $5** `nz/en/gpu/b200-180gb) | 180 GB | $11.02/h | $20.01/h | 21 | | [H200 SXM](https://gpu.nz/en/gpu/h200-141gb) | 141 GB | $5.83/h | $8.99/h | 26 | | [H200 NVL](https://gpu.nz/en/gpu/h200-nvl-141gb) | 141 GB | $7.27/h | $9.46`
- 🔎 **141gb) | 141 GB | $7** `/en/gpu/h200-141gb) | 141 GB | $5.83/h | $8.99/h | 26 | | [H200 NVL](https://gpu.nz/en/gpu/h200-nvl-141gb) | 141 GB | $7.27/h | $9.46/h | 49 | | [H100 SXM](https://gpu.nz/en/gpu/h100-sxm-80gb) | 80 GB | $2.71/h | $4.45/h`
- 🔎 **80gb) | 80 GB | $2** `gpu/h200-nvl-141gb) | 141 GB | $7.27/h | $9.46/h | 49 | | [H100 SXM](https://gpu.nz/en/gpu/h100-sxm-80gb) | 80 GB | $2.71/h | $4.45/h | 29 | | [H100 NVL](https://gpu.nz/en/gpu/h100-nvl-94gb) | 94 GB | $4.72/h | $5.25/h`
- 🔎 **94gb) | 94 GB | $4** `n/gpu/h100-sxm-80gb) | 80 GB | $2.71/h | $4.45/h | 29 | | [H100 NVL](https://gpu.nz/en/gpu/h100-nvl-94gb) | 94 GB | $4.72/h | $5.25/h | 10 | | [H100 PCIe](https://gpu.nz/en/gpu/h100-pcie-80gb) | 80 GB | $4.96/h | $4.98`

##    Kiro（AWS 旗下 AI IDE，免费档）（kiro-pricing）
- 状态: ok | https://kiro.dev/pricing
- 🔎 **Free trial: when you first upgrade to Pro, you’ll get the rest of the ** `# Pricing Free trial: when you first upgrade to Pro, you’ll get the rest of the month free, plus 500 trial credits to use within 12 months. ## KIRO FREE $0 per month - 50 credi`
- 🔎 **free trial work?** `### How does Kiro pricing work? ### Which models does Kiro use under the hood? ### How does the free trial work? ### What can I use credits for? ### How can I track my credit usage? ### How do Kiro workflows a`
- 🔎 **free tier available for Enterprise or AWS GovCloud (US) Regions?** `e charged for Kiro powers? ### Is Kiro pricing different in AWS GovCloud (US) Regions? ### Is the free tier available for Enterprise or AWS GovCloud (US) Regions?`
- 🔎 **credits to use within 12 months** `g Free trial: when you first upgrade to Pro, you’ll get the rest of the month free, plus 500 trial credits to use within 12 months. ## KIRO FREE $0 per month - 50 credits - Access to open weight models and Claude Sonnet 4.`
- 🔎 **credits** `the month free, plus 500 trial credits to use within 12 months. ## KIRO FREE $0 per month - 50 credits - Access to open weight models and Claude Sonnet 4.5 ## KIRO PRO $20 per user / month - 1,0`
- 🔎 **credits** `Access to open weight models and Claude Sonnet 4.5 ## KIRO PRO $20 per user / month - 1,000 credits - Access to premium models - Add-on credits ($0.04/credit) ## KIRO PRO+ $40 per user / month -`
- 🔎 **credits ($0** `Sonnet 4.5 ## KIRO PRO $20 per user / month - 1,000 credits - Access to premium models - Add-on credits ($0.04/credit) ## KIRO PRO+ $40 per user / month - 2,000 credits - Access to premium models - Add-o`
- 🔎 **credit)** `KIRO PRO $20 per user / month - 1,000 credits - Access to premium models - Add-on credits ($0.04/credit) ## KIRO PRO+ $40 per user / month - 2,000 credits - Access to premium models - Add-on credits (`
- 🔎 **credits** `ess to premium models - Add-on credits ($0.04/credit) ## KIRO PRO+ $40 per user / month - 2,000 credits - Access to premium models - Add-on credits ($0.04/credit) ## KIRO PRO MAX $100 per user / month`
- 🔎 **credits ($0** `4/credit) ## KIRO PRO+ $40 per user / month - 2,000 credits - Access to premium models - Add-on credits ($0.04/credit) ## KIRO PRO MAX $100 per user / month - 5,000 credits - Access to premium models - A`

##    FreeDB.tech（免费 MySQL 托管）（freedb）
- 状态: ok | https://freedb.tech
- 🔎 **1 GB of storage, daily backups, and TLS/SSL support** `When you need a database that stays online, upgrade to **Persistent MySQL Hosting ($5/month)** for 1 GB of storage, daily backups, and TLS/SSL support. Instant free MySQL database in seconds Persistent Pro databases (never expire) Automated daily`
- 🔎 **1 GB storage) on `pro** `de to the **$5/month Pro (Persistent) Plan** to remove the 30-day timer and host up to 5 databases (1 GB storage) on `pro.freedb.tech`. ## Web SQL Console & Backups Run queries in the dashboard SQL console, import `.sql`
- 🔎 **1 GB total storage** (MySQL 8 & PostgreSQL)** `, and staging servers. - ✓ **Persistent databases (never auto-deleted)** - ✓ **Up to 5 databases & 1 GB total storage** (MySQL 8 & PostgreSQL) - ✓ **Automated daily backups** (5-day retention) - ✓ **On-demand "Take Backup" snapshots & restore`
- 🔎 **1 GB of storage, and daily backups** `0-day sandbox), while the $5/month Pro plan gives you up to 5 persistent databases, 25 connections, 1 GB of storage, and daily backups. [Free PostgreSQL Database →](https://freedb.tech/free-postgresql-database) [Persistent PostgreSQL`
- 🔎 **Free plan includes 1 Postgres database (5 concurrent connections, 30-** `r project? You can also create a free PostgreSQL database on port 5432 from the same dashboard. The Free plan includes 1 Postgres database (5 concurrent connections, 30-day sandbox), while the $5/month Pro plan gives you up to 5 persistent databases, 25 connections, 1`
- 🔎 **/mo) PostgreSQL (Port 5432)** `Free Remote MySQL Hosting Persistent MySQL 8 Plan ($5/mo) PostgreSQL (Port 5432) # Free MySQL Database & Persistent Remote MySQL Hosting. Create a **free MySQL database** on port`
- 🔎 **/month)** for 1 GB of storage, daily backups, and TLS/SS** `nd prototypes. When you need a database that stays online, upgrade to **Persistent MySQL Hosting ($5/month)** for 1 GB of storage, daily backups, and TLS/SSL support. Instant free MySQL database in seconds Persistent Pro databases (never expire) Automat`
- 🔎 **/mo)](https://freedb** `L console [Create Free MySQL Database](https://freedb.tech/register) [Start Pro Persistent Plan ($5/mo)](https://freedb.tech/register?redirect=upgrade) [Compare Free vs Pro →](https://freedb.tech/plans) Migrating from`
- 🔎 **/month Pro (Persistent) Plan** to remove the 30-day time** `ent Remote MySQL Hosting Use **free remote MySQL hosting** for 30-day tests, or upgrade to the **$5/month Pro (Persistent) Plan** to remove the 30-day timer and host up to 5 databases (1 GB storage) on `pro.freedb.tech`. ## Web SQL Console & Backups Run`
- 🔎 **/month) when your project needs permanent storage, daily** `ema with a **free MySQL database** (30-day free remote MySQL hosting sandbox), or upgrade to Pro ($5/month) when your project needs permanent storage, daily backups, and more space. If you upgrade later, the 30-day timer on your existing databases is remov`
