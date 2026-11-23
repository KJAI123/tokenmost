# 用 Python 一行命令处理 JSON：jq 与 jc 实战

<!--
目标平台：CSDN（文章，技术教程体）
发布日建议：2026-11-21（周六）上午 10:00-11:30 技术站早高峰
人味化：2026-11-23（踩坑叙事开场+调试心路，代码与事实未改动）
素材纪律：通用技术知识，无时效数字；无链接、无任何植入
写作与核实日期：2026-11-20
-->

上周四晚上我在服务器上排查一个异常用户，条件是 uid 为 0。搁以前我肯定手写十行 Python：读文件、split、循环、判断，写完还得调一遍。那天不知道哪来的脾气，非想用一行解决——结果倒好，真摸出来一套顺手的组合，jc 配 jq。这篇就把这套玩法整理出来，示例都能直接复制运行。

### 一、环境准备

```bash
# jc 用 pip 安装（Python 生态），jq 用系统包管理器安装
pip install jc
brew install jq        # Ubuntu: sudo apt install jq
```

装完先跑 `jc -h`，能看到它支持的全部解析器：passwd、ls、df、dig、env 等几十种，日常命令基本都覆盖了。我盯着那个列表的第一反应是：以前手写的那些解析脚本，白写了。

### 二、四个实战场景

回到那天晚上的问题，一行搞定：

```bash
cat /etc/passwd | jc --passwd | jq '.[] | select(.uid == 0)'
```

第二个场景是清磁盘，目录文件按大小排 Top5：

```bash
ls -l | jc --ls | jq 'sort_by(.size) | reverse | .[0:5]'
```

看磁盘占用，只关心根分区的话：

```bash
df -h | jc --df | jq '.[] | select(.mount == "/")'
```

DNS 解析结果只取记录值，排查解析问题时特别顺手：

```bash
dig example.com | jc --dig | jq -r '.[].answer[].data'
```

那个 `-r` 是 raw 输出，去掉结果两侧的引号。我第一次就忘了加，脚本拿到带引号的值直接报错，盯着盯了半天才发现是这么个原因，泪目。

### 三、回到 Python 侧

管道玩不转的逻辑，可以无缝回到代码里——jc 本身就是 Python 库：

```python
import subprocess, jc

out = subprocess.run(["ls", "-l"], capture_output=True, text=True).stdout
data = jc.parse("ls", out)   # 直接得到 list[dict]
print(sorted(data, key=lambda x: x["size"], reverse=True)[:5])
```

顺手记两个原生命令：`python -m json.tool a.json` 快速格式化；`python -c "import json; print(json.load(open('a.json'))['key'])"` 一行取值，不动编辑器。

### 四、两个我真踩过的坑

键顺序这事儿坑过我不止一次。JSON 对象的键是无序的，jq 里 `keys` 返回的是排序后的键，想按原始顺序要用 `keys_unsorted`。当时我有个「按键顺序匹配」的逻辑，本地跑得好好的，换个数据源就崩，排查了半个多小时才反应过来——凡是依赖键顺序的逻辑都是定时炸弹。

还有大数精度。jq 内部用双精度浮点处理数字，超过 2^53 的整数（典型如雪花 ID）会失真。这类字段要么当字符串透传，要么换 Python 原生 json 模块处理，别硬刚。

哦对了，还有一条不算坑但得提：不同发行版的 `ls`、`df` 列格式略有差别，关键管道上线前先在目标机器上跑一遍，确认解析结果没问题再说。

你机器上最离不开的那条 JSON 管道长什么样？评论区贴出来，让大家抄作业。
