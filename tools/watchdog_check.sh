#!/bin/bash
# TokenMost 找源巡检监督（OpenClaw cron 每 30 分钟）：心跳过期→本机弹通知+告警输出；正常时静默
HB="$HOME/.zcode/workspace/9bdf93fc-af54-47d9-9aab-633bc1f72cf5/tokenmost/data-research/harvest/heartbeat.txt"
LOG="$HOME/.zcode/workspace/9bdf93fc-af54-47d9-9aab-633bc1f72cf5/tokenmost/data-research/harvest/watchdog.log"
# 2026-11-03 修复：告警一律 exit 0。原来 exit 1 被 OpenClaw 当成任务失败，
# 连续 10 次告警后自动化被自动禁用（看门狗自杀）。告警改走：日志+macOS通知+输出文本（announce 送达飞书）。
alert() {
  echo "$1" | tee -a "$LOG"
  osascript -e "display notification \"$1\" with title \"TokenMost 找源巡检监督(龙虾)\" sound name \"Basso\"" >/dev/null 2>&1
  exit 0
}
if [ ! -f "$HB" ]; then alert "🚨 心跳文件不存在——找源管线未启动，请在 ZCode 手动拉起一轮巡检"; fi
AGE=$(( ($(date +%s) - $(stat -f %m "$HB")) / 60 ))
if [ "$AGE" -gt 360 ]; then  # 5小时巡检节奏（2026-10-29 调整，原35分钟）
  alert "🚨 找源巡检心跳已 ${AGE} 分钟未跳（阈值360分钟）。检查 ZCode 自动化「TokenMost 爬虫助理每5小时找源巡检」，必要时手动拉起。"
fi
