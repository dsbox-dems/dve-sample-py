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

## Q:1 - **TODO:(q1-title)**

[^](#toc)

## Role

You are an expert Google "Antigravity" IDE user and Python developer,
specialising in NLP/NLU projects built on the latest PyTorch and CUDA environments.
Your Python environment is fully managed by `uv` with `pytest` fot testing and
`ruff` for code linting and formatting.

## Context

- Standard Python projects with PEP 621 and PEP 508 compliant `pyproject.toml`
- Testing framework: `pytest` (primary); `behave` is under active
  evaluation as a BDD/AI specification tool and _must_ be treated as a
  first-class target
- Test coverage support is desirable but not mandatory
- Supported IDEs: Visual Studio Code, Cursor
- Supported editors: `emacs` (configuration via `use-package`) and `vim`
  (LazyVim with latest Neovim)
- Language tooling: LSP protocol, `pyright` (type checking), `ruff`
  (linting and formatting)
- `Node.js` and `npm` are available at user level via `nvm`
- Container support: `podman` (code is shared between container and host)
- CI/CD under evaluation: Jenkins (local), GitLab CI / GitHub Actions (remote)

## Prerequisite

Before proposing any changes, _fetch and carefully parse_ the current Emacs
configuration available in `org-mode` literate programming format at:

- [site-pkgs.org](https://github.com/hute37/emacs-site/blob/master/site-pkgs.org)

Use the content of that file as the authoritative baseline for all proposed
modifications. Do not invent or assume configuration details not present in
that file.

## Objective

Propose a revised Emacs configuration for Python development that replaces or
meaningfully improves on the current setup. The proposal must cover the
following tools, each justified with explicit pros and cons against credible
alternatives:

- `python` (base mode and environment integration)
- `uv` (project and virtual-environment management)
- `pyright` (LSP-based static type checking)
- `ruff` (linting and formatting)
- `pytest` (test runner integration)
- `behave` (BDD test runner integration)

Additionally, provide a focused discussion of `treesitter` integration:

- Explain the role of `tree-sitter` (via `treesit` or `treesit-auto`) alongside
  the existing LSP architecture
- Evaluate whether `tree-sitter` should _complement_ LSP (e.g., for syntax
  highlighting and structural navigation) or _partially replace_ LSP features
- State your recommendation clearly and justify it

## Evaluation Criteria

When selecting and justifying packages, assess each against:

- Active maintenance and MELPA/ELPA availability
- Community adoption and issue-tracker health
- Compatibility with `emacs` 29+ built-in `treesit`
- Integration complexity within a `use-package` configuration style

## Output Format

Provide all proposed configuration changes as `org-mode` literate programming
blocks containing `emacs-lisp` source, following this structure:

Structure your full reply in _GitLab Flavored Markdown (GLFM)_ with strict
lint compliance:

- Place all codeblock delimiters at line start; avoid nested codeblocks
- Use _underscore markup_ for emphasis
- Prefer nested headings over bold/asterisk markup
- Use only dashes for unordered lists, with correct indentation
- Insert blank lines after headings, lists, and codeblocks
- Omit document-pipeline markup: `<details>`, `{=latex}` blocks,
  `[!tip]`/`[!note]` callouts, curly-brace fold tags, and internal footnote links
- Provide a _References_ section at the end as Markdown footnotes, prefixed
  with `rf-`, linked to relevant points in the answer text
- Provide an _Additional Notes_ section for any important information not
  explicitly requested




<details>
<summary></summary>

```{=latex}
\newpage
```

</details>

## Response Template

<details>
<summary>Example Markdown Structure:</summary>

TODO:(q1-template) ...

```markdown

## Overview

## Details

\`\`\`bash
#!/bin/bash

echo "$(date -isec) - (rc=${rc:-$?}) completed."

\`\`\`


```

</details>

# A:1 (Claude)

[^](#toc) **_TODO:(a1-ref-claude)_**

TODO:(a1-claude) ...

# A:1 (Gemini)

[^](#toc) **_TODO:(a1-ref-gemini)_**

TODO:(a1-gemini) ...

# A:1 (ChatGPT)

[^](#toc) **_TODO:(a1-ref-chatgpt)_**

TODO:(a1-chatgpt) ...

# A:1 (Perplexity)

[^](#toc) **_TODO:(a1-ref-perplexity)_**

TODO:(a1-perplexity) ...

## Q:1.2 (Perplexity)

[^](#toc) **_(=> continue)_**

TODO:(q1.2-perplexity) ...

---

## A:1.2 (Perplexity)

[^](#toc) **_(=> continue)_**

TODO:(a1.2-perplexity) ...

# A:1 (DeepSeek)

[^](#toc) **_TODO:(a1-ref-deepseek)_**

TODO:(a1-deepseek) ...

<!-- }}} \\ %1. -->
<!-- ::{{{ #TAG: TODO:(q2-section) // -->

# Q:2

## Q:2 - **TODO:(q2-title)**

[^](#toc)

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
