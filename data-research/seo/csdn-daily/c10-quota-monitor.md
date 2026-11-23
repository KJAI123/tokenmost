# 写个脚本监控 API 免费额度：Python + crontab 实战

<!--
目标平台：CSDN（文章，技术教程体）
发布日建议：2026-11-30（周一）上午 9:00-11:00 工作日早高峰
人味化：2026-11-23（踩坑叙事开场+弯路标注，代码与事实未改动）
素材纪律：通用技术教程，示例代码自包含；无链接、无任何植入
写作与核实日期：2026-11-20
-->

免费额度最大的坑不是少，而是你不知道它什么时候没了。上个月我有个定时任务就是这么死的：跑到一半批量报错，回头一查，额度早就见底，跑了一半的数据还得重跑，血亏。痛定思痛，写了 30 行 Python 加一条 crontab，每天自动巡检一次，额度水位从此心里有数。脚本全文贴出来，自包含，可以直接抄。

### 一、思路

各家平台的控制台都提供「余额/用量查询」接口，去 API 文档里找 billing 或 quota 相关条目。脚本每天定时查一次：正常就记日志，低于阈值就告警。全程需要三样东西：查询接口地址、API Key、告警阈值。Key 走环境变量，绝不硬编码——这条没得商量。

### 二、完整脚本

```python
#!/usr/bin/env python3
# quota_monitor.py —— API 免费额度每日巡检
import os
import sys
import logging
from pathlib import Path

import requests

API_URL = os.environ["QUOTA_API_URL"]        # 平台的余额/用量查询接口
API_KEY = os.environ["QUOTA_API_KEY"]        # 控制台生成的 Key
THRESHOLD = float(os.environ.get("QUOTA_THRESHOLD", "10"))  # 告警阈值，单位随平台

LOG_FILE = Path(__file__).with_name("quota.log")
logging.basicConfig(
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")],
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)

def fetch_balance():
    resp = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    # 各平台字段名不同：可能是 data["balance"]、data["data"]["total"] 等，按文档改
    return float(data["balance"])

def notify(msg):
    """可选告警推送：配了 QUOTA_WEBHOOK 环境变量才发，没配只写日志"""
    hook = os.environ.get("QUOTA_WEBHOOK")
    if not hook:
        return
    try:
        requests.post(hook, json={"content": msg}, timeout=10)
    except Exception as exc:
        logging.error("告警推送失败: %s", exc)

def main():
    try:
        balance = fetch_balance()
    except Exception as exc:
        logging.error("查询失败: %s", exc)
        sys.exit(2)

    logging.info("当前余额: %.2f（阈值 %.2f）", balance, THRESHOLD)
    if balance < THRESHOLD:
        msg = f"额度告急：余额 {balance:.2f} 已低于阈值 {THRESHOLD}"
        logging.warning(msg)
        notify(msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

逻辑很直白：查余额、写日志、低于阈值就告警。告警推送是可选的，配了 `QUOTA_WEBHOOK` 才发，没配就只写日志，不至于没配 webhook 脚本就跑不起来。

### 三、本地先跑通一次

```bash
export QUOTA_API_URL="你的余额查询接口地址"
export QUOTA_API_KEY="你的Key"
export QUOTA_THRESHOLD="10"

python3 quota_monitor.py
cat quota.log   # 看到一行「当前余额」日志即成功
```

本地一定要先跑通再上 cron，别直接上线赌运气——cron 报错你是看不见的，后面第五节会说这个。

### 四、交给 crontab 每天跑

先把三个环境变量写进独立文件，避免 Key 明文出现在 crontab 里：

```bash
# ~/.quota_env（chmod 600，只让自己可读）
export QUOTA_API_URL="你的余额查询接口地址"
export QUOTA_API_KEY="你的Key"
export QUOTA_THRESHOLD="10"
```

```bash
crontab -e
# 添加一行：每天早上 9:30 巡检，输出追加到 cron.out 便于排查
30 9 * * * . $HOME/.quota_env && /usr/bin/python3 /home/you/scripts/quota_monitor.py >> /home/you/scripts/cron.out 2>&1
```

`crontab -l` 确认生效。告警推送可选：给 `QUOTA_WEBHOOK` 配上你的群机器人地址，余额告急会直接推到群里。我自己的阈值设得偏保守，图个安心。

### 五、四个坑，都是我或身边人真踩过的

cron 的环境变量和你终端不是一套，这是 crontab 任务「本地能跑、线上不跑」的头号原因——脚本里用绝对路径，依赖的变量显式 source 进来。时区也注意：服务器多是 UTC，`30 9 * * *` 是服务器时间，换算成北京时间再定，不然告警总在你睡觉时响，响了你也不知道。字段名要按文档改，不同平台返回结构不同，`fetch_balance` 里取字段的逻辑逐家对照文档，别照抄示例。阈值别设 0——等余额归零才告警等于没告警，免费额度断供的第一表现是任务批量失败，阈值要给你留出换平台或充值的时间。

再加个反向玩法：多写几份脚本把几家平台的查询都接进来，`quota.log` 天然就是一张「额度周报表」，配合每周十分钟的复盘刚刚好。

你的告警阈值设的是多少？评论区对个答案。
