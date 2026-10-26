# 数据调研爬虫助理 — 任务书

> 角色：tokenmost 的第 4 号角色。只聚焦一件事：**获取信息**。终极目标：**信息获取零 token 化**——日常盯防完全不消耗 LLM，LLM 只在「新数据进站」时做一次增量判读。

## 演进路线（v1 → v3）

| 阶段 | 状态 | 做法 | Token 消耗 |
|---|---|---|---|
| **v1 人工调研** | ✅ 已完成首轮 | LLM 多源搜索 → findings 落盘（带来源+核实时间） | 高 |
| **v2 脚本半自动** | ✅ 已就绪（2026-10-27 首跑成功） | `tools/harvest.py` 纯标准库抓官方页 → 关键词上下文快照；LLM/人只读快照做增量判读 | 低 |
| **v3 零 token 日常** | 🎯 目标态 | harvest 定时跑（用户 crontab 或手动），diff 告警才需要人/LLM 介入；未变化的日子全程无人值守 | **≈0** |

v3 的落地方式（给用户的建议 crontab，非本助理可自设）：

```
# 每天 09:30 抓一轮，快照写入 data-research/harvest/
30 9 * * * cd ~/path/to/tokenmost && /usr/bin/python3 tools/harvest.py >> data-research/harvest/cron.log 2>&1
```

## 文件权属（并发协作协议，重要）

工作区存在多会话并行开发。**单写入方原则**：

| 文件/目录 | 归属 | 说明 |
|---|---|---|
| `deals.json` | 主会话/另一会话 | 站点主数据，爬虫助理**只读不写** |
| `tools/sync.py`、`tools/check.py`、`tools/sources.json` | 另一会话 | 其自建工具链，助理不碰 |
| `tools/harvest.py`、`tools/harvest_sources.json` | 爬虫助理 | 零 token 采集器 |
| `data-research/findings/` | 爬虫助理 | 调研发现（带来源、核实时间、可信度分级） |
| `data-research/harvest/` | 爬虫助理 | harvest 脚本快照输出 |

**数据流入契约**：findings 的「合并素材」小节 → 由 deals.json 的写入方审核后手工合入 → deals.json 的 `verified_at`/来源字段回写。爬虫助理永不直接改 deals.json。

## 合规边界（继承章程红线）

- 只抓公开页面、只记录官方或官方授权渠道的优惠
- 遵守 robots.txt（脚本内置检查，disallowed 即跳过）
- 限速 2 秒/请求、UA 标明身份、15 秒超时
- 不抓登录后内容、不碰个人数据、不绕反爬
- 搜到的「批量小号/多号切换」类玩法一律记录并标记**不予收录**（见 deals.json zcode-linuxdo 条目的先例）

## 下一轮待办（按价值排序）

1. 覆盖 findings 缺口平台：Kimi（platform.kimi.com）、MiniMax、AIHubMix、SambaNova、Together、Cerebras、Mistral、Cohere——多数 deals.json 已有条目，做交叉验证而非重复调研
2. harvest_sources.json 增补新平台的官方定价页 URL（另一会话的 sources.json 也可对齐）
3. Mintlify 类文档站（docs.bigmodel.cn 等）的 `_jsx(` 抽取噪声清洗，提升快照可读性
4. v3：diff 检测脚本（对比 latest.json 与上一份快照，变化才写告警文件）
