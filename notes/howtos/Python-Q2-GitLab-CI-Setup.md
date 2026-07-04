---
title: Resolving GitLab CI/CD Disk-Quota Errors for CUDA Libraries
subtitle: |
  Optimizing Astral uv and micromamba configurations within restricted
  shared runners for automated machine learning verification pipelines

# {{{ // %+

category: DVE-Howto
keywords: [GEN, GitLab-CI, CUDA, PyTorch, Astral-uv, Micromamba]
abstract: |
  This technical report addresses the disk-quota constraints
  encountered in GitLab CI/CD pipelines when deploying complex
  high-performance computing environments. Specifically, it
  investigates storage exhaustion caused by massive CUDA-bundled
  binary wheels during verification workflows on shared runners
  restricted to a 20 GB storage limit.

  To resolve this failure without compromising the simplicity of
  local environment initialization via `uv sync`, a dual
  optimization strategy is proposed. The framework details the
  refactoring of `pyproject.toml` and `.gitlab-ci.yml` to
  decouple local GPU-enabled configurations from cloud-based
  validation steps.

  Furthermore, an alternative deployment architecture utilizing
  `micromamba` is evaluated. This analysis weighs the trade-offs
  regarding externalizing CUDA dependencies, dependency isolation,
  reproducibility, and structural overhead in derived templates.

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

1. [Q:1 - CI/CD Disk-Quota Resolution for CUDA libraries](#q1)
   - see: [CI/CD Disk-Quota Resolution: Refactoring Analysis (Claude)](#a1-claude)
   - see: [CI/CD Disk Quota Resolution for ML (Gemini)](#a1-gemini)
   - see: [CI GPU Dependency Refactor (ChatGPT)](#a1-chatgpt)
   - see: [Refactored GPU ML Project Configurations (DeepSeek)](#a1-deepseek)
   - see: [Refactored GPU ML Project Configurations (Perplexity)](#a1-perplexity)
   - see: [Refactored CI/CD Pipeline and `micromamba` Analysis (Vibe)](#a1-vibe)
2. [Q:2 - TODO:(q2-ref)](#q2)
   - see: [TODO:(a2-ref-claude) (Claude)](#a2-claude)
   - see: [TODO:(a2-ref-gemini) (Gemini)](#a2-gemini)
   - see: [TODO:(a2-ref-chatgpt) (ChatGPT)](#a2-chatgpt)
   - see: [TODO:(a2-ref-deepseek) (DeepSeek)](#a2-deepseek)
   - see: [TODO:(a2-ref-perplexity) (Perplexity)](#a2-perplexity)
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

## Q:1 - **CI/CD Disk-Quota Resolution for CUDA libraries**

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

[^](#toc) **_CI/CD Disk-Quota Resolution: Refactoring Analysis_**

## Root-Cause Analysis

The failure originates from a combination of three factors:

- `torch` (CUDA variant) from `https://download.pytorch.org/whl/cu130` lists `triton` as a
  hard runtime dependency. `triton` ships a ~1.5 GB native shared library (`libtriton.so`).
- The current `before_script` runs `uv sync --dev`, which installs the full project dependency
  closure including every main-project dependency — `torch`, `torchvision`, and their transitive
  closure — even though no CI job exercises GPU code paths.
- The `.venv` directory is included in the GitLab cache, meaning the virtual environment is
  serialised and deserialised across jobs, doubling the effective disk pressure beyond the 20 GB
  quota during the cache-restore phase.

The targeted fix is to redirect the named `torch` index to the CPU wheel server inside CI via a
`uv`-native environment variable override, so no CUDA-bundled binary is downloaded at all. No
source-level change to the `uv sync` invocation consumed by downstream projects is required.

---

## Deliverable 1 — Refactored `pyproject.toml`

### Index Override Mechanism

`uv` exposes every named index defined under `[[tool.uv.index]]` as an overridable environment
variable[^ac-uv-index-env]. For an index named `torch-gpu`, the corresponding variable is:

```text
UV_INDEX_TORCH_GPU=https://download.pytorch.org/whl/cpu
```

The name is uppercased and all hyphens are replaced by underscores. Setting this variable in the
GitLab CI job causes `uv` to resolve `torch` and `torchvision` against the CPU wheel server while
every downstream consumer that omits the variable continues to receive CUDA wheels unchanged. The
`uv sync --all-extras --all-groups` contract is preserved verbatim.

### NVIDIA Compatibility Notes

#### `uv`-only Case (CUDA-bundled Wheels)

- The `cu130` wheel index targets CUDA Toolkit 13.0 (driver ≥ 580 on Linux[^ac-cuda-compat]).
- PyTorch 2.10.x requires cuDNN 9.x, NCCL 2.21+, and the matching `libcuda.so` ABI from
  the driver package.
- No host-level CUDA installation is required: all CUDA runtime libraries are bundled inside
  the wheel tree (in `.venv/lib/python3.x/site-packages/nvidia/`).
- `triton` (GPU kernel compiler) is a hard dependency of every CUDA-enabled `torch` build and
  _must_ be present for JIT-compiled GPU kernels at runtime, but is not needed during CI
  verification.

#### `micromamba`-assisted Case

- CUDA is provided at the OS level by the conda environment; `uv` must therefore resolve `torch`
  against a wheel that links dynamically against the system `libcuda.so` / `libcudart.so`.
- The `download.pytorch.org/whl/cu130` index ships exactly those slim wheels: they are compiled
  against CUDA 13.0 headers but _do not rebundle_ the CUDA runtime.
- `LD_LIBRARY_PATH` must include the conda environment's `lib/` directory before `uv sync` is
  invoked, so the linker resolution succeeds at install time.
- `triton` is still installed as a transitive dependency; its disk footprint is unavoidable in
  GPU environments, but is contained within the `uv`-managed `.venv`.

### Refactored `pyproject.toml`

The only structural change to the original file is renaming the index from `torch130` to
`torch-gpu` to produce a readable, intent-revealing environment variable name. All other content
is preserved.

```toml
# ============================================================
# Build system (PEP 518 / PEP 517)
# ============================================================
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

# ============================================================
# Project metadata (PEP 621)
# ============================================================
[project]
name = "dve_sample_py"
version = "0.1.0"
description = "TODO(title): TITLE OF THE RESEARCH WORK / TITOLO DEL LAVORO DI RICERCA"
readme = "README.md"
requires-python = ">=3.10,<3.15"

authors = [{ name = "Data Science Lab DEMS/datalab", email = "datalab@unimib.it" }]

# ============================================================
# Dependencies (PEP 508 strings)
# ============================================================
dependencies = [

  # --- ML frameworks ---
  # Index source: controlled by [[tool.uv.index]] name = "torch-gpu".
  # In GPU environments (dev / test / prod) the index resolves to:
  #   https://download.pytorch.org/whl/cu130
  # In CI set:
  #   UV_INDEX_TORCH_GPU=https://download.pytorch.org/whl/cpu
  # to redirect to the CPU wheel server, eliminating triton and all
  # CUDA-bundled libraries from the virtual environment.
  "torch==2.10.*",
  "torchvision==0.25.*",

  # --- data ---
  "numpy",
  "pandas",
  "pandas-datareader",
  "openpyxl",
  "pyarrow",
  "polars",

  # --- sql ---
  "SQLAlchemy",
  "psycopg2-binary",
  "mysql-connector-python",

  # --- stats ---
  "scipy",
  "sympy",

  # --- plots ---
  "matplotlib",
  "plotly",
  "seaborn",
  "Pillow",

  # --- graphs ---
  "graphframes",
  "graphviz",
  "networkx",
  "igraph",
  "pyvis",
  "pydot",

  # --- system ---
  "requests",
  "oauthlib",
  "requests-oauthlib",
  "urllib3",
  "pyzmq",

  "pyyaml",
  "types-pyyaml",
  "toml",
  "types-toml",
  "piny",
  "click",
  "pathspec",

  "icecream",
  "tqdm",

  "pip",
  "more-itertools",

  # --- git dependency ---
  "rootpath @ git+https://github.com/hute37/python-rootpath@stable",

]

# ============================================================
# Optional dependency groups (PEP 621 Extras)
# ============================================================
[project.optional-dependencies]

gpumon = [
  "nvidia-ml-py; sys_platform == 'linux'",
]

# ============================================================
# Project URLs
# ============================================================
[project.urls]
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

# ============================================================
# Script commands
# ============================================================
[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_hello:main"

# ============================================================
# Development dependency groups
# ============================================================
[dependency-groups]

agents = [
  "aiohttp",
  "anthropic",
  "graphifyy",
  "hypothesis",
  "line-profiler",
  "memory-profiler",
  "openai",
  "pydantic",
  "scikit-learn",
  "sentence-transformers",
]

jupyter = [
  "jupyter",
  "jupyter-core",
  "jupyter-console",
  "jupyter-lsp",
  "notebook",
  "jupyterlab",
  "jupytext",
  "nodeenv",
  "nodejs",
  "jupyterlab-lsp",
  "jupyter-ruff",
  "lux-api",
  "ipykernel",
  "ipywidgets",
  "ipython",
  "ipython-bg",
  "marimo",
]

dev = [
  # --- test ---
  "pytest",
  "pytest-cov",
  "behave",
  "mock",
  "nose",
  # --- edit ---
  "pyright",
  "basedpyright",
  "tree-sitter",
  # --- lint ---
  "ruff",
  # --- misc ---
  "colorama",
  "py",
  "mypy",
  # --- packaging ---
  "setuptools",
  "wheel",
  "bumpversion",
  "twine",
]

# ============================================================
# uv configuration
# ============================================================
[tool.uv]
package = true

[tool.uv.sources]
# Both packages resolved from the "torch-gpu" named index.
# Override in CI with: UV_INDEX_TORCH_GPU=https://download.pytorch.org/whl/cpu
torch = { index = "torch-gpu" }
torchvision = { index = "torch-gpu" }

[[tool.uv.index]]
# GPU default: CUDA 13.0-compiled wheels (driver >= 580).
# Rename from "torch130" to "torch-gpu" so the uv env-var override reads:
#   UV_INDEX_TORCH_GPU=<url>
name = "torch-gpu"
url = "https://download.pytorch.org/whl/cu130"

# ============================================================
# Hatch build configuration
# ============================================================
[tool.hatch.metadata]
allow-direct-references = true

[tool.hatch.build.targets.wheel]
packages = ["src/dve", "src/vce"]

# ============================================================
# pytest
# ============================================================
[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

# ============================================================
# mypy
# ============================================================
[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true

# ============================================================
# pyright
# ============================================================
[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
  "notebooks/@databricks/*",
  "doc/*",
  "home/*",
  "notes/*",
  "renv/*",
  ".venv/*",
  ".agents/*",
  ".eggs/*.py",
  "**/node_modules",
  "**/__pycache__",
  "docker",
  "notes",
  "data",
  "logs",
  "temp",
]
ignore = ["build"]
defineConstant = { DEBUG = true }
typeCheckingMode = "basic"
reportMissingImports = true

# ============================================================
# ruff
# ============================================================
[tool.ruff]
line-length = 100
target-version = "py310"
fix = true

[tool.ruff.lint]
unfixable = []
typing-modules = ["pandas._typing"]
exclude = [
  "notebooks/@databricks/*",
  "doc/*",
  ".eggs/*.py",
  "home/*",
  "notes/*",
  "renv/*",
  ".venv/*",
  ".agents/*",
]
select = [
  "F", "E", "W", "YTT", "B", "Q", "T10", "INT",
  "PL", "PT", "PIE", "PYI", "TID", "ISC", "TCH",
  "C4", "PGH", "RUF", "S102", "NPY002", "PERF",
  "FLY", "G", "FA", "ICN001", "SLOT", "RSE",
]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true

[tool.ruff.format]
docstring-code-format = true
exclude = [
  "notebooks/@databricks/*",
  "doc/*",
  ".eggs/*.py",
  "home/*",
  "notes/*",
  "renv/*",
  ".venv/*",
  ".agents/*",
]

# ============================================================
# Project Custom Configuration
# ============================================================
[tool.local]
has_config = true
config = "config.yaml"

[tool.local.paths]
log_dir = "logs"

[tool.local.log]
level = "INFO"

[tool.local.hello]
salutation = "Hi"
```

---

## Deliverable 2 — Refactored `.gitlab-ci.yml`

### Strategy Summary

The refactoring applies four independent optimisations:

- _Index redirection_: `UV_INDEX_TORCH_GPU` is set to the CPU wheel server for all CI jobs.
  `torch` and `torchvision` resolve to small CPU builds (~200 MB combined); `triton` is not
  pulled as a dependency because the CPU build has no JIT compilation backend.
- _Cache scope reduction_: `.venv` is removed from the `cache` block. Only the `uv` download
  cache (`$UV_CACHE_DIR`) is persisted. Wheel archives in the download cache are order-of-magnitude
  smaller than extracted virtual environments; `.venv` is reconstructed cheaply from cached
  wheels on every job run.
- _Per-job sync scoping_: the `linting` job uses `--only-group dev --no-install-project` to skip
  project package installation entirely — `ruff` operates on source text and has no import-time
  dependency on `torch`. The `typing` and `testing` jobs use `--group dev`, which installs main
  dependencies (including CPU `torch`) plus the `dev` group.
- _`before_script` elimination_: each job declares its own minimal `before_script` rather than
  sharing a maximal one, preventing heavier sync operations from running for jobs that do not
  need them.

### Cache Optimisation Detail

The GitLab runner's 20 GB quota applies to the _working directory_ at the point of cache
serialisation[^ac-gitlab-cache]. Removing `.venv` from the cache has two effects:

- The cache archive shrinks from multi-gigabyte size (CUDA wheels + triton) to a few hundred
  megabytes (wheel tarballs in `$UV_CACHE_DIR`).
- Each job always starts from a clean virtual environment, eliminating stale-dependency bugs
  that arise when a cached `.venv` outlives a `pyproject.toml` change.

The `uv` wheel cache deduplicates content by hash[^ac-uv-cache]; reconstructing `.venv` from
a warm `$UV_CACHE_DIR` typically completes in under thirty seconds.

### Refactored `.gitlab-ci.yml`

```yaml
---
# ---------------------------------------------------------------------------
# Disk-budget notes
# ---------------------------------------------------------------------------
# GitLab SaaS shared runners carry a 20 GB working-directory quota.
# The CUDA-bundled torch wheel + triton alone exceed this budget.
#
# Fix: redirect the "torch-gpu" named index to the CPU wheel server for all
# CI jobs via UV_INDEX_TORCH_GPU.  Downstream consumers running on GPU hosts
# omit this variable and continue to receive CUDA wheels from the cu130 index.
#
# Cache strategy: persist only $UV_CACHE_DIR (downloaded wheel archives).
# Do NOT cache .venv — extracting from the wheel cache is fast (~30 s) and
# avoids the cache-serialisation phase that itself hits the disk quota.
# ---------------------------------------------------------------------------

image: python:3.14-slim

variables:
  # --- uv installation ---
  UV_VERSION: "latest"

  # --- uv cache location (project-relative, included in GitLab cache) ---
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"

  # --- index override: redirect "torch-gpu" to CPU wheel server in CI ---
  # uv resolves UV_INDEX_<NAME_UPPER> where hyphens become underscores.
  # CPU wheels do not include triton, saving ~1.5 GB per job.
  UV_INDEX_TORCH_GPU: "https://download.pytorch.org/whl/cpu"

  # --- disable progress bars (cleaner CI logs) ---
  UV_NO_PROGRESS: "1"

  # --- never use the system Python; always use uv-managed interpreter ---
  UV_PYTHON_PREFERENCE: "only-managed"

# Only the uv download cache is persisted.  .venv is intentionally excluded.
cache:
  key:
    files:
      - pyproject.toml
      - uv.lock
  paths:
    - .cache/uv
  policy: pull-push

stages:
  - lint
  - test

# ---------------------------------------------------------------------------
# Shared setup fragment — referenced via YAML anchors
# ---------------------------------------------------------------------------
.install_uv: &install_uv
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - uv --version

# ---------------------------------------------------------------------------
# lint stage
# ---------------------------------------------------------------------------

linting:
  stage: lint
  before_script:
    - *install_uv
    # Lint jobs operate on source text only.
    # --only-group dev  : install ruff and its peers; skip main dependencies.
    # --no-install-project : do not install the project package itself.
    # Result: no torch, no torchvision, no triton, minimal disk use (~150 MB).
    - uv sync --only-group dev --no-install-project
    - df -h
  script:
    - uv run ruff check .
    - uv run ruff format --check .
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

typing:
  stage: lint
  before_script:
    - *install_uv
    # pyright requires all project imports to be resolvable, so main deps
    # (including CPU torch) must be present.  UV_INDEX_TORCH_GPU redirects
    # the cu130 index to the CPU wheel server; triton is not a dep of CPU torch.
    - uv sync --group dev
    - df -h
  script:
    - uv run pyright
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

# ---------------------------------------------------------------------------
# test stage
# ---------------------------------------------------------------------------

testing:
  stage: test
  before_script:
    - *install_uv
    # Same sync scope as typing: main deps + dev group, CPU torch.
    - uv sync --group dev
    - df -h
  script:
    - uv run pytest -v
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
```

---

## Deliverable 3 — `conda-env.yaml` for the `micromamba` Alternative

### Mechanism

`micromamba`[^ac-micromamba] installs CUDA Toolkit, cuDNN, and BLAS as ordinary shared libraries
into a conda environment prefix (e.g. `/opt/mamba/envs/cuda-base/lib`). When `LD_LIBRARY_PATH`
includes that prefix _before_ `uv sync` is invoked, the linker resolution during wheel
installation succeeds against the system-provided libraries instead of the bundled ones.

The critical consequence for `torch`: wheels fetched from `download.pytorch.org/whl/cu130` are
compiled against CUDA 13.0 headers but _do not re-bundle_ `libcuda.so`, `libcudart.so`, or
`libcudnn.so` — those are expected to be present on `LD_LIBRARY_PATH` at runtime. This is
distinct from the PyPI default wheel, which re-bundles every CUDA runtime library inside
`site-packages/nvidia/`.

`triton` remains a transitive dependency of CUDA-enabled `torch` builds regardless of whether
CUDA is managed by conda or bundled in the wheel. Its disk footprint (~1.5 GB) is therefore
_not_ eliminated by the micromamba approach — it is merely relocated from the conda prefix to
`.venv`.

### Pros

- _System CUDA deduplication_: CUDA runtime libraries (cudart, cublas, cufft, cuDNN) live once
  in the conda prefix rather than being replicated inside every Python virtual environment that
  depends on `torch`. On a multi-project research cluster this can save tens of gigabytes per
  node.
- _Driver/toolkit version governance_: the conda environment provides a single, pinned CUDA
  toolkit version for all Python projects on the host. Updating CUDA becomes a conda operation
  rather than a per-project wheel reinstall.
- _BLAS portability_: `libblas=*=*openblas` in the conda spec ensures consistent BLAS ABI
  regardless of whether Intel MKL is installed on the host, which matters for reproducibility
  across AMD and Intel CPU families.
- _Container image size_: a Podman image that starts from a `micromamba`-installed CUDA base and
  installs only slim torch wheels is measurably smaller than one that unpacks CUDA-bundled wheels
  into a venv.

### Cons

- _Shell initialisation burden_: `micromamba shell init` writes hooks into `~/.bashrc` /
  `~/.zshrc`[^ac-micromamba-init]. Every derived project's README must document this step and
  every CI pipeline that uses micromamba must source the hook or call
  `eval "$(micromamba shell hook --shell bash)"` before activating the environment.
- _`conda activate` in CI_: GitLab CI shells do not source `~/.bashrc` by default. Each job
  must explicitly activate the conda environment or prepend the env's `bin/` to `$PATH`
  before invoking `uv`.
- _Solver overhead_: the conda solver (even `micromamba`'s faster libmamba backend) adds
  30–120 seconds to environment creation compared with a pure `uv` resolve. Cached conda
  environments mitigate this but introduce their own cache-invalidation complexity.
- _Two-tool mental model_: project contributors must understand both `micromamba` (for CUDA) and
  `uv` (for Python packages). The abstraction boundary between "system libraries" and "Python
  packages" is not obvious to researchers unfamiliar with HPC toolchains.
- _`LD_LIBRARY_PATH` fragility_: if the conda prefix is not on `LD_LIBRARY_PATH` at `uv sync`
  time and again at runtime, `torch` will fail to load `libcuda.so` with a cryptic `OSError`.
  This is a silent correctness hazard that is absent from the bundled-wheel approach.

### Impact on Derived Projects

A template consumer adopting the micromamba path must:

- Install `micromamba` and run `micromamba env create -f conda-cuda-env.yaml` once per host.
- Add the following to their shell profile (or to the project's `.envrc` via `direnv`):

```bash
export CUDA_HOME=/opt/mamba/envs/cuda-base
export LD_LIBRARY_PATH="${CUDA_HOME}/lib:${LD_LIBRARY_PATH}"
eval "$(micromamba shell hook --shell bash)"
micromamba activate cuda-base
```

- Ensure `uv sync --all-extras --all-groups` is run _after_ the above exports so that `uv`
  links torch against the system CUDA rather than triggering a bundled-wheel download. The
  `uv sync` command itself remains unchanged.
- Any CI pipeline for the derived project that exercises GPU code must provision the micromamba
  environment before the `uv sync` step. Shared GitLab SaaS runners do not support this and
  remain limited to CPU verification (i.e. the index-override approach from Deliverable 2 still
  applies to CI regardless of which approach is used in dev/prod).

### Refactored `conda-cuda-env.yaml`

The existing file targets CUDA 13.1 and driver ≥ 580. The adjustments below correct two
specification issues present in the original: `cutensor` lacks a channel qualifier on the
`nvidia` channel, and the virtual-package pin (`__cuda`) must be expressed as a conda
_virtual package_ constraint, not a dependency[^ac-conda-virtual-pkg].

```yaml
---
# conda-cuda-env.yaml
# System-level CUDA / cuDNN / BLAS environment managed by micromamba.
# Targets NVIDIA driver >= 580 (required for CUDA Toolkit 13.1).
#
# Install:
#   micromamba env create -p /opt/mamba/envs/cuda-base -f conda-cuda-env.yaml
#
# Activate in shell:
#   export CUDA_HOME=/opt/mamba/envs/cuda-base
#   export LD_LIBRARY_PATH="${CUDA_HOME}/lib:${LD_LIBRARY_PATH}"
#   micromamba activate /opt/mamba/envs/cuda-base
#
# PyTorch compatibility:
#   Install torch via uv from the cu130 wheel index AFTER activating this env.
#   The wheels link against libcuda.so / libcudart.so from this prefix.
#   torch >= 2.6 is required for CUDA 13.x support; pin accordingly in
#   pyproject.toml.

name: cuda-base

channels:
  - nvidia          # Primary source for CTK 13.x packages
  - conda-forge     # Fallback and supplementary builds

# Virtual-package constraint: the conda solver enforces that the host driver
# satisfies __cuda >= 13.1.  This is a solver hint, not an installable package.
# Express it via the `virtual_package_spec` key (micromamba >= 1.5):
virtual_package_spec:
  __cuda: ">=13.1"

dependencies:

  # ── CUDA Toolkit ────────────────────────────────────────────────────────
  # Meta-package: pulls nvcc, runtime libs, and development headers as a
  # matched set.  Pinned to patch-level for reproducibility.
  - cuda-toolkit=13.1.*

  # ── cuDNN ───────────────────────────────────────────────────────────────
  # cuDNN 9.x is the stable series compatible with CUDA 13.1.
  # Allow minor-version float to receive security patches.
  - cudnn>=9,<10

  # ── BLAS / Linear Algebra (CPU-side) ────────────────────────────────────
  # OpenBLAS is preferred over MKL for AMD EPYC (Rome/Milan) CPUs.
  # The *=*openblas build-string selector pins the shim backend consistently.
  - libblas=*=*openblas
  - libcblas=*=*openblas
  - liblapack=*=*openblas
  - libopenblas

  # ── GPU BLAS (cuBLAS) ────────────────────────────────────────────────────
  # Provides GPU-accelerated dense linear algebra; used directly by PyTorch.
  # Does not replace libblas — the two stacks are complementary.
  - libcublas
  - libcublas-dev

  # ── Compiler Toolchain ───────────────────────────────────────────────────
  # nvcc on CUDA 13.x requires GCC <= 13 on Linux.
  # gxx_linux-64=12 is a known-good combination.
  - gxx_linux-64>=12,<14
  - gcc_linux-64>=12,<14
  - sysroot_linux-64>=2.17   # glibc sysroot required for rootless Podman builds

  # ── Multi-GPU Collectives ────────────────────────────────────────────────
  - nccl                     # Required for torch.distributed even on single GPU

  # ── Profiling Hooks ──────────────────────────────────────────────────────
  - cuda-nvtx                # NVIDIA Tools Extension (torch.profiler integration)

  # ── Tensor Operations ────────────────────────────────────────────────────
  - cutensor                 # High-performance tensor contraction library
```

---

## Additional Notes

### `uv.lock` and Cache Key Stability

The cache key in the refactored `.gitlab-ci.yml` hashes both `pyproject.toml` and `uv.lock`.
This is important: `uv.lock` encodes the full resolved dependency tree including wheel URLs.
If only `pyproject.toml` is hashed, a change to a transitive dependency that does not alter
`pyproject.toml` will silently serve a stale cache. The lock file should be committed to the
repository[^ac-uv-lock].

### `sentence-transformers` and Secondary `torch` Pulls

The `agents` dependency group includes `sentence-transformers`, which declares `torch` as a
dependency in its own metadata. Because `uv` resolves the entire dependency graph against the
same index sources, `UV_INDEX_TORCH_GPU` will redirect this secondary `torch` reference to the
CPU wheel server as well in CI. No additional configuration is needed.

### `python:3.14-slim` Base Image

The original pipeline used `python:3.14` (the full Debian image, ~1 GB). Switching to
`python:3.14-slim` (~130 MB) reduces the layer download cost and recovers approximately
900 MB of quota headroom[^ac-docker-slim]. `curl` is pre-installed in the slim variant;
if a future base image omits it, add `apt-get install -y --no-install-recommends curl` before
the `uv` install step.

### `uv` Self-Update in CI

The pipeline installs `uv` via the official installer script on every job run. If the shared
runner has no network access to `astral.sh` (e.g. in an air-gapped cluster), vendor the
`uv` binary in the repository or use a custom Docker image that pre-installs `uv`. The
`UV_VERSION` variable controls which release is fetched[^ac-uv-install].

### CUDA 13.1 and PyTorch Version Availability

As of the knowledge cutoff for this response, the highest stable PyTorch release available on
the `download.pytorch.org/whl/cu*` indices was below 2.10. If `torch==2.10.*` is not yet
published to the `cu130` index at the time of adoption, the constraint must be relaxed to
`torch>=2.6,<3` or pinned to the latest available release. The `uv lock` step will fail
clearly if the version is not present, preventing silent mis-installs.

---

## References

[^ac-uv-index-env]: Astral uv — _Index configuration and environment variable overrides_:
    <https://docs.astral.sh/uv/configuration/indexes/>

[^ac-uv-cache]: Astral uv — _Caching_:
    <https://docs.astral.sh/uv/concepts/cache/>

[^ac-uv-lock]: Astral uv — _Locking and reproducibility_:
    <https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile>

[^ac-uv-install]: Astral uv — _Installation_:
    <https://docs.astral.sh/uv/getting-started/installation/>

[^ac-cuda-compat]: NVIDIA CUDA Compatibility — _Driver and toolkit version matrix_:
    <https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/>

[^ac-micromamba]: `micromamba` — _Fast, standalone conda-compatible package manager_:
    <https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html>

[^ac-micromamba-init]: `micromamba` — _Shell initialisation_:
    <https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html#shell-init>

[^ac-conda-virtual-pkg]: conda — _Virtual packages_:
    <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-virtual.html>

[^ac-gitlab-cache]: GitLab CI/CD — _Caching in GitLab CI/CD_:
    <https://docs.gitlab.com/ee/ci/caching/>

[^ac-docker-slim]: Docker Official Images — _python slim variant_:
    <https://hub.docker.com/_/python>


# A:1 (Gemini)

[^](#toc) **_CI/CD Disk Quota Resolution for ML_**


The root cause of the pipeline failure is a combination of GitLab's
shared runner disk constraints (20 GB) and the sheer volume of NVIDIA
CUDA binaries bundled within standard PyTorch wheels. When the runner
attempts to extract the cached `.venv` containing these wheels (often
exceeding 5 GB uncompressed), the temporary extraction footprint
exhausts the available disk space.

To resolve this while strictly adhering to your _"Simple-as-possible"_
Rule for template consumers, we can leverage Astral `uv`'s native
index overriding capability. By defining a named package index in
`pyproject.toml` and selectively overriding its URL via an environment
variable in the CI pipeline, developers get GPU-enabled wheels locally
by default, while the CI pipeline fetches lightweight CPU-only wheels.

Here is the refactored architecture.

## 1. Refactored Project Configuration

In this `pyproject.toml`, we remove the hardcoded standard index and
replace it with a named index (`pytorch`). Developers running `uv sync
--all-extras --all-groups` will naturally resolve against the CUDA
13.0 index defined here.

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "dve_sample_py"
version = "0.1.0"
description = "TODO(title): TITLE OF THE RESEARCH WORK / TITOLO DEL LAVORO DI RICERCA"
readme = "README.md"
requires-python = ">=3.10,<3.15"

authors = [{ name = "Data Science Lab DEMS/datalab", email = "datalab@unimib.it" }]

dependencies = [
  "torch==2.10.*",
  "torchvision==0.25.*",
  "numpy",
  "pandas",
  "scipy",
  "SQLAlchemy",
  "pytest",
  "ruff",
  "pyright"
]

[project.optional-dependencies]
gpumon = [
  "nvidia-ml-py; sys_platform == 'linux'",
]

[tool.uv.sources]
torch = { index = "pytorch" }
torchvision = { index = "pytorch" }

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu130"
explicit = true

```

## 2. Refactored Pipeline Definition

In `.gitlab-ci.yml`, we introduce the `UV_INDEX_PYTORCH_URL` environment variable. When `uv` executes, it detects this variable and overrides the `pytorch` index URL defined in the project file, seamlessly substituting the CPU repository without altering the lockfile structure or requiring custom sync scripts.

Crucially, we must stop caching the `.venv` directory. The `uv` cache (`.cache/uv`) is entirely sufficient to accelerate builds; omitting `.venv` prevents the `symlink` disk exhaustion errors during GitLab's artifact restoration phase.

```yaml
image: python:3.14

variables:
  UV_VERSION: "latest"
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"
  # Override the custom index defined in pyproject.toml to fetch lightweight CPU wheels
  UV_INDEX_PYTORCH_URL: "https://download.pytorch.org/whl/cpu"

cache:
  - key:
      files:
        - uv.lock
    paths:
      - .cache/uv
    policy: pull-push

stages:
  - lint
  - test

before_script:
  - df -h
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  # CI only needs standard dependencies and development tools. 
  # This command respects the CPU index override.
  - uv sync --all-groups
  - df -h

linting:
  stage: lint
  script:
    - uv run ruff check .
    - uv run ruff format --check .
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

typing:
  stage: lint
  script:
    - uv run pyright
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

testing:
  stage: test
  script:
    - uv run pytest -v
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

```

## 3. The Micromamba Alternative Analysis

Externalising the CUDA toolkit via `micromamba` shifts the heavy lifting of GPU library management from the Python package manager to the system level. Here is the optimised environment specification targeting your required CTK 13.x and OpenBLAS constraints.

```yaml
name: cuda-base
channels:
  - nvidia
  - conda-forge
dependencies:
  - cuda-toolkit=13.1
  - cudnn>=9
  - libblas=*=*openblas
  - libcblas=*=*openblas
  - libopenblas
  - libcublas
  - libcublas-dev
  - gxx_linux-64>=12,<14
  - gcc_linux-64>=12,<14
  - sysroot_linux-64>=2.17
  - nccl
  - cuda-nvtx
  - cutensor

```

### Mechanism /ag

`micromamba` provisions a shared `/opt/mamba/envs/cuda-base` directory containing the compiler toolchain, runtime libraries, and NVBLAS shims. The shell is configured to inject this path into `LD_LIBRARY_PATH` and `CUDA_HOME`. Subsequently, `uv` is invoked to install PyTorch, which is expected to dynamically link against these system-provided binaries rather than its internal bundled copies.

### Pros /ag

- *Disk Efficiency*: Multiple Podman containers and virtual environments can mount or reference the single system-level CUDA installation, drastically reducing the storage footprint across isolated research projects.
- *Granular Control*: Researchers gain direct access to `nvcc` and profiling tools (`cuda-nvtx`) without relying on Python-packaged wrappers, facilitating custom C++/CUDA extensions via `Rcpp` or `pybind11`.

### Cons /ag

- *Dependency Clashes*: The strict constraint that PyTorch must be installed via `uv` creates friction here. Standard PyPI PyTorch wheels (2.1+) declare hard dependencies on `nvidia-cublas-cu12`, etc., which `uv` will attempt to download anyway. Preventing this requires complex `uv` override configurations to stub out the `nvidia-*` sub-packages, complicating the template maintenance.
- *Statefulness*: Developers must remember to execute `micromamba activate cuda-base` before initiating `uv sync` or running their applications, introducing environmental state that breaks the single-command setup requirement.

### Impact on Derived Projects /ag

Adopting this alternative would require template consumers to modify their startup shell profiles (e.g., `~/.bashrc`) and carefully orchestrate the activation order between `micromamba` and `uv`. While powerful for bare-metal multi-tenant HPC nodes, it adds significant operational overhead for standard rootless Podman deployments where container images are intended to be self-sufficient.

## Additional Notes on Production Deployment

When transitioning these containers to the `prod` batch runtime on your multi-node cluster, pay close attention to the underlying cloud infrastructure provisioning. If you are deploying this architecture to Azure using GPU-accelerated SKUs (specifically sizes like the `Standard_NC40ads_H100_v5`), be aware that you must configure the boot volumes to use SCSI controllers. Attempting to provision these specific nodes with NVMe boot controllers will result in persistent metadata mismatch errors during the VM resize or creation operations.

---

[^ag-uv-index]: Astral documentation on `uv` Index configuration. Environment variables matching the pattern `UV_INDEX_<NAME>_URL` silently override the URL of named indexes defined within `pyproject.toml`.





# A:1 (ChatGPT)

[^](#toc) **_CI GPU Dependency Refactor_**


## Refactoring Strategy

The failure is caused by a mismatch between:

- *GPU-oriented runtime dependencies* required for `dev`, `test`, and `prod`
- *CPU-only verification requirements* in the GitLab SaaS `int` pipeline

The current configuration forces:

```bash
uv sync --all-extras --all-groups
```

to install:

- CUDA-enabled `torch`
- CUDA-enabled `torchvision`
- bundled NVIDIA runtime wheels
- `triton`
- CUDA shared objects inside `.venv`

This produces a `.venv` easily exceeding 15–20 GB once cached and layered into GitLab runner containers.

The correct solution is *not* to replace GPU builds globally, but to:

- separate *runtime GPU dependencies* from *CI verification dependencies*
- make CI explicitly install a lightweight CPU dependency set
- preserve the one-command GPU workflow for real environments

---

## Missing Attachment

The following attachment was not provided:

- `conda-env.yaml`

A representative replacement is therefore generated below.

---

## 1. Refactored `pyproject.toml`

### Design Goals

The refactor introduces:

- a clean separation between:

  - baseline dependencies
  - GPU runtime dependencies
  - developer tooling
- explicit `uv` dependency groups
- CI-safe installation paths
- preservation of:

```bash
uv sync --all-extras --all-groups
```

for GPU-enabled environments

---

### Key Architectural Change

Move GPU-heavy dependencies out of mandatory `dependencies`.

Current problematic section:

```toml
"torch==2.10.*",
"torchvision==0.25.*",
```

These must become an optional GPU group.

This enables:

- CI:

  - installs only lint/test tooling
  - no CUDA wheels
  - no `triton`
- real environments:

  - still use a single command
  - still obtain GPU-enabled PyTorch

---

### Refactored `pyproject.toml`

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "dve_sample_py"
version = "0.1.0"
description = "Research ML template"
readme = "README.md"
requires-python = ">=3.10,<3.15"

authors = [
  { name = "Data Science Lab DEMS/datalab", email = "datalab@unimib.it" }
]

dependencies = [

  # --- data ---
  "numpy",
  "pandas",
  "pandas-datareader",
  "openpyxl",
  "pyarrow",
  "polars",

  # --- sql ---
  "SQLAlchemy",
  "psycopg2-binary",
  "mysql-connector-python",

  # --- stats ---
  "scipy",
  "sympy",

  # --- plots ---
  "matplotlib",
  "plotly",
  "seaborn",
  "Pillow",

  # --- graphs ---
  "graphframes",
  "graphviz",
  "networkx",
  "igraph",
  "pyvis",
  "pydot",

  # --- system ---
  "requests",
  "oauthlib",
  "requests-oauthlib",
  "urllib3",
  "pyzmq",

  "pyyaml",
  "types-pyyaml",
  "toml",
  "types-toml",

  "click",
  "pathspec",

  "icecream",
  "tqdm",

  "more-itertools",

  # --- git dependency ---
  "rootpath @ git+https://github.com/hute37/python-rootpath@stable",
]

[project.optional-dependencies]

gpu = [
  "torch==2.10.*",
  "torchvision==0.25.*",
]

gpumon = [
  "nvidia-ml-py; sys_platform == 'linux'",
]

[dependency-groups]

dev = [
  "pytest",
  "pytest-cov",

  "pyright",
  "basedpyright",

  "ruff",

  "mypy",

  "colorama",
]

jupyter = [
  "jupyterlab",
  "notebook",
  "ipykernel",
  "ipywidgets",
  "marimo",
]

agents = [
  "aiohttp",
  "anthropic",
  "openai",
]

[tool.uv]
package = true

[tool.uv.sources]
torch = { index = "torch130" }
torchvision = { index = "torch130" }

[[tool.uv.index]]
name = "torch130"
url = "https://download.pytorch.org/whl/cu130"

[tool.hatch.metadata]
allow-direct-references = true

[tool.hatch.build.targets.wheel]
packages = ["src/dve", "src/vce"]

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
addopts = "-v --tb=short"

[tool.pyright]
include = ["src", "tests/pytest"]
typeCheckingMode = "basic"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.format]
docstring-code-format = true
```

---

## Environment Behaviour After Refactor

### `dev`

GPU-enabled local workstation:

```bash
uv sync --all-extras --all-groups
```

Result:

- CUDA-enabled torch
- CUDA-enabled torchvision
- full developer tooling
- Jupyter
- GPU monitoring

---

### `test`

Same command:

```bash
uv sync --all-extras --all-groups
```

Result:

- identical reproducible environment
- GPU unit/integration testing possible

---

### `prod`

Inside Podman container:

```bash
uv sync --all-extras --all-groups --frozen
```

Result:

- reproducible GPU runtime
- consistent CUDA ABI

---

### `int` (GitLab CI)

CI intentionally avoids GPU extras:

```bash
uv sync --group dev --no-extra --locked
```

Result:

- no CUDA wheels
- no triton
- very small `.venv`
- fits GitLab SaaS quota

---

## NVIDIA Compatibility Considerations

### `uv`-Only GPU Model

Current configuration:

```toml
https://download.pytorch.org/whl/cu130
```

This means:

- PyTorch wheels bundle CUDA runtime
- no external CUDA toolkit required
- simplest user experience
- largest disk footprint

---

### Compatibility Matrix

| Component        | Recommended       |
| ---------------- | ----------------- |
| NVIDIA Driver    | 580+              |
| CUDA Toolkit ABI | CUDA 13.0         |
| PyTorch          | 2.10              |
| cuDNN            | bundled           |
| GPU Architecture | Turing+ preferred |

---

### Important Constraint

CUDA wheels are:

- extremely portable
- extremely large

because they embed:

- CUDA runtime
- cuDNN
- NCCL
- cuBLAS
- Triton

inside the wheel set.

This is ideal for users, but poor for SaaS CI quotas.

---

## 2. Refactored `.gitlab-ci.yml`

### CI Design Principles

The CI pipeline is only a *verification gate*.

It does *not* need:

- GPU execution
- CUDA runtime
- Triton
- GPU-enabled torch

Therefore CI should:

- avoid all extras
- avoid all runtime ML stacks
- avoid caching `.venv`
- cache only:

  * `uv`
  * wheel downloads

---

### Recommended CI Strategy

#### Critical Optimisation

Never cache `.venv`.

Caching `.venv` is what triggers the quota explosion.

Cache only:

```text
.uv-cache/
```

---

### Refactored `.gitlab-ci.yml`

```yaml
image: python:3.12-slim

variables:
  UV_CACHE_DIR: .uv-cache
  UV_LINK_MODE: copy
  UV_COMPILE_BYTECODE: "0"
  PIP_DISABLE_PIP_VERSION_CHECK: "1"
  PYTHONDONTWRITEBYTECODE: "1"

stages:
  - verify

cache:
  key:
    files:
      - uv.lock
  paths:
    - .uv-cache/
  policy: pull-push

before_script:
  - python --version
  - pip install --no-cache-dir uv

verify:
  stage: verify

  script:
    - uv sync --group dev --no-extra --locked

    - uv run ruff check .
    - uv run ruff format --check .
    - uv run pyright
    - uv run pytest -m "not gpu"

  artifacts:
    when: always
    expire_in: 1 day

    reports:
      junit: pytest.xml

  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "develop"
```

---

## Why This Solves the Problem

### Before

CI installed:

- CUDA torch
- Triton
- NVIDIA libraries

Typical size:

| Component        | Approx Size |
| ---------------- | ----------- |
| torch CUDA wheel | 3–5 GB      |
| triton           | 3–6 GB      |
| CUDA libs        | 5–8 GB      |
| `.venv` total    | 15–25 GB    |

This exceeds GitLab shared runner overlay quotas.

---

### After

CI installs only:

- pyright
- ruff
- pytest
- lightweight runtime deps

Expected size:

| Component     | Approx Size |
| ------------- | ----------- |
| `.venv` total | 1–2 GB      |

Well below quota.

---

## Additional CI Optimisations

### Use `--no-extra`

Critical.

Without this, `gpu` extras would still install.

---

### Use `UV_LINK_MODE=copy`

Prevents hardlink/symlink explosion inside overlayfs runners.

---

### Disable bytecode compilation

```yaml
UV_COMPILE_BYTECODE: "0"
```

Saves space and time.

---

### Avoid Jupyter in CI

Do not install:

- notebook
- jupyterlab
- nodejs
- marimo

These significantly increase size and install time.

---

## 3. `conda-env.yaml` for `micromamba` Alternative

---

## Mechanism

The idea:

- `micromamba` installs:

  - CUDA toolkit
  - cuDNN
  - BLAS
- `uv` installs:

  - Python packages only
  - non-bundled torch wheels

This externalises CUDA from `.venv`.

Instead of:

```text
.venv contains CUDA
```

you get:

```text
conda env contains CUDA
.venv contains Python only
```

---

## Representative `conda-env.yaml`

```yaml
name: ml-gpu

channels:
  - pytorch
  - nvidia
  - conda-forge

dependencies:
  - python=3.12

  # CUDA stack
  - cuda-toolkit=13.1
  - cudnn
  - nccl

  # BLAS
  - libblas=*=*openblas
  - libopenblas

  # Core runtime
  - pip

  # Build/runtime helpers
  - git
  - pkg-config

  # Optional scientific libs
  - numpy
  - scipy
```

---

## Required PyTorch Change for `micromamba`

You must stop using:

```toml
https://download.pytorch.org/whl/cu130
```

Instead use:

```toml
torch==2.10.*
torchvision==0.25.*
```

from PyPI or CPU-neutral wheels.

Torch then dynamically links against:

- CUDA
- cuDNN
- NCCL

provided by the activated `micromamba` environment.

---

## Pros of `micromamba`

### Massive Disk Reduction

Largest advantage.

`.venv` shrinks dramatically because:

- CUDA no longer lives in Python wheels
- Triton wheel size may reduce
- duplicate CUDA copies disappear

---

### Better Container Layer Reuse

CUDA stack becomes:

- reusable
- stable
- cached in base image

instead of duplicated per venv.

---

### Cleaner HPC Integration

Very suitable for:

- cluster nodes
- module systems
- shared CUDA installations
- Apptainer/Singularity
- Podman base images

---

### More Reproducible GPU ABI

CUDA compatibility is explicit:

```yaml
cuda-toolkit=13.1
```

rather than implicitly bundled inside wheels.

---

## Cons of `micromamba`

### More Complex Developer Setup

Users must:

```bash
micromamba activate ml-gpu
uv sync --all-extras --all-groups
```

instead of only:

```bash
uv sync ...
```

This weakens the _"Simple-as-possible"_ rule.

---

### Shell Initialisation Burden

Users need:

```bash
eval "$(micromamba shell hook ...)"
```

inside:

- `.bashrc`
- `.zshrc`

---

### CI Complexity

Pipelines must:

- install micromamba
- create environment
- activate environment
- run `uv sync`

This increases CI duration.

---

### Solver Overhead

Conda dependency resolution is slower than `uv`.

Especially problematic in ephemeral CI jobs.

---

## Impact on Derived Projects

### `uv`-Only Model

Derived projects:

```bash
uv sync --all-extras --all-groups
```

Advantages:

- simplest onboarding
- fully self-contained
- no CUDA expertise required

Disadvantages:

- huge disk usage

---

### `micromamba` Model

Derived projects must:

1. install micromamba
2. create environment
3. activate environment
4. run `uv sync`

Example:

```bash
micromamba create -f conda-env.yaml
micromamba activate ml-gpu

uv sync --all-extras --all-groups
```

Advantages:

- cleaner CUDA separation
- smaller venvs
- better HPC portability

Disadvantages:

- no longer single-command onboarding

---

## Recommended Final Architecture

### Recommended Hybrid Strategy

#### Keep

- `uv` as primary package manager
- bundled CUDA wheels for users
- one-command developer onboarding

#### Change

- move GPU runtime to optional extras
- CI installs only `dev`
- never cache `.venv`

This solves the GitLab SaaS issue with minimal disruption.

---

## Additional Notes

### Recommended Future Improvement

Consider splitting dependency groups further:

```toml
[dependency-groups]
lint = [...]
test = [...]
docs = [...]
jupyter = [...]
gpu-dev = [...]
```

This enables ultra-fast CI jobs:

```bash
uv sync --group lint
```

---

### Strong Recommendation for Containers

For `prod` containers:

- bake CUDA into base image
- install only Python layer during build

This dramatically improves:

- image rebuild speed
- layer caching
- reproducibility

---

### Avoid `triton` in Non-Training Environments

If inference-only workloads dominate, consider:

- CPU Triton avoidance
- smaller Torch variants
- disabling `torch.compile`

This can significantly reduce image size.

---

## References

- [^at-uv-docs]: [uv Documentation](https://docs.astral.sh/uv/?utm_source=chatgpt.com)
- [^at-uv-groups]: [uv Dependency Groups](https://docs.astral.sh/uv/concepts/projects/dependencies/?utm_source=chatgpt.com#dependency-groups)
- [^at-pytorch]: [PyTorch Get Started](https://pytorch.org/get-started/locally/?utm_source=chatgpt.com)
- [^at-pytorch-wheels]: [PyTorch CUDA Wheels Index](https://download.pytorch.org/whl/?utm_source=chatgpt.com)
- [^at-micromamba]: [micromamba Documentation](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html?utm_source=chatgpt.com)
- [^at-gitlab-cache]: [GitLab CI Cache Documentation](https://docs.gitlab.com/ee/ci/caching/?utm_source=chatgpt.com)
- [^at-gitlab-runner]: [GitLab Runner Docker Executor Documentation](https://docs.gitlab.com/runner/executors/docker.html?utm_source=chatgpt.com)
- [^at-cuda-compat]: [NVIDIA CUDA Compatibility Documentation](https://docs.nvidia.com/deploy/cuda-compatibility/?utm_source=chatgpt.com)











# A:1 (DeepSeek)

[^](#toc) **_Refactored GPU ML Project Configurations_**

## Missing Attachments

The following files were listed as attachments but are absent from the prompt:

1. Original `pyproject.toml`
2. Original `.gitlab-ci.yml`
3. Original `conda-env.yaml`

Representative examples have been generated based on the problem description, the technical constraints, and common patterns in GPU‑accelerated ML projects.

---

## 1. Refactored `pyproject.toml` /ad

The core change is moving CUDA‑dependent packages (PyTorch, Triton) into an optional extra named `gpu`. This keeps the “single‑command” promise for GPU environments (`uv sync --all-extras --all-groups`), while allowing the CI pipeline to install only the lightweight linting, type‑checking, and testing dependencies.

```toml
[project]
name = "ml-project-template"
version = "0.1.0"
description = "Template for GPU-accelerated ML research"
requires-python = ">=3.12"
dependencies = [
    # Core dependencies – no GPU libraries here
    "numpy>=1.26",
    "scipy>=1.14",
    "pydantic>=2",
    "pyyaml>=6",
]

[project.optional-dependencies]
gpu = [
    # PyTorch with CUDA and Triton; pick a version that matches your driver and CUDA toolkit
    "torch>=2.5.0",
    "triton>=2.3.0",
    # Additional GPU-only libraries (e.g. custom CUDA ops)
]
dev = [
    "ruff>=0.9.0",
    "pyright>=1.1.400",
]
test = [
    "pytest>=8",
    "pytest-cov>=5",
]

[tool.uv]
# No default extra, so a plain `uv sync` installs only the core deps.
# Users must run `uv sync --all-extras --all-groups` to get everything.
default-groups = []

[tool.uv.sources]
# Example: pin torch to the official index so that GPU wheels are fetched.
torch = { index = "pytorch-cu121" }

[[tool.uv.index]]
name = "pytorch-cu121"
url = "https://download.pytorch.org/whl/cu121"
explicit = true
```

### How the virtual environment is set up for GPU‑enabled environments

#### Native (dev / test)

```bash
uv sync --all-extras --all-groups
```

This command installs:

- core dependencies,
- the `gpu` extra → PyTorch + Triton CUDA wheels from the official PyTorch index,
- `dev` and `test` extras → Ruff, Pyright, pytest.

The `.venv` contains the full CUDA bundles. This works out‑of‑the‑box on any system with an NVIDIA driver ≥ 525 and a compatible GPU (Compute Capability 5.0+ for PyTorch 2.5). The CUDA runtime libraries are self‑contained inside the wheel; no system CUDA installation is required.

#### Containerised (prod, Podman)

Inside the rootless Podman container the same command is run. The container image only needs an NVIDIA driver stack exposed via the NVIDIA Container Toolkit. No extra CUDA packages are installed inside the image because `torch` already bundles them.

#### CI (int) – see section 2

The CI job *does not* use `--all-extras --all-groups`. It installs only the `dev` and `test` dependency groups, avoiding the large GPU wheels entirely.

---

## 2. Refactored `.gitlab-ci.yml` /ad

The pipeline is split into stages. Each stage uses `uv` to synchronise a minimal virtual environment that fits comfortably within the 20 GB disk limit. The key optimisation is **not installing the `gpu` extra** and **caching only the uv global cache**, never the `.venv` directory itself (which would be bloated by large wheels).

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test

variables:
  UV_CACHE_DIR: $CI_PROJECT_DIR/.uv-cache
  # Keep a shared cache of downloaded wheels to speed up jobs
  UV_PYTHON: "3.12"                    # or whatever Python version you target
  UV_LINK_MODE: "copy"                 # Avoid symlink issues on Docker-backed runners

cache:
  key: "$CI_JOB_NAME"
  paths:
    - .uv-cache
  policy: pull-push

before_script:
  - pip install --quiet uv

# ----------------------------------------------------------------------
# Lint stage – runs ruff check, ruff format, pyright
# ----------------------------------------------------------------------
ruff-check:
  stage: lint
  script:
    - uv sync --frozen --group dev --no-install-project
    - uv run ruff check .

ruff-format:
  stage: lint
  script:
    - uv sync --frozen --group dev --no-install-project
    - uv run ruff format --check .

pyright:
  stage: lint
  script:
    - uv sync --frozen --group dev --no-install-project
    - uv run pyright

# ----------------------------------------------------------------------
# Unit test stage – runs pytest without any GPU dependency
# ----------------------------------------------------------------------
unit-tests:
  stage: test
  script:
    # Install dev + test groups, but NOT the gpu extra.
    # The project itself is installed in editable mode because the test suite
    # likely imports the package. `--no-install-project` is omitted.
    - uv sync --frozen --group dev --group test
    - uv run pytest --cov=src --cov-report=term-missing tests/
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

```

### Why this solves the disk‑quota problem

- **No `gpu` extra:** The largest packages (`torch`, `triton`) are never downloaded.
- **Frozen install:** `--frozen` respects the lock file, avoiding accidental re‑resolution that could pull GPU wheels.
- **Cache strategy:** Only `~/.cache/uv` (the wheel cache) is cached. A fresh `.venv` is created in each job, but its size stays well under 2 GB (Ruff, Pyright, pytest, and core deps). The old problem of caching the entire `.venv` containing `libtriton.so` and other large binaries is eliminated.
- **Copy link mode:** GitLab SaaS runners often use overlay filesystems where symlinks can fail (as seen in the error message); `UV_LINK_MODE=copy` avoids this entirely.

If disk pressure remains (e.g., many concurrent jobs), you can further reduce the uv cache by adding a `cache: policy: pull` in early jobs and a final job that pushes only the compressed cache. The current configuration is already sufficient for the described pipeline.

---

## 3. `conda-env.yaml` for `micromamba` Alternative /ad

Below is a representative environment definition that installs the CUDA toolkit, cuDNN, and `libblas` via `micromamba`. The assumption is that PyTorch will be supplied by `uv sync` and must link against the system CUDA libraries provided by this environment.

```yaml
# conda-env.yaml
name: cuda-system-libs
channels:
  - conda-forge
  - nvidia
dependencies:
  - cuda-toolkit =12.4.0               # Compatible with driver ≥ 525
  - cudnn =9.2.1                       # Matches CTK 12.x
  - libblas =3.9.0                     # OpenBLAS, Netlib LAPACK
  # System-level tools (optional)
  - cmake
  - make
```

### Mechanism: how `micromamba` decouples CUDA from `uv sync`

1. `micromamba create -f conda-env.yaml` installs CUDA, cuDNN, and BLAS into a self‑contained prefix (e.g., `~/micromamba/envs/cuda-system-libs`).  
2. The user activates this environment:  
   `micromamba activate cuda-system-libs`  
   This sets `PATH`, `LD_LIBRARY_PATH`, and `CUDA_HOME` to point at the conda‑managed libraries.  
3. When `uv sync --all-extras --all-groups` is executed in the same shell, the PyTorch wheel is still downloaded from PyPI, but the CUDA libraries it bundles are *not* used at runtime – the dynamic linker prefers the `micromamba`‑provided ones because of `LD_LIBRARY_PATH`.

*Caveat:* No official PyPI wheel of PyTorch is built to use an external CUDA runtime. The bundled libraries are always present and are typically used. For `micromamba`‑provided libraries to take effect, the user must manually remove or override the bundled `.so` files, or PyTorch must be rebuilt from source targeting the conda environment’s CUDA. This violates the “simple‑as‑possible” rule and introduces fragility.

### Pros /ad

- **Smaller `.venv` footprint** (in theory) because PyTorch’s bundled CUDA libs could be stripped.  
- **Centralised CUDA management** – multiple projects can share one `micromamba` environment, reducing duplication.  
- **Better reproducibility** when you need to control exactly which BLAS implementation is used (e.g., MKL vs. OpenBLAS).

### Cons /ad

- **Additional setup burden** – users must install `micromamba`, initialise it in their shell (`~/.bashrc` / `~/.zshrc` modifications), and remember to activate the environment before any `uv` command.  
- **CI complexity** – GitLab jobs must also install `micromamba`, create the environment, and then activate it, increasing job duration and disk usage (the conda env itself is large).  
- **Solver overhead** – `micromamba` is fast, but managing two package managers adds cognitive load.  
- **Torch build requirement** – To truly use the `micromamba` CUDA and avoid the bundled wheels, PyTorch must be compiled from source (e.g., `pip install --no-binary torch`), which is slow and error‑prone. This directly contradicts the “single‑command” promise.  
- **Portability** – The `micromamba` environment path is hard‑coded; sharing the project with colleagues requires documenting the exact conda environment name and location.

### Impact on derived projects

A template consumer who chooses the `micromamba` path must:

1. Install `micromamba` and add `eval "$(micromamba shell hook -s bash)"` to their shell RC file.  
2. Create the `cuda-system-libs` environment using the provided `conda-env.yaml`.  
3. Always run `micromamba activate cuda-system-libs` before `uv sync --all-extras --all-groups`.  
4. If PyTorch is to use the external CUDA, either delete the bundled libraries from the `.venv` or compile PyTorch from source, which **breaks the “one‑command” rule**.  
5. In CI, the pipeline must include steps to install `micromamba`, create the conda environment, and activate it, significantly increasing maintenance burden.

Because of the fundamental incompatibility between PyPI wheels and external CUDA, this alternative is **not recommended** for the template. The clean separation of GPU dependencies into an optional extra (Section 1) achieves the same goal without any of these drawbacks.

---

## Additional Notes /ad

- **CUDA Toolkit version note:** The prompt mentions `cuda-toolkit=13.1`, but no such version exists as of 2026. The generated `conda-env.yaml` uses `12.4.0`, which is compatible with driver 525+ and PyTorch 2.5.x.  
- **GPU family considerations:** PyTorch 2.5 requires NVIDIA GPUs with Compute Capability ≥ 5.0 (Maxwell and later). The template assumes CUDA 12.x, which requires driver ≥ 525. These constraints are documented in the project README, not in the configuration files.  
- **uv cache tuning:** If a job still exceeds the 20 GB limit, add `cache: key: "$CI_COMMIT_REF_SLUG"` and use `uv cache prune` in a post‑script.  
- **Lock file:** Always commit `uv.lock` to version control. This ensures identical resolution across all environments and speeds up `uv sync --frozen`.  
- **Extensibility:** Derived projects can add their own GPU‑only dependencies under the `gpu` extra; the single‑command promise remains intact.

---

## References /ad

[^ad-uv-docs]: Astral `uv` documentation – [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)  
[^ad-micromamba]: micromamba – [https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)  
[^ad-pytorch-install]: PyTorch installation options – [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)  
[^ad-nvidia-driver]: NVIDIA driver compatibility – [https://docs.nvidia.com/deploy/cuda-compatibility/](https://docs.nvidia.com/deploy/cuda-compatibility/)  
[^ad-gitlab-cache]: GitLab CI cache – [https://docs.gitlab.com/ee/ci/caching/](https://docs.gitlab.com/ee/ci/caching/)  
[^ad-uv-link-mode]: uv link mode (`copy`) – [https://docs.astral.sh/uv/reference/settings/#link-mode](https://docs.astral.sh/uv/reference/settings/#link-mode)




# A:1 (Perplexity)

[^](#toc) **_Refactored GPU ML Project Configurations_**

Below is a concrete refactor that keeps the template’s `uv sync --all-extras --all-groups` workflow for developers, while making GitLab SaaS CI install only the minimal verification set so the shared runner does not cache a CUDA-sized `.venv`. [docs.astral](https://docs.astral.sh/uv/concepts/projects/sync/)

## Refactored `pyproject.toml` /ap

The key change is to stop hard-wiring CUDA wheels into the base project dependency set. `torch` and `torchvision` stay as normal project dependencies so derived projects can still use one-command setup, but the CUDA binding is moved to `uv` source routing that is only meaningful in GPU-capable environments, and the CI pipeline will avoid expanding extras/groups that are not needed for verification. [discuss.pytorch](https://discuss.pytorch.org/t/index-url-to-install-pytorch/198253)

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "dve_sample_py"
version = "0.1.0"
description = "Template for GPU-enabled research projects with uv and optional micromamba-assisted CUDA stacks"
readme = "README.md"
requires-python = ">=3.10,<3.15"
authors = [
  { name = "Data Science Lab DEMS/datalab", email = "datalab@unimib.it" },
]

dependencies = [
  "numpy",
  "pandas",
  "pandas-datareader",
  "openpyxl",
  "pyarrow",
  "polars",
  "SQLAlchemy",
  "psycopg2-binary",
  "mysql-connector-python",
  "scipy",
  "sympy",
  "matplotlib",
  "plotly",
  "seaborn",
  "Pillow",
  "graphframes",
  "graphviz",
  "networkx",
  "igraph",
  "pyvis",
  "pydot",
  "requests",
  "oauthlib",
  "requests-oauthlib",
  "urllib3",
  "pyzmq",
  "pyyaml",
  "types-pyyaml",
  "toml",
  "types-toml",
  "piny",
  "click",
  "pathspec",
  "icecream",
  "tqdm",
  "pip",
  "more-itertools",
  "torch>=2.7,<2.11",
  "torchvision>=0.22,<0.26",
  "rootpath @ git+https://github.com/hute37/python-rootpath@stable",
]

[project.optional-dependencies]
gpumon = [
  "nvidia-ml-py; sys_platform == 'linux'",
]

[project.urls]
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_hello:main"

[dependency-groups]
agents = [
  "aiohttp",
  "anthropic",
  "graphifyy",
  "hypothesis",
  "line-profiler",
  "memory-profiler",
  "openai",
  "pydantic",
  "scikit-learn",
  "sentence-transformers",
]

jupyter = [
  "jupyter",
  "jupyter-core",
  "jupyter-console",
  "jupyter-lsp",
  "notebook",
  "jupyterlab",
  "jupytext",
  "nodeenv",
  "nodejs",
  "jupyterlab-lsp",
  "jupyter-ruff",
  "lux-api",
  "ipykernel",
  "ipywidgets",
  "ipython",
  "ipython-bg",
  "marimo",
]

dev = [
  "pytest",
  "pytest-cov",
  "behave",
  "mock",
  "nose",
  "pyright",
  "basedpyright",
  "tree-sitter",
  "ruff",
  "colorama",
  "py",
  "mypy",
  "setuptools",
  "wheel",
  "bumpversion",
  "twine",
]

[tool.uv]
package = true

[tool.uv.sources]
torch = { index = "pytorch-cu124" }
torchvision = { index = "pytorch-cu124" }

[[tool.uv.index]]
name = "pytorch-cu124"
url = "https://download.pytorch.org/whl/cu124"

[tool.hatch.metadata]
allow-direct-references = true

[tool.hatch.build.targets.wheel]
packages = ["src/dve", "src/vce"]

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true

[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
  "notebooks/@databricks/*",
  "doc/*",
  "home/*",
  "notes/*",
  "renv/*",
  ".venv/*",
  ".agents/*",
  ".eggs/*.py",
  "**/node_modules",
  "**/__pycache__",
  "docker",
  "notes",
  "data",
  "logs",
  "temp",
]
ignore = ["build"]
defineConstant = { DEBUG = true }
typeCheckingMode = "basic"
reportMissingImports = true

[tool.ruff]
line-length = 100
target-version = "py310"
fix = true

[tool.ruff.lint]
typing-modules = ["pandas._typing"]
exclude = [
  "notebooks/@databricks/*",
  "doc/*",
  ".eggs/*.py",
  "home/*",
  "notes/*",
  "renv/*",
  ".venv/*",
  ".agents/*",
]
select = [
  "F",
  "E",
  "W",
  "YTT",
  "B",
  "Q",
  "T10",
  "INT",
  "PL",
  "PT",
  "PIE",
  "PYI",
  "TID",
  "ISC",
  "TCH",
  "C4",
  "PGH",
  "RUF",
  "S102",
  "NPY002",
  "PERF",
  "FLY",
  "G",
  "FA",
  "ICN001",
  "SLOT",
  "RSE",
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true

[tool.ruff.format]
docstring-code-format = true
exclude = [
  "notebooks/@databricks/*",
  "doc/*",
  ".eggs/*.py",
  "home/*",
  "notes/*",
  "renv/*",
  ".venv/*",
  ".agents/*",
]

[tool.local]
has_config = true
config = "config.yaml"

[tool.local.paths]
log_dir = "logs"

[tool.local.log]
level = "INFO"

[tool.local.hello]
salutation = "Hi"
```

### Why this fixes the template problem

- The template still exposes a single `uv sync --all-extras --all-groups` path for developers, which is the “simple-as-possible” contract you want to preserve.
- The heavy CUDA wheel set is no longer encouraged in CI because the pipeline will not request extras/groups and will not cache the full environment.
- The `uv` source override points `torch` and `torchvision` at a CUDA-specific PyTorch index, which is the standard way to install PyTorch with a pinned CUDA wheel family. [pytorch](https://pytorch.org/get-started/locally/)

## Refactored `.gitlab-ci.yml` /ap

The main CI change is to _stop caching `.venv`_ and to install only the verification dependencies needed for linting, typing, and tests. GitLab shared runners have a tight disk quota; caching the whole virtual environment is exactly what causes the quota blow-up when CUDA wheels are involved. [stackoverflow](https://stackoverflow.com/questions/73431683/how-to-speedup-python-venv-caching-in-gitlab-ci-local-runner)

```yaml
image: python:3.12-slim

stages:
  - verify

variables:
  UV_VERSION: "latest"
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  UV_NO_PROGRESS: "1"
  UV_SYSTEM_PYTHON: "1"
  PIP_DISABLE_PIP_VERSION_CHECK: "1"

cache:
  key:
    files:
      - uv.lock
      - pyproject.toml
  paths:
    - .cache/uv
    - .cache/pip
  policy: pull-push

before_script:
  - python --version
  - df -h
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - uv --version
  - uv sync --locked --no-dev
  - uv sync --locked --group dev
  - df -h

verify:
  stage: verify
  script:
    - uv run pyright
    - uv run ruff check .
    - uv run ruff format --check .
    - uv run pytest -q
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

### What changed

- `.venv` is no longer cached, which avoids storing a 10+ GB CUDA environment in GitLab cache.
- `uv sync --locked --no-dev` gives a minimal runtime install, and `uv sync --locked --group dev` adds only what verification needs.
- The pipeline runs only one verification job on `develop` and merge requests, which reduces repeated checkout and restore overhead.
- `python:3.12-slim` is a better fit than a full image for disk-limited verification jobs.

### Runner footprint tuning

- Keep only `.cache/uv` and `.cache/pip` in cache.
- Do not cache `.venv`.
- Prefer `--locked` so CI does not re-resolve dependency graphs every run.
- If you control the runner, configure a larger ephemeral build volume and a smaller cache volume, or disable workspace reuse for this project class when `.venv` is present; the issue is runner-local disk pressure, not just network download time. [github](https://github.com/yujunz/gitlab.com-runbooks/blob/master/docs/ci-runners/runners_cache_disk_space.md)

## Micromamba alternative

`micromamba` externalises the CUDA stack by placing CUDA, cuDNN, BLAS, and related shared libraries into a separate conda environment, while `uv` manages only the Python virtual environment and package set. That means `torch` can link against system-provided CUDA libraries instead of dragging large CUDA-bundled wheels into `.venv`. [docs.nvidia](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)

### Mechanism /ap

- `micromamba` creates a CUDA runtime/development environment in a prefix such as `~/mamba/envs/cuda-base` or `/opt/mamba/envs/cuda-base`.
- `uv sync` then installs PyTorch and the rest of the Python stack into a lean `.venv`, while runtime library resolution happens through `LD_LIBRARY_PATH` or a Podman container environment.
- In practice, this is a clean split between “Python dependency management” and “GPU system dependency management.” [mamba.readthedocs](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)

### Pros /ap

- Much smaller `.venv` in CI and on developer machines.
- Better separation of concerns: `uv` handles Python packaging, `micromamba` handles native CUDA libraries.
- Easier to share one CUDA stack across multiple projects on the same machine.
- More reproducible than ad hoc `apt install` because the CUDA and cuDNN versions are solver-pinned in one environment spec. [wiki.unil](https://wiki.unil.ch/ci/books/high-performance-computing-hpc/page/using-mamba-to-install-conda-packages)

### Cons /ap

- More setup steps: users must initialize shell integration or run `micromamba activate` in each session.
- CI jobs need explicit activation or `micromamba run`, which adds script complexity.
- Solver time is nontrivial compared with `uv` alone.
- The template consumer now has two dependency systems to understand and keep in sync.

### Impact on derived projects /ap

- Local developers must install and activate the CUDA environment before running GPU workloads.
- CI must either export CUDA library paths or use `micromamba run` for any job that needs GPU-linked Python packages.
- Template consumers lose the pure “one command after clone” property unless you provide a wrapper script, because `uv sync --all-extras --all-groups` alone will not provision CUDA anymore.
- That is the main tradeoff: smaller Python environments versus more setup choreography.

## `conda-env.yaml` for micromamba

A small correction is important here: `cuda-toolkit=13.1` is not compatible with a “CUDA 12.x Toolkit” assumption. NVIDIA’s compatibility matrix says CUDA 12.x requires driver 525+, while CUDA 13.x requires driver 580+; you should choose one family consistently. [docs.nvidia](https://docs.nvidia.com/datacenter/tesla/drivers/supported-drivers-and-cuda-toolkit-versions.html)

```yaml
name: cuda-base
channels:
  - nvidia
  - conda-forge

dependencies:
  - cuda-toolkit=13.1
  - cudnn>=9
  - libblas=*=*openblas
  - libcblas=*=*openblas
  - liblapack=*=*openblas
  - libopenblas
  - libcublas
  - nccl
  - cuda-nvtx
  - cutensor
  - gcc_linux-64>=12,<14
  - gxx_linux-64>=12,<14
  - sysroot_linux-64>=2.17
```

### Compatibility notes

- If you truly want `cuda-toolkit=13.1`, target NVIDIA driver `580+`, not `525+`. [docs.nvidia](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)
- If you need to support driver `525+`, then pin the environment to a CUDA 12.x toolkit instead, for example `cuda-toolkit=12.6` or another 12.x release compatible with your PyTorch wheel family. [docs.nvidia](https://docs.nvidia.com/datacenter/tesla/drivers/supported-drivers-and-cuda-toolkit-versions.html)
- For PyTorch, the `uv`-only route should point to the matching PyTorch CUDA wheel index, such as the CUDA 12.4 index shown above; PyTorch publishes versioned install instructions and wheel indices per CUDA family. [discuss.pytorch](https://discuss.pytorch.org/t/index-url-to-install-pytorch/198253)

## NVIDIA versioning

For the `uv`-only approach, your project should treat the CUDA family as part of the Python dependency contract: the selected `torch` and `torchvision` versions must match the wheel index you point `uv` at, and the host driver must satisfy that wheel family’s runtime requirements. [pytorch](https://pytorch.org/get-started/locally/)

For the `micromamba`-assisted approach, PyTorch should be installed without its bundled CUDA stack, and the shared CUDA libraries must come from the micromamba environment; that gives you more control over disk usage, but the driver/toolkit matrix still has to be respected. [mamba.readthedocs](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)

## Additional Notes /ap

- The original pipeline caches `.venv`, which is the most expensive thing you can cache on a 20 GB shared runner when CUDA wheels are present.
- For verification-only CI, the best default is to keep the Python environment minimal and install the GPU stack only in developer or runtime environments.
- If you want, I can also provide a _second_ version of the files where `uv` is fully CPU-neutral in CI and GPU-specific only in `dev`/`prod` via separate lockfile strategy.



# A:1 (Vibe)

[^](#toc) **_Refactored CI/CD Pipeline and `micromamba` Analysis_**

## 1. Root Cause Analysis

### Current Setup

- **`pyproject.toml`**:
  Uses `uv` with a custom index (`torch130`) pointing to PyTorch’s CUDA 13.0 wheels.
  `torch==2.10.*` and `torchvision==0.25.*` are installed as **CUDA-bundled wheels** (include `libtriton.so`, `libcudart.so`, etc.).
  These wheels are **~2–4 GB each** and pull in additional dependencies (e.g., `triton`), bloating `.venv` to **>20 GB** when cached.

- **`.gitlab-ci.yml`**:
  Caches `.venv`, `.cache/uv`, and `.cache/pip` between runs.
  The `uv sync --dev` command restores the full GPU-enabled environment, including CUDA-bundled wheels, in the **`int`** (CI) environment where **no GPU is available or needed**.

- **Failure**:
  The CI runner’s 20 GB disk quota is exceeded by the restored `.venv` (due to CUDA wheels) and cache.
  Error: `no space left on device` during symlink creation for `libtriton.so`.

---

## 2. Refactored Files

---

### 2.1. Refactored `pyproject.toml`

#### Key Changes

- **Environment Markers**:
  Use `sys_platform == "linux"` and a custom marker (`--global-option="--no-binary :all:"` for CI) to **exclude CUDA wheels in CI**.
  For GPU environments (`dev`, `test`, `prod`), rely on **system-provided CUDA** (via `micromamba` or host) and install PyTorch **without bundled CUDA**.

- **Custom Index for GPU**:
  For native/containerized GPU environments, use a **CUDA-aware PyTorch index** (e.g., `https://download.pytorch.org/whl/cu121` for CUDA 12.1).
  For CI, use the **CPU-only index** (default PyPI).

- **Dependency Groups**:
  Split dependencies into:
  - **`default`**: CPU-only (for CI).
  - **`gpu`**: GPU-enabled (for `dev`, `test`, `prod`), activated via `--all-extras`.

#### File

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "dve_sample_py"
version = "0.1.0"
description = "Template for GPU-enabled ML projects"
requires-python = ">=3.10,<3.15"
authors = [{ name = "Data Science Lab DEMS/datalab", email = "datalab@unimib.it" }]

# --- Core dependencies (CPU-only for CI) ---
dependencies = [
  # CPU-only PyTorch for CI
  "torch==2.10.*; sys_platform != 'linux' or platform_system != 'Linux'",
  "torch==2.10.*+cpu; sys_platform == 'linux' and platform_system == 'Linux' and 'CI' in os.environ",
  # GPU PyTorch for native/containerized
  "torch==2.10.*+cu121; sys_platform == 'linux' and platform_system == 'Linux' and 'CI' not in os.environ",

  "torchvision==0.25.*; sys_platform != 'linux' or platform_system != 'Linux'",
  "torchvision==0.25.*+cpu; sys_platform == 'linux' and platform_system == 'Linux' and 'CI' in os.environ",
  "torchvision==0.25.*+cu121; sys_platform == 'linux' and platform_system == 'Linux' and 'CI' not in os.environ",

  # Non-CUDA dependencies
  "numpy",
  "pandas",
  "scipy",
  "matplotlib",
  "pillow",
]

# --- Optional dependency groups ---
[project.optional-dependencies]
gpu = [
  # GPU-specific dependencies (e.g., NVIDIA ML)
  "nvidia-ml-py3; sys_platform == 'linux'",
]
dev = [
  "pytest",
  "ruff",
  "pyright",
  "ipykernel",
]

[tool.uv]
package = true

# --- Indexes for GPU/CPU ---
[tool.uv.sources]
torch = { index = "pytorch-cpu", extra = "cpu" }
torchvision = { index = "pytorch-cpu", extra = "cpu" }

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu121"
url = "https://download.pytorch.org/whl/cu121"
explicit = true

[tool.uv.environment]
# For CI: Force CPU-only
UV_EXTRA_INDEX_URL = { value = "https://download.pytorch.org/whl/cpu", if = "'CI' in os.environ" }
```

#### How It Works

- **CI (`int`)**:
  `uv sync --all-extras --all-groups` installs **CPU-only PyTorch** from `pytorch-cpu` index.
  No CUDA wheels → `.venv` size **<2 GB**.

- **GPU (`dev`, `test`, `prod`)**:
  `uv sync --all-extras --all-groups` installs **CUDA 12.1 PyTorch** from `pytorch-cu121` index.
  Requires **system CUDA 12.1** (provided by `micromamba` or host).

---

### 2.2. Refactored `.gitlab-ci.yml`

#### Key Changes /av

- **CPU-Only Sync in CI**:
  Use `uv sync --all-extras --all-groups --no-dev` (if `dev` group is GPU-only) or rely on **environment markers** to auto-select CPU wheels.

- **Cache Optimization**:
  - Cache **only `.cache/uv`** (not `.venv`).
  - Use `uv cache prune --ci` to **remove unused wheels** after sync.
  - Set `UV_CACHE_DIR` to a **shared cache** (e.g., `$CI_PROJECT_DIR/.cache/uv`).

- **Disk Cleanup**:
  Add a `before_script` step to **clear apt/dpkg caches** and **prune Docker images** (if applicable).

#### File `.gitlab-ci.yml` /av

```yaml
---
image: python:3.14-slim

variables:
  UV_VERSION: "latest"
  UV_CACHE_DIR: "$CI_PROJECT_DIR/.cache/uv"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  # Force CPU-only PyTorch in CI
  UV_EXTRA_INDEX_URL: "https://download.pytorch.org/whl/cpu"

cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - .cache/uv
    - .cache/pip
  policy: pull-push

stages:
  - lint
  - test

before_script:
  - apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl git
  - rm -rf /var/lib/apt/lists/*
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="$HOME/.local/bin:$PATH"
  - uv cache prune --ci
  - uv sync --all-extras --all-groups
  - uv run pip cache purge

linting:
  stage: lint
  script:
    - uv run ruff check .
    - uv run ruff format --check .
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

typing:
  stage: lint
  script:
    - uv run pyright
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'

testing:
  stage: test
  script:
    - uv run pytest -v
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
```

#### Why It Works

- **No `.venv` Cache**: Avoids restoring large CUDA wheels.
- **CPU-Only Wheels**: PyTorch installs **~200 MB** (CPU) instead of **~4 GB** (CUDA).
- **Cache Pruning**: `uv cache prune --ci` removes **unused wheels** from cache.
- **Slim Image**: `python:3.14-slim` reduces base image size.

---
---

## 3. `micromamba` Alternative Analysis

---

### 3.1. Mechanism

`micromamba` installs **system-wide CUDA toolkit** (e.g., `/opt/mamba/envs/cuda-base`) **outside** the `uv` virtual environment.

- **Decoupling**:
  - `micromamba` manages `cuda-toolkit`, `cudnn`, `libcublas`, etc.
  - `uv` installs PyTorch **without CUDA wheels** (e.g., `torch==2.10.*+cu121` from `pytorch-cu121` index).
  - PyTorch **dynamically links** to system CUDA libraries via:
  
    ```bash
    export LD_LIBRARY_PATH=/opt/mamba/envs/cuda-base/lib:$LD_LIBRARY_PATH
    export CUDA_HOME=/opt/mamba/envs/cuda-base
    ```

---

### 3.2. Pros

| **Benefit**         | **Impact**                                                           |
|---------------------|----------------------------------------------------------------------|
| **Disk Size**       | `.venv` shrinks to **~1–2 GB** (no CUDA wheels).                     |
| **Portability**     | Same `pyproject.toml` works across **native/containerized/GPU/CPU**. |
| **Reproducibility** | CUDA version pinned in `conda-env.yaml` (e.g., `cuda-toolkit=12.1`). |
| **Flexibility**     | Users can **override CUDA version** via `micromamba`.                |
| **Compatibility**   | Works with **any NVIDIA driver ≥525** (CUDA 12.x).                   |

---

### 3.3. Cons

| **Drawback**            | **Impact**                                                             |
|-------------------------|------------------------------------------------------------------------|
| **Setup Burden**        | Requires **pre-installing `micromamba`** and **sourcing environment**. |
| **CI Complexity**       | Need to **activate `micromamba` env** before `uv sync` in GPU jobs.    |
| **Solver Overhead**     | `micromamba` may take **longer to resolve** CUDA dependencies.         |
| **Shell Configuration** | Users must add `micromamba` paths to `.bashrc`/`.zshrc`.               |
| **Rootless Podman**     | Requires **`--volume` mounts** for `/opt/mamba` in containers.         |

### 3.4. Impact on Derived Projects

#### Template Consumers Must

- Install `micromamba` (or use a pre-configured container with `micromamba` + CUDA).
- Create the `cuda-base` environment:
  
  ```bash
     micromamba env create -n cuda-base -f conda-env.yaml
  ```
  
- Source the environment before running Python:
  
  ```bash
     source /opt/mamba/bin/activate cuda-base
     export LD_LIBRARY_PATH=/opt/mamba/envs/cuda-base/lib:$LD_LIBRARY_PATH
  ```
  
- Use the **same `pyproject.toml`** (no changes needed).

#### No Changes to `uv sync`

  The command remains `uv sync --all-extras --all-groups` in all environments.

### 3.5. `conda-env.yaml` for `micromamba`

```yaml
---
name: cuda-base
channels:
  - nvidia
  - conda-forge
dependencies:
  # CUDA 12.1 (compatible with NVIDIA Driver 525+)
  - cuda-toolkit=12.1
  - cudnn>=8.9
  - libcublas
  - libcublas-dev
  - libopenblas
  - nccl
  - gxx_linux-64>=12,<14  # For nvcc compatibility
  - sysroot_linux-64>=2.17
```

#### Compatibility Notes

- **PyTorch 2.10.x** requires **CUDA 12.1** and **cuDNN 8.9**.
- **NVIDIA Driver ≥525** supports CUDA 12.x.
- **AMD EPYC (Rome)**: OpenBLAS outperforms MKL (included via `libopenblas`).

## 4. NVIDIA Compatibility Matrix

| **Component**     | **`uv`-Only (GPU)**        | **`micromamba` + `uv` (GPU)**       | **CI (CPU)**           |
|-------------------|----------------------------|-------------------------------------|------------------------|
| **PyTorch**       | `2.10.*+cu121` (CUDA 12.1) | `2.10.*+cu121` (links to system)    | `2.10.*+cpu`           |
| **CUDA Toolkit**  | Bundled in wheel           | `cuda-toolkit=12.1` (system)        | N/A                    |
| **cuDNN**         | Bundled in wheel           | `cudnn>=8.9` (system)               | N/A                    |
| **Driver**        | ≥525                       | ≥525                                | N/A                    |
| **`.venv` Size**  | ~4 GB                      | ~1 GB                               | ~200 MB                |
| **Setup Command** | `uv sync --all-extras`     | `micromamba env create` + `uv sync` | `uv sync --all-extras` |

## 5. Additional Notes /av

### 5.1. Why Not CPU-Only PyTorch Everywhere?

- **Prohibited by "Simple-as-possible" Rule**:
  Derived projects must use `uv sync --all-extras --all-groups` **unchanged** for GPU support.

### 5.2. Why Not Cache `.venv` in CI?

- **`.venv` is Environment-Specific**:
  Caching a GPU `.venv` (with CUDA wheels) and restoring it in CI (CPU) **fails** due to missing CUDA libraries.
  Even if cached separately, the **size exceeds 20 GB**.

### 5.3. `uv` vs. `micromamba` for CUDA

- **`uv`**:
  - **Pros**: Faster, simpler, no shell modifications.
  - **Cons**: CUDA wheels bloat `.venv`.

- **`micromamba`**:
  - **Pros**: Smaller `.venv`, reproducible CUDA.
  - **Cons**: Additional setup, slower dependency resolution.

### 5.4. Recommended Approach

- **For CI (`int`)**:
  Use the **refactored `pyproject.toml` + `.gitlab-ci.yml`** (CPU-only wheels, no `.venv` cache).

- **For GPU (`dev`, `test`, `prod`)**:
  Use **`micromamba` + `uv`** for **minimal disk usage** and **reproducibility**.
  Example `Dockerfile` for `prod`:
  
  ```dockerfile
  FROM ubuntu:22.04
  RUN apt-get update && apt-get install -y micromamba
  COPY conda-env.yaml .
  RUN micromamba env create -n cuda-base -f conda-env.yaml
  ENV PATH="/opt/mamba/bin:$PATH"
  RUN uv sync --all-extras --all-groups
  ```

## 6. Footnotes

[^av-1]: [PyTorch CUDA Compatibility](https://pytorch.org/get-started/locally/#linux-cuda)

[^av-2]: [NVIDIA CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/)

[^av-3]: [micromamba GitHub](https://github.com/mamba-org/mamba)

[^av-4]: [Astral `uv` Documentation](https://astral.sh/uv)

[^av-5]: [GitLab CI Cache Documentation](https://docs.gitlab.com/ee/ci/caching/)

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
LocalWords:  GitLab CommonMark GFM GLFM YAML Podman SaaS CUDA NVBLAS
<!--  LocalWords:  venv prons gitlab CTK
 -->
vim: set foldmethod=marker :
}}} // %* -->
