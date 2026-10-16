"""Monthly capacity and cash model, an explicit implementation extension.

Run: python value_model.py input.json [--out result.json]
Python 3.10+, standard library only. Never infers layoffs or realized cash.
All money fields must use one declared currency; all durations are minutes.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def number(data: dict, key: str, nullable: bool = False) -> float | None:
    if key not in data:
        raise ValueError(f"missing field: {key}")
    value = data[key]
    if nullable and value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a finite nonnegative number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{key} must be finite") from exc
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{key} must be a finite nonnegative number")
    return result


def calculate(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    if data.get("period") != "month":
        raise ValueError("period must be month; normalize periods explicitly")
    if data.get("evidence_status") not in ("measured", "estimate"):
        raise ValueError("evidence_status must be measured or estimate")
    if not isinstance(data.get("currency"), str) or not data["currency"].strip():
        raise ValueError("currency is required; use one currency throughout")
    if not isinstance(data.get("quality_guardrails"), str) or not data["quality_guardrails"].strip():
        raise ValueError("quality_guardrails is required")
    volume = number(data, "cases_per_month")
    if not volume.is_integer():
        raise ValueError("cases_per_month must be an integer")
    before = number(data, "baseline_minutes")
    assisted = number(data, "assisted_minutes")
    review = number(data, "review_minutes")
    rework = number(data, "rework_minutes")
    hourly = number(data, "hourly_cost", nullable=True)
    cash = number(data, "realized_cash_savings_per_month", nullable=True)
    ongoing = number(data, "recurring_cost_per_month")
    setup = number(data, "one_off_cost")
    hours = volume * (before - assisted - review - rework) / 60
    capacity_value = None if hourly is None else hours * hourly
    net_cash = None if cash is None else cash - ongoing
    payback = setup / net_cash if net_cash is not None and net_cash > 0 else None
    values = (hours, capacity_value, net_cash, payback)
    if any(v is not None and not math.isfinite(v) for v in values):
        raise ValueError("computed result is not finite; check input magnitudes")
    return {
        "period": "month",
        "currency": data["currency"],
        "evidence_status": data["evidence_status"],
        "quality_guardrails": data["quality_guardrails"],
        "capacity_hours_per_month": hours,
        "capacity_equivalent_value_per_month": capacity_value,
        "realized_cash_savings_per_month": cash,
        "net_cash_savings_per_month": net_cash,
        "payback_months": payback,
        "cash_status": "unknown" if cash is None else "entered_not_independently_verified",
        "interpretation": "Capacity value is not cash savings. Estimates remain estimates. Quality must be checked separately.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        result = calculate(json.loads(args.input.read_text(encoding="utf-8-sig")))
        text = json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
        if args.out:
            args.out.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"value-model error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
