#!/bin/bash
# Repo sanity check: SKILL.md frontmatter, README links, em dashes in prose.
cd "$(dirname "$0")/.." || exit 1
fail=0
for d in skills/engineering/*/ skills/productivity/*/; do
  f="${d}SKILL.md"
  [ -f "$f" ] || { echo "missing $f"; fail=1; continue; }
  head -1 "$f" | grep -q '^---' || { echo "no frontmatter: $f"; fail=1; }
  grep -q '^name:' "$f" || { echo "no name: $f"; fail=1; }
  grep -q '^description:' "$f" || { echo "no description: $f"; fail=1; }
done
grep -oh '](\./[^)]*)' README.md | tr -d ']()' | while read -r p; do [ -e "$p" ] || { echo "broken link: $p"; exit 1; }; done || fail=1
if grep -rl '—' --include='*.md' . 2>/dev/null | grep -v '/productivity/' | grep -q .; then echo "em dash found"; fail=1; fi
[ $fail = 0 ] && echo OK
exit $fail
