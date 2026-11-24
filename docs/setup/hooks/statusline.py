"""Status line: model | session cost | context % | lines changed. Reads the JSON Claude Code sends on stdin."""
import json, sys

sys.stdout.reconfigure(encoding="utf-8")
try:
    d = json.load(sys.stdin)
except Exception:
    d = {}
cost = (d.get("cost") or {})
cw = d.get("context_window") or {}
parts = [(d.get("model") or {}).get("display_name") or "?"]
if cost.get("total_cost_usd") is not None:
    parts.append(f"US$ {cost['total_cost_usd']:.2f}")
if cw.get("used_percentage") is not None:
    parts.append(f"ctx {cw['used_percentage']:.0f}%")
if d.get("exceeds_200k_tokens"):
    parts.append(">200k")
print(" | ".join(parts))
