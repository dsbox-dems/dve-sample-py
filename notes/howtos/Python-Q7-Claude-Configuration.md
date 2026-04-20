---
title: TODO:(title)
subtitle: TODO:(subtitle)
# {{{ // %+

category: LLM-Style
keywords: [GEN, TODO:(keywords)]
abstract: |
  TODO:(abstract)
  
  ...

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

1. [Q:1 - TODO:(q1-ref)](#q1)
   - see: [TODO:(a1-ref-claude) (Claude)](#a1-claude)
   - see: [TODO:(a1-ref-gemini) (Gemini)](#a1-gemini)
   - see: [TODO:(a1-ref-chatgpt) (ChatGPT)](#a1-chatgpt)
   - see: [TODO:(a1-ref-perplexity) (Perplexity)](#a1-perplexity)
   - see: [TODO:(a1-ref-deepseek) (DeepSeek)](#a1-deepseek)
2. [Q:2 - TODO:(q2-ref)](#q2)
   - see: [TODO:(a2-ref-claude) (Claude)](#a2-claude)
   - see: [TODO:(a2-ref-gemini) (Gemini)](#a2-gemini)
   - see: [TODO:(a2-ref-chatgpt) (ChatGPT)](#a2-chatgpt)
   - see: [TODO:(a2-ref-perplexity) (Perplexity)](#a2-perplexity)
   - see: [TODO:(a2-ref-deepseek) (DeepSeek)](#a2-deepseek)
3. [A:a - TODO:(appendix-a)](#aa)
4. [A:b - Q1: Prompt distiller](#ab)
   - see: [Q1: Prompt distiller (Claude)](#ab-claude)
   - see: [Q1: Prompt distiller (Gemini)](#ab-gemini)
   - see: [Q1: Prompt distiller (ChatGPT)](#ab-chatgpt)
   - see: [Q1: Prompt distiller (Perplexity)](#ab-perplexity)
   - see: [Q1: Prompt distiller (DeepSeek)](#ab-deepseek)

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

[^](#toc) **_TODO:(a1-ref-chatgpt)_**

TODO:(a1-chatgpt) ...

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

## Q:2 - **TODO:(q2-title)**

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







## Question Prompt 2

TODO:(q1-prompt) ...


# A:2 (Claude)

[^](#toc) **_TODO:(a1-ref-claude)_**

TODO:(a2-claude) ...

# A:2 (Gemini)

[^](#toc) **_TODO:(a2-ref-gemini)_**

TODO:(a2-gemini) ...

# A:2 (ChatGPT)

[^](#toc) **_TODO:(a2-ref-chatgpt)_**

TODO:(a2-chatgpt) ...

# A:2 (Perplexity)

[^](#toc) **_TODO:(a2-ref-perplexity)_**

TODO:(a2-perplexity) ...

## Q:2.2 (Perplexity)

[^](#toc) **_(=> continue)_**

TODO:(q2.2-perplexity) ...

---

## A:2.2 (Perplexity)

[^](#toc) **_(=> continue)_**

TODO:(a2.2-perplexity) ...

# A:2 (DeepSeek)

[^](#toc) **_TODO:(a2-ref-deepseek)_**

TODO:(a2-deepseek) ...

<!-- }}} \\ %2. -->
<!-- ::{{{ #TAG: TODO:(aa-section) // -->
<details>
<summary></summary>

```{=latex}
\newpage
\clearpage
\appendix
```

</details>

# A:a

## A:a - **TODO:(aa-title)**

[^](#toc)

## Appendix a

TODO:(aa-text) ...

# A:b

## A:b - **Q2: Prompt distiller**

[^](#toc)

## Appendix b

### User

Act as an expert Prompt Engineer and AI Optimisation Specialist. Your
objective is to analyse, critique, and significantly enhance the
user-provided prompt.

The prompt you need to refine begins immediately after the line
starting with /PROMPT/ marker.

### Your Process

#### Analysis & Evaluation

- Assess the original prompt for clarity, context, constraint
  definition, and logical flow.
- Identify specific weaknesses, such as ambiguity, grammatical errors,
  logic gaps, or lack of sufficient context.
- Determine if the prompt would benefit from specific engineering
  techniques (e.g., Chain-of-Thought, persona adoption, or few-shot
  examples).

#### Critique Presentation

- Provide a brief, professional evaluation of the original text.
- List specific issues found and explain why they are problematic.
- Propose concrete improvements to address these issues.

#### Optimisation

- Rewrite the prompt to be precise, fluent, and highly effective.
- Ensure the English style is professional and grammatically correct.
- Clarify all requirements and specifications to minimise the risk
of AI hallucination or misinterpretation.

### Note

- Ignore extra Markdown used in rendering pipelines: GitLab GLFM
  repository view and pandoc PDF transformations.
- Keep this Markdown unaltered in reply.

In particular, ignore:

- <details><summary> HTML blocks
- {=latex} codeblocks
- [!tip] [!note] block quotes
- code folding tags '{{{' and '}}}'
- internal links: e.g. [^]

### Important

> Generate 3 responses to this prompt, each with their probability.

### Output Format

- Present your analysis and critique first.
- Output the final, polished version of the prompt at the very end.
- Separate every refined prompt from the analysis using a horizontal line
  (`---`) and the line start marker `/PROMPT/`.

---
/PROMPT/

TODO:(a2-prompt) ...

# A:b (Claude)

[^](#toc) **_TODO:(ab-ref-claude)_**

TODO:(ab-claude) ...

# A:b (Gemini)

[^](#toc) **_TODO:(ab-ref-gemini)_**

TODO:(a2-gemini) ...

# A:b (ChatGPT)

[^](#toc) **_TODO:(ab-ref-chatgpt)_**

TODO:(ab-chatgpt) ...

# A:b (Perplexity)

[^](#toc) **_TODO:(ab-ref-perplexity)_**

TODO:(ab-perplexity) ...

# A:b (DeepSeek)

[^](#toc) **_TODO:(ab-ref-deepseek)_**

TODO:(ab-deepseek) ...



<!-- }}} \\ %a. -->
<!-- {{{ // %*
LocalWords:  GitLab CommonMark GFM GLFM YAML
vim: set foldmethod=marker :
}}} // %* -->
