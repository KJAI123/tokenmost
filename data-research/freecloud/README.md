# freecloud 线 —— 薅免费云服务器管线

立项：2026-11-06 老板令，以公众号「数字生命斯派克」InstaBox 文章（mp.weixin.qq.com/s/qMabG5jASD-QcFx41Y14qg）为样例开线。
定位：盯防「免费云服务器/云电脑/Agent 沙盒」官方免费档——与 token 羊毛互补的算力羊毛（给 Agent 云端工位）。

## 结构

- `freecloud_sources.json` — 源注册表（官方定价/免费层页，现役 19 源）
- `freecloud_harvest.py` — 采集器（pagesift 内核·零 token·指纹 diff）
- `harvest/` — 快照输出（freecloud-YYYY-MM-DD.md + latest.json）
- `state.json` — 指纹基线（首跑建基线，之后变化才告警）
- `findings/` — 情报条目（带来源+核实时间）

## 用法

```bash
python3 data-research/freecloud/freecloud_harvest.py              # 全量（~19 源，分钟级）
python3 data-research/freecloud/freecloud_harvest.py --only instabox
python3 data-research/freecloud/freecloud_harvest.py --selftest   # 离线自检
```

依赖：宿主机 `pip3 install --user pagesift`（本机已装 0.81.2）；或容器跑（pagesift 在容器内 Linux 原生更顺，见 tools/docker_cycle.sh 分工：容器=国内源，宿主=海外源）。

## 产出协议

- findings 只落本目录 `findings/`；**deals.json 单写入方协议不变**——合入走 HANDOFF.md 由主会话裁决
- 建议纳入现有 5h 找源巡检（爬虫助理会话的 automation 每轮追加跑一次 freecloud_harvest.py）
- 变化告警只看指纹 diff；首跑全量基线不告警

## 免费档样例（首条，2026-11-06 官方页直核）

InstaBox（instabox.sh）Free $0：1 台机器 / 4 vCPU·8 GiB / 20 GiB 持久盘 / 5 快照 / 200 GiB 存储 / 空闲 30 分钟自动暂停 / max run 480 分钟 / 免费档可开 agent-browser·android·ci 三模板。详见 findings/2026-11-06-instabox.md。
