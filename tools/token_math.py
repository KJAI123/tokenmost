"""Static-page counterpart of assets/token-math.js; parity checked against every deal."""
import datetime

RATES = {"CNY": 1.75, "USD": .2625}


def entries(deal):
    if isinstance(deal.get("token_quota"), list):
        return deal["token_quota"]
    rows = []
    if deal.get("tokens_wan"):
        rows.append(dict(amount=deal["tokens_wan"]*10000, unit="tokens", period="monthly" if deal.get("cadence") == "monthly" else "once"))
    if deal.get("daily_wan"):
        rows.append(dict(amount=deal["daily_wan"]*10000, unit="tokens", period="daily"))
    return rows


def quota(deal, today=None):
    today = today or datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date()
    days = min(30, deal.get("quota_days") or 30)
    try:
        days = min(days, max(0, (datetime.date.fromisoformat(deal["deadline"][:10])-today).days+1))
    except (KeyError, ValueError):
        pass
    result = dict(once=0, daily=0, monthly=0, dailyMonth=0, total=0)
    if deal.get("verify_status") == "expired" or not days:
        return result
    for row in entries(deal):
        row_days = max(0, days-(row.get("starts_after_days") or 0))
        if not row_days:
            continue
        if row.get("convert") is False:
            continue
        if row["unit"] in RATES:
            value = row["amount"]/RATES[row["unit"]]*100
        else:
            value = row["amount"]*(1 if row["unit"] == "tokens" else row.get("tokens_per_unit", 0))/10000*(row.get("equivalent_factor") or 1)
        period = row.get("period", "once")
        if period == "weekly":
            result["monthly"] += value*row_days/7
        else:
            result[period] += value
            if period == "daily":
                result["dailyMonth"] += value*row_days
    result["total"] = result["once"]+result["monthly"]+result["dailyMonth"]
    return result


def free(deal):
    return (deal.get("published") is not False and deal.get("verify_status") != "expired"
            and deal.get("category") not in ("freecloud", "intel_source")
            and deal.get("type") not in ("warning", "price_low", "pricing_plan", "subscription_bonus", "status")
            and deal.get("via") not in ("subscribe", "subscription")
            and not any(deal.get(key) for key in ("quota_paid", "quota_upper_bound", "quota_conditional"))
            and deal.get("gate") not in ("startup", "audit", "oss"))


ESTIMATE_DEFAULTS = {"requestTokens": 4000, "pointTokens": 1000}


def estimate_quota(deal, e, today=None, settings=None):
    rows = entries(deal)
    if not e or e["quota_index"] >= len(rows):
        return None
    q = rows[e["quota_index"]]
    # Native tokens and fixed conversions are never counted again as scenarios.
    converted = q.get("convert") is not False and (q["unit"] == "tokens" or q.get("tokens_per_unit") or q["unit"] in RATES)
    if q["period"] not in ("once", "daily", "weekly", "monthly") or converted or deal.get("verify_status") == "expired":
        return None
    today = today or datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date()
    days = min(30, deal.get("quota_days") or 30)
    try:
        days = min(days, max(0, (datetime.date.fromisoformat(deal["deadline"][:10])-today).days+1))
    except (KeyError, ValueError):
        pass
    days = max(0, days-(q.get("starts_after_days") or 0))
    if not days:
        return None
    settings = {**ESTIMATE_DEFAULTS, **(settings or {})}
    method = e["method"]
    if method == "requests":
        value = settings["requestTokens"]*(e.get("scale") or 1)
        factors = dict(low=value/4, typical=value, high=value*2)
    elif method == "scenario":
        value = settings["pointTokens"]*(e.get("scale") or 1)
        factors = dict(low=value*.5, typical=value, high=value*2)
    elif method == "credit_value":
        factors = {key:e["unit_value"][key]/RATES[e["currency"]]*1e6 for key in ("low", "typical", "high")}
    elif method == "neurons":
        factors = {key:1e6/(row["input"]*.75+row["output"]*.25) for key,row in e["models"].items()}
    elif method == "model_examples":
        factors = {key:(row["input_tokens"]+row["output_tokens"])/row["credits"] for key,row in e["models"].items()}
    elif method == "model_rates":
        factors = {key:1000/(row["input"]*.75+row["output"]*.25) for key,row in e["models"].items()}
    elif method == "model_budget":
        factors = {key:1e6/row["price"] for key,row in e["models"].items()}
    else:
        return None
    quantities = e.get("quantity_range") or dict.fromkeys(("low", "typical", "high"), q["amount"])
    month_units = None
    if e.get("schedule"):
        month_units, before = 0, 0
        for step in e["schedule"]:
            month_units += max(0,min(step["days"],days-before))*step["amount"]
            before += step["days"]
    cap = e.get("token_cap_daily") or float("inf")
    period_tokens = {key:min(cap,quantities[key]*factors[key])/10000 for key in factors}
    cycles = days if q["period"] == "daily" else days/7 if q["period"] == "weekly" else 1
    daily = {key:period_tokens[key] if q["period"] == "daily" else 0 for key in factors}
    month = {key:period_tokens[key]*cycles if month_units is None else min(cap*days,month_units*factors[key])/10000 for key in factors}
    return dict(daily=daily,month=month,periodTokens=period_tokens,period=q["period"],days=days,pool=e.get("pool") or f"{deal['id']}:{e['quota_index']}",priority=e.get("priority") or 0,basis=e)


def estimates(deal, today=None, settings=None):
    definitions = deal.get("quota_estimates", [deal["daily_estimate"]] if deal.get("daily_estimate") else [])
    return [value for e in definitions if (value := estimate_quota(deal,e,today,settings))]


def estimate(deal, today=None, settings=None):
    rows = estimates(deal,today,settings)
    if not rows:
        return None
    if len(rows) == 1:
        return rows[0]
    return dict(rows=rows,period="mixed",days=rows[0]["days"],**{period:{key:sum(row[period][key] for row in rows) for key in ("low","typical","high")} for period in ("daily","month")})


def estimate_many(deals, today=None, settings=None):
    pools = {}
    for deal in deals:
        for value in estimates(deal,today,settings) if free(deal) else []:
            if value["pool"] not in pools or pools[value["pool"]]["priority"] < value["priority"]:
                pools[value["pool"]] = value
    return {**{period:{key:sum(v[period][key] for v in pools.values()) for key in ("low", "typical", "high")} for period in ("daily", "month")}, "count":len(pools)}


def estimate_assumption(deal, e=None):
    if e is None:
        definitions = deal.get("quota_estimates", [deal["daily_estimate"]] if deal.get("daily_estimate") else [])
        return "；".join(estimate_assumption(deal,item) for item in definitions)
    if e.get("method") == "requests":
        scale = e.get("scale") or 1
        return f"默认每次请求含输入+输出 {1000*scale:g}/{4000*scale:g}/{8000*scale:g} Tokens。"
    if e.get("method") == "scenario":
        scale = e.get("scale") or 1
        return f"示意假设：每积分 {500*scale:g}/{1000*scale:g}/{2000*scale:g} Tokens，非官方兑换率。"
    if e.get("method") == "credit_value":
        values = e["unit_value"]
        return f"按积分售价 {values['low']:.6g}/{values['typical']:.6g}/{values['high']:.6g} {e['currency']}/积分，除以 DS Flash {RATES[e['currency']]} {e['currency']}/百万估购买力，不代表实际 Token。"
    if e.get("method") == "neurons":
        return "按公开模型 Neurons 计价、输入:输出=3:1、无缓存估算，模型选择改变可用量。"
    if e.get("method") == "model_examples":
        return "按官方模型示例的输入+输出 Tokens 与每轮 Credits 推算，非固定 Token 赠额；实际随模型、上下文及缓存变化。"
    if e.get("method") == "model_rates":
        return "按官方积分/千Token模型价格，假设输入:输出=3:1、无缓存推算；同一积分池的模型情景不重复相加。"
    if e.get("method") == "model_budget":
        return "按原始余额与官方每百万输入Token价格推算，仅计输入、不估输出；同笔余额不重复折算DS购买力。"
    return ""
