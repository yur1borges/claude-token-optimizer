# ADR 0002: Install by links, plugin later

## Decision

Today installation is by symbolic links (`scripts/link-skills.sh`) in `~/.claude/skills` and `~/.agents/skills`. Packaging as a Claude Code plugin is left for later.

## Why

With links, editing the skill in the repo changes the installed one immediately, without republishing. A plugin only pays off if other people will install it. If it becomes a plugin, the manifest must list exactly the promoted set, validated with `claude plugin validate . --strict`.
