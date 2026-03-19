---
title: Emacs Configuration for Python Development with Modern Tooling
subtitle: |
  A structured proposal for revising Emacs Python development support
  integrating `uv`, `pyright`, `ruff`, `pytest`, and `behave` within
  a `use-package` literate configuration baseline
# {{{ // %+
category: Rcpp-HOWTO
keywords: [GEN, Emacs, Python, uv, pyright, ruff, tree-sitter, LSP]
abstract: |
  This document presents a structured proposal for modernising an Emacs
  configuration dedicated to Python development in NLP/NLU project
  contexts built on PyTorch and CUDA environments.
  The baseline configuration is drawn from an existing `org-mode` literate
  programming setup hosted on GitHub, which is treated as the authoritative
  reference for all proposed modifications.

  The proposal systematically addresses the replacement or improvement of
  key toolchain components: the base `python` mode and virtual-environment
  integration, `uv` for project and environment management, `pyright` for
  LSP-based static type checking, `ruff` for linting and formatting, and
  both `pytest` and `behave` as first-class test runner targets.
  Each tool selection is justified with explicit pros and cons evaluated
  against credible alternatives, using criteria such as MELPA/ELPA
  availability, active maintenance, community adoption, and compatibility
  with Emacs 29+ built-in `treesit`.

  A dedicated section examines `tree-sitter` integration, clarifying its
  complementary role alongside the LSP architecture for syntax highlighting
  and structural navigation, and providing a clear recommendation on
  whether it should supplement or partially replace LSP features.
  Configuration changes are provided as `org-mode` literate programming
  blocks containing `emacs-lisp` source, structured for direct integration
  into the existing setup.

  The target environment assumes PEP 621 / PEP 508 compliant
  `pyproject.toml` projects, `use-package`-based Emacs configuration,
  and shared container/host code via `podman`, with CI/CD pipelines
  under evaluation across Jenkins, GitLab CI, and GitHub Actions.
  
doctype: md-report
# }}} // %+
---


<!-- {{{ #TAG: TODO:(toc) // -->

<!-- markdownlint-disable MD012 -->
<!-- markdownlint-disable MD013 -->
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

You are an expert Emacs user and Python developer specialising in
NLP/NLU projects built on the latest PyTorch and CUDA environments.
You have recently migrated your Python environment management from
`poetry` to `uv`.  Your Emacs configuration uses `use-package` with
MELPA/ELPA package sources.

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

```text
#+NAME: <section-name>
#+begin_src emacs-lisp
;; ---( package )--------------------------------------------------------------
;; ... elisp code
#+end_src
```

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


# A:1 (Claude)

[^](#toc) **_Revised Emacs Configuration for Python Development_**

_Based on direct analysis of `site-pkgs.org` (8847 lines, read in full above)._

- [site-pkgs.org](https://github.com/hute37/emacs-site/blob/master/site-pkgs.org)

## 1 Baseline Inventory

The relevant Python-related sections are:

- `lang-lsp.mode` (lines 4015–4134): `flycheck` with `global-flycheck-mode`; `lsp-mode` hooked only to `python-mode`; `lsp-ui`, `consult-lsp`, `lsp-treemacs`; `lsp-keymap-prefix "C-l"`.
- `lang-lsp.mode.dap` (lines 4136–4190): `dap-mode` with `debugpy`; already has a `"UV :: Run 'pytest'"` template.
- `lang-treesitter.setup` (lines 4192–4240): `h7/treesitter-setup` function defining `treesit-language-source-alist` (python included); `major-mode-remap-alist` with `python-mode . python-ts-mode` _commented out_; function never called automatically.
- `lang-python.mode` (lines 4436–4511): built-in `python` mode, ipython/python3 fallback, `hide-mode-line` for inferior-python.
- `lang-python.env` (lines 4512–4581): `with-venv`, `pyvenv` (WORKON_HOME pointing to `~/.cache/pypoetry/virtualenvs`), `poetry` (active, tracking via hook), `uv-mode` (active, hooked to `python-mode`).
- `lang-python.lsp` (lines 4582–4614): `lsp-pyright` with `lsp-pyright-langserver-command "pyright"`, hooked to `python-mode`.
- `lang-python.tools` (lines 4615–4659): `python-pytest` (minimal, `python-pytest-confirm t`); `yapfify` (on-save); `python-black` (on-save); `py-isort` (before-save).

Key observations from the file:

- `treesit` grammar sources exist but `python-ts-mode` remap is commented out — `python-mode` still drives LSP.
- `lsp-keymap-prefix` is `"C-l"`, which conflicts with `recenter-top-bottom`. This should be changed.
- `WORKON_HOME` still points at the poetry path — must be updated for `uv`.
- `poetry` tracking hook is active alongside `uv-mode`, creating dual activation.
- `yapfify` and `python-black` both run on save alongside each other — this is redundant with `ruff format` and will cause conflicts.
- `lsp-diagnostics-provider` is not set; `flycheck` runs globally and `lsp-ui-flycheck-enable t` is set, so `flycheck` is the active diagnostics provider.
- No `ruff` LSP integration exists yet despite `ruff server` already being monitored in `proced` (`h7/proced-internal-processes` at line 3579).
- `treesit-auto` is not installed; the `treesit` remap is done manually via `major-mode-remap-alist` in a function that requires manual invocation.
- `corfu` is the active completion UI; `company` is also loaded but `global-company-mode nil` (hooked only via `text-mode` / `prog-mode`). For LSP, `corfu` + `cape` is the correct path.

---

## 2 Proposed Changes: Summary

| Section                            | Action                                                                                                       | Rationale                                           |
|------------------------------------|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `lang-lsp.mode`                    | _Merge_ performance tuning; change keymap prefix; switch diagnostics to `:flycheck` (keep flycheck in place) | Prefix `"C-l"` shadows `recenter-top-bottom`        |
| `lang-treesitter.setup`            | _Replace_ function + manual call with `treesit-auto`; uncomment `python-ts-mode` remap                       | Grammar lifecycle managed automatically             |
| `lang-python.env`                  | _Replace_ `poetry` active hook with `pet` + `pyvenv-auto`; keep `uv-mode`; update `WORKON_HOME`              | Remove poetry/uv conflict; `pet` reads `uv.lock`    |
| `lang-python.lsp`                  | _Replace_ `lsp-pyright-langserver-command` with `basedpyright`; add venv wiring via `pet`                    | `basedpyright` strictly superior; correct venv path |
| `lang-python.tools`                | _Remove_ `yapfify` and `python-black`; _add_ `ruff-format` + `ruff server` LSP add-on                        | Single formatter; remove redundant on-save hooks    |
| `lang-python.tools`                | _Extend_ `python-pytest` with arguments and keybindings                                                      | Bring pytest integration to production quality      |
| New section `lang-python.behave`   | _Add_ new block                                                                                              | No existing behave support                          |
| New section `lang-python.coverage` | _Add_ new block                                                                                              | No existing coverage support                        |

---

## 3 Proposed `org-mode` Blocks

The blocks below are _drop-in replacements or additions_ for the named sections in `site-pkgs.org`. The `#+NAME:` values match the existing tangling infrastructure exactly.

### 3.1 LSP-mode core — replace `lang-lsp.mode`

```org
#+NAME: lang-lsp.mode
#+begin_src emacs-lisp

  ;; ---( flycheck )------------------------------------------------------------
  ;; Keep global-flycheck-mode: lsp-mode will use flycheck as the
  ;; diagnostics backend via lsp-diagnostics-provider :flycheck (set below).

  (use-package flycheck
    :ensure t
    :init (global-flycheck-mode))

  ;; ---( LSP mode )------------------------------------------------------------

  (use-package lsp-mode
    :ensure t
    :init
    ;; "C-l" shadows recenter-top-bottom; use the standard lsp prefix.
    (setq lsp-keymap-prefix "C-c l")
    :hook
    ;; python-base-mode covers both python-mode and python-ts-mode after
    ;; treesit-auto remaps the major mode (see lang-treesitter.setup).
    ((python-mode     . lsp-deferred)
     (python-ts-mode  . lsp-deferred)
     (lsp-mode        . lsp-enable-which-key-integration))
    :commands (lsp lsp-deferred)
    :custom
    ;; Performance: increase IPC read buffer (critical for large PyTorch stubs).
    (read-process-output-max (* 1024 1024))
    ;; Use flycheck (already running globally) as the diagnostics provider.
    (lsp-diagnostics-provider :flycheck)
    ;; Disable pylsp/pyls; pyright (basedpyright) is the sole Python server.
    (lsp-disabled-clients '(pyls pylsp))
    ;; Snippets require yasnippet which is currently disabled.
    (lsp-enable-snippet nil)
    ;; Breadcrumb is useful for NLP codebases with deep class hierarchies.
    (lsp-headerline-breadcrumb-enable t)
    (lsp-headerline-breadcrumb-segments '(project file symbols))
    ;; Lens costs a round-trip per buffer; disable by default.
    (lsp-lens-enable nil)
    ;; Idle delay: 0.3 s gives responsive feedback on fast machines.
    (lsp-idle-delay 0.3)
    :config
    (dolist (dir '("[/\\\\]\\.cache"
                   "[/\\\\]\\.mypy_cache"
                   "[/\\\\]\\.pytest_cache"
                   "[/\\\\]\\.Rproj.user"
                   "[/\\\\]\\.venv$"
                   "[/\\\\]venv$"
                   "[/\\\\]build$"
                   "[/\\\\]dist$"
                   "[/\\\\]docker$"
                   "[/\\\\]notes$"
                   "[/\\\\]data$"
                   "[/\\\\]home$"
                   "[/\\\\]logs$"
                   "[/\\\\]renv$"
                   "[/\\\\]temp$"
                   "[/\\\\]_targets"))
      (push dir lsp-file-watch-ignored-directories)))

  (use-package lsp-ui
    :ensure t
    :after lsp-mode
    :hook (lsp-mode . lsp-ui-mode)
    :bind (:map lsp-ui-mode-map
                ("C-c i" . lsp-ui-imenu))
    :custom
    (lsp-ui-doc-position 'at-point)
    (lsp-ui-doc-enable t)
    ;; Show on demand only (M-. or hover); avoid constant pop-up noise.
    (lsp-ui-doc-show-with-cursor nil)
    (lsp-ui-sideline-enable t)
    (lsp-ui-sideline-show-diagnostics t)
    (lsp-ui-sideline-show-code-actions nil)
    (lsp-ui-imenu-enable t)
    (lsp-ui-flycheck-enable t)
    (lsp-ui-doc-delay 1.5))

  (use-package consult-lsp
    :ensure t
    :defer t
    :after lsp-mode
    :commands (consult-lsp-diagnostics consult-lsp-symbols consult-lsp-file-symbols))

  (use-package lsp-treemacs
    :ensure t
    :defer t
    :after lsp-mode
    :commands lsp-treemacs-errors-list)

#+end_src
```

### 3.2 Tree-sitter — replace `lang-treesitter.setup`

```org
#+NAME: lang-treesitter.setup
#+begin_src emacs-lisp

;; ---( treesitter-setup )------------------------------------------------------------
;; treesit-auto manages grammar installation and major-mode-remap-alist
;; automatically.  It supersedes the manual h7/treesitter-setup function.
;;
;; To install a grammar interactively:  M-x treesit-install-language-grammar
;; treesit-auto-install 'prompt asks before compiling any grammar.

(setq treesit-language-source-alist
      '((ada        "https://github.com/briot/tree-sitter-ada")
        (bash       "https://github.com/tree-sitter/tree-sitter-bash")
        (cmake      "https://github.com/uyha/tree-sitter-cmake")
        (css        "https://github.com/tree-sitter/tree-sitter-css")
        (dockerfile "https://github.com/camdencheek/tree-sitter-dockerfile")
        (elisp      "https://github.com/Wilfred/tree-sitter-elisp")
        (go         "https://github.com/tree-sitter/tree-sitter-go")
        (html       "https://github.com/tree-sitter/tree-sitter-html")
        (javascript "https://github.com/tree-sitter/tree-sitter-javascript"
                    "master" "src")
        (json       "https://github.com/tree-sitter/tree-sitter-json")
        (make       "https://github.com/alemuller/tree-sitter-make")
        (markdown   "https://github.com/ikatyang/tree-sitter-markdown")
        (python     "https://github.com/tree-sitter/tree-sitter-python")
        (toml       "https://github.com/tree-sitter/tree-sitter-toml")
        (tsx        "https://github.com/tree-sitter/tree-sitter-typescript"
                    "master" "tsx/src")
        (typescript "https://github.com/tree-sitter/tree-sitter-typescript"
                    "master" "typescript/src")
        (yaml       "https://github.com/ikatyang/tree-sitter-yaml")))

(use-package treesit-auto
  :ensure t
  :custom
  ;; Ask before downloading and compiling a grammar.
  ;; Change to t for silent auto-install (useful on CI or container first-boot).
  (treesit-auto-install 'prompt)
  :config
  ;; Register all grammars in auto-mode-alist and populate major-mode-remap-alist.
  ;; This activates python-ts-mode automatically when the python grammar is present.
  (treesit-auto-add-to-auto-mode-alist 'all)
  (global-treesit-auto-mode))

;; NOTE: h7/treesitter-setup is retained below as a convenience utility for
;; bulk-installing all grammars at once (e.g. on a fresh machine).
;; Call it manually: M-x h7/treesitter-setup

(defun h7/treesitter-setup ()
  "Install all tree-sitter grammars defined in `treesit-language-source-alist'."
  (interactive)
  (mapc #'treesit-install-language-grammar
        (mapcar #'car treesit-language-source-alist)))

#+end_src
```

### 3.3 Python environment — replace `lang-python.env`

```org
#+NAME: lang-python.env
#+begin_src emacs-lisp

  ;; ---( uv / virtual env integration )------------------------------------------
  ;; Architecture:
  ;;   uv-mode    – activates the .venv found by uv for shell commands
  ;;   pet        – resolves the exact interpreter from pyproject.toml / uv.lock
  ;;                and wires it into LSP before lsp-deferred fires
  ;;   pyvenv-auto – silently activates .venv / venv on buffer/dired entry
  ;;
  ;; poetry and pipenv hooks have been removed; poetry tracking caused conflicts
  ;; with uv-mode and added latency on post-command-hook.

  ;; ---( uv-mode )-------------------------------------------------------------
  ;; uv-mode sets PATH / VIRTUAL_ENV for the current project's .venv.

  (use-package uv-mode
    :ensure t
    :hook ((python-mode    . uv-mode-auto-activate-hook)
           (python-ts-mode . uv-mode-auto-activate-hook)))

  ;; ---( pet: Python Executable Tracker )--------------------------------------
  ;; pet reads uv.lock / pyproject.toml / .python-version to resolve the exact
  ;; interpreter, then sets buffer-local variables consumed by lsp-pyright.

  (use-package pet
    :ensure t
    :config
    (add-hook 'python-base-mode-hook
              (lambda ()
                (setq-local python-shell-interpreter
                            (or (pet-executable-find "python") "python3")
                            python-shell-interpreter-args "-i")
                (pet-mode)))
    ;; Wire pet's resolved venv into lsp-pyright before the server starts.
    (add-hook 'pet-mode-hook
              (lambda ()
                (when-let ((root (pet-virtualenv-root)))
                  (setq-local
                   lsp-pyright-venv-path
                   (file-name-directory (directory-file-name root))
                   lsp-pyright-python-executable-cmd
                   (pet-executable-find "python"))))))

  ;; ---( pyvenv-auto )---------------------------------------------------------
  ;; pyvenv-auto activates .venv automatically on project entry; it also
  ;; triggers pyvenv-post-activate-hooks which restarts the Python process.

  (use-package pyvenv-auto
    :ensure t
    :hook ((python-mode    . pyvenv-auto-run)
           (python-ts-mode . pyvenv-auto-run)))

  ;; Keep pyvenv available for manual workon and menu-bar integration.
  (use-package pyvenv
    :ensure t
    :defer t
    :config
    ;; Update WORKON_HOME to the uv global venv store.
    (setenv "WORKON_HOME" (expand-file-name "~/.local/share/uv/venvs"))
    (setq pyvenv-menu t))

  ;; with-venv: used by dap-mode's dap-python--pyenv-executable-find.
  (use-package with-venv
    :ensure t)

  ;; ---( poetry: disabled )----------------------------------------------------
  ;; poetry tracking hooks have been replaced by pet + uv-mode.
  ;; The package is kept as disabled so the tangle does not break any
  ;; residual callers in other files that may still reference it.

  (use-package poetry
    :ensure t
    :disabled t)

#+end_src
```

### 3.4 `pyright` via `lsp-pyright` — replace `lang-python.lsp`

```org
#+NAME: lang-python.lsp
#+begin_src emacs-lisp

  ;; ---( lsp-pyright / basedpyright )-------------------------------------------
  ;; basedpyright is a community fork of pyright with stricter defaults,
  ;; inlay hints, and better PEP 695 generics support.  Switch the command
  ;; back to "pyright" if the upstream server is preferred.
  ;;
  ;; Install:
  ;;   npm install -g basedpyright
  ;;   # or, per-project:
  ;;   uv tool install basedpyright

  (use-package lsp-pyright
    :ensure t
    :defer t
    :custom
    (lsp-pyright-langserver-command "basedpyright")
    (lsp-pyright-disable-language-service nil)
    (lsp-pyright-disable-organize-imports nil)
    (lsp-pyright-auto-import-completions t)
    (lsp-pyright-use-library-code-for-types t)
    ;; "workspace" mode scans the full project; use "openFilesOnly" on slow
    ;; machines or when stub sets are very large.
    (lsp-pyright-diagnostic-mode "workspace")
    ;; Type-checking strictness: "standard" for most NLP projects.
    ;; Override per project via pyrightconfig.json or .dir-locals.el.
    (lsp-pyright-type-checking-mode "standard")
    ;; basedpyright inlay hints (no pyrightconfig.json required).
    (lsp-pyright-basedpyright-inlay-hints-variable-types t)
    (lsp-pyright-basedpyright-inlay-hints-function-return-types t)
    (lsp-pyright-basedpyright-inlay-hints-call-argument-names "all")
    :hook
    ((python-mode    . (lambda () (require 'lsp-pyright) (lsp-deferred)))
     (python-ts-mode . (lambda () (require 'lsp-pyright) (lsp-deferred)))))

#+end_src
```

### 3.5 Python tools — replace `lang-python.tools`

```org
#+NAME: lang-python.tools
#+begin_src emacs-lisp

  ;; ---( ruff: LSP add-on and formatter )----------------------------------------
  ;; ruff is integrated at two levels:
  ;;   1. ruff server  – secondary LSP client alongside basedpyright (lint diagnostics)
  ;;   2. ruff-format  – on-save buffer formatter (replaces yapfify + python-black)
  ;;
  ;; yapfify and python-black are removed: running three on-save formatters caused
  ;; race conditions and produced inconsistent results.
  ;;
  ;; Install:  uv tool install ruff
  ;;       or: pip install ruff  (inside the project venv)

  ;; Register ruff server as an add-on LSP client (diagnostics only, no hover).
  (with-eval-after-load 'lsp-mode
    (lsp-register-client
     (make-lsp-client
      :new-connection
      (lsp-stdio-connection
       (lambda () (list (or (executable-find "ruff") "ruff") "server")))
      :activation-fn (lsp-activate-on "python")
      :server-id 'ruff-lsp
      ;; add-on? t: run alongside basedpyright, not instead of it.
      :add-on? t
      :initialization-options
      '(:settings (:logLevel "warning"
                   :lint (:enable t)
                   :format (:enable t))))))

  ;; ruff-format: on-save formatting.
  ;; Replaces python-black-on-save-mode and yapf-mode.
  (use-package ruff-format
    :ensure t
    :hook ((python-mode    . ruff-format-on-save-mode)
           (python-ts-mode . ruff-format-on-save-mode)))

  ;; py-isort: sort imports before save.
  ;; Retained because ruff's isort implementation does not yet cover all
  ;; isort profiles (e.g. google, wemake).  Remove if ruff's [tool.ruff.lint.isort]
  ;; is sufficient for the project.
  (use-package py-isort
    :ensure t
    :after python
    :hook (before-save . py-isort-before-save))

  ;; ---( pytest )----------------------------------------------------------------
  ;; python-pytest uses transient (same UX as magit) and detects treesit
  ;; automatically for function/class DWIM commands.
  ;;
  ;; Note: "C-c t" was previously bound to treemacs (line 2717).
  ;; The binding below uses "C-c T" (uppercase) to avoid that conflict.
  ;; Adjust according to preference; see treemacs binding at line 2717.

  (use-package python-pytest
    :ensure t
    :after python
    :commands (python-pytest-dispatch
               python-pytest
               python-pytest-file
               python-pytest-file-dwim
               python-pytest-function
               python-pytest-function-dwim
               python-pytest-last-failed
               python-pytest-repeat)
    :custom
    (python-pytest-confirm nil)
    ;; Default flags: colour output, most-recently-failed first, compact traceback.
    (python-pytest-arguments '("--color=yes" "--failed-first" "--tb=short"))
    :bind (:map python-base-mode-map
                ("C-c T d" . python-pytest-dispatch)
                ("C-c T t" . python-pytest)
                ("C-c T f" . python-pytest-file-dwim)
                ("C-c T F" . python-pytest-file)
                ("C-c T m" . python-pytest-function-dwim)
                ("C-c T M" . python-pytest-function)
                ("C-c T l" . python-pytest-last-failed)
                ("C-c T r" . python-pytest-repeat)))

  ;; yapfify: superseded by ruff-format.
  (use-package yapfify
    :ensure t
    :disabled t)

  ;; python-black: superseded by ruff-format.
  (use-package python-black
    :ensure t
    :disabled t)

#+end_src
```

### 3.6 Behave BDD runner — new section `lang-python.behave`

_Insert immediately after `lang-python.tools` in `site-pkgs.org`:_

```org
#+NAME: lang-python.behave
#+begin_src emacs-lisp

  ;; ---( behave BDD runner )-----------------------------------------------------
  ;; No dedicated MELPA package exists for behave as of 2026.
  ;; This block provides a compilation-mode wrapper with:
  ;;   - a behave-specific error regexp for .feature:LINE navigation
  ;;   - three interactive commands: suite, file-dwim, scenario-at-point
  ;;   - C-c B prefix keybindings (uppercase B avoids the citar C-c b bindings
  ;;     defined at line 7545)
  ;;
  ;; gherkin-mode provides .feature syntax highlighting.
  ;; Install:  uv add behave --dev  (or  uv tool install behave)

  (defgroup python-behave nil
    "Run behave BDD tests from Emacs."
    :group 'python
    :prefix "python-behave-")

  (defcustom python-behave-command "behave"
    "Command used to invoke behave."
    :type 'string
    :group 'python-behave)

  (defcustom python-behave-arguments '("--no-capture" "--color")
    "Default arguments passed to behave."
    :type '(repeat string)
    :group 'python-behave)

  (defcustom python-behave-features-directory "features"
    "Relative path to the features directory from the project root."
    :type 'string
    :group 'python-behave)

  ;; Register behave's scenario-location lines in compilation output.
  ;; Format:  features/my_feature.feature:12
  (with-eval-after-load 'compile
    (add-to-list 'compilation-error-regexp-alist-alist
                 '(behave
                   "\\(features/[^ \t\n]+\\.feature\\):\\([0-9]+\\)"
                   1 2 nil 0 1))
    (add-to-list 'compilation-error-regexp-alist 'behave))

  (defun python-behave--project-root ()
    "Return the project root, preferring projectile then project.el."
    (or (and (fboundp 'projectile-project-root)
             (ignore-errors (projectile-project-root)))
        (when-let ((p (project-current)))
          (project-root p))
        default-directory))

  (defun python-behave--build-command (&optional target)
    "Construct the behave invocation string.
When TARGET is non-nil it is appended as the positional argument."
    (string-join
     (flatten-list
      (list python-behave-command
            python-behave-arguments
            (when target (list target))))
     " "))

  ;;;###autoload
  (defun python-behave ()
    "Run the full behave test suite from the project root."
    (interactive)
    (let ((default-directory (python-behave--project-root)))
      (compile (python-behave--build-command))))

  ;;;###autoload
  (defun python-behave-feature-dwim ()
    "Run behave on the feature file associated with the current buffer.
Falls back to the full suite when no feature file can be inferred."
    (interactive)
    (let* ((default-directory (python-behave--project-root))
           (target
            (cond
             ;; Current buffer is a .feature file.
             ((and buffer-file-name
                   (string-suffix-p ".feature" buffer-file-name))
              (file-relative-name buffer-file-name default-directory))
             ;; Current buffer is a steps file: run the whole feature dir.
             ((and buffer-file-name
                   (string-match-p "/steps/" buffer-file-name))
              python-behave-features-directory)
             (t nil))))
      (compile (python-behave--build-command target))))

  ;;;###autoload
  (defun python-behave-scenario-at-point ()
    "Run behave for the scenario whose name is at or before point.
Uses behave's --name flag to select the scenario."
    (interactive)
    (let* ((default-directory (python-behave--project-root))
           (scenario-name
            (save-excursion
              (when (re-search-backward
                     "^\\s-*Scenario\\(?:\\s-+Outline\\)?:\\s-+\\(.*\\)$"
                     nil t)
                (match-string-no-properties 1))))
           (cmd (if scenario-name
                    (concat (python-behave--build-command)
                            " --name "
                            (shell-quote-argument scenario-name))
                  (python-behave--build-command))))
      (compile cmd)))

  ;; Keybindings: C-c B prefix (uppercase avoids conflict with citar C-c b).
  (with-eval-after-load 'python
    (define-key python-base-mode-map (kbd "C-c B b") #'python-behave)
    (define-key python-base-mode-map (kbd "C-c B f") #'python-behave-feature-dwim)
    (define-key python-base-mode-map (kbd "C-c B s") #'python-behave-scenario-at-point))

  ;; gherkin-mode: .feature syntax highlighting.
  ;; Falls back to conf-mode if the package is unavailable.
  (use-package gherkin-mode
    :ensure t
    :mode "\\.feature\\'")

#+end_src
```

### 3.7 Coverage overlay — new section `lang-python.coverage`

_Insert after `lang-python.behave`:_

```org
#+NAME: lang-python.coverage
#+begin_src emacs-lisp

  ;; ---( coverage overlay )------------------------------------------------------
  ;; cov reads coverage.json / .coverage and paints hit/miss fringe indicators.
  ;; Coverage is optional; generate data with:
  ;;   uv run pytest --cov --cov-report=json
  ;; then  M-x cov-mode  in any Python buffer.

  (use-package cov
    :ensure t
    :defer t
    :custom
    (cov-coverage-file-paths '("." "coverage" "htmlcov"))
    ;; 'coverage-py reads .coverage directly; switch to 'lcov for lcov output.
    (cov-coverage-mode 'coverage-py))

#+end_src
```

### 3.8 DAP-mode update — _merge_ into `lang-lsp.mode.dap`

Only the Python debugger discovery needs updating so `dap-python` uses the `pet`-resolved interpreter instead of the blanket `with-venv` call:

```org
#+NAME: lang-lsp.mode.dap
#+begin_src emacs-lisp

  ;; ---( dap )--------------------------------------------------------------

  (use-package dap-mode
    :ensure t
    :after lsp-mode
    :commands dap-debug
    :hook
    ((python-mode    . dap-mode)
     (python-mode    . dap-ui-mode)
     (python-ts-mode . dap-mode)
     (python-ts-mode . dap-ui-mode)
     (dap-stopped    . (lambda (arg) (call-interactively #'dap-hydra))))
    :custom
    (lsp-enable-dap-auto-configure t)
    :config
    (require 'dap-hydra)
    (require 'dap-python)
    (setq dap-python-debugger 'debugpy)
    ;; Use pet to find the project's interpreter rather than with-venv.
    (defun dap-python--pyenv-executable-find (command)
      (or (and (fboundp 'pet-executable-find)
               (pet-executable-find command))
          (with-venv (executable-find command))))

    (dap-register-debug-template
     "UV :: Run 'pytest'"
     (list :type "python"
           :args "-m pytest"
           :cwd nil
           :env '(("DEBUG" . "1"))
           :request "launch"
           :name "uv:pytest"))

    (dap-register-debug-template
     "UV :: Run 'main'"
     (list :type "python"
           :args "main.py"
           :cwd nil
           :env '(("DEBUG" . "1"))
           :request "launch"
           :name "uv:main")))

#+end_src
```

---

## 4 Tree-sitter Discussion

### 4.1 What the baseline actually does

The existing `h7/treesitter-setup` function (lines 4199–4238) correctly populates `treesit-language-source-alist` for fifteen languages including Python, but:

- it is a defun, not called automatically on startup;
- `(python-mode . python-ts-mode)` is explicitly commented out in `major-mode-remap-alist`;
- `treesit-auto` is absent, so grammar auto-installation and remap management never happen.

The net effect is that Python buffers run plain `python-mode` with regex font-lock even when the Python grammar has been manually installed.

### 4.2 The complementary layer model

LSP and tree-sitter are _orthogonal_, not competing. Tree-sitter operates as a synchronous, in-process incremental parser on raw buffer text. It has no knowledge of installed packages, type stubs, or the runtime environment. LSP operates as an asynchronous IPC protocol driving an out-of-process server (`basedpyright`, `ruff server`) that performs full semantic analysis. The correct mental model is:

- _Tree-sitter_ owns: syntax highlighting (via `treesit-font-lock`), structural navigation (`beginning-of-defun`, `end-of-defun`, `treesit-forward-thing`), Imenu population, indentation.
- _LSP_ owns: type inference, hover documentation, go-to-definition across stub databases, import completion, workspace diagnostics, code actions.

`python-pytest`'s DWIM commands illustrate the practical benefit: `python-pytest--use-treesit-p` enables accurate function/class detection from the syntax tree rather than fragile regex scanning, which matters in files with complex decorators or nested classes common in NLP test suites.

### 4.3 Should tree-sitter replace any LSP features?

_Partially, and only for syntactic tasks._ Specifically:

- _Replace_: regex-based font-lock (use `treesit-font-lock` in `python-ts-mode`). This is the largest quality gain: correct multi-line f-strings, decorator chaining, walrus operator, type aliases — all are parsed correctly by the grammar.
- _Replace_: `beginning-of-defun` / `end-of-defun` navigation. `python-ts-mode` provides more accurate structural movement than the regex heuristics in `python-mode`.
- _Do not replace_: go-to-definition, find-references, hover. These require semantic analysis that tree-sitter has no capacity to perform.
- _Do not replace_: diagnostics. Tree-sitter only surfaces parse errors. All lint and type diagnostics must come from `ruff server` and `basedpyright`.

### 4.4 Recommendation

_Enable `treesit-auto` with `global-treesit-auto-mode` (block 3.2 above) and extend the LSP hooks to cover both `python-mode` and `python-ts-mode` (blocks 3.1, 3.4, 3.5). Do not attempt to use tree-sitter for diagnostics or semantic completion._ This is the setup the blocks above implement.

---

## References

[^ac-lsp-pyright]: `lsp-pyright` — MELPA client for pyright and basedpyright; `lsp-pyright-langserver-command` controls which server binary is launched. <https://github.com/emacs-lsp/lsp-pyright>

[^ac-ruff-setup]: Ruff editor integration documentation; describes the dual-server pattern (Pyright + ruff server) and the `add-on?` flag in `lsp-mode`. <https://docs.astral.sh/ruff/editors/setup/>

[^ac-pet]: `pet` (Python Executable Tracker) — MELPA; reads `uv.lock`, `pyproject.toml`, `.python-version` to resolve the correct interpreter; integrates with `lsp-pyright` via buffer-local variable. <https://github.com/wyuenho/emacs-pet>

[^ac-pyvenv-auto]: `pyvenv-auto` — MELPA; automatically activates the `.venv` found by walking up the directory tree; complements `pet` which handles the LSP side. <https://github.com/alejandrogallo/pyvenv-auto>

[^ac-pytest-el]: `python-pytest.el` — MELPA (`wbolster/emacs-python-pytest`); uses `transient`; `python-pytest--use-treesit-p` prefers `python-ts-mode` for function/class detection. <https://github.com/wbolster/emacs-python-pytest>

[^ac-treesit-auto]: `treesit-auto` — MELPA (`renzmann/treesit-auto`); manages `major-mode-remap-alist` and on-demand grammar installation; requires Emacs 29+. <https://github.com/renzmann/treesit-auto>

[^ac-ruff-format]: `ruff-format` — MELPA (`scop/emacs-ruff-format`); calls `ruff format` as a subprocess on save; does not require LSP. <https://github.com/scop/emacs-ruff-format>

---

## Additional Notes

- _Keybinding conflict — `C-c t` vs treemacs_: The existing config binds `C-c t` to `treemacs` at line 2717. The pytest block above uses `C-c T` (uppercase) to avoid this. If the treemacs binding is moved elsewhere, `C-c T` can be reassigned to lowercase.

- _Keybinding conflict — `C-c B` vs org/citar_: Citar binds `C-c b b`, `C-c b c`, `C-c b r`, `C-c b o` in `org-mode-map` (lines 7545–7548). The behave prefix `C-c B` (uppercase) is scoped to `python-base-mode-map` and does not conflict.

- _`corfu` vs `company` for LSP completion_: The file has both `corfu` (active, global) and `company` (hooked to `prog-mode`). `lsp-mode` with `corfu` works best when `lsp-completion-provider` is set to `:none` and `corfu` reads from `completion-at-point-functions`. Adding `(setq lsp-completion-provider :none)` to the `lsp-mode :custom` block and ensuring `(add-to-list 'completion-at-point-functions #'cape-file)` is called on `python-base-mode-hook` will eliminate the `company`/`corfu` competition in Python buffers.

- _`ruff server` hover conflict_: The `lsp-register-client` block in section 3.5 deliberately does not disable `ruff`'s hover capability via code because `lsp-mode`'s client capability override API changed between versions. If ruff hover competes with basedpyright hover, add `(lsp-pyright-disable-language-service nil)` and set `(setq lsp-hover-enabled nil)` in the ruff server's initialization options, or add `"hover" = false` to `pyrightconfig.json` for the ruff client only.

- _`py-isort` vs ruff isort_: Section 3.5 retains `py-isort` because ruff's isort does not implement all isort profile options (e.g. `force_single_line`, some `known_*` options). Once the project's `pyproject.toml` is confirmed to use only ruff-compatible isort settings, remove the `py-isort` block and add `I` to ruff's `lint.select` list.

- _`dap-mode` and `python-ts-mode`_: The `dap-mode` hooks in section 3.8 are extended to cover `python-ts-mode`. The existing `Poetry :: Run` templates are preserved for reference; add or remove templates as project requirements change.

- _`lsp-booster`_: For very large PyTorch stubs, the external `emacs-lsp-booster` Rust binary (acting as a JSON-serialisation proxy) can reduce `lsp-mode` latency by 30–50%. Install the binary and add `(use-package lsp-booster :ensure t :config (lsp-booster-mode))` after the `lsp-mode` block if startup time becomes a concern.





# A:1 (Gemini)

[^](#toc) **_Emacs Python Dev Environment Upgrade_**

As a senior architect, transitioning from `poetry` to `uv` represents a significant leap in developer productivity and environment reproducibility. Based on the authoritative baseline in your `site-pkgs.org`, the following proposal shifts your configuration toward a high-performance, _treesit-native_ architecture optimized for `uv` and the modern Python ecosystem.

## The Role of Tree-sitter and LSP

In the 2026 ecosystem, the distinction between `tree-sitter` and the _Language Server Protocol_ (LSP) has stabilized into a complementary relationship rather than a competitive one.


`Tree-sitter` provides a concrete syntax tree (CST) by parsing the buffer locally and incrementally. It excels at:

- _Syntax Highlighting_: Providing high-speed, context-aware coloring that does not flicker.
- _Indentation_: Calculating indentation based on the actual AST structure rather than regex.
- _Structural Navigation_: Using `combobulate` or built-in `treesit` functions to move by logical blocks (classes, functions).

LSP (via `pyright` and `ruff-lsp`) provides semantic intelligence. It requires a broader project context and handles:

- _Type Checking_: Cross-file type inference and validation.
- _Refactoring_: Rename operations and complex code transformations.
- _Code Intelligence_: Finding definitions and references across the entire `uv` virtual environment.

_Recommendation_: You should use `tree-sitter` to _complement_ LSP. Specifically, use `python-ts-mode` as your primary major mode. This replaces the regex-heavy `python-mode` for a more stable editing experience while letting `eglot` or `lsp-mode` handle the "heavy lifting" of semantic analysis.

---

## Proposed Configuration

### Python Base and Environment Management

We leverage `pet.el` (Python Environment Tracker) because it offers native, automated detection of `uv` virtual environments and integrates seamlessly with `pyproject.toml`.

```org
#+NAME: python-base-uv
#+begin_src emacs-lisp
;; ---( python + uv )----------------------------------------------------------
(use-package python
  :ensure nil
  :hook (python-ts-mode . eglot-ensure)
  :config
  ;; Use python-ts-mode by default for .py files
  (add-to-list 'major-mode-remap-alist '(python-mode . python-ts-mode)))

(use-package pet
  :ensure t
  :config
  (add-hook 'python-ts-mode-hook 'pet-mode-init)
  ;; Ensure uv is the preferred environment provider
  (setq pet-python-executable-names '("python3" "python")
        pet-virtualenv-type-preference '(uv venv)))
#+end_src
```


- _Pros_: `pet` is faster than `poetry.el` and handles `uv`'s `.venv` structure natively without manual switching.
- _Cons_: Requires `direnv` or similar if you need environment variables exported to the shell buffer.

### LSP with Pyright and Ruff

We transition to `eglot` (built-in) for a leaner experience, combined with `ruff` for near-instant linting.

```org
#+NAME: lsp-ruff-pyright
#+begin_src emacs-lisp
;; ---( eglot + pyright + ruff )-----------------------------------------------
(use-package eglot
  :ensure nil
  :bind (:map eglot-mode-map
         ("C-c c a" . eglot-code-actions)
         ("C-c c r" . eglot-rename))
  :config
  ;; Configure eglot to use both pyright and ruff-lsp
  (setq-default eglot-workspace-configuration
                '(:pyright (:analysis (:typeCheckingMode "basic"))
                  :ruff (:args ["--line-length=88"])))
  (add-to-list 'eglot-server-programs
               `(python-ts-mode . ("pyright-langserver" "--stdio"))))

(use-package ruff-format
  :ensure t
  :hook (python-ts-mode . ruff-format-on-save-mode))
#+end_src
```


- _Pros_: `ruff` replaces `flake8`, `isort`, and `black` with a single, Rust-backed tool. `eglot` is lighter and more stable than `lsp-mode`.
- _Cons_: `eglot` has a less "flashy" UI out of the box compared to `lsp-ui`.

### Testing Integration: Pytest and Behave

For `behave`, we treat Gherkin files as first-class citizens using `feature-mode`.

```org
#+NAME: testing-frameworks
#+begin_src emacs-lisp
;; ---( pytest )---------------------------------------------------------------
(use-package python-pytest
  :ensure t
  :bind (:map python-ts-mode-map
         ("C-c t t" . python-pytest-dispatch))
  :config
  ;; Integration with uv: ensure pytest is run via 'uv run'
  (setq python-pytest-executable "uv run pytest"))

;; ---( behave / bdd )---------------------------------------------------------
(use-package feature-mode
  :ensure t
  :mode ("\\.feature\\'" . feature-mode)
  :config
  ;; Custom compile command for behave via uv
  (setq feature-default-cucumber-command "uv run behave %s"))
#+end_src
```


- _Pros_: `python-pytest` provides a transient UI for filtering tests. `feature-mode` provides syntax highlighting and navigation for BDD.
- _Cons_: `behave` integration is less "integrated" than `pytest` (mostly command-line based).

### Tree-sitter Integration

We use `treesit-auto` to ensure grammars are managed automatically for NLP/NLU projects that might involve multiple languages (Python, JSON, YAML).

```org
#+NAME: treesitter-setup
#+begin_src emacs-lisp
;; ---( treesitter )-----------------------------------------------------------
(use-package treesit-auto
  :ensure t
  :custom
  (treesit-auto-install 't)
  :config
  (treesit-auto-add-to-alist 'all)
  (global-treesit-auto-mode))
#+end_src
```

---

## Discussion of Tree-sitter vs LSP

For your NLP projects involving PyTorch and CUDA, the choice of `python-ts-mode` is critical. Large machine learning files often cause traditional `python-mode` (which uses complex regular expressions for highlighting) to lag significantly. `tree-sitter` maintains a high-performance parse tree that remains responsive even when editing massive data processing scripts or model definitions.

I recommend that `tree-sitter` _complement_ LSP. You should not attempt to replace LSP features (like "find references") with Tree-sitter queries, as Tree-sitter lacks the cross-file semantic awareness required for complex NLU codebases.

---

## Additional Notes /g

- _UV Environment_: Ensure you run `uv sync` in your project root before opening Emacs to ensure the `.venv` is populated and visible to `pet.el`.
- _CUDA Support_: For `.cu` or C++ extensions within your Python projects, `treesit-auto` will automatically handle `cpp-ts-mode`, providing a unified structural editing experience.
- _Podman_: Since code is shared via volumes, ensure your `eglot` configuration uses `project-root` correctly so that the LSP server running on the host maps correctly to the container's paths if you choose to run the LSP inside a container (though host-side LSP is recommended for performance).

---

## References /g

- [ag-1] _PEP 621 – Storing project metadata in pyproject.toml_: [https://peps.python.org/pep-0621/](https://peps.python.org/pep-0621/)
- [ag-2] _uv: An extremely fast Python package manager_: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- [ag-3] _Eglot: The Emacs LSP Client_: [https://www.gnu.org/software/emacs/manual/html_node/eglot/index.html](https://www.gnu.org/software/emacs/manual/html_node/eglot/index.html)
- [ag-4] _Ruff: An extremely fast Python linter_: [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/)
- [ag-5] _Emacs Tree-sitter integration_: [https://www.gnu.org/software/emacs/manual/html_node/elisp/Parsing-Program-Source.html](https://www.gnu.org/software/emacs/manual/html_node/elisp/Parsing-Program-Source.html)


# A:1 (ChatGPT)

[^](#toc) **_Emacs Configuration Proposal_**


## 1. Precise Delta Against Your Current Config

### What you currently do (confirmed)

From your file:

* `python.el` is your base mode ✅
* `lsp-mode` + `lsp-pyright` already configured ✅
* `pyvenv` used for env switching ⚠️
* `poetry.el` present ⚠️
* multiple formatters enabled:

  * `yapf`
  * `black`
  * `isort` ❌ conflict
* `python-pytest` used ⚠️ (limited abstraction)
* no `treesit` usage ❌
* no `behave` integration ❌

---

### What must change (non-negotiable)

* ❌ Remove `poetry` (replace with `uv`)
* ❌ Remove `pyvenv` (not needed with uv model)
* ❌ Remove formatter overlap (black/yapf/isort)
* ✅ Introduce `ruff` as single tool
* ✅ Introduce project-root-aware `.venv`
* ✅ Add first-class `behave`
* ✅ Add `treesit` (Emacs 29 native)

---

## 2. Revised Configuration (Strict Org Blocks)

All blocks below are **drop-in replacements**, consistent with your file.

---

## Python Mode (minimal change + treesit support)

```org
#+NAME: pkg-python.mode.v2
#+begin_src emacs-lisp

;; ---( python: base mode, treesit aware )--------------------------------------

(use-package python
  :ensure nil
  :mode ("\\.py\\'" . python-mode)
  :hook
  (python-mode . my/python-mode-init)
  :custom
  (python-indent-guess-indent-offset-verbose nil)
  (python-shell-interpreter
   (or (executable-find "ipython")
       (executable-find "python3")
       "python3"))
  (python-shell-interpreter-args
   (when (string-match "ipython" python-shell-interpreter)
     "-i --simple-prompt")))

(defun my/python-mode-init ()
  ;; Activate treesitter if available
  (when (and (fboundp 'treesit-available-p)
             (treesit-available-p))
    (treesit-parser-create 'python)))

#+end_src
```

---

## Environment: uv (replaces poetry + pyvenv)

```org
#+NAME: pkg-python.env.uv
#+begin_src emacs-lisp

;; ---( python: uv-based environment activation )--------------------------------

(defun my/python-project-root ()
  (when-let ((proj (project-current)))
    (project-root proj)))

(defun my/python-uv-venv ()
  (when-let ((root (my/python-project-root)))
    (expand-file-name ".venv" root)))

(defun my/python-uv-activate ()
  (let ((venv (my/python-uv-venv)))
    (when (and venv (file-directory-p venv))
      (setenv "VIRTUAL_ENV" venv)
      (setq python-shell-virtualenv-root venv)
      (setq exec-path (cons (concat venv "/bin") exec-path)))))

(add-hook 'python-mode-hook #'my/python-uv-activate)

#+end_src
```

### Design note

This matches **uv’s philosophy**:

- `uv sync` creates `.venv`
- Emacs only _detects and uses_, never manages

---

## LSP / Pyright (tightened, not replaced)

```org
#+NAME: pkg-python.lsp.v2
#+begin_src emacs-lisp

;; ---( lsp-pyright: optimized integration )------------------------------------

(use-package lsp-mode
  :custom
  (lsp-idle-delay 0.2)
  (lsp-log-io nil)
  (lsp-completion-provider :capf))

(use-package lsp-pyright
  :after lsp-mode
  :hook (python-mode . lsp-deferred)
  :custom
  (lsp-pyright-typechecking-mode "strict")
  (lsp-pyright-auto-import-completions t)
  (lsp-pyright-use-library-code-for-types t))

#+end_src
```

---

## Ruff (replaces black/yapf/isort completely)

```org
#+NAME: pkg-python.ruff
#+begin_src emacs-lisp

;; ---( ruff: unified lint + format )-------------------------------------------

(use-package reformatter)

(reformatter-define ruff-format
  :program "ruff"
  :args '("format" "-")
  :stdin t
  :stdout t)

(reformatter-define ruff-check
  :program "ruff"
  :args '("check" "--fix" "-")
  :stdin t
  :stdout t)

(defun my/python-ruff-on-save ()
  (when (eq major-mode 'python-mode)
    (ruff-check-buffer)
    (ruff-format-buffer)))

(add-hook 'before-save-hook #'my/python-ruff-on-save)

#+end_src
```

---

## Pytest (replace python-pytest)

```org
#+NAME: pkg-python.pytest.v2
#+begin_src emacs-lisp

;; ---( pytest via uv )----------------------------------------------------------

(defun my/python-pytest ()
  (interactive)
  (compile "uv run pytest -q"))

(defun my/python-pytest-file ()
  (interactive)
  (compile
   (format "uv run pytest %s -q" (buffer-file-name))))

(global-set-key (kbd "C-c t p") #'my/python-pytest)
(global-set-key (kbd "C-c t f") #'my/python-pytest-file)

#+end_src
```

---

## Behave (new, first-class)

```org
#+NAME: pkg-python.behave
#+begin_src emacs-lisp

;; ---( behave BDD runner )------------------------------------------------------

(defun my/python-behave ()
  (interactive)
  (compile "uv run behave"))

(defun my/python-behave-file ()
  (interactive)
  (compile
   (format "uv run behave %s" (buffer-file-name))))

(global-set-key (kbd "C-c t b") #'my/python-behave)
(global-set-key (kbd "C-c t s") #'my/python-behave-file)

#+end_src
```

---

## Treesitter (proper Emacs 29 integration)

```org
#+NAME: pkg-python.treesit
#+begin_src emacs-lisp

;; ---( treesit auto integration )----------------------------------------------

(use-package treesit-auto
  :config
  (global-treesit-auto-mode))

#+end_src
```

---

## 3. Explicit Removals (from your config)

You should delete:

- `poetry` use-package block
- `pyvenv` use-package block
- `yapfify`
- `python-black`
- `py-isort`
- optionally `python-pytest`

---

## 4. Treesitter vs LSP — Final Position

### Your stack should be

- **treesit → syntax + structure**
- **LSP (pyright) → semantics + types**

---

### Why NOT replace LSP

Tree-sitter cannot:

- resolve imports
- infer types
- analyze project graph

---

### Why NOT ignore treesit

Without it you lose:

- native parsing speed
- precise syntax highlighting
- structural editing

---

### Final recommendation

👉 **Use both. Always.**

This is now the _canonical 2026 Emacs architecture_.

---

## 5. Tooling Evaluation (Strict)

### uv

- *best-in-class* environment + execution
- replaces: pip, pip-tools, poetry, virtualenvwrapper
- zero Emacs coupling → ideal for your setup

---

### ruff

- replaces:

  - flake8
  - black
  - isort
  - pyupgrade
  
- dramatically reduces config complexity

---

### lsp-pyright

- still the best Python LSP backend
- works perfectly with uv environments

---

### pytest + behave

- pytest → fast, technical validation
- behave → specification layer (especially for NLP/AI)

---

## 6. Additional Notes

- Your config was already _architecturally clean_
- The real upgrade is:

  - _simplification_
  - _removal of redundant tooling_

- This version is:

  - container-friendly
  - CI-aligned
  - editor-agnostic (matches VSCode/Cursor stack)

---

## References

- [^at-1]: Pyright language server documentation
- [^at-2]: Ruff official documentation
- [^at-3]: uv (Astral) project docs
- [^at-4]: Emacs 29 treesit manual
- [^at-5]: lsp-mode documentation

---

If you want next step, I can:

- generate a **perfect `pyproject.toml` for uv + ruff + pytest + behave**
- align this with your **Podman devcontainer workflow**
- or build a **CI pipeline (GitLab / GitHub Actions) consistent with this setup**

>> YES, generate a **perfect `pyproject.toml` for uv + ruff + pytest + behave**

Below is a **production-grade `pyproject.toml`** tailored for your stack:

- `uv` (environment + dependency management)
- `ruff` (linting + formatting + import sorting)
- `pytest` (primary testing)
- `behave` (BDD / NLP specification layer)

It is:

- fully **PEP 621 compliant**
- strictly **PEP 508 dependency syntax**
- optimized for **reproducibility, CI, and container workflows**
- aligned with your Emacs/LSP setup (pyright + ruff)

---

## Complete `pyproject.toml`

```toml
[build-system]
requires = ["hatchling>=1.24"]
build-backend = "hatchling.build"

[project]
name = "your-project-name"
version = "0.1.0"
description = "Short description of the project"
readme = "README.md"
requires-python = ">=3.11"

authors = [
  { name = "Your Name", email = "your@email.com" }
]

license = { text = "MIT" }

dependencies = [
  # --- core runtime dependencies ---------------------------------------------

  "torch>=2.2",
  "numpy>=1.26",
]

# Optional dependency groups (PEP 621 standard)
[project.optional-dependencies]

dev = [
  # --- testing ---------------------------------------------------------------

  "pytest>=8.0",
  "pytest-cov>=4.1",

  # --- BDD -------------------------------------------------------------------

  "behave>=1.2.6",

  # --- linting / formatting --------------------------------------------------

  "ruff>=0.4.0",

  # --- typing / LSP ----------------------------------------------------------

  "pyright>=1.1.350",

  # --- utilities -------------------------------------------------------------

  "ipython>=8.20",
]

# Optional: explicit grouping for uv (non-standard but supported)
[tool.uv]

# uv prefers in-project virtual environments
venv = ".venv"

# Optional: dependency groups shortcut (uv supports this)
[tool.uv.dependency-groups]
dev = [
  "pytest",
  "pytest-cov",
  "behave",
  "ruff",
  "pyright",
  "ipython",
]

# -----------------------------------------------------------------------------
# Ruff configuration (single source of truth for lint + format + import sorting)
# -----------------------------------------------------------------------------

[tool.ruff]
line-length = 88
target-version = "py311"

# Enable modern, strict rule set
lint.select = [
  "E",   # pycodestyle errors
  "F",   # pyflakes
  "I",   # import sorting (replaces isort)
  "B",   # bugbear
  "UP",  # pyupgrade
  "N",   # naming
  "C4",  # comprehensions
  "SIM", # simplifications
]

lint.ignore = [
  "E501",  # handled by formatter
]

# Auto-fix everything safe
fix = true

# Import sorting config
[tool.ruff.lint.isort]
known-first-party = ["your_project_name"]

# Formatter (replaces black)
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

# -----------------------------------------------------------------------------
# Pytest configuration
# -----------------------------------------------------------------------------

[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]

python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Optional markers
markers = [
  "slow: marks slow tests",
  "integration: marks integration tests",
]

# -----------------------------------------------------------------------------
# Coverage (optional but recommended)
# -----------------------------------------------------------------------------

[tool.coverage.run]
branch = true
source = ["your_project_name"]

[tool.coverage.report]
show_missing = true
skip_covered = true

# -----------------------------------------------------------------------------
# Behave configuration (BDD)
# -----------------------------------------------------------------------------

[tool.behave]
paths = ["features"]
format = ["progress"]
stdout_capture = false
stderr_capture = false

# -----------------------------------------------------------------------------
# Pyright (LSP consistency with Emacs)
# -----------------------------------------------------------------------------

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"

reportMissingImports = true
reportUnusedVariable = true
reportUnusedImport = true

venvPath = "."
venv = ".venv"

# -----------------------------------------------------------------------------
# Optional: project scripts (nice with uv run)
# -----------------------------------------------------------------------------

[project.scripts]
test = "pytest:main"
bdd = "behave.__main__:main"
```

---

## Design Rationale (Concise but Opinionated)

### 1. Build backend: `hatchling`

- *Why not poetry-core?* → you're migrating away from Poetry
- *Why not setuptools?* → heavier, legacy complexity
- `hatchling` is:

  - minimal
  - fast
  - fully PEP-compliant

---

### 2. `uv` integration model

- `uv` does **not require special config**
- We only:

  - standardize `.venv`
  - optionally define dependency groups

Typical workflow:

```bash
uv sync --all-extras
uv run pytest
uv run behave
```

---

## 3. Ruff replaces everything

You do NOT need:

- black
- isort
- flake8
- pyupgrade

This reduces:

- config duplication
- tool conflicts
- CI complexity

---

## 4. pytest + behave separation

- `pytest` → correctness, fast feedback
- `behave` → specification (ideal for NLP pipelines)

This matches your **AI/NLU architecture goals**.

---

## 5. Pyright alignment with Emacs

- Matches your `lsp-pyright` config
- Ensures:

  - identical diagnostics in editor + CI
  - no “works in editor but not in CI” issues

---

## 6. Recommended Project Layout

```text
.
├── pyproject.toml
├── src/
│   └── your_project_name/
├── tests/
├── features/
│   └── *.feature
├── .venv/
```

---

## 7. Additional Notes

- Prefer `src/` layout → avoids import shadowing
- Always run:

  ```bash
  uv sync
  ```

  after modifying dependencies
- In CI:

  ```bash
  uv sync --all-extras
  uv run pytest
  uv run behave
  ```

---

## References /t

- [^at-11]: PEP 621 — Project metadata
- [^at-12]: PEP 508 — Dependency specification
- [^at-13]: Ruff documentation
- [^at-14]: Pytest documentation
- [^at-15]: Behave documentation
- [^at-16]: Pyright configuration reference
- [^at-17]: Hatchling build backend

---

If you want next step, I can:

- generate a **matching CI pipeline (GitLab / GitHub Actions)**
- align this with your **Podman container images**
- or produce a **`uv.lock` reproducibility strategy for research workflows**

>> YES, generate a **matching CI pipeline (GitLab / GitHub Actions)**

Below are **production-grade CI pipelines** aligned _exactly_ with your stack:

- `uv` for environment + execution
- `ruff` as single lint/format tool
- `pytest` + `behave` as first-class citizens
- `pyright` for type checking
- optimized for **reproducibility, caching, and fast cold starts**

I’ll give you both:

- GitLab CI (self-hosted / enterprise-friendly)
- GitHub Actions (public / cloud-native)

---

## 1. GitLab CI Pipeline

### Key design choices

- Uses official Python image (no custom image required)
- Installs `uv` via bootstrap script (fast)
- Caches `.venv` + `uv` artifacts
- Parallel stages:

  - lint
  - type-check
  - test (pytest)
  - bdd (behave)

---

### `.gitlab-ci.yml`

```yaml
stages:
  - lint
  - type
  - test
  - bdd

variables:
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.uv-cache"
  VENV_PATH: "$CI_PROJECT_DIR/.venv"

default:
  image: python:3.11-slim

before_script:
  - apt-get update && apt-get install -y curl
  - curl -Ls https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - uv --version

  # Sync environment (dev deps included)
  - uv sync --all-extras

cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - .venv/
    - .uv-cache/

# -----------------------------------------------------------------------------
# Lint (ruff)
# -----------------------------------------------------------------------------

lint:
  stage: lint
  script:
    - uv run ruff check .
    - uv run ruff format --check .

# -----------------------------------------------------------------------------
# Type checking (pyright)
# -----------------------------------------------------------------------------

type-check:
  stage: type
  script:
    - uv run pyright

# -----------------------------------------------------------------------------
# Pytest
# -----------------------------------------------------------------------------

test:
  stage: test
  script:
    - uv run pytest --maxfail=1 --disable-warnings -q

# -----------------------------------------------------------------------------
# Behave (BDD)
# -----------------------------------------------------------------------------

bdd:
  stage: bdd
  script:
    - uv run behave

```

---

### Optional improvements (GitLab)

#### 1. Parallelization

```yaml
test:
  parallel: 2
```

#### 2. Artifacts (coverage)

```yaml
artifacts:
  reports:
    coverage_report:
      coverage_format: cobertura
      path: coverage.xml
```

---

## 2. GitHub Actions Pipeline

### Key design choices

- Uses `actions/setup-python`
- Native caching for `uv`
- Matrix-ready (Python versions)
- Faster than GitLab on cold start

---

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.11"]

    steps:
      # -----------------------------------------------------------------------
      # Checkout
      # -----------------------------------------------------------------------

      - name: Checkout
        uses: actions/checkout@v4

      # -----------------------------------------------------------------------
      # Python
      # -----------------------------------------------------------------------

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      # -----------------------------------------------------------------------
      # Install uv
      # -----------------------------------------------------------------------

      - name: Install uv
        run: |
          curl -Ls https://astral.sh/uv/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Verify uv
        run: uv --version

      # -----------------------------------------------------------------------
      # Cache
      # -----------------------------------------------------------------------

      - name: Cache uv + venv
        uses: actions/cache@v4
        with:
          path: |
            .venv
            ~/.cache/uv
          key: ${{ runner.os }}-uv-${{ hashFiles('pyproject.toml') }}

      # -----------------------------------------------------------------------
      # Sync environment
      # -----------------------------------------------------------------------

      - name: Install dependencies
        run: uv sync --all-extras

      # -----------------------------------------------------------------------
      # Lint (ruff)
      # -----------------------------------------------------------------------

      - name: Ruff lint
        run: uv run ruff check .

      - name: Ruff format check
        run: uv run ruff format --check .

      # -----------------------------------------------------------------------
      # Type checking (pyright)
      # -----------------------------------------------------------------------

      - name: Pyright
        run: uv run pyright

      # -----------------------------------------------------------------------
      # Tests (pytest)
      # -----------------------------------------------------------------------

      - name: Pytest
        run: uv run pytest --maxfail=1 --disable-warnings -q

      # -----------------------------------------------------------------------
      # BDD (behave)
      # -----------------------------------------------------------------------

      - name: Behave
        run: uv run behave

```

---

## 3. Critical Design Notes

### Why `uv sync --all-extras`

Because you defined:

```toml
[project.optional-dependencies]
dev = [...]
```

This ensures CI includes:

- pytest
- behave
- ruff
- pyright

---

## Why NOT separate jobs (GitHub)

- Shared `.venv` = faster
- Less duplication
- Simpler logs

GitLab benefits more from stage separation due to runner model.

---

## Why cache `.venv`

- `uv` is fast, but dependency resolution still costs time
- caching `.venv` gives **~3–10× speedup**

---

### Why no Docker image

You use **Podman locally**, but in CI:

- native runners are faster
- fewer layers
- simpler debugging

You can still add container jobs later.

---

## 4. Optional Advanced Enhancements

### 1. Strict CI mode (recommended)

Add to ruff:

```bash
uv run ruff check . --exit-non-zero-on-fix
```

---

### 2. Fail on type warnings

In `pyproject.toml`:

```toml
[tool.pyright]
typeCheckingMode = "strict"
```

(already set)

---

### 3. Coverage enforcement

```yaml
- name: Coverage
  run: uv run pytest --cov=your_project_name --cov-fail-under=85
```

---

### 4. Pre-commit parity

Use same tools locally:

```bash
uv run ruff check .
uv run pyright
uv run pytest
```

---

## 5. Final Architecture Summary

Your stack is now:

- **Editor**

  - Emacs + LSP (pyright) + treesit
  
- **Tooling**

  - ruff (all formatting/linting)
  
- **Environment**

  - uv + `.venv`
  
- **Testing**

  - pytest (core)
  - behave (spec layer)
  
- **CI**

  - identical commands → no drift

👉 This is a **fully converged modern Python toolchain (2026 standard)**

---

## Additional Notes

- This setup is **editor-agnostic**:

  - works identically in VSCode / Cursor
  
- Perfectly compatible with:

  - Podman containers
  - reproducible research workflows
  
- Minimal tool surface → maximum reliability

---

If you want next step, I can:

- generate a **Podman devcontainer (Dockerfile + compose) matching this**
- add **multi-GPU / CUDA CI runners strategy**
- or build a **release pipeline (versioning + publishing)**




# A:1 (Perplexity)

[^](#toc) **_Emacs Python Support_**

Python development in Emacs benefits from LSP integration with Pyright for type checking and Ruff for linting, building on the existing `lsp-mode` and `lsp-pyright` setup in your `site-pkgs.org`. The configuration already supports `python-ts-mode`, `uv-mode`, `pytest`, and Poetry/Pyenv; proposed changes enhance Ruff LSP, pytest keybindings, and add behave support while recommending Tree-sitter complement LSP. All packages are MELPA-available, actively maintained (e.g., `ruff-lsp` 2026 updates), and `use-package` compatible with Emacs 29+ treesit.


## Baseline Analysis

Your config remaps `python-mode` to `python-ts-mode`, enables `lsp-pyright` on `python-mode` hook (update to ts-mode), includes `uv-mode`, `python-pytest`, `py-isort`, `python-black`, and `yapfify`. No Ruff, behave, or explicit treesit-auto; LSP uses `lsp-mode` with `lsp-ui`. Poetry/pyvenv tracked but uv prioritized per role.

## Tree-sitter Recommendation

Tree-sitter via `treesit-auto` complements LSP by providing precise syntax highlighting, folding, and navigation without replacing semantic features like type checking. Pros: native Emacs 29+, faster parsing than regex; cons: requires grammar install. Recommend complement—activate `python-ts-mode` (already present) + `treesit-auto` for auto-parsing. [github](https://github.com/renzmann/treesit-auto/)

```org
#+NAME: treesitter-enhance
#+begin_src emacs-lisp
;; ---( Tree-sitter Auto Enhance )------------------------------------------------
(use-package treesit-auto
  :ensure t
  :config
  (add-to-list 'treesit-language-source-alist
               '((python . "https://github.com/tree-sitter/tree-sitter-python")))
  (global-treesit-auto-mode))
#+end_src
```

## Python and UV Integration

Built-in `python-ts-mode` with `uv-mode` auto-activation handles envs efficiently; pros over pyvenv: faster resolution, PEP 508 compliance; cons: newer, less mature than Poetry. Retain existing, add indicator. [github](https://github.com/z80dev/uv-mode)

```org
#+NAME: python-uv
#+begin_src emacs-lisp
;; ---( Python UV Refine )--------------------------------------------------------
(use-package uv-mode
  :ensure t
  :hook (python-ts-mode . uv-mode-auto-activate-hook)
  :custom (uv-mode-indicator t))
#+end_src
```

## Pyright LSP Type Checking

Existing `lsp-pyright` is optimal; pros: fast, venv-aware; cons vs mypy: less strict gradual typing. Tweak hook to ts-mode, disable organize-imports (defer to Ruff). [github](https://github.com/emacs-lsp/lsp-pyright/issues/95)

```org
#+NAME: pyright-refine
#+begin_src emacs-lisp
;; ---( Pyright LSP Refine )-----------------------------------------------------
(use-package lsp-pyright
  :ensure t
  :hook (python-ts-mode . (lambda ()
                            (lsp-deferred)
                            (setq lsp-pyright-disable-organize-imports t)))
  :custom
  (lsp-pyright-auto-import-completions t))
#+end_src
```

## Ruff Linting/Formatting

Add `ruff-lsp` atop Pyright; single Rust binary replaces black/isort/flake8 (drop `py-isort`, `python-black`); pros: 100x faster, all-in-one; cons: config via pyproject.toml only. [docs.astral](https://docs.astral.sh/ruff/editors/setup/)

```org
#+NAME: ruff-add
#+begin_src emacs-lisp
;; ---( Ruff LSP Add )------------------------------------------------------------
(use-package ruff-lsp
  :ensure t
  :hook (python-ts-mode . (lambda ()
                            (lsp-deferred)
                            (lsp-register-client
                             (make-lsp-client :new-connection-function
                                              #'lsp-stdio-connection
                                              :major-modes '(python-ts-mode)
                                              :server-id 'ruff)))))
#+end_src
```
## Pytest Runner

Existing `python-pytest` is solid; pros: DWIM dispatch; cons vs compilation: less flexible for custom args. Enhance bindings. [github](https://github.com/wbolster/emacs-python-pytest)

```org
#+NAME: pytest-bind
#+begin_src emacs-lisp
;; ---( Pytest Bindings )---------------------------------------------------------
(use-package python-pytest
  :ensure t
  :bind (:map python-ts-mode-map
              ("C-c t d" . python-pytest-dispatch)
              ("C-c t f" . python-pytest-file-dwim)
              ("C-c t F" . python-pytest-function-dwim)))
#+end_src
```

## Behave BDD Runner

No native package; use `compile` with `uv run behave` for first-class support. Pros: Gherkin for AI specs; cons: manual vs pytest DWIM. [github](https://github.com/Nick287/Behave-Quick-Start)

```org
#+NAME: behave-compile
#+begin_src emacs-lisp
;; ---( Behave Compile )----------------------------------------------------------
(use-package compile
  :ensure nil
  :bind (:map python-ts-mode-map
              ("C-c b r" . (lambda ()
                             (interactive)
                             (compile "uv run behave")))))
#+end_src
```

## Integration Notes

Insert blocks after existing Python/LSP sections in `site-pkgs.org`. Remove/disable `py-isort`, `yapfify`, `python-black` post-Ruff. Test: `M-x lsp-workspace-restart`; ensure `uv add ruff-lsp pyright pytest behave` in pyproject.toml.

## Additional Notes /p

- Treesit grammars: `M-x treesit-install-language-grammar python`.
- Podman: Share `pyproject.toml`/`.venv` via volumes.
- CI: GitLab CI stage `uv sync && ruff check && pytest && behave`.
- MELPA health: All active 2026 (e.g., `uv-mode` recent). [reddit](https://www.reddit.com/r/emacs/comments/1kp095s/starting_uvel_an_emacs_frontend_package_for_the/)

## References /p

- [^ap-1]: uv-mode GitHub. [github](https://github.com/z80dev/uv-mode)
- [^ap-2]: lsp-pyright env. [github](https://github.com/emacs-lsp/lsp-pyright/issues/95)
- [^ap-3]: python-pytest. [github](https://github.com/wbolster/emacs-python-pytest)
- [^ap-4]: treesit-auto. [github](https://github.com/renzmann/treesit-auto/)
- [^ap-5]: Ruff docs. [docs.astral](https://docs.astral.sh/ruff/editors/setup/)
- [^ap-6]: ruff-lsp. [github](https://github.com/astral-sh/ruff-lsp)


# A:1 (DeepSeek)

[^](#toc) **_Emacs Python Configuration Update Advice_**

Based on a thorough review of your `site-pkgs.org` Emacs configuration, I recommend a set of modern, performant, and well‑integrated packages for Python development. The current setup can be streamlined by adopting tools that are actively maintained, leverage Emacs 29+ built‑in features, and align with the 2026 Python ecosystem (uv, pyright, ruff, pytest, behave). Below are the proposed configuration blocks, each with a justification that weighs pros and cons against credible alternatives.

---

## Python Base Mode and Environment Integration

**Proposed configuration**

```org
#+NAME: setup-python-base
#+begin_src emacs-lisp
;; ---( python )----------------------------------------------------------------
(use-package python
  :ensure nil   ; built-in
  :hook (python-mode . (lambda ()
                          (setq-local indent-tabs-mode nil)
                          (setq-local python-indent-offset 4)))
  :custom
  (python-shell-interpreter "python3")
  (python-shell-virtualenv-root nil)  ; set dynamically via envrc
  :config
  ;; Use built-in treesitter if available
  (when (and (fboundp 'treesit-available-p) (treesit-available-p))
    (add-hook 'python-mode-hook #'treesit-parser-create 'python)))
#+end_src
```

**Justification**  

- _python.el_ (built‑in) is stable and requires no external package.
- Environment integration is delegated to `envrc` (see below) because it works seamlessly with `uv`’s `.venv` directories and respects `.envrc` files.
- Alternatives like `pyvenv` or `pyenv-mode` are less universal; `envrc` handles any environment manager and is widely adopted.
- The hook sets basic indentation style and prepares for treesitter, which is recommended later.

---

## uv Project and Virtual‑Environment Management

**Proposed configuration**

```org
#+NAME: setup-uv-env
#+begin_src emacs-lisp
;; ---( uv / direnv integration )-----------------------------------------------
(use-package envrc
  :ensure t
  :hook (after-init . envrc-global-mode)
  :config
  ;; Automatically load environment when entering a project with .envrc
  (setq envrc-debug nil))
#+end_src
```

**Justification**

- `envrc` (MELPA) directly supports `direnv`, which can be configured to activate `uv`’s virtual environment (e.g., with `layout python` or `source .venv/bin/activate` in `.envrc`).
- **Pros**: Zero Emacs‑side knowledge of `uv`; works with any tool that produces a `.envrc`.
- **Cons**: Requires the user to create `.envrc` files manually (a one‑time setup).
- Alternatives: `pyvenv` would need manual activation per project; `pyenv-mode` does not understand `uv`. `envrc` is the most future‑proof and integrates with Emacs’ `process-environment` perfectly.

---

## pyright LSP Integration

### Proposed configuration

```org
#+NAME: setup-pyright
#+begin_src emacs-lisp
;; ---( lsp-mode + pyright )----------------------------------------------------
(use-package lsp-mode
  :ensure t
  :hook ((python-mode . lsp-deferred)
         (lsp-mode . lsp-enable-which-key-integration))
  :commands lsp
  :custom
  (lsp-completion-provider :capf)
  (lsp-log-io nil)
  (lsp-document-sync-method 'incremental)
  (lsp-keymap-prefix "C-c l"))

(use-package lsp-pyright
  :ensure t
  :after lsp-mode
  :hook (python-mode . (lambda () (require 'lsp-pyright) (lsp-deferred)))
  :custom
  (lsp-pyright-typechecking-mode "strict")  ; optional
  (lsp-pyright-disable-organize-imports nil)) ; defer to ruff
#+end_src
```

### Justification

- `lsp-pyright` uses Microsoft’s pyright, the fastest and most accurate Python language server.
- **Pros**: Excellent type checking, completion, and refactoring; large community; MELPA availability.
- **Cons**: Heavier than `eglot`; requires Node.js (already available via `nvm`).
- Alternatives: `eglot` with `pyright` is simpler but lacks some LSP‑Mode conveniences (e.g., `lsp-ui`). Given your existing LSP usage, sticking with `lsp-mode` is consistent.
- Community adoption is extremely high; issue tracker active.

---

## ruff (Linting and Formatting)

### ruff Proposed configuration

```org
#+NAME: setup-ruff
#+begin_src emacs-lisp
;; ---( ruff )------------------------------------------------------------------
(use-package ruff-format
  :ensure t
  :hook (python-mode . (lambda ()
                          (setq-local format-all-formatters '(("Python" ruff-format)))))
  :config
  ;; Optionally point to your pyproject.toml
  (setq ruff-format-args '("--config" "pyproject.toml")))

(use-package flycheck-ruff
  :ensure t
  :after flycheck
  :hook (python-mode . (lambda () (flycheck-mode +1)))
  :config
  (setq flycheck-ruff-max-line-length 88)) ; match your formatter
#+end_src
```

### ruff Justification

- `ruff` unifies linting and formatting in one extremely fast tool.
- `ruff-format` (MELPA) provides a `format-all` integration; `flycheck-ruff` gives real‑time linting.
- **Pros**: Speed, active development, single dependency, respects `pyproject.toml`.
- **Cons**: Ruff does not yet support all flake8 plugins, but covers most rules.
- Alternatives: `black` + `isort` + `flake8` would require three separate packages and slower execution. `ruff` is now the community standard.
- Both packages are on MELPA and have healthy issue trackers.

---

## pytest Test Runner Integration

### pytest Proposed configuration

```org
#+NAME: setup-pytest
#+begin_src emacs-lisp
;; ---( pytest )----------------------------------------------------------------
(use-package pytest
  :ensure t
  :commands (pytest-pdb pytest-one pytest-last-failed)
  :hook (python-mode . (lambda ()
                          (local-set-key (kbd "C-c t") 'pytest-pdb)
                          (local-set-key (kbd "C-c T") 'pytest-one)))
  :custom
  (pytest-cmd-flags "-v"))
#+end_src
```

### pytest Justification

- The `pytest` package (MELPA) offers a simple interface to run tests, debug with pdb, and repeat last failures.
- **Pros**: Dedicated test runner with key bindings; works out of the box with `pytest`.
- **Cons**: Does not display results in a test‑specific buffer (uses `compilation-mode`).
- Alternatives: `python-pytest` (less active), `nose` (deprecated), or custom `compile` commands. The `pytest` package is the most straightforward.
- Active maintenance and good MELPA availability.

---

## behave BDD Test Runner Integration

### behave Proposed configuration

```org
#+NAME: setup-behave
#+begin_src emacs-lisp
;; ---( behave )----------------------------------------------------------------
(use-package feature-mode
  :ensure t
  :mode ("\\.feature\\'" . feature-mode)
  :config
  (defun run-behave ()
    "Run behave from project root."
    (interactive)
    (let ((default-directory (projectile-project-root)))
      (compile "behave --no-capture")))

  (defun run-behave-scenario ()
    "Run the behave scenario at point (requires line number)."
    (interactive)
    (let* ((file (buffer-file-name))
           (line (line-number-at-pos))
           (default-directory (projectile-project-root)))
      (compile (format "behave --no-capture %s:%d" file line))))

  :hook (feature-mode . (lambda ()
                           (local-set-key (kbd "C-c b") 'run-behave)
                           (local-set-key (kbd "C-c s") 'run-behave-scenario))))
#+end_src
```

### behave Justification

- `feature-mode` (MELPA) provides syntax highlighting and indentation for Gherkin files.  
- Custom commands run `behave` via `compile` for whole suite or current scenario.  
- **Pros**: Lightweight, leverages Emacs’ built‑in compilation mode.  
- **Cons**: No specialised test‑result viewer; uses standard `compilation-mode`.  
- Alternatives: `cucumber.el` (Ruby‑focused), no dedicated `behave` package. This approach is simple and effective.  
- `feature-mode` is actively maintained and integrates well with Emacs 29.

---

## Treesitter Integration (Complement vs. Replace)

### Treesitter Proposed configuration

```org
#+NAME: setup-treesitter
#+begin_src emacs-lisp
;; ---( treesit-auto )----------------------------------------------------------
(use-package treesit-auto
  :ensure t
  :custom
  (treesit-auto-install 'prompt)   ; prompt before downloading grammars
  :config
  ;; Automatically use treesitter modes for all supported languages
  (treesit-auto-add-to-auto-mode-alist 'all)
  (global-treesit-auto-mode))
#+end_src
```

### Treesitter Discussion

- **Role of tree‑sitter**: It provides precise, incremental syntax highlighting and structural navigation (e.g., `treesit-sexp`). This complements the semantic information provided by LSP (type checking, references, renaming).
- **Complement vs. replace**: LSP cannot be replaced by tree‑sitter because tree‑sitter lacks cross‑file analysis, type awareness, and refactoring capabilities. Conversely, LSP highlighting is often less accurate and slower than tree‑sitter.
- **Recommendation**: **Complement**. Use tree‑sitter for syntax highlighting, indentation, and code folding; rely on LSP (pyright) for all language‑server features. This hybrid approach gives the best of both worlds.
- *Compatibility*: Emacs 29+ has built‑in `treesit`. `treesit-auto` (MELPA) automatically downloads and installs grammars, reducing friction. It is actively maintained and works flawlessly with `use-package`.
- *Integration complexity*: Minimal—just install `treesit-auto` and enable it. The grammar for Python is included, and the mode will switch to `python-ts-mode` automatically. The earlier hook in `setup-python-base` ensures the parser is created, but `treesit-auto` already handles this.

---

## References

[^rf-envrc]: `envrc` MELPA page – https://melpa.org/#/envrc  
[^rf-lsp-mode]: `lsp-mode` documentation – https://emacs-lsp.github.io/lsp-mode/  
[^rf-pyright]: pyright language server – https://github.com/microsoft/pyright  
[^rf-ruff]: Ruff – https://github.com/astral-sh/ruff  
[^rf-pytest-el]: `pytest` Emacs package – https://github.com/arthurnn/pytest  
[^rf-feature-mode]: `feature-mode` – https://github.com/michaelklishin/cucumber.el (modern fork)  
[^rf-treesit-auto]: `treesit-auto` – https://github.com/renzmann/treesit-auto  

## Additional Notes

- All proposed packages are available on MELPA and have seen recent commits (as of 2026).  
- The configuration assumes you have `use-package` already set up; if not, add `(require 'use-package)` early in your init.  
- For `ruff`, ensure the `ruff` executable is installed in your environment (`uv tool install ruff` or via project dependency).  
- The `pytest` package uses the `pytest` executable from the virtual environment; `envrc` guarantees it is on `PATH`.  
- Behave integration relies on `projectile` for project root detection. If you don’t use Projectile, replace `projectile-project-root` with `locate-dominating-file` looking for `.behave` or `pyproject.toml`.  
- Treesitter grammars require a C compiler toolchain at install time; if you run Emacs on a system without one, set `treesit-auto-install` to `never` and install grammars manually.





<!-- }}} \\ %1. -->
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
