# Glossary

## Terms

**Skill**: A reusable prompt/instruction package that teaches Claude a specific capability. Has a `SKILL.md` defining trigger, behavior, and success criteria.

**Bucket**: Top-level category under `skills/`: engineering, productivity, misc, in-progress, deprecated.

**Promoted**: Skills in engineering/ or productivity/ that ship in the local harness and appear in README.md.

**User-invoked**: Skill only reachable by human trigger (e.g., `/skill-name`). `disable-model-invocation: true`.

**Model-invoked**: Skill reachable by model or human. No invocation restriction.

**ADR**: Architecture Decision Record. Numbered markdown files in `.agents/adr/`.

**Marketplace**: External skill source (GitHub repo). Configured in settings.json.

**Combo**: Model routing configuration mapping task categories to subagents.

**Hook**: Script that runs on Claude Code events (PreToolUse, SessionStart, etc.).

**Subagent**: Specialized agent type with model/effort config (e.g., programador, revisor).