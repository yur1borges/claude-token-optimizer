# Changelog

All notable changes to this skills repository.

## [Unreleased]

### Changed (2026-11-10)
- docs/setup section 8: measured prefix (35.7k tokens), `Artifact` tool denied (minus 12.2k per session), 1 h cache confirmed, compact instructions, and what was evaluated and not adopted
- docs/setup rewritten with the current setup and the why of each item, of what was removed and of each swap
- settings.example.json: Opus + effort low, 1 h cache, precomputed compaction, disabled plugins listed, cavecrew deny
- New example hooks: filtra-testes.py and loop-edicao.py; pre-compact.py updated (HANDOFF.md, ~800 words)
- Example agents: triage (Haiku) and revisor
- AGENTS.md reflects the current agents

### Deprecated
- brainstorming, llm-council, writing-plans moved to skills/deprecated

### Added
- docs/setup: sanitized snapshot of skills layout, hooks (PreCompact, rtk) and token-saving settings
- Initial skill bucket structure (engineering, productivity, misc, in-progress, deprecated)
- 14 engineering skills: brainstorming, find-skills, graphify, humanizer, impeccable, llm-council, systematic-debugging, task-observer, taste-skill, test-driven-development, teste-leigo, ui-ux-pro-max, verification-before-completion, writing-plans
- 2 productivity skills: caveman, ponytail
- Documentation pages for all promoted skills
- Agent definitions in AGENTS.md
- ADR 0001: Skill bucket organization
- ADR 0002: Ship as a Claude Code plugin
- Link script: scripts/link-skills.sh

## [1.0.0] - 2026-11-04

### Added
- Repository initialized with mattpocock/skills structure