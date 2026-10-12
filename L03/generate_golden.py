"""Boundary cases from the stand's engines: one JSONL line per case on stdout.

The engines are pure functions; app.seed is used only as the list of
operations (customers, transactions) the bot can be asked about.
The stand clock is fixed at AS_OF, so the boundaries come from the data:
we walk the combinations and keep the ones closest to each window edge
(last day inside, first day outside) plus one from the middle of the range.

Run (local python is too old for the engines, so use the stand container):
  docker compose exec -T stand python - < oleh-salnikov/L03/generate_golden.py > sets/l03-boundaries.jsonl
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

if globals().get("__file__", "<stdin>") != "<stdin>":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from app import seed
from app.engines import disputes, fx, limits, policy

AS_OF = date(2026, 9, 15)
CLOCK = "2026-09-15T10:00:00Z"

CUSTOMERS = {c[0]: {"tier": c[3], "hold": bool(c[4]), "fx_used": c[5]}
             for c in seed.CUSTOMERS}
ACCOUNT_OWNER = {a[0]: a[1] for a in seed.ACCOUNTS}
TXS = {t[0]: {"account_id": t[1], "date": date.fromisoformat(t[2]),
              "amount": t[3], "currency": t[4], "merchant": t[5],
              "direction": t[6], "status": t[8]}
       for t in seed.TRANSACTIONS}

WHY_GROUNDED = ("a money figure: level 2 with a tolerance, read from the tool "
                "result in the trace and then from the answer")


def case(cid, text, expected, meta):
    meta.setdefault("context", {})["clock"] = CLOCK
    return {
        "id": cid,
        "input": text,
        "expected_output": expected,
        "context": meta.pop("context"),
        "additional_metadata": meta,
    }


def fx_cases():
    """Free allowance: exactly used up (spread 0), 1 EUR over (full spread,
    all-or-nothing), middle of the free range, middle of the paid range."""
    out = []
    for cust in ("CUS-0001", "CUS-0002", "CUS-0003"):
        tier, used = CUSTOMERS[cust]["tier"], CUSTOMERS[cust]["fx_used"]
        remaining = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier] - used
        plan = [
            ("edge-in", remaining, "allowance_ignored"),
            ("edge-out", remaining + 1, "partial_allowance"),
            ("mid-in", round(remaining / 2), "allowance_ignored"),
            ("mid-out", remaining + policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier],
             "wrong_spread"),
        ]
        for label, amount, failure in plan:
            q = fx.quote(amount, "EUR", "USD", tier, allowance_used_eur=used)
            out.append(case(
                f"FXB-{cust[-2:]}-{label}",
                f"I'm {cust}. Convert {amount:g} EUR to USD. "
                f"What is the final amount I receive?",
                f"{q.final_amount:.2f} USD",
                {"layer": "generation", "oracle": "engine",
                 "assertion": "tool_grounded_numeric",
                 "tool": "quote_fx", "field": "final_amount",
                 "expected_number": round(q.final_amount, 2), "tolerance": 0.02,
                 "source": "edge", "failure_mode": failure,
                 "severity": "high", "runs": 1, "added_in": "l03",
                 "gate": "daily", "boundary": f"allowance {label}",
                 "context": {"customer_id": cust},
                 "engine_call": (f"fx.quote({amount:g}, 'EUR', 'USD', {tier!r}, "
                                 f"allowance_used_eur={used})"),
                 "expected_spread_pct": q.spread_pct,
                 "why_this_level": WHY_GROUNDED}))

    # C-08: CUS-0007 has the whole tier-2 allowance left, so the allowance
    # itself (spread 0) and 1 EUR over it (full spread, all-or-nothing)
    cust = "CUS-0007"
    tier, used = CUSTOMERS[cust]["tier"], CUSTOMERS[cust]["fx_used"]
    remaining = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier] - used
    for cid, label, amount, failure in (
            ("FX-006", "edge-in", remaining, "allowance_ignored"),
            ("FX-007", "edge-out", remaining + 1, "partial_allowance")):
        q = fx.quote(amount, "EUR", "USD", tier, allowance_used_eur=used)
        out.append(case(
            cid,
            f"I'm {cust}. Convert {amount:g} EUR to USD. "
            f"What is the final amount I receive?",
            f"{q.final_amount:.2f} USD",
            {"layer": "generation", "oracle": "engine",
             "assertion": "tool_grounded_numeric",
             "tool": "quote_fx", "field": "final_amount",
             "expected_number": round(q.final_amount, 2), "tolerance": 0.02,
             "source": "edge", "failure_mode": failure,
             "severity": "high", "runs": 1, "added_in": "l03",
             "gate": "daily", "boundary": f"allowance {label}",
             "context": {"customer_id": cust},
             "engine_call": (f"fx.quote({amount:g}, 'EUR', 'USD', {tier!r}, "
                             f"allowance_used_eur={used})"),
             "expected_spread_pct": q.spread_pct,
             "why_this_level": WHY_GROUNDED}))
    return out


def outgoing(cust):
    """Same filter as tools.check_limits: settled outgoing transfers."""
    return [{"date": t["date"], "amount_eur": policy.to_eur(t["amount"], t["currency"])}
            for t in TXS.values()
            if ACCOUNT_OWNER[t["account_id"]] == cust
            and t["direction"] == "out" and t["status"] == "settled"]


def limit_cases():
    """Daily window = AS_OF, monthly window = AS_OF's calendar month.
    Per edge, the customer whose transfer lies closest to it."""
    month_start = AS_OF.replace(day=1)
    mid_month = month_start + (AS_OF - month_start) / 2
    by_cust = {c: outgoing(c) for c in CUSTOMERS}
    by_cust = {c: t for c, t in by_cust.items() if t}

    def pick(dates_of, key):
        cands = [(key(d), c) for c, ts in by_cust.items()
                 for d in dates_of(ts) if key(d) is not None]
        return min(cands)[1] if cands else None

    plan = [
        # transfer made today: counts in the daily window
        ("daily-edge-in", "DAILY", pick(
            lambda ts: [t["date"] for t in ts],
            lambda d: 0 if d == AS_OF else None)),
        # latest transfer made before today: just outside the daily window
        ("daily-edge-out", "DAILY", pick(
            lambda ts: [max(t["date"] for t in ts)],
            lambda d: (AS_OF - d).days if d < AS_OF else None)),
        # earliest transfer in this month: just inside the monthly window
        ("monthly-edge-in", "MONTHLY", pick(
            lambda ts: [t["date"] for t in ts],
            lambda d: (d - month_start).days if d >= month_start else None)),
        # latest transfer before this month: just outside the monthly window
        ("monthly-edge-out", "MONTHLY", pick(
            lambda ts: [t["date"] for t in ts],
            lambda d: (month_start - d).days if d < month_start else None)),
        # transfers in the middle of the month
        ("monthly-mid", "MONTHLY", pick(
            lambda ts: [t["date"] for t in ts],
            lambda d: abs((d - mid_month).days) if d.month == AS_OF.month else None)),
    ]
    out = []
    for label, kind, cust in plan:
        if cust is None:
            continue
        tier = CUSTOMERS[cust]["tier"]
        st = limits.status(tier, AS_OF, by_cust[cust])
        field = "daily_remaining_eur" if kind == "DAILY" else "monthly_remaining_eur"
        value = getattr(st, field)
        out.append(case(
            f"LIMB-{label}-{cust[-2:]}",
            f"I'm {cust}. How much of my {kind} transfer limit is left?",
            f"EUR {value:,.2f}",
            {"layer": "generation", "oracle": "engine",
             "assertion": "tool_grounded_numeric",
             "tool": "check_limits", "field": field,
             "expected_number": round(value, 2), "tolerance": 1.0,
             "source": "edge",
             "failure_mode": "wrong_window" if "edge" in label else "daily_as_monthly",
             "severity": "high", "runs": 1, "added_in": "l03",
             "gate": "daily", "boundary": label,
             "context": {"customer_id": cust},
             "transfer_dates": sorted({t["date"].isoformat() for t in by_cust[cust]}),
             "engine_call": f"limits.status({tier!r}, {AS_OF}, transfers)",
             "why_this_level": WHY_GROUNDED}))
    return out


def dispute_cases():
    """Walk every settled transaction x reason code; margin = days left in
    the window on AS_OF. Per reason code keep the last eligible (smallest
    margin >= 0), the first expired (margin closest to -1) and the one
    nearest the middle of the window. Plus one compliance-hold case."""
    combos = []
    for tx_id, tx in TXS.items():
        if tx["status"] not in policy.DISPUTABLE_STATUSES:
            continue
        hold = CUSTOMERS[ACCOUNT_OWNER[tx["account_id"]]]["hold"]
        age = (AS_OF - tx["date"]).days
        for reason, window in policy.DISPUTE_WINDOWS_DAYS.items():
            combos.append({"tx_id": tx_id, "reason": reason, "hold": hold,
                           "window": window, "margin": window - age})

    chosen = []
    for reason, window in policy.DISPUTE_WINDOWS_DAYS.items():
        free = [c for c in combos if c["reason"] == reason and not c["hold"]]
        inside = [c for c in free if c["margin"] >= 0]
        outside = [c for c in free if c["margin"] < 0]
        picks = []
        if inside:
            picks.append(("edge-in", min(inside, key=lambda c: c["margin"])))
        if outside:
            picks.append(("edge-out", max(outside, key=lambda c: c["margin"])))
        if inside:
            mid = min(inside, key=lambda c: abs(c["margin"] - window / 2))
            if all(mid is not p for _, p in picks):
                picks.append(("mid-window", mid))
        chosen += picks
    held = [c for c in combos if c["hold"] and c["margin"] >= 0]
    if held:
        chosen.append(("hold-mid-window",
                       min(held, key=lambda c: abs(c["margin"] - c["window"] / 2))))

    out = []
    for label, c in chosen:
        tx = TXS[c["tx_id"]]
        r = disputes.check(c["reason"], tx["date"], tx["status"], AS_OF, c["hold"])
        out.append(case(
            f"DISB-{c['tx_id']}-{c['reason']}-{label}",
            f"Transaction {c['tx_id']} ({tx['merchant']}, "
            f"{tx['date'].strftime('%d %B %Y')}). Reason: "
            f"{c['reason'].replace('_', ' ')}. Can I still dispute it?",
            f"eligible = {str(r.eligible).lower()}",
            {"layer": "action", "oracle": "engine",
             "assertion": "tool_result_flag",
             "tool": "check_dispute_eligibility", "field": "eligible",
             "expected_flag": r.eligible,
             "source": "edge",
             "failure_mode": "engine_seam" if c["hold"] else "wrong_window",
             "severity": "critical", "runs": 1, "added_in": "l03",
             "gate": "daily", "boundary": label,
             "margin_days": c["margin"],
             "context": {"transaction_id": c["tx_id"], "reason_code": c["reason"]},
             "engine_call": (f"disputes.check({c['reason']!r}, {tx['date']}, "
                             f"{tx['status']!r}, {AS_OF}, "
                             f"compliance_hold={c['hold']})"),
             "deadline": r.deadline,
             "failing_check": next(
                 (k for k, v in r.checks.items() if v.startswith("fail")),
                 None),
             "why_this_level": "eligibility is a boolean the engine "
                               "decides; level 1 on the tool result"}))
    return out


def main():
    cases = fx_cases() + limit_cases() + dispute_cases()
    for c in cases:
        meta = c["additional_metadata"]
        c["additional_metadata"] = {k: v for k, v in meta.items() if v is not None}
        print(json.dumps(c, ensure_ascii=False))
    print(f"# {len(cases)} boundary cases generated from the engines", file=sys.stderr)


if __name__ == "__main__":
    main()
