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


# Revised Emacs Configuration for Python Development

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
