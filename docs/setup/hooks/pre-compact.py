#!/usr/bin/env python3
"""PreCompact hook for Claude Code: tell compaction what to preserve and drop.

Prints PRESERVE/DROP guidance as additional context so a compacted session
keeps decisions, current state and next step, instead of re-injecting full
memory afterwards.
"""
import json

GUIDANCE = (
    "Compact summary: max ~6000 chars, terse bullets, no code dumps or file "
    "contents (cite path:line instead). KEEP: goal, user rules/requests verbatim, "
    "decisions+why, changed files, current state, next step, blockers. "
    "DROP: tool output, test logs, superseded attempts, memory dumps, skill text."
)

print(json.dumps({"additionalContext": GUIDANCE}))
