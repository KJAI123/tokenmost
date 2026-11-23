#!/usr/bin/env python3
"""Read-only source coverage report and regression check against a saved deals.json."""
import argparse
from hashlib import sha256
from collections import Counter
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
SOURCE_KINDS = {"official", "community", "aggregator", "firsthand"}


def link_key(url):
    if not isinstance(url, str) or any(ch.isspace() for ch in url):
        return None
    try:
        p = urlsplit(url)
        if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password:
            return None
        port = p.port
    except ValueError:
        return None
    netloc = p.netloc.lower()
    if (p.scheme, port) in (("https", 443), ("http", 80)):
        netloc = netloc.rsplit(":", 1)[0]
    query = urlencode(sorted((k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                             if not k.lower().startswith("utm_")))
    return urlunsplit((p.scheme, netloc, p.path.rstrip("/"), query, p.fragment))


def harvest_source_id(url):
    key = link_key(url)
    if not key:
        raise ValueError("invalid source URL")
    host = urlsplit(key).hostname.removeprefix("www.")
    slug = re.sub(r"[^a-z0-9]+", "-", host).strip("-")
    return f"{slug[:24]}-{sha256(key.encode()).hexdigest()[:10]}"


def registry_errors(sources, registry):
    counts = Counter(s.get("id") for s in sources)
    for sid, n in counts.items():
        if not sid or n > 1:
            yield f"{registry}: 信源 ID 缺失或重复: {sid!r} ({n} 条)"
    for s in sources:
        if "auto_verify" in s and not isinstance(s["auto_verify"], bool):
            yield f"{registry}: {s.get('id')}: auto_verify 需要布尔值"


def evidence_errors(deals):
    for d in deals:
        if d.get("published") and not link_key(d.get("url")):
            yield f"{d.get('id', '?')}: 公开领取入口必须是有效的 HTTP(S) 地址"
        if "sources" not in d:
            continue
        sid = d.get("id", "?")
        if not isinstance(d["sources"], list):
            yield f"{sid}: sources 必须是数组"
            continue
        seen = set()
        for n, source in enumerate(d["sources"], 1):
            if not isinstance(source, dict):
                yield f"{sid}: sources[{n}] 必须是对象"
                continue
            key = link_key(source.get("url"))
            title = source.get("title")
            if not key or not isinstance(title, str) or not title.strip():
                yield f"{sid}: sources[{n}] 需要可用的 HTTP(S) URL 和标题"
                continue
            if "kind" in source and (not isinstance(source["kind"], str) or source["kind"] not in SOURCE_KINDS):
                yield f"{sid}: sources[{n}] 的 kind 无效"
            if key in seen:
                yield f"{sid}: sources[{n}] 信源 URL 重复"
            seen.add(key)


def evidence_snapshot(deals):
    return {
        d["id"]: {link_key(source.get("url")) for source in d["sources"]
                  if isinstance(source, dict) and link_key(source.get("url"))}
        for d in deals if isinstance(d.get("sources"), list) and d["sources"]
    }


def lost_evidence(before, after):
    """Protect recorded evidence even after a deal is archived or marked expired."""
    return {sid: sorted(links - after.get(sid, set()))
            for sid, links in before.items() if links - after.get(sid, set())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--against", type=Path, help="已审阅的历史 deals.json 快照")
    args = parser.parse_args()
    deals = json.loads((ROOT / "deals.json").read_text())
    evidence = evidence_snapshot(deals)
    errors = list(evidence_errors(deals))
    if args.against:
        prior = evidence_snapshot(json.loads(args.against.read_text()))
        errors.extend(f"{sid}: 丢失信源 {url}" for sid, urls in lost_evidence(prior, evidence).items()
                      for url in urls)
    candidates = json.loads((ROOT / "data-research/source_candidates.json").read_text())["candidates"]
    watch = json.loads((ROOT / "tools/sources.json").read_text())["sources"]
    harvest = json.loads((ROOT / "tools/harvest_sources.json").read_text())["sources"]
    errors.extend(registry_errors(watch, "tools/sources.json"))
    errors.extend(registry_errors(harvest, "tools/harvest_sources.json"))
    active = [d for d in deals if d.get("published", True) and d.get("verify_status") != "expired"
              and d.get("category") != "intel_source" and d.get("type") != "warning"]
    monitored = {did for s in watch for did in s.get("deals", [])}
    monitored.update(a["deal"] for s in watch for a in s.get("actions", []) if "deal" in a)
    domains = len({urlsplit(s["url"]).hostname for s in harvest if not s.get("disabled")})
    statuses = Counter(d.get("verify_status", "unknown") for d in active)
    print(f"在架 {len(active)} 条 | 独立信源 {sum(d['id'] in evidence for d in active)} 条"
          f" | 已绑定监控 {sum(d['id'] in monitored for d in active)} 条")
    print("状态: " + " / ".join(f"{key} {n}" for key, n in sorted(statuses.items())))
    print(f"候选 {len(candidates)} 个 | 采集 {sum(not s.get('disabled') for s in harvest)} 个（{domains} 域）"
          f" | 同步/监控 {len(watch)} 个")
    state_path = ROOT / ".sync-state.json"
    if state_path.exists():
        entries = json.loads(state_path.read_text()).get("entry_links", {})
        active_ids = {d["id"] for d in active}
        probed = {did for row in entries.values() for did in row.get("deals", [])}
        print(f"领取入口检查 {len((probed - monitored) & active_ids)} 条 | 条款或入口覆盖 {len((probed | monitored) & active_ids)}/{len(active_ids)} 条")
    for err in errors:
        print("ERROR:", err)
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
