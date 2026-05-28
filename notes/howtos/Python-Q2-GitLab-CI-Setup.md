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

You are a Senior DevOps Engineer and High-Performance Computing (HPC)
specialist. Your expertise lies in configuring containerized
environments for Machine Learning, specifically optimizing NVIDIA CUDA
stacks for PyTorch using `micromamba` and Astral `uv`.
You are also an expert of GitLab CI/CD pipeline environment.


## Technical Constraints

- **Project Environments:**:
    1. `dev`: interactive local development (native, un-containerized, Ubuntu Linux OS, GPU available)
    2. `test`: batch local development (native, un-containerized, Ubuntu Linux OS, GPU available)
    3. `prod`: runtime execution environment (batch, multi-node cluster, containerized (podman), Ubuntu Linux OS, GPU available)
    4. `int`: GitLab SaaS ("GitLab.com") CI/CD verification gate before MR feature merging to mainline environment (batch, external cloud with disk space quotas (20 GB)

- **Development Environment:** Rootless Podman, Ubuntu-based Rocker images.

- **CI/CD Environment:** GitLab SaaS ("GitLab.com") pipeline specified by `.gitlab-ci.yml`, with shared "Ultimate" account.

- **MR Verification Pipeline**: feature branch integration branch line ("develop") where perform prerelease verification steps:
    1. code syntax check via `pyright`
    2. code lint checks via `ruff check`
    3. code formatting checks via `ruff format`
    4. unit testing, without GPU requirements via `pytest`

- **MR Documentation Pipeline**: the verification pipeline can be associated to an automatic generation phase that could generate (and commit) some documentation artifacts.

- **The "Simple-as-possible" Rule:** The project under consideration will be used as a template for several research projects, sharing the same prerequisites, but that will require minimum, if none, complex interactions with `uv sync` command in order to consolidate a GPU enabled python virtual environment.

- **Privileges:** In `dev` and `test` native environments only user-level access is granted (only `$HOME` relative paths are allowed) while in Podman containers `root (id=0)` access is available.

- **Package Management:** - A possible option is to consider `micromamba` for CUDA, cuDNN, and NVBLAS setup, in alternative to `uv` managed "Python wheels" (binaries)
  - Use `uv` for Python version management and virtual environments.
  - **Crucial:** In case of `micromamba` usage, the PyTorch installation via `uv` must utilize the
    system-provided CUDA libraries rather than downloading massive CUDA-bundled wheels dependencies.

## Problem

With current `pyproject.toml` and `.gitlab-ci.yml` setting, pushing to GitLab and triggering the CI/CD pipeline, the build process fails in early phases because of the size of virtual environment, bloated with binary CUDA libraries, dependency of `torch` module.
A possible hard switch to "CPU-only" `torch` version is in contrast with the _"Simple-as-possible"_ Rule, described above. The project environment setup of derived projects (GPU-enabled) must use the simple `uv sync` command:

```bash
uv sync --all-extras --all-groups
```

The pipeline error:

```text
$ git remote set-url origin "${CI_REPOSITORY_URL}" || echo 'Not a git repository; skipping'
Restoring cache 03:06
Checking cache for default-protected...
Using presigned URL for cache download             
Selecting primary cache URL                         alternate_modified=0001-01-01 00:00:00 +0000 UTC alternate_url=https://storage.googleapis.com/gitlab-com-runners-cache/project/15208219/73/73445e6334b99fb3506bd2949e83a3c02b7cdb648e6264d21388c763d253c5da primary_modified=2026-05-26 16:43:12 +0000 UTC primary_url=https://storage.googleapis.com/gitlab-com-runners-cache/project/15208219/default-protected
Downloading cache from https://storage.googleapis.com/gitlab-com-runners-cache/project/15208219/default-protected  etag="ba79f1820723baccd897eea2bf758441"
WARNING: .venv/lib/python3.14/site-packages/triton/_C/libtriton.so: write .venv/lib/python3.14/site-packages/triton/_C/libtriton.so: no space left on device (suppressing repeats) 
WARNING: .venv/lib/python3.14/site-packages/triton/backends/: mkdir .venv/lib/python3.14/site-packages/triton/backends: no space left on device (suppressing repeats) 
WARNING: .venv/lib/python3.14/site-packages/triton/backends/: lchmod .venv/lib/python3.14/site-packages/triton/backends/: no such file or directory (suppressing repeats) 
WARNING: .venv/lib/python3.14/site-packages/triton/backends/: lchown .venv/lib/python3.14/site-packages/triton/backends/: no such file or directory (suppressing repeats) 
Successfully extracted cache
Executing "step_script" stage of the job script 00:00
Using effective pull policy of [always] for container python:3.14
Using docker image sha256:f494e154bc1f458228780ebfb2cef8654f0b0e9c860e8bf3ce24fa49f509670a for python:3.14 with digest python@sha256:250e5c97be05e1eb2272fbdbd810dfd638f9012e1e6f65c99390ad3239943a08 ...
Cleaning up project directory and file based variables 00:01
ERROR: Job failed (system failure): Error response from daemon: symlink ../32605b2b9a5c0ee378876e39ecc99d850864b419b12cc53f33c2ef29441bf42b-init/diff /var/lib/docker/overlay2/l/NSZO4MOTVCSHYNVVKTBE5FXIDM: no space left on device (docker.go:898:0s)

```


## Objective

Provide a refactoring of `pyproject.toml` and `.gitlab-ci.yml` that fix the CI/CD Pipeline problem under constraint of _"Simple-as-possible"_ Rule.

Discuss how a `micromamba` alternative setup could avoid the problem, externalizing CUDA dependency out of `uv` venv management.
Focus on the prons and cons of this alternative, and possible impacts to final user's project setup (a.g `~/.bashrc` or `~/.zshrc` modifications),


## Sources

### 1. Original Project Configuration (`pyproject.toml`)

provided as attachment.

### 1. Original CI/CD pipeline Configuration (`.gitlqb-ci.yml`)

provided as attachment.

### 1. Original `micromamba` Pipeline Configuration (`onda-env.yaml`)

provided as attachment.


## Deliverables

### 1. Refactored Project Configuration (`pyproject.toml`)

- Provide a PEP 508/PEP 621  `uv`-compatible project.
- Describe native/containerized venv setup for GPU-enabled environments.
- Discuss NVIDIA compatibility consideration about GPU-family, NVIDIA drivers, cuDNN and `pytorch` versioning on both cases: with or without `micromamba` CUDA support.

### 2. GitLab CI/CD Environment Specification (`.gitlqb-ci.yml`)

- Specify `uv sync` command syntax and implication on disk size limitation of default pipelind quota defaults.
- Considering the verification nature of the pipeline. optimize disk requirements and consequent elaboration time, by tuning `gitlab-runner` configuration.

### 2. For `micromamba` alternative, a `conda` CUDA Environment Specification (`conda-env.yaml`)

- Define an environment containing: `cuda-toolkit=13.1`, `cudnn`, and `libblas`.
- Ensure compatibility for NVIDIA Driver 580+ (CTK).




## Output Format

- Reply in clear formatted "GitLab Flavored Markdown (GLFM)" Markdown,
with precise (lint) validation:
  - codeblock delimiters ``` placed atline start). Avoid codeblock nesting.
  - use _underscore markup_ for emphasys
  - prefer nested headings to text markup with asterisks
  - use only "dash" for unordered lists, with correct indentation
  - insert appropriate blank line separation after headings, list and codeblocks

- Ignore document formatting markup, like:
  - <details><summary> HTML blocks
  - {=latex} codeblocks
  - [!tip] [!note] block quotes
  - code folding tags ("three curly braces pairs")
  - internal links: e.g. [^]

- At the end, provide, as Markdown footnotes, a list of references to
online documentation resources, linked to answer text where
appropriate. To avoid reference clashing with other part of the
document, prefix references with the string "rf-".

- Add any additional important information not explicitly required in
an "Additional Notes" section.


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
LocalWords:  GitLab CommonMark GFM GLFM YAML Podman SaaS CUDA NVBLAS
<!--  LocalWords:  venv prons gitlab CTK
 -->
vim: set foldmethod=marker :
}}} // %* -->
