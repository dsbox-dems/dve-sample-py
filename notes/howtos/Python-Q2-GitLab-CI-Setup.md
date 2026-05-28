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
<!-- markdownlint-disable MD013 -->
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

## Q:1 - **TODO:(q1-title)**

[^](#toc)


## Role

You are a Senior DevOps Engineer and High-Performance Computing (HPC) specialist.
Your expertise covers containerised environments for Machine Learning, specifically
optimising NVIDIA CUDA stacks for PyTorch using `micromamba` and Astral `uv`.
You are also an expert in GitLab CI/CD pipeline configuration.

## Technical Constraints

- _Project Environments_:
    1. `dev`: interactive local development (native, un-containerised, Ubuntu Linux, GPU available)
    2. `test`: batch local development (native, un-containerised, Ubuntu Linux, GPU available)
    3. `prod`: batch runtime on a multi-node cluster (containerised via Podman, Ubuntu Linux, GPU available)
    4. `int`: GitLab SaaS (`GitLab.com`) CI/CD verification gate before MR merging to mainline
       (batch, shared cloud runner, disk quota: 20 GB)

- _Development Environment_: Rootless Podman, Ubuntu-based images.

- _CI/CD Environment_: GitLab SaaS pipeline defined in `.gitlab-ci.yml`, shared "Ultimate" account.

- _MR Verification Pipeline_: runs on the `develop` integration branch and performs:
    1. Static type checking via `pyright`
    2. Lint checks via `ruff check`
    3. Format checks via `ruff format`
    4. Unit tests (no GPU required) via `pytest`

- _The "Simple-as-possible" Rule_: This project is a template for multiple research projects
  sharing the same prerequisites. Derived projects must be able to set up a GPU-enabled Python
  virtual environment with a single command:

```bash
uv sync --all-extras --all-groups
```

  No complex, project-specific post-sync steps are permitted.

- _Privileges_: In `dev` and `test` environments, only user-level access is granted (`$HOME`-relative
  paths only). Inside Podman containers, `root` (uid=0) access is available.

- _Package Management_:
  - `uv` manages Python version selection and virtual environments.
  - `micromamba` is a candidate alternative for installing `cuda-toolkit`, `cudnn`, and `libblas`,
    externalising CUDA from the `uv`-managed virtual environment.
  - _Crucial_: if `micromamba` is used, PyTorch must be installed by `uv` against the
    system-provided CUDA libraries, _not_ via CUDA-bundled wheel downloads.

## Problem Statement

The CI/CD pipeline fails in early stages because the `.venv` restored from cache exceeds the
20 GB disk quota of the GitLab SaaS shared runner. The root cause is that `torch`, when installed
via `uv sync`, pulls in massive CUDA-bundled binary wheels (including `triton` shared libraries).

A hard switch to a CPU-only `torch` variant is explicitly prohibited by the _"Simple-as-possible"_
Rule: derived GPU-enabled projects must continue to use `uv sync --all-extras --all-groups`
without modification.

The observed pipeline error is:

```text
WARNING: .venv/lib/python3.14/site-packages/triton/_C/libtriton.so:
  write: no space left on device

ERROR: Job failed (system failure): Error response from daemon:
  symlink [...]: no space left on device (docker.go:898:0s)
```

## Objective

Provide a concrete refactoring of `pyproject.toml` and `.gitlab-ci.yml` that resolves the
disk-quota failure while respecting the _"Simple-as-possible"_ Rule.

Additionally, analyse the `micromamba` alternative setup as a means of externalising the CUDA
dependency from `uv` virtual environment management. Structure the analysis as follows:

- _Mechanism_: how `micromamba` decouples CUDA from `uv sync`.
- _Pros_: benefits for disk size, portability, and reproducibility.
- _Cons_: additional setup burden (e.g. `~/.bashrc` / `~/.zshrc` modifications, `conda activate`
  in CI steps, solver overhead).
- _Impact on derived projects_: what a template consumer must do differently.

## Source Files

The following configuration files are provided as attachments. If any attachment is absent,
state which file is missing and proceed by generating a representative example based on the
constraints above.

1. _Original `pyproject.toml`_ — current project configuration.
2. _Original `.gitlab-ci.yml`_ — current CI/CD pipeline definition.
3. _Original `conda-env.yaml`_ — existing `micromamba` environment specification.

## Deliverables

### 1. Refactored `pyproject.toml`

- Produce a PEP 508 / PEP 621 compliant, `uv`-compatible project file.
- Describe how the virtual environment is set up for GPU-enabled environments,
  both native and containerised.
- Discuss NVIDIA compatibility considerations: GPU family, driver version, cuDNN, and
  PyTorch versioning — for both the `uv`-only and `micromamba`-assisted cases.

### 2. Refactored `.gitlab-ci.yml`

- Specify the correct `uv sync` command and flags for the CI context.
- Optimise disk usage and job duration given the 20 GB shared runner quota,
  focusing on the verification nature of the pipeline (no GPU, no large binary wheels needed).
- Tune cache configuration and `gitlab-runner` settings to minimise footprint.

### 3. `conda-env.yaml` for `micromamba` Alternative

- Define a `micromamba`/`conda` environment containing `cuda-toolkit=13.1`, `cudnn`,
  and `libblas`.
- Ensure compatibility with NVIDIA Driver 525+ and the CUDA 12.x Toolkit (CTK).
- Note any version pinning required for PyTorch compatibility.

## Output Format

- Reply in clear, formatted GitLab Flavored Markdown (GLFM) with lint-valid structure:
  - Place all codeblock delimiters (` ``` `) at line start; avoid nested codeblocks.
  - Use _underscore markup_ for emphasis.
  - Prefer nested headings over bold/asterisk text markup.
  - Use only dashes for unordered lists, with correct indentation.
  - Insert a blank line after every heading, list block, and codeblock.

- Ignore document-pipeline formatting markup:
  - `<details><summary>` HTML blocks
  - `{=latex}` codeblocks
  - `[!tip]` / `[!note]` block quotes
  - Code-folding tags (`{{{` / `}}}`)
  - Internal cross-reference links (e.g. `[^]`)

- At the end, provide Markdown footnotes for all referenced online documentation,
  linked inline where appropriate. Prefix all footnote identifiers with `rf-` to avoid
  clashes with document-level references.

- Add any important information not explicitly requested above in an _"Additional Notes"_ section.


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
LocalWords:  GitLab CommonMark GFM GLFM YAML Podman SaaS CUDA NVBLAS
<!--  LocalWords:  venv prons gitlab CTK
 -->
vim: set foldmethod=marker :
}}} // %* -->
