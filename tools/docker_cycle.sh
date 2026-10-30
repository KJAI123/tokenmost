#!/bin/bash
# 爬虫管线完整周期（容器内执行）：采集→diff→公众号→TG→验证→摘要
set -u
cd /app
echo "=== [1/5] harvest（$(ls tools/harvest_sources.json >/dev/null && python3 -c "import json;print(len(json.load(open('tools/harvest_sources.json'))['sources']))" 2>/dev/null) 源）==="
python3 tools/harvest.py 2>&1 | tail -3
echo "=== [2/5] diff ==="
python3 tools/harvest_diff.py 2>&1 | tail -2
echo "=== [3/5] 公众号管线 ==="
python3 tools/weixin_pipeline.py 2>&1 | tail -3
echo "=== [4/5] Telegram 监视器 ==="
python3 tools/telegram_monitor.py 2>&1 | tail -3
echo "=== [5/5] 内容验证（批量100）==="
python3 tools/verify_sources.py --limit 100 2>&1 | grep -E "待验证|验证统计" || true
echo "=== 周期完成 $(date -u '+%Y-%m-%d %H:%M UTC') ==="
