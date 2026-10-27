#!/bin/bash
# resume.sh — 断线重连恢复器
# 用途：会话断线/重开后跑一次，立即掌握断点和数据现状；配合每30分钟自动监督任务使用
cd "$(dirname "$0")/.." || exit 1

echo "════════ tokenmost 断点状态 $(date '+%F %T') ════════"
echo
echo "── 任务队列（SESSION_STATE.md）──"
grep -E '^\s*-\s*\[' SESSION_STATE.md 2>/dev/null || echo "（无状态文件，先读 SESSION_STATE.md）"
echo
echo "── 数据快照 ──"
python3 -c "
import json
d = json.load(open('deals.json'))
pub = sum(1 for x in d if x.get('published'))
ver = sum(1 for x in d if x.get('verify_status')=='verified')
print(f'deals.json: {len(d)} 条（发布 {pub} / 验证 {ver}）')
deep = sorted(__import__('glob').glob('data-deep/deep-r*.json'))
print(f'deep 分片: {len(deep)} 个（最新: {deep[-1].split(chr(47))[-1] if deep else \"无\"}）')
"
echo
echo "── 校验 ──"
python3 tools/check.py >/dev/null 2>&1 && echo "check.py PASS ✓" || echo "check.py FAIL ✗（需修复后才能推版）"
echo
echo "── 最近提交 ──"
git log --oneline -5 2>/dev/null || echo "（无 git 记录）"
echo
echo "── 续命指令 ──"
echo "1. 读 SESSION_STATE.md 任务队列，从第一个未完成项继续"
echo "2. deep-r*.json 未合并 → 合并进 deals.json（按 id 去重）→ check.py → git push"
echo "3. 后台主管 agent 翻车（并发限额）→ 等几分钟重新拉起，串行一次一个"
