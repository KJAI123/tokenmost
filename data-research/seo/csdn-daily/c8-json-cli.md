# 用 Python 一行命令处理 JSON：jq 与 jc 实战

<!--
目标平台：CSDN（文章，技术教程体）
发布日建议：2026-11-21（周六）上午 10:00-11:30 技术站早高峰
结构说明：钩子 → 环境准备 → 4 个实战例 → Python 侧联动 → 避坑（键顺序/大数精度）→ 互动；Markdown 全语法、代码块完整
素材纪律：通用技术知识，无时效数字；无链接、无任何植入
-->

处理 JSON 不一定要写 Python 脚本——`jc`（Python 写的命令行工具）配合 `jq`，一条管道就能把日常命令的输出变成可查询的结构化数据。本文全部示例可直接复制运行。

### 一、环境准备

```bash
# jc 用 pip 安装（Python 生态），jq 用系统包管理器安装
pip install jc
brew install jq        # Ubuntu: sudo apt install jq
```

`jc -h` 可以看到它支持的全部解析器：passwd、ls、df、dig、env 等几十种，日常命令几乎都覆盖了。

### 二、四个实战场景

**例 1：把 /etc/passwd 变成 JSON，找出 uid 为 0 的用户**

```bash
cat /etc/passwd | jc --passwd | jq '.[] | select(.uid == 0)'
```

**例 2：目录文件按大小排 Top5**

```bash
ls -l | jc --ls | jq 'sort_by(.size) | reverse | .[0:5]'
```

**例 3：只看根分区的磁盘占用**

```bash
df -h | jc --df | jq '.[] | select(.mount == "/")'
```

**例 4：DNS 解析结果只取记录值**

```bash
dig example.com | jc --dig | jq -r '.[].answer[].data'
```

`-r` 是 raw 输出，去掉结果两侧的引号，脚本里拿过来就能直接用。

### 三、回到 Python 侧

jc 本身就是 Python 库，管道玩不转的逻辑可以无缝回到代码里：

```python
import subprocess, jc

out = subprocess.run(["ls", "-l"], capture_output=True, text=True).stdout
data = jc.parse("ls", out)   # 直接得到 list[dict]
print(sorted(data, key=lambda x: x["size"], reverse=True)[:5])
```

顺手记两个原生命令：`python -m json.tool a.json` 快速格式化；`python -c "import json; print(json.load(open('a.json'))['key'])"` 一行取值，不动编辑器。

### 四、避坑

1. **键顺序不可依赖**：JSON 对象的键是无序的。jq 里 `keys` 返回的是排序后的键，想按原始顺序要用 `keys_unsorted`。凡是「按键顺序匹配」的逻辑都是定时炸弹。
2. **大数精度丢失**：jq 内部用双精度浮点处理数字，超过 2^53 的整数（典型如雪花 ID）会失真。这类字段要么当字符串透传，要么换 Python 原生 json 模块处理。
3. **命令输出因系统而异**：不同发行版的 `ls`、`df` 列格式略有差别，关键管道上线前先在目标机器上跑一遍确认解析结果。

你机器上最离不开的那条 JSON 管道长什么样？评论区贴出来，让大家抄作业。
