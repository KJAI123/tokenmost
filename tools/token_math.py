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
        if row.get("convert") is False:
            continue
        if row["unit"] in RATES:
            value = row["amount"]/RATES[row["unit"]]*100
        else:
            value = row["amount"]*(1 if row["unit"] == "tokens" else row.get("tokens_per_unit", 0))/10000*(row.get("equivalent_factor") or 1)
        period = row.get("period", "once")
        if period == "weekly":
            result["monthly"] += value*30/7
        else:
            result[period] += value
    result["dailyMonth"] = result["daily"]*days
    result["total"] = result["once"]+result["monthly"]+result["dailyMonth"]
    return result


def free(deal):
    return (deal.get("published") is not False and deal.get("verify_status") != "expired"
            and deal.get("category") not in ("freecloud", "intel_source")
            and deal.get("type") not in ("warning", "price_low", "pricing_plan", "subscription_bonus", "status")
            and deal.get("via") not in ("subscribe", "subscription")
            and not any(deal.get(key) for key in ("quota_paid", "quota_upper_bound", "quota_conditional"))
            and deal.get("gate") not in ("startup", "audit", "oss"))
