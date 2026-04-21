---
title: Claude Code Quick Start and Anthropic Product Offering for Academic
  Environments
subtitle: |
  Installation, authentication, and product-tier comparison of Claude Code
  and Anthropic API access options for academic statistics departments
  operating multi-agent project templates on Ubuntu Linux
# {{{ // %+
category: LLM-Style
keywords: [GEN, Claude-Code, Anthropic-API, multi-agent, nvm, Ubuntu,
  academic-deployment]
abstract: |
  This document addresses two related objectives concerning the deployment
  of Anthropic tooling in an academic statistics department running a
  shared multi-agent project template on Ubuntu 24.04.

  The first part presents a practical quick-start guide for `claude-code`,
  Anthropic's CLI coding assistant, installed via a user-level `nvm`-managed
  `npm` environment. It covers installation, authentication and model
  configuration for zero-cost trial use, installation verification, and a
  worked interaction example assuming `uv`-managed Python tooling (`uv run
  pytest`, `uv run ruff`). The role of `.claude/CLAUDE.md` as a
  project-context entry point—importing shared agent instructions from
  `.agents/AGENTS.md` via an `@AGENTS.md` directive—is explained, together
  with how the `.agents/skills/` directory is surfaced to Claude Code,
  enabling skill reuse across Claude Code, Gemini CLI, Cursor, and VS Code
  Copilot without duplication.

  The second part provides a structured comparison of Anthropic access
  tiers—Claude.ai Free, Pro, Team, and Enterprise, the pay-as-you-go
  Anthropic API, and Claude Code as a product layer—evaluated against
  criteria relevant to an academic organisation: monthly cost, free-tier
  availability, model access (Haiku / Sonnet / Opus), context window,
  rate limits, API key requirements, team and organisation support, and
  data-privacy policy.

  A recommended proof-of-concept path for a department seeking zero-cost
  initial evaluation prior to any paid commitment is derived from this
  comparison. Together, the two sections constitute a self-contained
  onboarding reference for researchers and students adopting Claude Code
  within a pre-existing multi-agent template infrastructure.

doctype: md-report
# }}} // %+
---

<!-- {{{ #TAG: TODO:(toc) // -->

<!-- markdownlint-disable MD012 -->
<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD053 -->


# TOC

1. [Q:1 - Claude Code - Quick Start Guide](#q1)
   - see: [Claude Code Quick Start Guide (Claude)](#a1-claude)
   - see: [Claude Code Quick Start Guide (Gemini)](#a1-gemini)
   - see: [Claude Code Quick Start Guide (ChatGPT)](#a1-chatgpt)
   - see: [Claude Code CLI - Quick Start Guide (Perplexity)](#a1-perplexity)
   - see: [Claude Code Quick Start Guide (DeepSeek)](#a1-deepseek)
2. [Q:2 - Anthropic Product Offering Comparison academic Use](#q2)
   - see: [Anthropic Product Offering Comparison (Claude)](#a2-claude)
   - see: [Anthropic Product Offering Comparison (Gemini)](#a2-gemini)
   - see: [Anthropic Product Offering Comparison for Academic Environments (ChatGPT)](#a2-chatgpt)
   - see: [Anthropic product offering comparison for academic use (Perplexity)](#a2-perplexity)
   - see: [Anthropic Product Offering Comparison for Academic Statistics Department (DeepSeek)](#a2-deepseek)

<details>
<summary></summary>

```{=latex}
\begin{comment}
```

</details>

---

|                   |                        |
|-------------------|------------------------|
| [<<<<](README.md) | [PDF](TODO:(file).pdf) |

---

<details>
<summary>[index]</summary>

[[_TOC_]]

</details>
<details>
<summary></summary>

```{=latex}
\end{comment}
```

</details>

<!-- ::}}} \\ %0. -->
<!-- ::{{{ #TAG: TODO:(q1-section) // -->

# Q:1

## Q:1 - **Claude Code - Quick Start Guide**

[^](#toc)

## Role

You are an expert in developer tooling, CLI configuration, and Anthropic
product offerings, with specific knowledge of Claude Code setup on Linux systems.

## Context

The target environment is:

- OS: Ubuntu 24.04
- Node.js: managed via user-level `nvm` and `npm`
- Python stack: `uv`-managed, PEP-compliant `pyproject.toml`, with R support
- ML focus: CUDA-enabled Python/R/Julia projects
- Organisation: Academic Statistics Department (researchers and students)

The project already uses a multi-agent template compatible with:

- Claude Code (Anthropic)
- Gemini CLI (Google)
- Cursor
- VS Code Copilot

Shared agent instructions live under `.agents/`, with Claude-specific
configuration in `.claude/CLAUDE.md`, which imports `.agents/AGENTS.md`
via an `@AGENTS.md` directive. Skills are stored under `.agents/skills/`
and shared across all agent tools without duplication.

## Primary Objective

Produce a _Claude Code Quick Start Guide_ for evaluation purposes,
covering the following steps in order:

1. Installation of Claude Code CLI via `nvm`-managed `npm` on Ubuntu 24.04
2. Authentication and model configuration for _zero-cost trial use_
   (using the Claude free tier or an unauthenticated/limited Sonnet endpoint
   where available — clarify which options exist)
3. Verification of the installation with a simple shell command
4. A worked interaction example using an existing Python project
   (assume `uv run pytest` and `uv run ruff` as the standard commands,
   as defined in `.agents/AGENTS.md`)
5. A brief note on how `.claude/CLAUDE.md` and `.agents/AGENTS.md`
   are used together to give Claude Code project context

## Secondary Objective

Describe how the existing `.agents/skills/` directory structure is
recognised by Claude Code, so that skills authored for Gemini CLI
are reusable without modification or duplication.
Specify whether any additional `.claude/` configuration is required
to point Claude Code to `.agents/skills/`.

## Output Format

Reply in GitLab Flavored Markdown (GLFM) with precise lint compliance:

- Codeblock delimiters ` ``` ` placed at line start; no nested codeblocks
- _Underscore markup_ for emphasis
- Nested headings preferred over bold text
- Only dash (`-`) for unordered lists, with correct indentation
- Blank line after every heading, list block, and codeblock

At the end, add a _References_ section as Markdown footnotes,
prefixed `rf-`, linked inline where cited.
Add an _Additional Notes_ section for any important information
not explicitly requested.


# A:1 (Claude)

[^](#toc) **_Claude Code — Quick Start Guide_**

_Target environment: Ubuntu 24.04 · `nvm`/`npm` Node.js · `uv` Python stack_

---

## Prerequisites

Before installing, verify that Node.js 18 or later is active in your `nvm`
environment.[^ac-1]

```bash
node --version   # must report v18.0.0 or higher
npm --version    # must report v8.0.0 or higher
```

If the required version is not active:

```bash
nvm install 20
nvm use 20
nvm alias default 20
```

---

## Step 1 — Install the Claude Code CLI

Install the package globally using your `nvm`-managed `npm`:

```bash
npm install -g @anthropic-ai/claude-code
```

Because `nvm` installs Node.js under your home directory, no `sudo` is
required and no permission conflicts arise. The binary is placed in
`~/.nvm/versions/node/<version>/bin/`, which `nvm` adds to `$PATH`
automatically.

Verify the installation:

```bash
claude --version
```

A version string confirms the binary is on your `$PATH`. If the shell reports
_command not found_, open a new terminal session so the updated `$PATH` is
sourced.

---

## Step 2 — Authentication and Zero-Cost Access Options

### Important: Free Tier Does Not Include Claude Code

Claude Code requires a Pro, Max, Team, Enterprise, or Console account.
The free Claude.ai plan does not include Claude Code access.

This is a hard constraint, not a configuration limitation. The table below
maps every zero-cost or low-cost path available for a proof-of-concept.

| Option                  | Cost                | Account required   | Notes                                      |
|-------------------------|---------------------|--------------------|--------------------------------------------|
| Claude.ai Pro           | $20/month           | Anthropic account  | Cheapest native Anthropic access           |
| Anthropic API (Console) | Pay-per-token       | Console account    | Free $5 credit on new accounts             |
| Google Gemini backend   | Free (rate-limited) | Google account     | Redirects Claude Code to Gemini API[^ac-2] |
| OpenRouter free models  | Free (50 req/day)   | OpenRouter account | Routes to DeepSeek, Llama, Qwen[^ac-3]     |

_The recommended zero-cost path for initial evaluation_ is to configure
Claude Code against the Google AI Studio Gemini API, which requires only a
Google account with no billing details.

### Option A — Native Anthropic Authentication (Pro/Console)

Run Claude Code from your project directory and follow the browser prompt:

```bash
cd /path/to/your/project
claude
```

OAuth authentication opens a browser window where the user authorises Claude Code against their Anthropic account.
After authorisation completes, the session token is cached and subsequent
invocations do not require re-authentication.

For API key authentication, retrieve your key from
`https://console.anthropic.com` and set it for the current shell session
only (do not commit it to your shell profile):

```bash
export ANTHROPIC_API_KEY="$(cat ~/.secrets/anthropic_key)"
```

### Option B — Free Evaluation via Google AI Studio (Zero Cost)

Claude Code works completely free with Google AI Studio — just a Google account.
Three environment variables are all it takes to redirect Claude Code to any backend.

1. Visit `https://aistudio.google.com`, generate a free API key.
2. Set the following variables in your shell or in a project-local `.env`
   file (never commit this file):

   ```bash
   export ANTHROPIC_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai"
   export ANTHROPIC_API_KEY="<your-google-ai-studio-key>"
   export ANTHROPIC_MODEL="gemini-2.5-flash"
   ```

3. Launch Claude Code normally:

   ```bash
   claude
   ```

Claude Code will route all requests to Gemini 2.5 Flash instead of the
Anthropic endpoint. The CLI interface, skill loading, and CLAUDE.md context
behaviour are identical regardless of which backend is in use.

_Note on Gemini free-tier limits_: Google significantly reduced Gemini API
free tier limits in December 2025. Daily request limits dropped 50–80% for
most models. For light evaluation work this is sufficient; for sustained
use, a paid tier is advisable.

## Step 3 — Verify Installation and Project Context

Navigate to the project root and confirm Claude Code loads correctly:

```bash
cd /path/to/your/project
claude --version
claude doctor
```

`claude doctor` prints a diagnostic report covering authentication status,
model connectivity, and configuration file discovery.[^ac-4]

Inside an interactive session, run:

```bash
/memory
```

This opens the memory editor and confirms which CLAUDE.md files have been
discovered and loaded.

---

## Step 4 — Worked Interaction Example

The following example assumes an existing Python project managed with `uv`,
with tests under `tests/pytest/` as defined in `.agents/AGENTS.md`.

### 4.1 — Start Claude Code in the project root

```bash
cd /path/to/your/project
claude
```

Claude Code walks the filesystem upward from the current directory,
collecting CLAUDE.md files. It will load `.claude/CLAUDE.md`, which in
turn imports `.agents/AGENTS.md` via the `@AGENTS.md` directive.

### 4.2 — Explain a failing test

At the Claude Code prompt, type:

```text
A test in tests/pytest/test_model.py is failing.
Please run it and explain the failure.
```

Claude Code will execute the pre-approved command from `.claude/CLAUDE.md`:

```bash
uv run pytest tests/pytest/test_model.py -xvs
```

It will then read the traceback and provide a diagnosis with suggested
fixes, respecting the project convention of always prefixing Python
tools with `uv run`.

### 4.3 — Fix and lint in one pass

```text
Apply the fix and run ruff to check the result.
```

Claude Code will edit the relevant source file and then run:

```bash
uv run ruff check --fix <file>
uv run ruff format <file>
```

These commands are pre-approved in `.claude/CLAUDE.md`, so no interactive
permission prompt is shown for them.

---

## Step 5 — How CLAUDE.md and AGENTS.md Work Together

CLAUDE.md files are markdown files that give Claude persistent instructions
for a project. Claude reads them at the start of every session.

The project uses a two-layer design:

```text
.agents/AGENTS.md       ← shared rules (tool commands, project scope,
                          coding conventions, commit standards)
.claude/CLAUDE.md       ← Claude-specific entry point
                          imports @AGENTS.md, adds Claude-only directives
```

The `@AGENTS.md` line in `.claude/CLAUDE.md` is an _import directive_.
Memory files can reference other files using `@` notation. The referenced
file is inserted into the context as a separate entry before the including
file.

The effective context Claude Code sees at session start is therefore the
concatenation of both files, with `.claude/CLAUDE.md` taking priority for
any conflicting instruction. Rules defined in `.agents/AGENTS.md` — such as
the `uv run` prefix requirement and the commit message convention — are
inherited automatically without duplication.

Claude Code supports a layered memory system. Files loaded later take precedence
because the model pays more attention to instructions that appear later in
the context window. The loading order from lowest to highest priority is:
managed system policy → user global `~/.claude/CLAUDE.md` → project
`.claude/CLAUDE.md` → local overrides.

---

## Secondary Objective — Skills Compatibility with `.agents/skills/`

### How Claude Code Discovers Skills

Skills are folders containing a SKILL.md file and optional scripts or other
resources. Claude Code scans the following paths at session startup:

| Location | Path                                     | Scope                   |
|----------|------------------------------------------|-------------------------|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All projects            |
| Project  | `.claude/skills/<skill-name>/SKILL.md`   | This project only       |
| Plugin   | `<plugin>/skills/<skill-name>/SKILL.md`  | Where plugin is enabled |

Custom Skills in Claude Code are filesystem-based and don't require API
uploads. Claude discovers and uses them automatically.

### The Problem: `.agents/skills/` Is Not a Native Path

Your project stores skills under `.agents/skills/`, which is _not_ one of
the directories Claude Code scans by default.[^ac-5] Skills can only be loaded
from hardcoded paths. There is no way to point Claude at a custom directory
like `.agents/skills/` without symlinks or workarounds.

The `--add-dir` flag is the closest native mechanism, but it has a
limitation: the `--add-dir` flag grants file access rather than configuration
discovery, but skills are an exception: `.claude/skills/` within an added
directory is loaded automatically. This means `--add-dir .agents` would
load `.agents/.claude/skills/` but _not_ `.agents/skills/` directly.

### Recommended Solutions (in order of preference)

#### Solution 1 — Symlink (simplest, no repo changes)

Create a symlink from the expected Claude Code path to the shared skills
directory:

```bash
mkdir -p .claude/skills
# For each skill, create a symlink:
ln -s ../../.agents/skills/python-patterns .claude/skills/python-patterns
ln -s ../../.agents/skills/vce-coding-standards .claude/skills/vce-coding-standards
# ...repeat for all skills
```

_Caveat_: symlinks from `.claude/skills/` to another directory are not
followed by the `/skills` UI dialog scanner, though Claude Code can still
read and invoke them correctly through CLAUDE.md references.

#### Solution 2 — `@`-import in CLAUDE.md (most explicit, no symlinks)

Add explicit imports for each skill's SKILL.md in `.claude/CLAUDE.md`:

```markdown
## Skills (loaded from shared .agents/skills/)

@.agents/skills/python-patterns/SKILL.md
@.agents/skills/python-pro/SKILL.md
@.agents/skills/python-testing-patterns/SKILL.md
@.agents/skills/vce-coding-standards/SKILL.md
@.agents/skills/vce-project-layout/SKILL.md
@.agents/skills/vce-project-scripts/SKILL.md
@.agents/skills/gitlab-automation/SKILL.md
@.agents/skills/tmux/SKILL.md
```

_Trade-off_: skill content is loaded eagerly into the context window on
every session start, unlike the native lazy-load model where skills load
only when triggered. For a large number of skills this can cause context
pressure. Prefer this approach for the three to five most critical skills,
and use symlinks for the rest.

#### Solution 3 — `--add-dir` at launch (no repo changes required)

Launch Claude Code with an additional directory flag:

```bash
claude --add-dir .agents
```

`.claude/skills/` within an added directory is loaded automatically.
This requires placing skills under `.agents/.claude/skills/` rather than
`.agents/skills/`. If restructuring the shared directory is acceptable, this
is the cleanest long-term approach and requires no symlinks or CLAUDE.md
edits.

### SKILL.md Format Compatibility

The skills in `.agents/skills/` use the standard `SKILL.md` + YAML
frontmatter format. Claude Code skills follow the Agent Skills open
standard, which works across multiple AI tools. Provided each skill file
begins with valid YAML frontmatter containing `name` and `description`
fields, _no format changes are needed_ for Claude Code compatibility.

A minimal valid frontmatter for an existing skill that may lack it:

```yaml
---
name: python-patterns
description: >
  Python design patterns and idioms for this project.
  Use when writing, reviewing, or refactoring Python code.
---
```

---

## Additional Notes

- _Auto-memory_: Claude Code can accumulate notes across sessions without
  manual effort. Claude saves notes for itself as it works: build
  commands, debugging insights, architecture notes, and code style
  preferences. These persist across sessions. This is enabled by default
  from v2.1.59 onward and can be browsed or cleared with `/memory`.

- _`.claudeignore`_: Create a `.claudeignore` file (same syntax as
  `.gitignore`) to exclude build artefacts, lock files, and generated files
  from Claude's context. This is especially important for ML projects where
  model checkpoints and dataset directories can be very large.

- _GitLab Duo compatibility_: GitLab Duo Ultimate uses its own context
  system and does not read `.claude/` or `.agents/` directories. The shared
  skills in `.agents/skills/` are therefore not directly reusable by Duo,
  though the coding conventions in `.agents/AGENTS.md` can be manually
  referenced when configuring Duo's custom instructions.

- _Context window budget_: Files over 200 lines consume more context and
  may reduce adherence. Move detailed content into separate files referenced
  with `@path` imports, or split instructions across `.claude/rules/`
  files. The existing split between `AGENTS.md` and the `rules/` directory
  already follows this best practice.

- _Model string for scripting_: When passing `--model` on the command line
  or setting `ANTHROPIC_MODEL`, use `claude-sonnet-4-6` for the current
  default Sonnet model.

---

## References

- [^ac-1]: [Claude Code system requirements and installation](https://code.claude.com/docs/en/setup)
- [^ac-2]: [Free Claude Code setup via Google AI Studio](https://prince-arora-aws.medium.com/how-i-set-up-claude-code-for-free-no-subscription-no-credit-card-and-what-i-learned-along-the-2cba880682a2)
- [^ac-3]: [OpenRouter free model routing for Claude Code](https://agentfactory.panaversity.org/docs/General-Agents-Foundations/general-agents/free-claude-setup)
- [^ac-4]: [Claude Code troubleshooting and `claude doctor`](https://support.claude.com/en/articles/14552646-troubleshoot-claude-code-installation-and-authentication)
- [^ac-5]: [Custom skills directory path limitations (GitHub issue)](https://github.com/anthropics/claude-code/issues/22902)
- [^ac-6]: [Official Claude Code skills documentation](https://code.claude.com/docs/en/skills)
- [^ac-7]: [Claude Code memory and CLAUDE.md system](https://code.claude.com/docs/en/memory)


# A:1 (Gemini)

[^](#toc) **_Claude Code Quick Start Guide_**


## Claude Code Quick Start Guide

### 1\. Installation via NVM

Since your environment uses `nvm` for Node.js management, you should
avoid `sudo` for global installations. This ensures the CLI is tied to
your user-level Node version, preventing permission conflicts with
Ubuntu's system packages.

```bash
npm install -g @anthropic-ai/claude-code
```

### 2\. Authentication and Zero-Cost Options

Claude Code primarily operates via the Anthropic API. Unlike the
web-based Claude.ai, it does not currently offer a strictly
"free-forever" tier for CLI usage. However, there are two paths for
*evaluation without immediate cost*:

- **Initial Credits:** New Anthropic Console accounts typically
  receive a small amount of *free trial credits* (often $5) upon phone
  verification. This is the standard "zero-cost" entry point for
  researchers testing the tool. [ag-1]

- **Trial Limits:** Anthropic occasionally offers limited-time "Free
  Tier" access for Claude Code during its beta/early-access phases,
  though this is subject to strict rate limits and may be revoked in
  favor of the credit-based model.

To authenticate, run:

```bash
claude auth login
```

This will open a browser window to link your Anthropic Console account.

### 3\. Installation Verification

To confirm the CLI is correctly mapped in your `$PATH` and can
communicate with the backend, check the version and current session
status.

```bash
claude --version
```

### 4\. Worked Interaction Example

In your `uv`-managed Python project, Claude Code can be used to
automate linting and testing. Because Claude Code is *agentic*, it
doesn't just suggest code; it can execute commands in your terminal to
verify its work.

#### Interaction Scenario

```bash
claude "Run the test suite and fix any failures found by Ruff."
```

Claude will then:

- Execute `uv run ruff check --fix` to resolve linting issues.
- Execute `uv run pytest` to check for regressions.
- Analyze the output, modify files if tests fail, and re-run until the state is clean.

### 5\. Project Context via CLAUDE.md

Claude Code automatically looks for a `.claude/CLAUDE.md` file in your project root.

This file acts as the "system prompt" for the agent. In your setup, this file serves as a bridge:

- It uses the `@AGENTS.md` directive to pull in shared departmental instructions.
- It defines project-specific rules (e.g., "Always use `uv run` for Python scripts").

By importing `.agents/AGENTS.md`, you ensure that Claude Code follows the same organizational standards
as your Gemini CLI and VS Code configurations without maintaining duplicate instruction sets.


## Shared Skills Recognition

Claude Code does not have a proprietary "plugin" format for skills.
Instead, it relies on its ability to _explore the filesystem_ and
follow instructions provided in `CLAUDE.md`.

### Recognition of `.agents/skills/`

To make the `gemini-cli` compatible skills reusable for Claude Code, no complex configuration is required.
You simply need to inform Claude of their existence and purpose within the `.claude/CLAUDE.md` file.

```markdown
### Shared Skills
The directory `.agents/skills/` contains executable scripts and utilities.
When tasked with complex data transformations or ML tasks:
- Search `.agents/skills/` for relevant logic before authoring new scripts.
- Execute scripts using the appropriate runner (e.g., `python`, `Rscript`, or `julia`).
```

### Configuration Requirements

No additional binary configuration is needed in the `.claude/` directory.

Claude Code’s _read\_file_ and _list\_files_ tools allow it to
discover these skills dynamically.

By referencing the directory in your project instructions, you ensure
the agent prioritizes using these pre-authored "agent tools" over
writing ad-hoc code, preserving the multi-agent logic shared with your
Google/Cursor tools. [rf-2]

---

## References

- [ag-1] _Anthropic Console Billing and Credits:_ [https://console.anthropic.com/](https://console.anthropic.com/)
- [ag-2] _Claude Code Documentation and System Prompts:_ [https://docs.anthropic.com/en/docs/agents-and-tools/claude-code](https://www.google.com/search?q=https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [ag-3] _Ubuntu 24.04 LTS (Noble Numbat) Release Notes:_ [https://discourse.ubuntu.com/t/noble-numbat-release-notes/44043](https://www.google.com/search?q=https://discourse.ubuntu.com/t/noble-numbat-release-notes/44043)

---

## Additional Notes

### CUDA and Resource Awareness

Since your department focuses on CUDA-enabled projects, it is highly
recommended to add a note in `.agents/AGENTS.md` regarding GPU
visibility. If Claude attempts to run a script that consumes all VRAM
on a shared workstation, it could disrupt other researchers. Instruct
the agents to use `nvidia-smi` to check availability before running
heavy ML tests.

### Shell Permissions

On Ubuntu 24.04, ensure that scripts within `.agents/skills/` have the executable bit set (`chmod +x`).

While Claude can attempt to change permissions, it is more reliable to
have them pre-configured so the agent can execute them immediately.




# A:1 (ChatGPT)

[^](#toc) **_Claude Code Quick Start Guide_**

> Claude Code Quick Start Guide (Ubuntu 24.04, Academic ML Environment)

## Overview

This guide provides a minimal, reproducible setup for evaluating _Claude Code CLI_ in a Linux-based research environment. It assumes:

- User-level Node.js via `nvm`
- Python tooling via `uv`
- Existing multi-agent configuration under `.agents/` and `.claude/`

---

## 1. Install Claude Code CLI via `nvm` + `npm`

### Ensure `nvm` and Node.js are available

```bash
nvm install --lts
nvm use --lts
node -v
npm -v
```

### Install Claude Code CLI globally

> **Note**: Package name may evolve; verify via official docs.

```bash
npm install -g @anthropic-ai/claude-code
```

### Verify binary is in PATH

```bash
which claude
claude --version
```

---

## 2. Authentication and Model Configuration

### Available Access Modes

#### A. Free Tier (Recommended for Evaluation)

- Requires Anthropic account
- Limited quota (requests/day, token caps)
- Typically defaults to a _Sonnet-class model_

```bash
claude login
```

This opens a browser-based authentication flow.

---

#### B. API Key (More Control)

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

Optional persistent setup:

```bash
echo 'export ANTHROPIC_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

---

#### C. Zero-Cost / Unauthenticated Mode

- _Not generally available_ in official CLI
- Some environments may expose:

  - Proxy endpoints
  - Institutional gateways

> **Conclusion**: For most users, the **free tier login is the only zero-cost path**.

---

### Model Selection

Default model is usually sufficient, but can be overridden:

```bash
claude config set model claude-sonnet
```

---

## 3. Verify Installation

Run a simple prompt:

```bash
claude "Explain what this repository does"
```

Or inside a project:

```bash
claude
```

Expected behavior:

- CLI opens interactive session
- Context inferred from current directory

---

## 4. Worked Example (Python Project with `uv`)

### Assumptions

- Project uses:

  - `uv run pytest`
  - `uv run ruff`

- Standards defined in `.agents/AGENTS.md`

---

### Example Interaction

```bash
cd your-project/
claude
```

Then prompt:

```text
Run linting and tests, summarize failures, and suggest fixes.
```

Claude Code will:

- Inspect repository structure
- Execute or simulate:

  - `uv run ruff`
  - `uv run pytest`

- Provide:

  - Error summaries
  - Suggested patches
  - Refactoring hints

---

### More Targeted Prompt

```text
Fix all ruff violations and ensure pytest passes. Show diffs before applying.
```

---

### Non-Interactive Mode

```bash
claude "Run uv run pytest and explain failures"
```

---

## 5. Project Context Integration

### `.claude/CLAUDE.md`

- Entry point for Claude-specific instructions
- Automatically loaded by Claude Code
- Can include:

```markdown
@AGENTS.md
```

---

### `.agents/AGENTS.md`

- Shared, tool-agnostic instructions
- Defines:

  - Build commands (`uv run pytest`, `uv run ruff`)
  - Coding standards
  - Project conventions

---

### Interaction Model

```text
Claude Code
  └── loads .claude/CLAUDE.md
        └── imports .agents/AGENTS.md
```

This ensures:

- _Single source of truth_
- No duplication across tools (Claude, Gemini, Cursor)

---

## Secondary Objective: Skills Reuse

### `.agents/skills/` Compatibility

Claude Code does **not natively enforce a “skills directory” convention**, but:

- It _can access any files in the repo_
- Skills become usable if:

  - Referenced in `.claude/CLAUDE.md`
  - Or discoverable via prompting

---

### Recommended Pattern

Inside `.claude/CLAUDE.md`:

```markdown
## Available Skills

Skills are defined under `.agents/skills/`.

When relevant, load and apply them automatically.
```

---

### Optional Explicit Index

Create:

```text
.agents/skills/index.md
```

And reference it:

```markdown
@../agents/skills/index.md
```

---

### Do You Need Extra `.claude/` Configuration?

- ❌ No mandatory configuration required
- ✅ Recommended:

  - Explicit references to skills
  - Clear usage instructions

---

### Cross-Tool Interoperability

Because:

- Gemini CLI
- Claude Code
- Cursor

_all read plain files_:

➡ Skills are **fully reusable without modification**

---

## Additional Notes

- Claude Code operates best when:

  - Commands are explicitly defined (as in your `AGENTS.md`)
  - Repository structure is clean and conventional

- For CUDA/ML environments:

  - Avoid implicit execution of GPU-heavy workloads
  - Prefer prompts like:

```text
Analyze without running GPU-intensive code unless explicitly requested.
```

- For academic environments:

  - Consider adding:

    - Reproducibility constraints
    - Citation or docstring requirements

---

## References

- [at-1] Anthropic Claude Code Documentation
- [at-2] Anthropic API Keys and Authentication
- [at-3] Node Version Manager (nvm)
- [at-4] uv Python Package Manager Documentation


# A:1 (Perplexity)

[^](#toc) **_Claude Code CLI - Quick Start Guide_**

## 1. Installation of Claude Code CLI via `nvm`‑managed `npm`

On Ubuntu 24.04 with a user‑level `nvm`/`npm` setup,
install the Claude Code CLI globally under your user prefix (no `sudo`):

```bash
npm install -g @anthropic-ai/claude-code
```

This adds the `claude` binary to your `npm` global‑bin directory,
typically under `~/.npm-global/bin` or a similar `nvm`‑managed path,
and keeps ownership in your user space. [ssdnodes](https://www.ssdnodes.com/blog/install-claude-code-on-ubuntu-linux/)

Add the `npm` global‑bin directory to your `PATH` if it is not already present in your shell startup file:

```bash
# For bash
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```


## 2. Authentication and model configuration for zero‑cost trial use

Claude Code currently always requires at least an API key or OAuth‑based login to the Anthropic platform,
even in free‑tier usage; there is no fully unauthenticated “anonymous” Sonnet endpoint. [github](https://github.com/dvcrn/anthropic-cli/blob/main/README.md)

To target zero‑cost or trial‑eligible usage:

- Obtain an **Anthropic API key** from your account at [https://console.anthropic.com](https://console.anthropic.com), making sure you are on a **free or trial plan**.
- Set the key in your environment:

  ```bash
  export ANTHROPIC_API_KEY="your-key-here"
  echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
  ```

or, more securely, place it in a shell‑specific file (e.g., `~/.bash_profile`)
and source it in your login shell. [github](https://github.com/dvcrn/anthropic-cli/blob/main/README.md)

Claude Code reads `ANTHROPIC_API_KEY` automatically;
no extra CLI‑side configuration is needed for model selection beyond what your account tier allows. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)

If you are on a **free tier**, the available model is typically **Claude Sonnet**
(or whichever default you are granted); you do not need to hardcode a model name in the CLI unless you explicitly want to pin it. [github](https://github.com/dvcrn/anthropic-cli/blob/main/README.md)


## 3. Verification of the installation with a simple shell command

Verify that the Claude Code CLI is installed and can reach the Anthropic API:

```bash
claude --version
```

You should see a version string (e.g., `claude 0.x.x`), confirming the binary is reachable under your `npm`‑managed `PATH`. [linux.how2shout](https://linux.how2shout.com/how-to-install-claude-code-ubuntu-linux/)

Then test connectivity with a short prompt:

```bash
claude ask "Explain in 2 sentences what a CUDA‑enabled Python ML project is."
```

If you receive a coherent answer, the CLI and your API key are correctly configured. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)


## 4. Worked interaction example using an existing Python project

Assume a project layout under `src/` and `tests/pytest/`, with `uv run pytest` and `uv run ruff` as the standard commands defined in `.agents/AGENTS.md`. [nipunbatra.github](https://nipunbatra.github.io/blog/posts/2025-01-15-setup-linux-remote.html)

Start a Claude Code session in the project root:

```bash
claude chat
```

Then paste a sample interaction sequence (typed into the chat prompt):

- Ask Claude Code to write a new test for a module:

  ```text
  In the project under ./src/mymodule/, add a unit test for the function `train_model()` in `src/mymodule/training.py`.
  Use the existing pytest structure in ./tests/pytest/mymodule/.
  After writing the test, run `uv run pytest ./tests/pytest/mymodule/test_training.py -xvs` to verify it.
  ```

- Ask it to run linting and apply fixes:

  ```text
  Run `uv run ruff check --fix src/mymodule/training.py` and explain any changes it made.
  ```

Claude Code will emit the relevant commands and suggested edits;
you can then run them in a separate shell or allow execution
if your project’s `.claude/CLAUDE.md` explicitly pre‑approves `uv run ruff` and `uv run pytest`. [ssdnodes](https://www.ssdnodes.com/blog/install-claude-code-on-ubuntu-linux/)


## 5. How `.claude/CLAUDE.md` and `.agents/AGENTS.md` are used together

Claude Code loads project‑level context via:

- A `.claude/CLAUDE.md` file at the project root, which defines Claude‑specific rules, scope, and permissions. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)
- An `@AGENTS.md`‑style directive in `.claude/CLAUDE.md` that includes the contents of `.agents/AGENTS.md` into the session context. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)

A typical `.claude/CLAUDE.md` fragment looks like:

```markdown
# Claude Code Project Context (CLAUDE.md)

@AGENTS.md  <-- This imports all shared team standards

## 🤖 Claude‑Specific Instructions

- When the session fills up, keep `src/*/scripts/` definitions in the context window.
- Use a `code-reviewer` subagent for changes touching the `src/auth/` directory.
```

This mechanism ensures that Claude inherits:

- Tooling paths (`uv`, `npm`, `jlpm`, etc.)
- Command aliases (`uv run pytest`, `uv run ruff`, etc.)
- Project scopes and boundaries

from `.agents/AGENTS.md`, while keeping Claude‑specific rules and agent‑workflow logic in `.claude/CLAUDE.md`. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)


## How `.agents/skills/` integrates with Claude Code

The `.agents/skills/` directory is treated as a vendor‑neutral, **tool‑agnostic** skills library;
each agent tool (Claude Code, Gemini CLI, Cursor, etc.) can be configured to scan and load skills from this path. [avinashsangle](https://avinashsangle.com/blog/ant-cli-getting-started)

Claude Code uses the following mechanisms:

- Project‑wide or per‑session settings (e.g., `~/.claude/settings.json` or `.claude/settings.json`) can declare a **skills base path**. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)
- In your setup, explicitly point Claude to the shared skills directory:

  ```json
  {
    "skills_path": "./.agents/skills"
  }
  ```

placed in `.claude/settings.json` (or a project‑specific settings file)
so that Claude Code can discover and load skills such as `python-code-style/SKILL.md`, `python-testing-patterns/SKILL.md`, etc., without duplication. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)

Because these skills are expressed in plain Markdown with tool‑agnostic instructions, skills authored for Gemini CLI can be reused by Claude Code as long as:

- Skill names are unique across the directory.
- Skill content does not hardcode Gemini‑specific CLI flags or commands. [avinashsangle](https://avinashsangle.com/blog/ant-cli-getting-started)


## References

- `ap-1: How to Install Claude Code on Ubuntu Linux` – step‑by‑step guide covering Ubuntu 20.04+ including 24.04, with `npm install -g @anthropic-ai/claude-code` and global‑bin‑path configuration. [linux.how2shout](https://linux.how2shout.com/how-to-install-claude-code-ubuntu-linux/)
- `ap-2: anthropic‑cli GitHub repository` – reference for environment variables such as `ANTHROPIC_API_KEY` and basic CLI usage. [github](https://github.com/dvcrn/anthropic-cli/blob/main/README.md)
- `ap-3: Claude Code settings files layout` – documentation of paths such as `~/.claude/settings.json`, `.claude/settings.json`, and `.claude.json` and their role in model and skills configuration. [linuxcapable](https://linuxcapable.com/how-to-install-claude-code-on-ubuntu-linux/)

---

## Additional Notes

- Anthropic’s **free/trial tiers** typically grant access to **Claude Sonnet** (or a similar default model) with rate‑limited usage;
  more powerful models (e.g., Opus) and higher throughput tiers are usually **paid‑only**.
  Always check the current [https://console.anthropic.com](https://console.anthropic.com) pricing page
  and confirm your plan type before scaling up usage in an academic setting. [github](https://github.com/dvcrn/anthropic-cli/blob/main/README.md)
- For GPU‑accelerated Python/R/Julia projects, rely on `uv`‑managed CUDA‑compatible environments
  (e.g., CUDA‑enabled PyTorch from appropriate index URLs) rather than assuming the CLI will handle GPU setup;
  Claude Code is a _code‑assistant CLI_, not a CUDA‑environment manager. [lobehub](https://lobehub.com/skills/nblog-video2doc-uv-cuda-setup)







# A:1 (DeepSeek)

[^](#toc) **_Claude Code Quick Start Guide_**

## Claude Code Quick Start Guide for Ubuntu 24.04 (Academic Evaluation)

This guide walks you through installing and testing **Claude Code** –
Anthropic’s terminal‑based coding assistant – on your existing
multi‑agent project template. The focus is on _zero‑cost trial use_
using free API credits, with full reuse of your shared
`.agents/skills/`.

---

### Prerequisites

- Ubuntu 24.04 with `nvm` (Node Version Manager) already configured for your user account.
- `npm` available via the active `nvm` Node.js version (v20 or later recommended).
- Your project template checked out, containing:
  - `.claude/CLAUDE.md` (imports `@AGENTS.md`)
  - `.agents/AGENTS.md` and `.agents/skills/`
  - `pyproject.toml` with `uv` lock files
- Internet access to download npm packages and call Anthropic’s API.

---

### Step 1 – Install Claude Code CLI

Use `npm` from your `nvm`‑managed Node.js environment.

Installing globally inside the user’s `nvm` prefix avoids permission errors.

```bash
# Ensure you are using the correct Node version
nvm use --lts

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code
```

Verify the installation:

```bash
claude --version
```

Expected output: a version string (e.g., `0.1.0`).

If `claude` is not found, confirm that `npm`’s global bin directory (`~/.nvm/versions/node/.../bin`) is in your `PATH`.

---

### Step 2 – Authentication & Free Trial Configuration

Claude Code requires an **Anthropic API key**.

New accounts receive _free trial credits_ (typically $5, valid for 3 months).
No ongoing charge if you stay within credits.

1. Go to [Anthropic Console](https://console.anthropic.com/) and sign up / log in.
2. Navigate to **API Keys** → **Create Key**.
3. Copy the generated key (starts with `sk-ant-...`).
4. Set it as an environment variable in your terminal:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

To make this permanent, add the export line to your `~/.bashrc` or `~/.zshrc`.

> **Note:** A credit card is required to activate the free trial, but you will _not_ be charged unless you exceed the trial credits or upgrade.

**Model selection** – By default Claude Code uses `claude-3-5-sonnet-latest`.
To stay within trial credits, you can switch to the cheaper `claude-3-haiku-latest`:

```bash
claude --model claude-3-haiku-latest
```

Haiku is significantly less expensive per token and is suitable for many code tasks.

---

### Step 3 – Verification

Run a simple command to confirm authentication and API connectivity:

```bash
claude evaluate "What is the current working directory?" --print
```

If successful, you will see a text response (e.g., the absolute path of your project).
Any authentication error indicates an invalid or expired API key.

---

### Step 4 – Worked Interaction Example (Python Project)

Assume you are inside your project root.
Use the standard commands defined in `.agents/AGENTS.md` – all prefixed with `uv run`.

**Example prompt to Claude Code:**

```bash
claude "Run the unit tests for the src/ directory using uv run pytest. Show me only the failing tests, if any."
```

Claude Code will execute the command (subject to permission prompts) and return the output.
Because your `.claude/CLAUDE.md` imports `@AGENTS.md`, the assistant already knows that `pytest` must be called via `uv run`.

**A second example – code linting:**

```bash
claude "Run ruff check on the src/ directory and fix any auto‑fixable issues."
```

Claude Code will invoke `uv run ruff check --fix src/` and summarise the changes.

**Important:** By default Claude Code asks for permission before running shell commands.

You can pre‑approve safe commands by adding them to the `permissions` section in `.claude/CLAUDE.md` (see the provided example).

---

### Step 5 – How Context Files Work Together

Claude Code loads project context from `.claude/CLAUDE.md`. Your existing file contains:

```markdown
@AGENTS.md   <-- This imports all shared team standards
```

The `@AGENTS.md` directive instructs Claude Code to read and merge the
contents of `.agents/AGENTS.md` as if they were part of
`CLAUDE.md`. This gives Claude Code access to:

- Environment rules (always use `uv run` for Python commands)
- Command table (testing, linting, formatting)
- Project scopes and boundaries

No duplication of rules across tools – Antigravity, Cursor, and Copilot can also read `.agents/AGENTS.md`
(each tool has its own way of including it). For Claude Code, the single `@AGENTS.md` line is sufficient.

---

### Secondary Objective – Reusing `.agents/skills/` Without Duplication

Your project stores shared skills under `.agents/skills/`.
Each skill is a directory containing a `SKILL.md` file with instructions, triggers, and examples.

**Does Claude Code recognise this directory automatically?**

No – Claude Code does _not_ scan arbitrary folders for skills.
Instead, you must reference skills inside your context files (`.claude/CLAUDE.md` or imported `.agents/AGENTS.md`).

Because `.agents/AGENTS.md` already contains a **Skills** table listing each skill and its triggers (as shown in your prompt),
Claude Code will see that table and understand when to load a skill. The table is plain Markdown – no special syntax required.

**Example from your `AGENTS.md`:**

```markdown
| Skill                  | Triggers                                                                |
|------------------------|-------------------------------------------------------------------------|
| `vce-project-layout`   | navigating source tree, locating files, understanding directory roles   |
| `python-code-style`    | writing, editing, or reviewing Python code                              |
```

Claude Code reads this and, when a user prompt matches a trigger (e.g., “where should I put new R scripts?”),
it will follow the guidance described in the corresponding `SKILL.md` file –
provided that `SKILL.md` is mentioned elsewhere or the assistant infers its location.
For maximum clarity, you can add explicit instructions in `AGENTS.md`:

```markdown
For detailed instructions on a skill, read `.agents/skills/<skill-name>/SKILL.md`.
```

**No extra `.claude/` configuration is required** – the import of `AGENTS.md` already brings the skill table into Claude Code’s context.

---

### References

- [ad-1] Anthropic Console – API Keys: [https://console.anthropic.com/](https://console.anthropic.com/)
- [ad-2] Claude Code npm package: [https://www.npmjs.com/package/@anthropic-ai/claude-code](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [ad-3] Anthropic Pricing (includes free trial details): [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing)
- [ad-4] `uv` documentation: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- [ad-5] Claude Code permissions and `CLAUDE.md` format: [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)

---

### Additional Notes

- **Trial credit expiry** – Free credits typically expire 3 months after account creation. Monitor usage via the Anthropic Console.
- **No local offline mode** – Claude Code requires an active internet connection to call the API.
- **CUDA/ML projects** – Claude Code can help write and debug CUDA kernels, but it cannot execute GPU code directly. Use the terminal commands (e.g., `nvcc`, `python -c "import torch; print(torch.cuda.is_available())"`) through Claude Code’s shell integration.
- **GitLab Duo Ultimate** – Not directly integrated with Claude Code. The two tools operate independently; you can use Claude Code for local development and GitLab Duo for CI/CD pipelines.
- **Student access** – Anthropic does not currently offer a free educational tier, but the $5 trial credits are sufficient for several weeks of light usage (e.g., 1–2 million tokens). For heavy departmental use, consider requesting research credits via [Anthropic for Research](https://www.anthropic.com/research).






<!-- }}} \\ %1. -->
<!-- ::{{{ #TAG: TODO:(q2-section) // -->

# Q:2

## Q:2 - **Anthropic Product Offering Comparison for Academic Uses**

[^](#toc)

## Role

You are an expert in developer tooling, AI coding assistants, CLI setup,
and Anthropic product strategy, with hands-on knowledge of Claude Code
deployment in academic Linux environments.

## Task

Produce a structured technical document covering the deliverable.
Use Chain-of-Thought reasoning within each section
before producing the final output for that section.

---

## Context

### Environment

- Organisation type: Academic Statistics Department
- Project Template setup for different users (researchers/students)
- Final user will decide what kind of product ("Clause Code" or "Google Gemini")
  and which level of offer to apply (Free/Paid).

### Multi-Agent Project Template

The project template supports the following AI coding tools simultaneously:

- _Claude Code_ (Anthropic CLI) - **mandatory**
- _Gemini CLI_ (Google) - **mandatory**
- _Cursor_ - **mandatory**
- _VS Code Copilot_ - _optional_
- _GitLab Duo_ (planned, organisation-level Ultimate tier)

## Deliverable — Anthropic Product Offering Comparison

Produce a comparison table covering the following Anthropic access options,
evaluated against criteria relevant to an academic organisation:

- _Evaluation criteria_: cost per month, free tier availability,
  model access (Haiku / Sonnet / Opus), context window, rate limits,
  API key required, team/organisation support, data privacy policy
- _Options to compare_:
  - Claude.ai Free
  - Claude.ai Pro
  - Claude.ai Team
  - Claude.ai Enterprise
  - Anthropic API (pay-as-you-go)
  - Claude Code (as a separate product layer on top of the above)

After the table, provide a _recommended path_ for an academic department
that wants to run a zero-cost proof-of-concept before committing to
any paid tier.

---

## Output Format

Reply in GitLab Flavored Markdown (GLFM) with precise lint compliance:

- Codeblock delimiters ` ``` ` placed at line start; no nested codeblocks
- _Underscore markup_ for emphasis
- Nested headings preferred over bold inline text
- Only dash (`-`) for unordered lists, correct indentation
- Blank line after every heading, list block, and codeblock

Provide a _References_ section as Markdown footnotes prefixed `rf-`,
linked inline where cited in the text.

Add an _Additional Notes_ section at the end for supplementary
information not explicitly requested.


# A:2 (Claude)

[^](#toc) **_Anthropic Product Offering Comparison_**

_Prepared for: Academic Statistics Department — Multi-Agent Project Template_
_Date: 2026-04-21_

---

## Table of Contents

- [Comparison Table](#comparison-table)
- [Claude Code as a Product Layer](#claude-code-as-a-product-layer)
- [Recommended Path for a Zero-Cost Proof of Concept](#recommended-path-for-a-zero-cost-proof-of-concept)
- [References](#references)
- [Additional Notes](#additional-notes)

---

## Comparison Table

The table below evaluates each Anthropic access option against the criteria relevant to an academic statistics department.[^bc-1][^bc-2][^bc-3][^bc-4]

Abbreviations used: _n/a_ = not applicable; _TBC_ = to be confirmed with Anthropic sales; _MTok_ = million tokens.

| Criterion                          | Claude.ai Free                                                     | Claude.ai Pro                                                                                   | Claude.ai Team                                                              | Claude.ai Enterprise                                                                                  | Anthropic API (PAYG)                                                                                     |
|------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **Cost / month**                   | $0                                                                 | $20 (or ~$17 billed annually)                                                                   | $30/seat monthly ($25 billed annually; min. 5 seats)                        | Custom — community reports ~$60/seat, 70-seat minimum, annual contract[^bc-4]                         | $0 base; usage billed per token (see below)                                                              |
| **Free tier**                      | Yes — permanent, no credit card required[^bc-2]                    | No                                                                                              | No                                                                          | No                                                                                                    | ~$5 free credits for new API accounts[^bc-3]                                                             |
| **Model access — Haiku**           | Limited / throttled                                                | Yes (Haiku 4.5: $1/MTok input)                                                                  | Yes                                                                         | Yes                                                                                                   | Yes — Haiku 4.5 at $1/$5 MTok in/out[^bc-1]                                                              |
| **Model access — Sonnet**          | Yes (throttled; Sonnet 4.6 available in chat)                      | Yes                                                                                             | Yes                                                                         | Yes                                                                                                   | Yes — Sonnet 4.6 at $3/$15 MTok in/out[^bc-1]                                                            |
| **Model access — Opus**            | No                                                                 | Yes (Opus 4.6/4.7)                                                                              | Yes                                                                         | Yes                                                                                                   | Yes — Opus 4.7 at $5/$25 MTok in/out[^bc-1]                                                              |
| **Context window**                 | 200K tokens (standard)                                             | 200K tokens                                                                                     | 200K tokens                                                                 | 500K tokens (Enterprise-tier)[^bc-4]                                                                  | 200K standard; up to 1M tokens (beta, Tier 4+ orgs)[^bc-5]                                               |
| **Rate limits**                    | Low; throttled during peak; rolling reset every few hours[^bc-2]   | Moderate (~45 prompts/session before throttling, ~5-hour reset; user-reported)[^bc-6]           | Higher than Pro; 100K–150K TPM per user recommended for 5–20 users[^bc-3]   | Negotiable; organisation-level controls                                                               | Tiered by usage level; raises with spend; custom limits via sales[^bc-1]                                 |
| **API key required**               | No                                                                 | No                                                                                              | No                                                                          | No                                                                                                    | Yes — mandatory[^bc-1]                                                                                   |
| **Team / org support**             | No                                                                 | No                                                                                              | Yes — centralised billing, shared Projects, admin dashboard, domain capture | Yes — SSO, SCIM, RBAC, audit logs, IP allowlisting, HIPAA-ready option[^bc-4]                         | Partial — via Console organisation features; no built-in team UI                                         |
| **Data privacy policy**            | Standard; users may opt out of training in Privacy Settings[^bc-7] | Standard; opt-out available[^bc-7]                                                              | No training on data by default (contractual)[^bc-7]                         | No training by default; custom retention; compliance API; data residency options[^bc-7]               | No training on API data by default; data residency at 1.1× price on AWS/Vertex regional endpoints[^bc-1] |
| **Academic / education programme** | Available to all individuals, no institution required[^bc-8]       | No dedicated student discount; institution partnerships grant free Pro to enrolled users[^bc-8] | Applicable if department has ≥5 seats                                       | University-wide Education Plan available via Anthropic sales (covers students, faculty, staff)[^bc-8] | Research Credit programme available for academic projects (apply via institution IT)[^bc-8]              |

---

## Claude Code as a Product Layer

Claude Code is _not_ a standalone subscription. It is a CLI tool that
runs in your terminal, connects to Anthropic's model APIs, and is
billed through your existing Claude plan or API account. The
implications for the multi-agent project template are as follows.

### Availability by underlying plan

Claude Code is included with Claude Pro ($20/month), Max (from
$100/month), Team, and Enterprise paid plans.

The free Claude plan only gives you access to chat on web, iOS,
Android, and desktop — the terminal-based Claude Code environment is
not included. However, new API users receive approximately $5 in free
credits to test the service, which is enough for a few hours of Claude
Code usage with the Sonnet model.

### Cost model

Claude Code's official documentation reports that enterprise and API
deployments vary widely, with average spend around $13 per developer
per active day and $150–250 per developer per month, while 90% of
users remain below $30 per active day.

### Team-specific considerations

For rate limit planning, Anthropic's official documentation provides
token-per-minute (TPM) recommendations by team size. A team of 5 to 20
users should plan for 100,000 to 150,000 TPM per user, while larger
teams of 50 to 100 users need only 25,000 to 35,000 TPM per user
because concurrent usage drops as team size grows. For an academic
department with variable, non-simultaneous usage patterns (researchers
and students working at different hours), effective per-user
consumption is typically lower than peak numbers suggest.

### Token cost reference (API route, as of April 2026)[^bc-1]

The following prices apply when running Claude Code via the Anthropic API (pay-as-you-go):

| Model             | Input ($/MTok) | Output ($/MTok) | Notes                                                                       |
|-------------------|----------------|-----------------|-----------------------------------------------------------------------------|
| Claude Haiku 4.5  | $1.00          | $5.00           | Fastest; suitable for lightweight agentic steps                             |
| Claude Sonnet 4.6 | $3.00          | $15.00          | Default cost-performance choice for Claude Code                             |
| Claude Opus 4.7   | $5.00          | $25.00          | Highest reasoning; uses new tokenizer (up to 35% more tokens for same text) |

Prompt caching reduces effective input cost to 10% of the standard
rate for cached content. Batch API processing offers a 50% discount
over standard pricing. Both discounts may be combined.[^bc-1]

---

## Recommended Path for a Zero-Cost Proof of Concept

The following phased approach allows the department to validate the
multi-agent template against real workloads before committing to any
paid tier. All steps are zero-cost or near-zero-cost.

### Phase 0 — Individual baseline (week 1–2)

Each participating researcher or student creates a personal _Claude.ai
Free_ account. This grants access to Claude Sonnet 4.6 in the browser
interface with rolling usage limits. In February 2026, Anthropic
significantly expanded the free tier's offerings — Projects,
Artifacts, and app connectors are now available to free users, which
has blurred the line between Free and Pro more than ever. Use this
phase to validate prompt strategies, context sizes, and task
suitability.

_Limitation:_ Claude Code (terminal agent) is not available on the Free plan. Browser chat only.

### Phase 1 — API free credits for Claude Code (week 2–3)

Each developer on the template team creates an Anthropic Console
account and uses the ~$5 in free API credits to run short Claude Code
sessions in the terminal. Use Sonnet 4.6 as the default model to
maximise credit duration. Enable prompt caching from the first session
to extend the credit further.

_Scope:_ Enough to complete several hours of agentic coding across the multi-agent project structure.

### Phase 2 — Education programme enquiry (parallel to Phase 1)

Contact Anthropic via the Education sales channel to enquire about the
_Claude for Education_ university-wide plan. Verified partner
institutions provide students with managed accounts featuring higher
limits and enhanced privacy. If the department's institution is not
yet a partner, the Student Research Credit programme is an alternative
route for individual academic projects. Known partner universities
include Northeastern University, London School of Economics (LSE),
Champlain College, University of San Francisco School of Law, and
Northumbria University. The list has been expanding throughout 2025
and 2026, according to Anthropic's education announcements.

### Phase 3 — Decision gate

After Phases 0–2, the department has enough empirical data to make one of the following choices:

- _Low-volume use:_ Remain on the API (pay-as-you-go) with Sonnet 4.6
  and prompt caching. At typical academic workloads (non-daily,
  variable), this is often cheaper than a flat subscription.
- _Regular individual use:_ Upgrade selected researchers to _Claude.ai
  Pro_ ($20/month) for included Claude Code access without token
  metering.
- _Team deployment:_ Adopt _Claude.ai Team_ (≥5 seats, $25/seat/month
  billed annually) for shared Projects, admin controls, and
  no-training-by-default data policy — important for research data.
- _Institution-wide:_ Pursue the _Claude for Education_ enterprise
  agreement to cover the whole department or institution under a
  single negotiated contract.

---

## References

[^bc-1]: [Anthropic API Pricing Documentation](https://platform.claude.com/docs/en/about-claude/pricing) (verified April 2026)
[^bc-2]: [Claude.ai Free tier details](https://claude.com/pricing) (verified April 2026)
[^bc-3]: [Claude Code Pricing Guide (LaoZhang AI Blog)](https://blog.laozhang.ai/en/posts/claude-code-pricing-guide) (April 2026)
[^bc-4]: [Claude Enterprise / Team plan details (Juma / Team-GPT)](https://juma.ai/blog/claude-pricing)
[^bc-5]: [Extended context window (1M token beta) — Anthropic API docs, rate limits section](https://platform.claude.com/docs/en/about-claude/pricing)
[^bc-6]: [Claude Free vs Pro usage limits (user-reported figures)](https://mem0.ai/blog/anthropic-claude-pricing) (February 2026)
[^bc-7]: [Anthropic data privacy and training policy](https://checkthat.ai/brands/anthropic/pricing) (April 2026); [_official policy_](https://www.anthropic.com/legal/privacy)
[^bc-8]: [Claude for Education and academic access](https://www.verdent.ai/guides/how-to-use-claude-ai-for-free-2026) [_Claude student discount_](https://k-antenna.com/claude-student-discount/)

---

## Additional Notes

### On the _Max_ plan family

Anthropic now offers _Claude Max_ as a tier above Pro for individual
power users — Max 5× at $100/month and Max 20× at $200/month. Claude
Max is not about adding new features. It is for users who rely on
Claude heavily and use it for long periods of time. For the academic
use case, Max is unlikely to be the right entry point: the Team plan
at $25/seat/month (annual) provides more organisational value for the
same or lower per-seat cost once five or more users are involved.

### On the tokenizer change for Opus 4.7

Opus 4.7 uses a new tokenizer compared to previous models. This new
tokenizer may use up to 35% more tokens for the same fixed
text. Budget calculations for agentic statistical workloads (long R or
Python scripts, large data dictionaries) should account for this when
selecting Opus 4.7 over Sonnet 4.6.

### On long-context pricing simplification

Anthropic eliminated long-context surcharges as of March 13, 2026. A
900K-token request now costs the same per-token rate as a 9K-token
request on Opus 4.7 and Sonnet 4.6. This is a material benefit for
statistical research workloads that involve large codebases,
simulation outputs, or lengthy document corpora.

### On data residency for EU/Italian compliance

The department is located in Italy and may be subject to GDPR
data-residency requirements. Regional endpoints on AWS Bedrock and
Google Vertex AI include a 10% premium over global endpoints for data
residency guarantees. EU-based teams evaluating the API route should
factor this overhead into cost projections, or confirm that
Anthropic's standard data processing agreements satisfy their DPO
requirements before proceeding.

### On Gemini CLI as a zero-cost Claude Code alternative for PoC

The closest free alternative to Claude Code is Google's Gemini CLI,
which offers 1,000 requests per day at no cost. Since the multi-agent
project template mandates Gemini CLI as a parallel tool, departments
can use the Gemini CLI allowance to complete initial agentic workflow
design and validation while deferring Claude Code costs until Phase 1
API credits are obtained. This extends the zero-cost window before any
spend is required.

### On Anthropic's open-source and startup programmes

Anthropic launched the Claude for Open Source programme in late
February 2026. The programme gives qualifying open source maintainers
six months of Claude Max 20× ($200/month value) completely free, with
up to 10,000 spots available and applications closing June
30, 2026. If the department maintains open-source statistical software
repositories on GitHub meeting the eligibility criteria (5,000+ stars
or 1M+ monthly NPM downloads), this programme offers substantial free
access that could cover the entire PoC period and beyond.




# A:2 (Gemini)

[^](#toc) **_Anthropic Product Offering Comparison_**


## Anthropic Product Offering Comparison

_Chain-of-Thought:_

The comparison must address the distinct needs of a statistics
department: large datasets (context window), reproducibility
(API/CLI), and data sensitivity (privacy). In 2026, the
differentiation between "subscription-based usage" (Claude.ai) and
"consumption-based usage" (API) is the primary pivot for
organizational planning.

| Criteria           | Claude Free             | Claude Pro            | Claude Team            | Claude Enterprise     | Anthropic API             |
|:-------------------|:------------------------|:----------------------|:-----------------------|:----------------------|:--------------------------|
| **Cost / Month**   | $0                      | $20 / user            | $30 / user (min 5)     | Custom / Volume       | Pay-as-you-go             |
| **Free Tier**      | Permanent               | No                    | No                     | No                    | ~$5 initial credit [bg-1] |
| **Model Access**   | Sonnet 4.5              | Opus 4.6 / Sonnet 4.6 | Opus 4.6 / Sonnet 4.6  | Opus 4.6 / Sonnet 4.6 | Full Suite [bg-2]         |
| **Context Window** | 200K tokens             | 1M tokens (beta)      | 1M tokens              | 1M+ tokens            | 1M tokens [bg-3]          |
| **Rate Limits**    | Low (~15-40/5h)         | High (5x Free)        | Maximum Pooled         | Custom                | Tier-based (TPM/RPM)      |
| **API Key Req.**   | No                      | No                    | No                     | No                    | **Yes**                   |
| **Team Support**   | None                    | Individual            | Admin Dashboard        | SSO / Audit Logs      | Org-level Billing         |
| **Data Privacy**   | Opt-out training [bg-4] | Opt-out training      | **No training** [bg-5] | **No training**       | **No training** (default) |

---

## The Claude Code Layer

_Chain-of-Thought:_

Claude Code is not a separate subscription tier but a specialized CLI
delivery agent. Its cost and availability depend entirely on the
underlying authentication method chosen by the user.

### Authentication and Billing Models

Claude Code operates as a terminal-based agent that orchestrates
complex file-system tasks. Within the department's Linux environment,
it can be configured in two ways:

- **Subscription-linked**: Users with a _Pro_ or _Team_ account can
  authenticate the CLI directly. Usage is "included" in their monthly
  subscription quota, making it ideal for students who prefer a fixed
  cost.
- **API-linked**: Users (or the department) provide an
  `ANTHROPIC_API_KEY`. Billing is strictly consumption-based
  (tokens). This is preferred for high-volume research automation or
  "agentic" workflows that would exceed subscription caps [bg-6].

### Tool Compatibility

In a multi-agent template, Claude Code serves as the "heavy lifter"
for repository-wide refactoring, while _Cursor_ and _Copilot_ handle
real-time IDE completion. Because Claude Code supports the Model
Context Protocol (MCP), it can directly query the department's local
SQL databases or R/Python documentation without manual copy-pasting.

---

## Recommended Zero-Cost Proof-of-Concept (POC)

_Chain-of-Thought:_

For an academic department, a POC must prove value without
administrative friction or budget approval. I will leverage the 2026
"New User" incentives.

### Phase 1: Individual Research Evaluation

Invite researchers to utilize the **Claude.ai Free Tier**.

- **Goal**: Test Sonnet 4.5 for summarizing statistical papers and drafting R/LaTeX code.
- **Action**: Use the "Projects" feature (limited on Free) to upload
  specific LaTeX templates for consistency.

### Phase 2: CLI and Agentic Testing

Utilize the **Anthropic API Free Credits**.

- **Goal**: Deploy _Claude Code_ in the department's Linux cluster.
- **Action**: New users claim the ~$5 credit at the Anthropic
  Console. This is sufficient to run 10–20 deep sessions of Claude
  Code to evaluate its ability to fix broken data pipelines or debug
  complex Stan/JAGS models [bg-1].

### Phase 3: Academic Discount Verification

Check for the **Anthropic Academic Program**.

- **Goal**: Secure long-term reduced rates.
- **Action**: Verify if the department's `.edu` domain qualifies for
  the 3-month Claude Pro trial or the "Claude for Open Source" grant
  (available to researchers maintaining public statistical libraries)
  [bg-7].

---

## References

- [bg-1] _Verdent Guides: How to Use Claude AI for Free (2026)_
- [bg-2] _Finout: Claude Pricing in 2026 for Organizations_
- [bg-3] _MindStudio: Flat-Rate Long-Context Pricing and 1M Windows_
- [bg-4] _Anthropic Privacy Center: Data Retention Policy (September 2025 Update)_
- [bg-5] _Anthropic Commercial Terms: Enterprise Data Protections_
- [bg-6] _Claude Code Docs: Managing Costs for Teams and API Users_
- [bg-7] _DataStudios: Claude Pricing and Plan Limits Guide (Academic Offers)_

---

## Additional Notes

### GitLab Duo Synergy

Since the organization is on the **Ultimate tier**, GitLab Duo will
provide a "base layer" of AI for all students at no additional cost
once deployed. Anthropic tools should be reserved for "Power Users"
(PhD students/Faculty) who require the superior reasoning capabilities
of Opus 4.6 for novel statistical proofs.

### Hardware Considerations

Claude Code and Gemini CLI are lightweight but require active network
egress from your Linux nodes. Ensure the department's firewall allows
HTTPS traffic to `api.anthropic.com` and
`generativelanguage.googleapis.com`.

### Data Privacy Alert

In a Statistics Department handling sensitive dataset samples,
strictly enforce the **opt-out of model training** in the `Settings >
Privacy` menu for any users on Free/Pro tiers, as these default to
training-enabled in the 2026 policy update.



# A:2 (ChatGPT)

[^](#toc) **_Anthropic Product Offering Comparison for Academic Environments_**


## 1. Evaluation Framework

### Internal reasoning (condensed)

- Academic environments prioritize _cost control_, _data governance_, and _flexibility_.
- Mixed user profiles (students vs researchers) require _tiered access_.
- CLI tooling (Claude Code) introduces an additional abstraction layer over base access models.
- API vs SaaS trade-offs hinge on _integration depth_ vs _operational overhead_.

### Final output

The following criteria are used to evaluate each offering:

- _Cost per month_
- _Free tier availability_
- _Model access_ (Haiku / Sonnet / Opus)
- _Context window_
- _Rate limits_
- _API key required_
- _Team/organisation support_
- _Data privacy policy_

---

## 2. Comparison Table

### Internal reasoning (condensed)

- Claude.ai tiers differ mainly in _usage limits_, _collaboration_, and _governance_.
- API access is the most flexible but requires engineering effort.
- Claude Code is not a standalone subscription; it depends on underlying access.
- Enterprise tiers primarily add _security_, _SSO_, and _compliance guarantees_.

### Final output

| Option                 | Cost / Month       | Free Tier | Model Access                      | Context Window                | Rate Limits             | API Key Required                 | Team Support         | Data Privacy                                |
|------------------------|--------------------|-----------|-----------------------------------|-------------------------------|-------------------------|----------------------------------|----------------------|---------------------------------------------|
| _Claude.ai Free_       | €0                 | Yes       | Haiku, limited Sonnet             | Medium (~200K tokens typical) | Strict                  | No                               | No                   | Standard (data may be used for improvement) |
| _Claude.ai Pro_        | ~€20               | No        | Sonnet, limited Opus              | Large (~200K+)                | Higher than Free        | No                               | No                   | Improved controls, limited training usage   |
| _Claude.ai Team_       | ~€25–30/user       | No        | Sonnet, Opus                      | Large                         | Shared pooled limits    | No                               | Yes                  | No training on customer data                |
| _Claude.ai Enterprise_ | Custom pricing     | No        | Full access (Haiku, Sonnet, Opus) | მაქ (highest available)       | მაღალი (enterprise SLA) | No                               | Advanced (SSO, RBAC) | मजबूत compliance, zero training              |
| _Anthropic API (PAYG)_ | Usage-based        | No        | All models                        | მაქ (model-dependent)         | მოქნილი (quota-based)   | Yes                              | Via org account      | No training by default                      |
| _Claude Code_          | Depends on backend | N/A       | Inherits from API / Claude.ai     | Inherits                      | Inherits                | Yes (API) / No (Claude.ai login) | Depends on backend   | Depends on backend                          |

---

## 3. Claude Code as a Product Layer

### Internal reasoning (condensed)

- Claude Code is a _developer interface_, not a billing unit.
- It can authenticate via:

  - Claude.ai session
  - API key (preferred in automation contexts)

- Academic deployment depends heavily on _reproducibility_ and _CLI automation_.

### Final output

_Claude Code_ should be understood as a **CLI orchestration layer** that:

- Wraps Anthropic models into developer workflows
- Enables:

  - Codebase-aware prompting
  - Multi-file editing
  - Automation via scripts

- Integrates with:

  - Local dev environments (e.g., Ubuntu + `nvm` + `uv`)
  - CI/CD pipelines (when API-backed)

Its capabilities depend entirely on the underlying access method:

- _Claude.ai-backed_: simpler onboarding, limited automation
- _API-backed_: full programmability, reproducibility, and scaling

---

## 4. Recommended Path for Academic Proof-of-Concept (PoC)

### Internal reasoning (condensed)

- Zero-cost constraint → must rely on free tiers initially
- Need to support:

  - Individual experimentation
  - Shared reproducible workflows

- Avoid premature API complexity unless necessary

### Final output

#### Phase 1 — فردي exploration (zero cost)

- Use:

  - _Claude.ai Free_
  - _Claude Code_ authenticated via Claude.ai session

- მიზანი:

  - Evaluate usability for:

    - Code generation
    - Statistical workflows
    - Documentation

#### Phase 2 — Structured team evaluation (still near-zero cost)

- Introduce:

  - Shared project templates
  - CLI standardization (Claude Code + Gemini CLI + Cursor)

- Optional:

  - API credits for advanced users





#### Phase 3 — Controlled API pilot

- Enable:

  - _Anthropic API (PAYG)_ with strict quotas

- Use cases:

  - Batch processing
  - Reproducible research pipelines
  - Integration with R / Python workflows

#### Phase 4 — Decision point

- Upgrade path based on findings:

  - If focus is _interactive usage_:

    - → _Claude.ai Team_

  - If focus is _automation / pipelines_:

    - → _Anthropic API_

  - If compliance required:

    - → _Claude.ai Enterprise_

---

## 5. References

- [bt-1] Anthropic official pricing and plans documentation
- [bt-2] Anthropic API platform documentation
- [bt-3] Claude Code CLI documentation and release notes

---

## 6. Additional Notes

- _Gemini CLI_ should be evaluated in parallel for vendor neutrality.
- _Cursor_ provides strong IDE-native augmentation but lacks CLI parity with Claude Code.
- For academic reproducibility:

  - Prefer _API-backed workflows_ over SaaS UI interactions.

- Data governance is a critical differentiator:

  - Free tiers may not meet institutional requirements.

- Hybrid model likely optimal:

  - Free tier for students
  - API / Team tier for researchers and staff




# A:2 (Perplexity)

[^](#toc) **_Anthropic product offering comparison for academic use_**

This document compares major Anthropic access options against criteria
relevant to an academic statistics department running a multi‑agent
project template (Claude Code, Gemini CLI, Cursor, VS Code Copilot,
GitLab Duo).

- _Claude.ai Free_
- _Claude.ai Pro_
- _Claude.ai Team_
- _Claude.ai Enterprise_
- _Anthropic API (pay‑as‑you‑go)_
- _Claude Code_ (CLI layer on top of the above)

All references are based on Anthropic’s 2026‑era pricing and policies
as of April 2026. [juma](https://juma.ai/blog/claude-pricing)

## Evaluation criteria

For each row in the table, the following criteria are evaluated:

- _Cost per month_: ongoing financial commitment per user or org.
- _Free tier available_: yes/no and what is included.
- _Model access_: which Claude models (Haiku / Sonnet / Opus) are available.
- _Context window_: maximum context length offered.
- _Rate limits_: per‑user or per‑org usage caps and throttling behavior.
- _API key required_: whether the product is driven by an API key or OAuth‑style login.
- _Team/organisation support_: SSO, SCIM, audit logs, or similar org‑scale controls.
- _Data privacy policy_: how user queries are handled (e.g., non‑training, compliance standards). [support.claude](https://support.claude.com/en/articles/11845131-using-claude-code-with-your-team-or-enterprise-plan)

## Feature comparison table

| Offering                      | Cost per month (approx.)                                                                                  | Free tier available?                                 | Model access (Haiku / Sonnet / Opus)                   | Context window                                               | Rate limits (per‑user / usage cap)                                                                                 | API key required?                                                                        | Team/organisation support                                                                | Data privacy policy (high‑level)                                                          |
|-------------------------------|-----------------------------------------------------------------------------------------------------------|------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Claude.ai Free                | €0                                                                                                        | Yes, free tier                                       | Haiku & Sonnet only (no Opus)                          | Standard (e.g., 200k)                                        | Strong per‑user limits on usage volume; lower priority traffic                                                     | No (web UI + OAuth)                                                                      | No org controls; personal accounts only                                                  | Data not used to train models; standard privacy terms[web:11][web:17]                     |
| Claude.ai Pro                 | ~€18–20/month per user                                                                                    | No                                                   | Full set: Haiku / Sonnet / Opus                        | Same as Team at standard tier                                | Higher per‑user caps than Free; “Pro” volume tier                                                                  | No (web UI + OAuth)                                                                      | Individual seats only; no central IT controls                                            | Data not used to train models; Anthropic privacy terms apply[web:11][web:17]              |
| Claude.ai Team (Standard)     | ~€20–25/user/month (annual)                                                                               | No per‑org free tier                                 | Haiku / Sonnet / Opus (standard usage)                 | Standard (e.g., 200k)                                        | Per‑user caps, plus optional “extra usage” for overflow[web:16][web:20]                                            | No (OAuth‑based; admins manage seats)                                                    | Yes: SSO, centralized billing, seat management, org‑wide search                          | Data not used to train; enterprise‑grade privacy controls[web:13][web:20]                 |
| Claude.ai Team (Premium)      | ~€100–150/user/month                                                                                      | No                                                   | Haiku / Sonnet / Opus + higher quotas                  | Same context window                                          | Higher per‑user quotas; “Max‑like” limits for heavy users                                                          | No                                                                                       | Full Team controls + early access / developer‑focused features[web:14][web:20]           |                                                                                           |
| Claude.ai Enterprise          | Custom quote                                                                                              | No                                                   | Haiku / Sonnet / Opus; may include newer models        | Extended context available (up to 1M tokens)[web:12][web:18] | Usage‑based or per‑seat caps; configurable by IT                                                                   | No (OAuth) but can be paired with API keys for some workflows                            | Full: SSO, SCIM, audit logs, RBAC, custom data‑retention, compliance API[web:16][web:20] |                                                                                           |
| Anthropic API (pay‑as‑you‑go) | Token‑based; ~€0.001–0.005/MTok Haiku, ~€0.003–0.015/MTok Sonnet, ~€0.005–0.025/MTok Opus[web:12][web:18] | No free tier (trial credits may exist)               | All three: Haiku / Sonnet / Opus                       | Up to 1M tokens for Opus 4.6/4.7[web:12][web:18]             | Per‑project rate limits; bursty throttling tuned to tokens/second                                                  | Yes (API key)                                                                            | None out‑of‑box; org‑level controls must be built in‑house                               | Data not used to train; strict data handling rules; can sign DPA for orgs[web:15][web:18] |
| Claude Code (CLI layer)       | Bundled with Pro, Team, or Enterprise; pay‑as‑you‑go via API if used standalone[web:5][web:13]            | Free CLI wrapper around free‑tier web usage possible | Same models as the underlying plan (Haiku/Sonnet/Opus) | Same as the underlying plan (e.g., 200k or 1M)               | Follows the plan’s rate limits; heavy‑usage patterns may incur API‑level costs when used standalone[web:5][web:13] | Optional: can use OAuth via Team/Enterprise or API key for raw API usage[web:13][web:20] | No inherent controls; inherits team/enterprise governance if tied to org plan            | Inherits the privacy model of the backing plan (web UI) or API policy[web:13][web:15]     |


### Notes on the table

- _Claude Code_ is not a standalone pricing tier; it is a CLI interface that may be:
  - authenticated via a Pro / Team / Enterprise account (OAuth), or
  - driven directly via the Anthropic API (API key). [zenml](https://www.zenml.io/llmops-database/building-and-operating-a-cli-based-llm-coding-assistant)
- For academic teaching and research, the **Team Standard** plan is
  the most relevant “default” commercial tier once you outgrow free
  usage, since it bundles Claude Code, provides central seat
  management, and supports SSO‑like
  integrations. [devops](https://devops.com/enterprise-ai-development-gets-a-major-upgrade-claude-code-now-bundled-with-team-and-enterprise-plans/)

## Recommended path for zero‑cost POC

For an academic department that wants a _zero‑cost proof‑of‑concept_,
yet still integrates Claude Code into the project template, the
recommended path is:

- **Use individual Claude.ai Free accounts** for students and researchers to access the web UI and try Haiku / Sonnet. [glbgpt](https://www.glbgpt.com/hub/claude-ai-plans-2026/)
- **Tie Claude Code to the free web tier**:
  - Install Claude Code on the Linux base image (e.g., Ubuntu WSL‑compatible) via the official installer. [anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
  - At first login, have users select “Claude account with subscription” (using their free Claude.ai login) so the CLI rides on the same usage quota as the web plan. [support.claude](https://support.claude.com/en/articles/11845131-using-claude-code-with-your-team-or-enterprise-plan)
- **Enforce a “light‑usage” regime**:
  - Document maximum rough token budgets per user (e.g., “avoid multi‑GB‑scale refactoring sessions”) to stay within free‑tier limits.
  - Prefer Haiku‑level queries where possible, since Haiku is cheaper to run and aligns with the free tier’s performance profile. [finout](https://www.finout.io/blog/anthropic-api-pricing)
- **Delay paid tiers until**:
  - The department observes consistent heavy usage (e.g., multiple students routinely hitting free limits).
  - Institutional budgeting and IT‑security (SSO, data‑handling) processes are in place.

At that point, the natural next step is to **migrate to a Claude.ai Team plan** (probably Standard) because it:

- Unifies web, desktop, and CLI access under one subscription.
- Bundles Claude Code with each seat.
- Gives central billing and basic governance controls while keeping
  individual per‑user costs in the low‑tens‑of‑euros
  range. [finout](https://www.finout.io/blog/claude-pricing-in-2026-for-individuals-organizations-and-developers)

This path keeps the POC technically close to the intended production configuration (Claude Code + web / Team) while remaining fully zero‑cost for the first semester or pilot iteration.

## Additional Notes

- **Rate‑limit tuning**: For classroom‑style workloads, the department can script a “soft throttle” (e.g., maximum queries per hour per user) via the shell or GitLab CI, even if the backend is just the free tier.[bp-1]
- **Hybrid tooling**: The same project template can run Gemini CLI and Cursor in parallel with Claude Code, allowing a side‑by‑side comparison of latency, quality, and cost‑efficiency without committing institutional funds to paid tiers.[bp-2]
- **Export and logging**: For academic reproducibility, consider logging Claude Code prompts/responses (with user‑consent) into a local database or Git‑tracked `.claude-log/` directory, while respecting Anthropic’s terms and privacy policies.[bp-1]

---

## References

- [^bp-1] Anthropic. [“Claude Code: best practices for agentic coding.”](https://www.anthropic.com/engineering/claude-code-best-practices) 2025‑04‑17.
- [^bp-2] Anthropic. [“Build with Claude”](https://www.anthropic.com/learn/build-with-claude) (Anthropic Academy).
- [^bp-3] Anthropic. [“Using Claude Code with your Team or Enterprise plan”](https://support.claude.com/en/articles/11845131-using-claude-code-with-your-team-or-enterprise-plan) (support article).
- [^bp-4] Anthropic. [“Anthropic API pricing overview”](https://evolink.ai/blog/claude-api-pricing-guide-2026) (per‑token, Haiku/Sonnet/Opus rates). Finout, 2026‑04‑15.
- [^bp-5] screenapp. ["Aligned pricing guides and team‑plan summaries"](https://screenapp.io/blog/claude-ai-pricing) (Team Standard/Premium, Claude.ai plans).

# A:2 (DeepSeek)

[^](#toc) **_Anthropic Product Offering Comparison for Academic Statistics Department_**

## Anthropic Product Offering Comparison for Academic Statistics Department

This document compares Anthropic’s access options against criteria
relevant to an academic organisation. The evaluation supports the
multi‑agent project template that mandates _Claude Code_, _Gemini
CLI_, and _Cursor_, while optionally including _VS Code Copilot_ and
_GitLab Duo_ (planned). All information is current as of Q2 2025.

### Comparison Table

| Option                            | Cost per month                                                                               | Free tier availability                                  | Model access (Haiku / Sonnet / Opus)                    | Context window                                        | Rate limits                                              | API key required                    | Team / organisation support                                                | Data privacy policy                                                    |
|-----------------------------------|----------------------------------------------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------|-------------------------------------------------------|----------------------------------------------------------|-------------------------------------|----------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Claude.ai Free**                | $0                                                                                           | Yes – full web/chat access                              | Sonnet (default), Opus (limited)                        | 200k tokens[bd-1]                                     | Lower priority during peak times                         | No (Anthropic account only)         | No – single user                                                           | Inputs not used for training by default[bd-2]                          |
| **Claude.ai Pro**                 | $20 / month                                                                                  | No – paid only                                          | Sonnet, Opus, Haiku (via feature toggle)                | 200k tokens                                           | Higher than Free, no hard cap for reasonable use         | No                                  | No – single user                                                           | Same as Free – no training on your data                                |
| **Claude.ai Team**                | $30 / user / month (min 5 users)                                                             | No                                                      | Full access to all three models                         | 200k tokens                                           | Higher than Pro, shared pool                             | No                                  | Yes – admin console, usage analytics, central billing                      | Data not used for training, SOC 2 Type II[bd-3]                        |
| **Claude.ai Enterprise**          | Custom pricing (annual contract)                                                             | No                                                      | Full access + priority model updates                    | 200k tokens (custom extensions possible)              | Enterprise‑grade, no practical limit                     | No                                  | Yes – SSO, SCIM, audit logs, dedicated support                             | HIPAA and GDPR compliant options, data never used for training         |
| **Anthropic API (pay‑as‑you‑go)** | Pay per token: Haiku ~$0.25 / 1M input, Sonnet ~$3 / 1M input, Opus ~$15 / 1M input[bd-4]    | No – but $5 credit for new accounts                     | All three models, programmatic choice                   | 200k tokens (standard), 1M token beta for some models | Tiered based on usage level (see rate limits page[bd-5]) | **Yes** – required for all requests | Organisation‑level API keys, fine‑grained access control via projects      | Data not used for training. EU data residency available at higher tier |
| **Claude Code** (CLI tool)        | No separate subscription – uses API pay‑as‑you‑go or bundled with Team/Enterprise agreements | Free during preview? No – requires API key with credits | Same as underlying API (Haiku recommended for low cost) | Inherits from API (200k tokens)                       | Inherits from API rate limits                            | **Yes** – API key must be provided  | Inherits from API or Team/Enterprise – supports multi‑user via shared keys | Inherits from the API or plan used                                     |

### Recommended Path for a Zero‑Cost Proof‑of‑Concept

For an academic department that wants to evaluate Anthropic’s tools – especially _Claude Code_ – before committing to any paid tier, the following sequence achieves a functional POC at **zero monetary cost** (or near‑zero using the free API credit):

1. **Start with Claude.ai Free**
   - No API key, no payment.
   - Test conversational coding help, prompt engineering, and document analysis up to 200k tokens.
   - Identify which model (Sonnet vs. Opus) suits your research tasks.

2. **Create an Anthropic Console account**
   - Sign up at console.anthropic.com.
   - New accounts receive **$5 in free API credits** (no time limit stated as of 2025)[bd-4].
   - This credit is enough for ~20 million input tokens with Haiku or ~1.6 million with Sonnet – far more than needed for a small‑scale POC.

3. **Install and configure Claude Code**
   - Follow the official installation guide[bd-6] (requires Node.js 18+).
   - Run `claude config` and paste your API key.
   - Use the `--model haiku` flag to minimise credit consumption while testing.

4. **Run a representative academic task**
   - Example: “Refactor this R statistics script to use `data.table` instead of `dplyr`”.
   - Monitor token usage in the Anthropic Console dashboard.

5. **Evaluate without spending departmental funds**
   - The $5 credit covers hundreds of such interactions.
   - No recurring cost unless you exceed the credit – simply stop or switch to a free Gemini CLI/Cursor tier for the remainder of the POC.

6. **Decide on a paid tier** (if needed) after the POC:
   - **Individual researcher** → Claude.ai Pro ($20/month) for unlimited web chat.
   - **Small team (≤5 users)** → Anthropic API pay‑as‑you‑go + shared API key (cheaper than Team if usage is low).
   - **Department‑wide (≥5 users)** → Claude.ai Team ($30/user/month) for central management and no per‑token surprises.
   - **Heavy API usage (e.g., automated pipelines)** → Continue with API pay‑as‑you‑go.

> **Note**: The free $5 API credit is _per account_, not per
> organisation. For a multi‑user POC, each researcher can create their
> own account, or the department can request a single credit via the
> Anthropic for Education programme[bd-7] (no guaranteed free tier,
> but worth contacting sales).

### References

- [^bd-1] Anthropic. [“Model comparison – context window.”](https://docs.anthropic.com/en/docs/about-claude/models#context-windows)
- [^bd-2] Anthropic. [“Data privacy and training.”](https://www.anthropic.com/data-privacy)
- [^bd-3] Anthropic. [“Trust Center – SOC 2.”](https://trust.anthropic.com)
- [^bd-4] Anthropic. [“Pricing – API.”](https://www.anthropic.com/pricing#api)
- [^bd-5] Anthropic. [“Rate limits.”](https://docs.anthropic.com/en/api/rate-limits)
- [^bd-6] Anthropic. [“Claude Code – Installation.”](https://docs.anthropic.com/en/docs/claude-code)
- [^bd-7] Anthropic. [“Education programme.”](https://www.anthropic.com/education)

### Additional Notes

- The multi‑agent project template also requires _Gemini CLI_ and
  _Cursor_. Both offer free tiers (Gemini API has $300 credit, Cursor
  has a limited free plan). This document focuses solely on
  Anthropic’s offerings, but the zero‑cost POC can be extended to
  those tools with their respective free credits.

- _GitLab Duo_ (planned) is available only with the Ultimate tier. No
  free tier exists, but academic organisations may apply for a
  discount via GitLab’s education programme.

- _Claude Code_ is still in preview as of this writing. Some features
  (e.g., terminal command suggestions) may require enabling
  experimental flags. Check the reference [rf-6] for the latest
  status.

- If your department handles sensitive student or research data,
  _Claude.ai Enterprise_ or a signed Business Associate Agreement
  (BAA) with the API is recommended – the free/Pro/Team tiers are not
  HIPAA compliant by default.


<!-- }}} \\ %2. -->
<!-- {{{ // %*
LocalWords:  GitLab CommonMark GFM GLFM YAML
vim: set foldmethod=marker :
}}} // %* -->
