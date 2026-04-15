# Claude Code Project Context (CLAUDE.md)

@AGENTS.md  <-- This imports all shared team standards

## 🤖 Claude-Specific Instructions

### Context Management

- When the session fills up, prioritize keeping the `src/*/scripts/`
  definitions in the context window.

### Subagents

- Use a `code-reviewer` subagent for any changes touching the `auth/` directory.

### Permissions

You are pre-approved to run:

- `git status`
- `npm run lint`
- `ruff`
