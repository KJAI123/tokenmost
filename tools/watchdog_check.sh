#!/bin/bash
# TokenMost 找源巡检监督（OpenClaw cron 每 30 分钟）：心跳过期→本机弹通知+告警输出；正常时静默
HB="$HOME/.zcode/workspace/9bdf93fc-af54-47d9-9aab-633bc1f72cf5/tokenmost/data-research/harvest/heartbeat.txt"
LOG="$HOME/.zcode/workspace/9bdf93fc-af54-47d9-9aab-633bc1f72cf5/tokenmost/data-research/harvest/watchdog.log"
alert() {
  echo "$1" | tee -a "$LOG"
  osascript -e "display notification \"$1\" with title \"TokenMost 找源巡检监督(龙虾)\" sound name \"Basso\"" >/dev/null 2>&1
  exit 1
}
if [ ! -f "$HB" ]; then alert "🚨 心跳文件不存在——找源管线未启动，请在 ZCode 手动拉起一轮巡检"; fi
AGE=$(( ($(date +%s) - $(stat -f %m "$HB")) / 60 ))
if [ "$AGE" -gt 35 ]; then
  alert "🚨 找源巡检心跳已 ${AGE} 分钟未跳（阈值35分钟）。检查 ZCode 自动化「TokenMost 爬虫助理每15分钟找源巡检」，必要时手动拉起。"
fi
