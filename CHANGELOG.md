# Changelog

All notable changes to this skills repository.

## [Unreleased]

### Changed (2026-11-10)
- docs/setup reescrito em pt-BR com o setup atual e o porquê de cada item, do que saiu e de cada troca
- settings.example.json: Opus + effort low, cache 1 h, compactação pré-calculada, plugins desligados listados, deny dos cavecrew
- Hooks de exemplo novos: filtra-testes.py e loop-edicao.py; pre-compact.py atualizado (HANDOFF.md, ~800 palavras)
- Agentes de exemplo: triage (Haiku) e revisor
- AGENTS.md reflete os agentes atuais

### Deprecated
- brainstorming, llm-council, writing-plans movidas para skills/deprecated

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