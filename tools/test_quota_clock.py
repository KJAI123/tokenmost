"""Exercise public quota APIs with real clock instants, including their default clocks."""
import ast
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
from unittest.mock import patch

import token_math as math

ROOT = Path(__file__).resolve().parent.parent
TIMES = ["2026-11-23T08:59:00+08:00", "2026-11-23T09:00:00+08:00", "2026-11-23T09:01:00+08:00"]
cases = []


def add(name, times, expected, **fields):
    deal = {"id": name, "token_quota": [{"amount": 1_000_000, "unit": "tokens", "period": "once"}], **fields}
    cases.extend({"deal": deal, "time": time, "expected": amount} for time, amount in zip(times, expected))


add("exact", TIMES, [100, 0, 0], deadline="2026-11-23T09:00:00+08:00")
add("date-only", TIMES+["2026-11-24T00:00:00+08:00"], [100, 100, 100, 0], deadline="2026-11-23")
add("starts", ["2026-11-20T18:59:59+08:00", "2026-11-20T19:00:00+08:00", "2026-11-20T19:00:01+08:00"],
    [0, 100, 100], starts_at="2026-11-20T19:00:00+08:00", deadline="2026-11-23T09:00:00+08:00")
add("utc-input", ["2026-11-22T23:59:00Z", "2026-11-23T01:00:00Z"], [100, 0],
    deadline="2026-11-23T09:00:00+08:00", token_quota=[{"amount": 1_000_000, "unit": "tokens", "period": "daily"}])
add("early-morning", ["2026-11-23T02:59:00+08:00", "2026-11-23T03:00:00+08:00"], [100, 0],
    deadline="2026-11-23T03:00:00+08:00", token_quota=[{"amount": 1_000_000, "unit": "tokens", "period": "daily"}])

js = """
const math=require('./assets/token-math.js'), ActualDate=Date, results=[];
for(const item of JSON.parse(process.argv[1])) {
  global.Date=class extends ActualDate {
    constructor(...args){super(...(args.length?args:[item.time]));}
    static now(){return new ActualDate(item.time).getTime();}
  };
  results.push({explicit:math.quota(item.deal,new Date(item.time)).total,
    default:math.quota(item.deal).total,phase:math.phase(item.deal),cell:math.cell(item.deal)});
}
global.Date=ActualDate;console.log(JSON.stringify(results));
"""
node = os.environ.get("TOKENMOST_NODE") or shutil.which("node") or "/Applications/ZCode.app/Contents/MacOS/ZCode"
result = subprocess.run([node, "-e", js, json.dumps(cases)], cwd=ROOT, text=True, capture_output=True,
                        env={**os.environ, "ELECTRON_RUN_AS_NODE": "1"})
assert result.returncode == 0, result.stderr
dynamic = json.loads(result.stdout)
ActualDateTime = datetime.datetime
for item, actual in zip(cases, dynamic):
    at = ActualDateTime.fromisoformat(item["time"].replace("Z", "+00:00"))
    expected = item["expected"]
    assert actual["explicit"] == actual["default"] == expected, (item, actual)
    assert math.quota(item["deal"], at)["total"] == expected, item

    class FrozenDateTime(ActualDateTime):
        @classmethod
        def now(cls, tz=None):
            stamp = cls.fromisoformat(item["time"].replace("Z", "+00:00"))
            return stamp.astimezone(tz) if tz else stamp.replace(tzinfo=None)

    with patch.object(math.datetime, "datetime", FrozenDateTime):
        assert math.quota(item["deal"])["total"] == expected, item
    if item["deal"]["id"] == "starts" and expected == 0:
        assert actual["phase"] == "upcoming" and "即将开始" in actual["cell"], actual
    if item["deal"].get("deadline", "").endswith("09:00:00+08:00") and at >= ActualDateTime.fromisoformat(item["deal"]["deadline"]):
        assert actual["phase"] == "expired" and "已失效" in actual["cell"], actual

# Run only the actual sync cutoff function; importing the full collector is unnecessary.
module = ast.parse((ROOT/"tools/sync.py").read_text())
function = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "deadline_passed")
scope = {"datetime": datetime}
exec(compile(ast.Module(body=[function], type_ignores=[]), "sync-cutoff", "exec"), scope)
for time, expired in zip(TIMES, [False, True, True]):
    at = ActualDateTime.fromisoformat(time)
    assert scope["deadline_passed"]("2026-11-23T09:00:00+08:00", at) == expired
    assert scope["deadline_passed"]("2026-11-23", at) is False
print(f"Clock checks passed: {len(cases)} explicit/default clock cases, timezone parity, start labels and sync cutoff.")
