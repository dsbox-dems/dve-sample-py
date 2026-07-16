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
   - see: [TODO:(a1-ref-vibe) (Vibe)](#a1-vibe)
2. [Q:2 - TODO:(q2-ref)](#q2)
   - see: [TODO:(a2-ref-claude) (Claude)](#a2-claude)
   - see: [TODO:(a2-ref-gemini) (Gemini)](#a2-gemini)
   - see: [TODO:(a2-ref-chatgpt) (ChatGPT)](#a2-chatgpt)
   - see: [TODO:(a2-ref-perplexity) (Perplexity)](#a2-perplexity)
   - see: [TODO:(a2-ref-deepseek) (DeepSeek)](#a2-deepseek)
   - see: [TODO:(a2-ref-vibe) (Vibe)](#a2-vibe)
3. [A:a - TODO:(appendix-a)](#aa)


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

You are an expert in GitLab CI/CD pipelines for multi-repository environments, specialising in:

- targeting testing and deployment across multiple environments (`development`, `testing`, `staging`, `production`)
- authorising CI/CD pipeline jobs across a multi-repository setup (public upstream repository, private downstream fork, and public GitHub mirror)
- Python project automation using `uv`, including pre-release validation with `pyright`, `ruff`, and `pytest`, and post-release container image build and delivery via Podman to a public container registry
- DevOps best practices for private Git-based, multi-environment configuration management and versioning

## Terminology

To avoid ambiguity, use these terms consistently throughout your response:

- _upstream_ — the canonical public repository
- _downstream_ — the private fork, extended with unmerged features
- _mirror_ — the public GitHub copy of the upstream repository

## Context

Two GitLab projects share the same Python codebase, managed with `uv`:

- _Public upstream project_: `ub-dems-public/ds-lab/dve-simple-py`, branch `main`
- _Private downstream project_: `ub-dems/vs-base/dve-simple-py`, branches `main` and `development`
- _Public mirror project_ (GitHub): `ub-dems/dve-simple-py`, branch `main`

Requirements to address:

- inter-repository authorisation so that pipelines in the downstream project can trigger merge requests and tag jobs on the upstream project, and push the codebase to the mirror
- public container registry credentials, available as CI/CD pipeline variables
- environment-dependent configuration data (API access tokens, database credentials), available consistently across CI/CD pipelines, local development, and application runtime

Before answering, reason through each environment (`development`, `testing`, `staging`, `production`) and each repository (upstream, downstream, mirror) as a distinct combination, so that environment-specific and repository-specific nuances are not collapsed into a single generic answer.

## Objective

1. Configuration management best practices
   - constraint: all configuration data must reside in private GitLab repositories
   - constraint: avoid duplication between GitLab CI/CD variables and local development/runtime configuration
   - _deliverable_: a pros/cons comparison of `git submodule` versus a parallel checkout of a configuration repository (accessed via relative path, no symbolic links), with a final recommendation

2. GitLab environment support for multi-environment pipelines
   - pipeline targets: `development`, `testing`, `staging`, `production`
   - _deliverable_: a strategy, with a supporting table (environment → configuration source URL → resolution mechanism), for resolving the correct configuration URL per environment

3. Inter-repository authorisation (GitLab-to-GitLab and GitLab-to-GitHub)
   - constraint: authorisation is required only for CI/CD pipelines, not for local development
   - _deliverable_: an explanation of how default values declared in a `spec:inputs:` header can be overridden at pipeline trigger time, including which override mechanisms apply to protected branches/environments

4. Public container registry and secrets availability
   - constraint: `podman push` must work identically in GitLab pipelines and local development
   - constraint: the same applies to API access tokens and database credentials
   - _deliverable_: a table mapping each secret type to its storage location and retrieval mechanism, per context (pipeline vs. local)

5. Parallel container image builds
   - constraint: each container image is built as an independent parallel job
   - constraint: the job graph must implement a failure-aware dependency chain
   - _deliverable_: a description (or `.gitlab-ci.yml` sketch) of the job graph and its failure-handling behaviour

6. DevOps strategy synthesis
   - propose concrete operative procedures covering objectives 1–5
   - discuss critical points and compare the pros and cons of the alternatives considered
   - provide references to relevant online materials (articles, tutorials, discussions)

## Output Format

Reply in clear, lint-valid GitLab Flavored Markdown (GLFM):

- place codeblock delimiters (```) at the start of the line; avoid nested codeblocks
- use _underscore markup_ for emphasis
- prefer nested headings over asterisk-based text markup
- use dashes only for unordered lists, with correct indentation
- insert a blank line after every heading, list, and codeblock

Disregard the following non-standard formatting markup if encountered elsewhere:

- `<details><summary>` HTML blocks
- `{=latex}` codeblocks
- `[!tip]` / `[!note]` blockquotes
- triple-curly-brace code-folding tags
- internal links (e.g. `[^]`)

At the end of the response, list references to online documentation as Markdown footnotes, prefixed with `rf-` to avoid clashing with other references in the document, and link them inline to the relevant answer text.

Add any additional relevant information not explicitly requested, under an _Additional Notes_ section.



<details>
<summary></summary>

```{=latex}
\newpage
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

# A:1 (DeepSeek)

[^](#toc) **_TODO:(a1-ref-deepseek)_**

TODO:(a1-deepseek) ...

# A:1 (Perplexity)

[^](#toc) **_TODO:(a1-ref-perplexity)_**

TODO:(a1-perplexity) ...

# A:1 (Vibe)

[^](#toc) **_TODO:(a1-ref-vibe)_**

TODO:(a1-vibe) ...

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

# A:2 (DeepSeek)

[^](#toc) **_TODO:(a2-ref-deepseek)_**

TODO:(a2-deepseek) ...

# A:2 (Perplexity)

[^](#toc) **_TODO:(a2-ref-perplexity)_**

TODO:(a2-perplexity) ...

# A:2 (Vibe)

[^](#toc) **_TODO:(a2-ref-vibe)_**

TODO:(a2-vibe) ...

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

<!-- }}} \\ %a. -->
<!-- {{{ // %*
LocalWords:  GitLab CommonMark GFM GLFM YAML
vim: set foldmethod=marker :
}}} // %* -->
