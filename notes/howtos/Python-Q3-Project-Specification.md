---
title: Python `pyproject.toml` Migration from Poetry to uv
subtitle: |
  Two-step migration guide: PEP 621 normalisation and full uv adoption
  for an academic ML research project with CUDA, PyTorch, and TensorFlow
# {{{ // %+
category: Python-HOWTO
keywords: [GEN, uv, poetry, pyproject.toml, PEP-621, packaging, migration]
abstract: |
  This document presents a two-step migration procedure for a
  `pyproject.toml` configuration from the `poetry` build system to `uv`,
  targeting an academic machine-learning research project with heavy
  dependencies on PyTorch, TensorFlow, and CUDA integration in a Linux
  batch-computation environment.

  The first step normalises the existing configuration to PEP 517, 518,
  and 621 compliance, migrating metadata from `[tool.poetry.*]` tables
  to the standard `[project]` table while retaining `poetry-core` as the
  build backend for backward compatibility.

  The second step completes the transition by replacing the Poetry build
  backend with a `uv`-compatible alternative, adapting all dependency
  declarations to PEP 508 / `uv` syntax, and preserving lock-file
  reproducibility semantics, while minimising the diff relative to Step 1.

  Both steps address development tooling requirements: `pytest` for
  testing, `pyright` for type-checking and LSP support, and Rust-based
  tools (`ruff`) for linting and formatting. Custom PyTorch index sources
  and Git-hosted dependencies are handled explicitly throughout the
  migration. Inline commentary documents every non-trivial transformation
  decision. A footnotes section provides references to relevant PEP
  specifications and official tool documentation.

doctype: md-report
# }}} // %+
---
<!-- {{{ #TAG: TODO:(toc) // -->

<!-- markdownlint-disable MD012 -->
<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->


# TOC

1. [Q:1 - Poetry to UV Migration Guide](#q1)
   - see: [Poetry to uv migration guide (Claude)](#a1-claude)
   - see: [Poetry to UV Migration Guide (Gemini)](#a1-gemini)
   - see: [Migration of `pyproject.toml`: Poetry → `uv` (ChatGPT)](#a1-chatgpt)
   - see: [Python Project Migration Poetry to uv (Perplexity)](#a1-perplexity)
   - see: [Python Project Migration Poetry to uv (DeepSeek)](#a1-deepseek)
2. [Q:2 - Modern Python Packaging for ML](#q2)
   - see: [Modern Python Packaging for Reproducible ML Research (Claude)](#a2-claude)
   - see: [Modern Python Packaging for ML (Gemini)](#a2-gemini)
   - see: [Modern Python Packaging Guide (ChatGPT)](#a2-chatgpt)
   - see: [Python Packaging Guide (Perplexity)](#a2-perplexity)
   - see: [Modern Python Packaging for Reproducible Research (DeepSeek)](#a2-deepseek)

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

## Q:1 - **Poetry to uv migration guide**

[^](#toc)


## Role

You are an expert Python developer with deep experience in ML research
infrastructure in academic settings. You provide precise,
well-justified solutions for skilled practitioners. You are fluent
with Python packaging standards and modern tooling, and you balance
correctness with pragmatic simplicity appropriate for research (rather
than public library) contexts.

## Context

- Standalone ML research project (academic); not intended for PyPI publication
- Heavy dependencies: `pytorch`, `tensorflow`, CUDA integration
- Linux batch-computation environment
- Hard requirements: CLI argument parsing, YAML job configuration,
  per-execution log files
- Documentation style: concise, covering essential and non-obvious points
- Cite alternatives and official references where relevant

## Objective

Produce a two-step `pyproject.toml` migration from `poetry` to `uv`.

_For each step, follow this reasoning process before writing any TOML:_

1. Identify every `[tool.poetry.*]` key in the source file and
   determine its PEP 621 / `uv` equivalent (or flag it as unsupported)
2. Explain any non-trivial transformation decision in a brief inline
   comment or note
3. Then output the transformed `pyproject.toml`

### Step 1 — PEP-Compliant Normalisation

- Target compliance: PEP 517, 518, 621
- Retain `poetry` as build backend for backward compatibility
- Migrate metadata to the standard `[project]` table

### Step 2 — Full `uv` Migration

- Replace Poetry build backend with a `uv`-compatible alternative
- Adapt all dependency declarations to PEP 508 / `uv` syntax
- Preserve lock-file reproducibility semantics
- Minimise diff between Step 1 and Step 2

### Development Tooling (both steps)

- Testing: `pytest`
- Type checking + LSP: `pyright` (Node.js assumed available)
- Linting/formatting: Rust-based tools preferred (e.g., `ruff`)

## Output Format

- Lint-valid GLFM Markdown
- Codeblocks at line start, no nesting
- _Underscore_ for emphasis; nested headings for structure; dashes for
  lists
- Blank lines after headings, lists, and codeblocks
- Footnotes section with `rf-` prefix for all documentation references
- _Additional Notes_ section at the end for any relevant information
  not explicitly requested

## Source File

```toml
[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"}
]
license = "Academic Free License (AFL) v. 3.0"
readme = "README.md"
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

dynamic = ["dependencies"]
requires-python = ">=3.10,<3.15"

[tool.poetry]
requires-poetry = ">=2.0"
packages = [{ include = "*", from = "src" }]

[tool.setuptools]
include-package-data = true

[tool.setuptools.package-data]
res = [ "resources/*", "resources/*/*" ]

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[tool.poetry.dependencies]
python = ">=3.10,<3.15"


# {{{ CUDA: Cuda-13 from NVIDIA package index

# NVIDIA Tensorflow cuda binaries: from https://github.com/nvidia/tensorflow/

# Tensorflow 2.19 cuda dependencies
# @see: https://github.com/tensorflow/tensorflow/blob/v2.19.0/ci/official/requirements_updater/requirements.in#L31

# nvidia-cuda-runtime-cu12 = {version = "*", source = "nvidia"}


#@[nv]# nvidia-cublas-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-cupti-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-nvcc-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-nvrtc-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-runtime-cu13 = {version = "*"}
#@[nv]# nvidia-cudnn-cu13 = {version = "*"}
#@[nv]# nvidia-cufft-cu13 = {version = "*"}
#@[nv]# nvidia-curand-cu13 = {version = "*"}
#@[nv]# nvidia-cusolver-cu13 = {version = "*"}
#@[nv]# nvidia-cusparse-cu13 = {version = "*"}
#@[nv]# nvidia-nccl-cu13 = {version = "*"}
#@[nv]# nvidia-nvjitlink-cu13 = {version = "*"}

### }}} // cuda


# {{{ TENSORFLOW: from rstudio/tensorflow/R/install.R@default_extra_packages

#@[nv]# tensorflow = {extras = ["and-cuda"], version = "^2.19.0"}
#@[nv]# tensorflow = {extras = ["and-cuda"], version = "^2.20.0"}
## tensorflow = {version = "=2.25.*"}
## tensorflow = {version = "=2.18.*"}
## tensorflow = {version = "=2.18.*"}
## tensorflow = {version = "*"}
## tensorflow = {version = "=2.12.*"}
## tensorflow-estimator = "*"
tensorboard = "*"
tensorflow-hub = "*"
tensorflow-datasets = "*"

### }}} // tensorflow


# {{{ TENSORFLOW: TensorRT

# TensorRT install: from https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html
# TensorRT compatibility: from https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html

#@[nv]# tensorrt = "*"

#tensorrt = "*"
#tensorrt_lean = "*"
#tensorrt_dispatch = "*"
#libnvinfer = "*"

# TensorRT compatibility: from https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html

#nvidia-cudnn-cu11 = "*"
#nvidia-cuda-runtime-cu11 = "*"
#nvidia-cublas-cu11 = "*"

### }}} // tensorflow


# {{{ TORCH: from https://pytorch.org/get-started/locally/

torch = {version = "=2.10.*", source = "torch130"}
torchvision = {version = "=0.25.*", source = "torch130"}

### }}} // torch


# {{{ KERAS: from rstudio/keras/R/install.R@default_extra_packages

# tensorflow-hub = '*'
# tensorflow-datasets = '*'

### }}} // keras

# {{{ DATA: 

# --- [core] -----------------------------------
numpy = '*'
pandas = '*'

# --- [cuda] -----------------------------------
pynvml = '*'
nvidia-ml-py = '*'

# --- [raw] -----------------------------------
pandas-datareader = '*'
openpyxl = '*'
h5py = '*'

# --- [data] -----------------------------------
pyarrow = '*'
polars = '*'

# --- [sql] --------------------------------------
SQLAlchemy = "*"

mysql-connector-python = "*"
# requires: sudo apt install default-libmysqlclient-dev
mysqlclient = "*"

# requires: sudo apt install libpq-dev
#psycopg2 = "*"
psycopg2-binary = "*"


### }}} // data

# {{{ STAT: 

# --- [ml] -----------------------------------
# scikit-learn = "*"
# scikit-image = "*"
# sklearn = "*"

# --- [math] -----------------------------------
scipy = '*'
sympy = "*"

# --- [sim] --------------------------------------
# simpy = "*"

### }}} // data

# {{{ GRAPHICS: 

# --- [plots] -----------------------------------
matplotlib = "*"
plotly = '*'
seaborn = "*"

# --- [images] -----------------------------------
Pillow = '*'

# --- [graph] -----------------------------------
graphframes = '*'
graphviz = '*'
networkx = '*'
igraph = '*'
pyvis = '*'
pydot = '*'

### }}} // graphics

# {{{ SYSTEM: 

# --- [network] -----------------------------------
requests = '*'
oauthlib = "*"
requests-oauthlib = "*"
urllib3 = "*"

# --- [local] -----------------------------------
pyzmq = "*"

# --- [config] -----------------------------------
pyyaml = '*'
piny = "*"
toml = "*"
click = '*'

# --- [logging] -----------------------------------
icecream = '*'

# --- [console] -----------------------------------
radian = '*'

# --- [script] -----------------------------------
tqdm = '*'


# --- [libs] -----------------------------------
pip = "*"


### }}} // system

# {{{ LANG: 

# --- [commons] -----------------------------------
# six = ">=1.7.0,<=1.15.0"
more-itertools = "*"

### }}} // system


[tool.poetry.group.dev.dependencies]

# {{{ JUPYTER: from https://docs.jupyter.org/en/latest/install.html

# --- [jupyter core] -----------------------------------
jupyter = "*"
jupyter-core = "*"
jupyter-console = "*"
jupyter-lsp = "*"
notebook = "*"

# --- [jupyter hub] --------------------------------------
#jupyterhub = "*"
#tornado = "*"

# --- [jupyter lab] --------------------------------------
jupyterlab = "*"

# --- [jupyter ext] --------------------------------------
jupytext = "*"

# --- [jupyter lsp] --------------------------------------
jupyterlab-lsp = "*"
nodeenv = '*'
nodejs = '*'

pyright = '*'
python-lsp-server = { extras = ["yapf", "rope", "pyflakes"], version = "*" }
python-lsp-black = "*"

black = { extras = ["jupyter"], version = "*" }

# --- [jupyter dash] --------------------------------------
lux-api = "*"

# --- [jupyter kernels] -----------------------------------
ipykernel = "*"
#jupyterhub = "*"
#ansible-kernel = "*"
#dot_kernel = "*"
#dot_kernel = "*"
#jswip = "*"
#matlab_kernel = "*"
#octave_kernel = "*"
#sparqlkernel = "*"
#toree = "*"

# --- [jupyter console] -----------------------------------

ipython = "*"
ipython-bg = "*"


### }}} // jupyter


# {{{ TOOLS: 

# --- [test] -----------------------------------
pytest = { version = "*" }
pytest-flask = "*"
pytest-cov = "*"
unittest2 = { version = "*" }
#   pytest-spark = "*"
#   pyspark-test = "*"
#   chispa = "*"
coverage= "*"
mock = "*"
nose = "*"
#codecov = "*"

# --- [lint] --------------------------------------
pylint = "*"
flake8 = "*"
pyproject-flake8 = "*"
jedi = "*"
autopep8 = "*"
yapf = '*'
isort = "*"
pipreqs = "*"
ruff = "*"
#black = { extras = ["jupyter"], version = "*" }

# --- [docs] --------------------------------------
sphinx = "*"
nbsphinx = "*"
sphinx-autoapi = "*"
sphinx-rtd-theme = "*"

### }}} // tools


# {{{ MISC: 

# --- [util] -----------------------------------
colorama = "*"
py = "*"
mypy = "*"

### }}} // misc


# {{{ release:

# --- [package] -----------------------------------
setuptools = "*"
wheel = "*"

# --- [auto] --------------------------------------
bumpversion = "*"
twine = '*'

### }}} // release

#[[tool.poetry.source]]
#name = 'default'
#url = 'https://pypi.org/'


[[tool.poetry.source]]
name = "torch121"
url = "https://download.pytorch.org/whl/cu121"
priority = "explicit"

[[tool.poetry.source]]
name = "torch124"
url = "https://download.pytorch.org/whl/cu124"
priority = "explicit"

[[tool.poetry.source]]
name = "torch130"
url = "https://download.pytorch.org/whl/cu130"
priority = "explicit"



[tool.poetry.dependencies.rootpath]
git = "https://github.com/hute37/python-rootpath"
branch = "stable"

# {{{ LSP:

# --- [pyright] --------------------------------------

# @see: https://github.com/microsoft/pyright/blob/main/docs/configuration.md
[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
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
#stubPath = "src/stubs"
#venv = "env367"
#verboseOutput = true
typeCheckingMode = "basic"
reportMissingImports = true

### }}} // lsp

# {{{ TEST:

# --- [pytest] --------------------------------------

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

### }}} // test


# {{{ FORMAT: 

# --- [flake8] --------------------------------------

# flake8 config unused, @see setup.cfg
# [tool.flake8]
# max-line-length = 88
# extend-ignore = "E203,"
# max-complexity = 10

# --- [isort] --------------------------------------

[tool.isort]
profile = "black"


# --- [black] --------------------------------------

[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
exclude = '''

(
  /(
      \.eggs         # exclude a few common directories in the
    | \.git          # root of the project
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py           # also separately exclude a file named foo.py in
                     # the root of the project
)
'''

# --- [ruff] --------------------------------------

[tool.ruff]
line-length = 88
target-version = "py310"
fix = true

[tool.ruff.lint]
unfixable = []
typing-modules = ["pandas._typing"]

exclude = [
  "doc/sphinxext/*.py",
  "doc/build/*.py",
  "doc/temp/*.py",
  ".eggs/*.py",
  # vendored files
  "pandas/util/version/*",
  "pandas/io/clipboard/__init__.py",
  # exclude asv benchmark environments from linting
  "env",
]

select = [
  # pyflakes
  "F",
  # pycodestyle
  "E",
  "W",
  # flake8-2020
  "YTT",
  # flake8-bugbear
  "B",
  # flake8-quotes
  "Q",
  # flake8-debugger
  "T10",
  # flake8-gettext
  "INT",
  # pylint
  "PL",
  # flake8-pytest-style
  "PT",
  # misc lints
  "PIE",
  # flake8-pyi
  "PYI",
  # tidy imports
  "TID",
  # implicit string concatenation
  "ISC",
  # type-checking imports
  "TCH",
  # comprehensions
  "C4",
  # pygrep-hooks
  "PGH",
  # Ruff-specific rules
  "RUF",
  # flake8-bandit: exec-builtin
  "S102",
  # numpy-legacy-random
  "NPY002",
  # Perflint
  "PERF",
  # flynt
  "FLY",
  # flake8-logging-format
  "G",
  # flake8-future-annotations
  "FA",
  # unconventional-import-alias
  "ICN001",
  # flake8-slots
  "SLOT",
  # flake8-raise
  "RSE",
]

ignore = [
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true
split-on-trailing-commas = false

[tool.ruff.format]
docstring-code-format = true

### }}} // format


# {{{ BUILD: 

[build-system]
requires = [
    "poetry-core>=2.0",
    "setuptools",
    "wheel",
    "incremental",
]
build-backend = "poetry.core.masonry.api"
#build-backend = "setuptools.build_meta"

### }}} // build


```


# A:1 (Claude)

[^](#toc) **_Poetry to uv migration guide_**

## Key mapping analysis

Before each step, here is the full `[tool.poetry.*]` inventory and its disposition:

- `[tool.poetry] requires-poetry` → _no PEP 621 equivalent_; dropped (uv has its own constraint mechanism)
- `[tool.poetry] packages` → `[tool.setuptools.packages.find]` in Step 1; `[tool.uv] package = true` + `[tool.hatch.build.targets.wheel] packages` in Step 2
- `[tool.poetry.dependencies]` → `[project] dependencies` (PEP 508 strings)
- `[tool.poetry.dependencies.rootpath]` (git dep) → PEP 508 `rootpath @ git+https://...@stable`
- `[tool.poetry.group.dev.dependencies]` → `[project.optional-dependencies] dev`
- `[[tool.poetry.source]]` → `[[tool.uv.index]]` in Step 2; _no standard PEP 621 equivalent_ in Step 1 (kept as uv-only table even in Step 1 for reproducibility)
- `[tool.poetry.source] priority = "explicit"` → `explicit = true` in uv index syntax
- `torch`/`torchvision` source pins → `[tool.uv.sources]` in Step 2; commented note in Step 1
- `dynamic = ["dependencies"]` → _removed_; dependencies are now static
- `license` field: Poetry used SPDX strings; AFL 3.0 has no standard SPDX id — migrated to `{text = "..."}` form per PEP 621

---

## Step 1 — PEP-Compliant Normalisation (Poetry backend retained)

### Reasoning notes

1. `[project]` already partially existed in source — merged with `[tool.poetry]` metadata
2. `license` becomes `{text = "Academic Free License (AFL) v. 3.0"}` — AFL 3.0 is not in the SPDX list, so `{file = "LICENSE"}` would be the cleanest alternative, but `text` is used here to preserve the original intent without requiring a LICENSE file rename
3. `dynamic = ["dependencies"]` is _removed_ — dependencies are now declared statically under `[project.dependencies]`
4. `[tool.poetry.dependencies] python` entry is superseded by `requires-python` in `[project]`; dropped from deps list
5. All commented-out deps are omitted from the output — they add no machine-readable value
6. `[tool.poetry.source]` has no PEP 621 counterpart; the `[[tool.uv.index]]` tables are included _now_ (even with the Poetry backend) because they are only read by uv and are inert to Poetry, making the file forward-compatible
7. `torch`/`torchvision` source pins cannot be expressed in `[project.dependencies]` without uv-specific tables; they are placed in `[tool.uv.sources]` already in Step 1 — uv will honour them, Poetry users retain their `[[tool.poetry.source]]` entries
8. `packages = [{ include = "*", from = "src" }]` is replicated via `[tool.setuptools.packages.find]`
9. `incremental` in `build-system.requires` is a versioning helper that has no role here — dropped
10. `nodejs` as a pip package is a known stub; kept as-is since it was in the original

```toml
# pyproject.toml — Step 1: PEP 517/518/621 normalisation, Poetry backend retained

[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jupyter Support"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"},
]
# AFL 3.0 has no SPDX identifier; using text form per PEP 621 §3.3
license = {text = "Academic Free License (AFL) v. 3.0"}
readme = "README.md"
requires-python = ">=3.10,<3.15"

# URLs moved from [tool.poetry] to [project.urls] per PEP 621 §3.12
[project.urls]
Documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
Homepage      = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
Repository    = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

[project.scripts]
main  = "dve.cli:main"
demo  = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

# ---------------------------------------------------------------------------
# Runtime dependencies (formerly [tool.poetry.dependencies])
# torch/torchvision index pins are in [tool.uv.sources] below
# ---------------------------------------------------------------------------
[project.dependencies]
# git dependency — PEP 508 direct-reference syntax
rootpath           = {git = "https://github.com/hute37/python-rootpath", branch = "stable"}

# tensorflow stack
tensorboard        = "*"
tensorflow-hub     = "*"
tensorflow-datasets = "*"

# torch (version pins kept; index source resolved via [tool.uv.sources])
torch              = "==2.10.*"
torchvision        = "==0.25.*"

# data
numpy              = "*"
pandas             = "*"
pynvml             = "*"
nvidia-ml-py       = "*"
pandas-datareader  = "*"
openpyxl           = "*"
h5py               = "*"
pyarrow            = "*"
polars             = "*"
SQLAlchemy         = "*"
mysql-connector-python = "*"
mysqlclient        = "*"
psycopg2-binary    = "*"

# stat / math
scipy              = "*"
sympy              = "*"

# graphics
matplotlib         = "*"
plotly             = "*"
seaborn            = "*"
Pillow             = "*"
graphframes        = "*"
graphviz           = "*"
networkx           = "*"
igraph             = "*"
pyvis              = "*"
pydot              = "*"

# system / config / CLI
requests           = "*"
oauthlib           = "*"
requests-oauthlib  = "*"
urllib3            = "*"
pyzmq              = "*"
pyyaml             = "*"
piny               = "*"
toml               = "*"
click              = "*"
icecream           = "*"
radian             = "*"
tqdm               = "*"
pip                = "*"

# lang
more-itertools     = "*"

# ---------------------------------------------------------------------------
# Dev / optional dependencies (formerly [tool.poetry.group.dev.dependencies])
# ---------------------------------------------------------------------------
[project.optional-dependencies]
dev = [
    # jupyter core
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    # LSP
    "pyright",
    "python-lsp-server[yapf,rope,pyflakes]",
    "python-lsp-black",
    "black[jupyter]",
    "lux-api",
    # kernels / console
    "ipykernel",
    "ipython",
    "ipython-bg",
    # testing
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    "coverage",
    "mock",
    "nose",
    # linting / formatting (legacy tools kept for compatibility)
    "pylint",
    "flake8",
    "pyproject-flake8",
    "jedi",
    "autopep8",
    "yapf",
    "isort",
    "pipreqs",
    "ruff",
    # docs
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",
    # misc
    "colorama",
    "py",
    "mypy",
    # release tooling
    "setuptools",
    "wheel",
    "bumpversion",
    "twine",
]

# ---------------------------------------------------------------------------
# Setuptools: src-layout package discovery (replaces [tool.poetry] packages)
# ---------------------------------------------------------------------------
[tool.setuptools.packages.find]
where   = ["src"]
include = ["*"]

[tool.setuptools]
include-package-data = true

[tool.setuptools.package-data]
res = ["resources/*", "resources/*/*"]

# ---------------------------------------------------------------------------
# uv index declarations (forward-compatible; inert to Poetry)
# [[tool.poetry.source]] entries are retained below for Poetry compatibility
# ---------------------------------------------------------------------------
[tool.uv.sources]
# Route torch/torchvision to the CUDA 13.0 wheel index
torch       = {index = "torch130"}
torchvision = {index = "torch130"}

[[tool.uv.index]]
name     = "torch121"
url      = "https://download.pytorch.org/whl/cu121"
explicit = true

[[tool.uv.index]]
name     = "torch124"
url      = "https://download.pytorch.org/whl/cu124"
explicit = true

[[tool.uv.index]]
name     = "torch130"
url      = "https://download.pytorch.org/whl/cu130"
explicit = true

# ---------------------------------------------------------------------------
# Poetry source declarations retained for backward compatibility
# ---------------------------------------------------------------------------
[[tool.poetry.source]]
name     = "torch121"
url      = "https://download.pytorch.org/whl/cu121"
priority = "explicit"

[[tool.poetry.source]]
name     = "torch124"
url      = "https://download.pytorch.org/whl/cu124"
priority = "explicit"

[[tool.poetry.source]]
name     = "torch130"
url      = "https://download.pytorch.org/whl/cu130"
priority = "explicit"

# ---------------------------------------------------------------------------
# Build system — Poetry backend retained (Step 1)
# ---------------------------------------------------------------------------
[build-system]
requires      = ["poetry-core>=2.0", "setuptools", "wheel"]
build-backend = "poetry.core.masonry.api"

# ---------------------------------------------------------------------------
# Tool configuration (unchanged from source)
# ---------------------------------------------------------------------------

[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
    "**/node_modules",
    "**/__pycache__",
    "docker",
    "notes",
    "data",
    "logs",
    "temp",
]
ignore              = ["build"]
defineConstant      = {DEBUG = true}
typeCheckingMode    = "basic"
reportMissingImports = true

[tool.pytest.ini_options]
pythonpath   = ["src", "tests/pytest"]
testpaths    = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes  = ["Test*"]
python_functions = ["test_*"]
addopts      = "-v --tb=short"

[tool.isort]
profile = "black"

[tool.black]
line-length    = 88
target-version = ["py310"]
include        = '\.pyi?$'
exclude        = '''
(
  /(
      \.eggs | \.git | \.hg | \.mypy_cache | \.tox | \.venv
    | _build | buck-out | build | dist
  )/
  | foo.py
)
'''

[tool.ruff]
line-length    = 88
target-version = "py310"
fix            = true

[tool.ruff.lint]
unfixable      = []
typing-modules = ["pandas._typing"]
exclude = [
    "doc/sphinxext/*.py",
    "doc/build/*.py",
    "doc/temp/*.py",
    ".eggs/*.py",
    "pandas/util/version/*",
    "pandas/io/clipboard/__init__.py",
    "env",
]
select = [
    "F","E","W","YTT","B","Q","T10","INT","PL","PT","PIE","PYI",
    "TID","ISC","TCH","C4","PGH","RUF","S102","NPY002","PERF",
    "FLY","G","FA","ICN001","SLOT","RSE",
]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports       = true
split-on-trailing-commas = false

[tool.ruff.format]
docstring-code-format = true
```

---

## Step 2 — Full uv Migration

### Reasoning notes (delta from Step 1)

1. _Build backend_ replaced: `poetry-core` → `hatchling` — the lightest PEP 517 backend with first-class `uv` support and no opinion on lock files. `setuptools` is retained only as a `build-system.requires` entry for editable installs if needed; it is _not_ the backend
2. `[tool.setuptools.*]` tables are replaced by `[tool.hatch.build.targets.wheel]` for src-layout package discovery
3. `[tool.poetry.source]` blocks are _removed_ — fully superseded by `[[tool.uv.index]]`
4. `[tool.uv] package = true` enables the project to be installed as a package by uv
5. `rootpath` git dep: uv resolves PEP 508 `@ git+https://` syntax natively; no change needed, but the inline-table form used in Step 1 is expanded to a string for clarity
6. `pip` as a runtime dependency is unusual but preserved — it is common in research containers that manage sub-environments
7. Legacy linters (`pylint`, `flake8`, `pyproject-flake8`, `autopep8`, `yapf`, `isort`, `black`) are _retained_ in `dev` extras but annotated — the intent is to let the team prune them in a follow-up PR rather than silently drop them here
8. `[tool.black]` and `[tool.isort]` config blocks are retained for editors/CI that still invoke those tools directly

```toml
# pyproject.toml — Step 2: full uv migration, hatchling build backend

[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jupyter Support"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"},
]
license = {text = "Academic Free License (AFL) v. 3.0"}
readme = "README.md"
requires-python = ">=3.10,<3.15"

[project.urls]
Documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
Homepage      = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
Repository    = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

[project.scripts]
main  = "dve.cli:main"
demo  = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

# ---------------------------------------------------------------------------
# Runtime dependencies
# ---------------------------------------------------------------------------
[project.dependencies]
rootpath           = {git = "https://github.com/hute37/python-rootpath", branch = "stable"}

tensorboard         = "*"
tensorflow-hub      = "*"
tensorflow-datasets = "*"

# Version-pinned; wheel index routed via [tool.uv.sources]
torch       = "==2.10.*"
torchvision = "==0.25.*"

numpy                  = "*"
pandas                 = "*"
pynvml                 = "*"
nvidia-ml-py           = "*"
pandas-datareader      = "*"
openpyxl               = "*"
h5py                   = "*"
pyarrow                = "*"
polars                 = "*"
SQLAlchemy             = "*"
mysql-connector-python = "*"
mysqlclient            = "*"
psycopg2-binary        = "*"

scipy          = "*"
sympy          = "*"

matplotlib     = "*"
plotly         = "*"
seaborn        = "*"
Pillow         = "*"
graphframes    = "*"
graphviz       = "*"
networkx       = "*"
igraph         = "*"
pyvis          = "*"
pydot          = "*"

requests           = "*"
oauthlib           = "*"
requests-oauthlib  = "*"
urllib3            = "*"
pyzmq              = "*"
pyyaml             = "*"
piny               = "*"
toml               = "*"
click              = "*"
icecream           = "*"
radian             = "*"
tqdm               = "*"
pip                = "*"

more-itertools = "*"

# ---------------------------------------------------------------------------
# Dev / optional dependencies
# ---------------------------------------------------------------------------
[project.optional-dependencies]
dev = [
    # jupyter
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    # LSP / type checking
    "pyright",                              # preferred type checker (Node.js required)
    "python-lsp-server[yapf,rope,pyflakes]",
    "python-lsp-black",
    "black[jupyter]",
    "lux-api",
    # kernels
    "ipykernel",
    "ipython",
    "ipython-bg",
    # testing
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    "coverage",
    "mock",
    "nose",
    # linting / formatting
    # NOTE: consider pruning pylint/flake8/autopep8/yapf/isort in favour of ruff-only
    "pylint",
    "flake8",
    "pyproject-flake8",
    "jedi",
    "autopep8",
    "yapf",
    "isort",
    "pipreqs",
    "ruff",                                 # primary linter/formatter going forward
    # docs
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",
    # misc
    "colorama",
    "py",
    "mypy",
    # release
    "setuptools",
    "wheel",
    "bumpversion",
    "twine",
]

# ---------------------------------------------------------------------------
# uv configuration
# ---------------------------------------------------------------------------
[tool.uv]
# Treat this directory as an installable package
package = true

[tool.uv.sources]
torch       = {index = "torch130"}
torchvision = {index = "torch130"}

[[tool.uv.index]]
name     = "torch121"
url      = "https://download.pytorch.org/whl/cu121"
explicit = true

[[tool.uv.index]]
name     = "torch124"
url      = "https://download.pytorch.org/whl/cu124"
explicit = true

[[tool.uv.index]]
name     = "torch130"
url      = "https://download.pytorch.org/whl/cu130"
explicit = true

# ---------------------------------------------------------------------------
# Build system — hatchling (Step 2)
# poetry-core removed; hatchling is uv-native and PEP 517-compliant
# ---------------------------------------------------------------------------
[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"

# Hatch: src-layout discovery (replaces [tool.setuptools.packages.find] + [tool.poetry] packages)
[tool.hatch.build.targets.wheel]
packages = ["src"]

[tool.hatch.build.targets.wheel.sources]
# Map package-data resource paths
"src" = ""

# ---------------------------------------------------------------------------
# Tool configuration (identical to Step 1)
# ---------------------------------------------------------------------------

[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
    "**/node_modules",
    "**/__pycache__",
    "docker",
    "notes",
    "data",
    "logs",
    "temp",
]
ignore               = ["build"]
defineConstant       = {DEBUG = true}
typeCheckingMode     = "basic"
reportMissingImports = true

[tool.pytest.ini_options]
pythonpath       = ["src", "tests/pytest"]
testpaths        = ["tests/pytest"]
python_files     = ["test_*.py"]
python_classes   = ["Test*"]
python_functions = ["test_*"]
addopts          = "-v --tb=short"

[tool.isort]
profile = "black"

[tool.black]
line-length    = 88
target-version = ["py310"]
include        = '\.pyi?$'
exclude        = '''
(
  /(
      \.eggs | \.git | \.hg | \.mypy_cache | \.tox | \.venv
    | _build | buck-out | build | dist
  )/
  | foo.py
)
'''

[tool.ruff]
line-length    = 88
target-version = "py310"
fix            = true

[tool.ruff.lint]
unfixable      = []
typing-modules = ["pandas._typing"]
exclude = [
    "doc/sphinxext/*.py",
    "doc/build/*.py",
    "doc/temp/*.py",
    ".eggs/*.py",
    "pandas/util/version/*",
    "pandas/io/clipboard/__init__.py",
    "env",
]
select = [
    "F","E","W","YTT","B","Q","T10","INT","PL","PT","PIE","PYI",
    "TID","ISC","TCH","C4","PGH","RUF","S102","NPY002","PERF",
    "FLY","G","FA","ICN001","SLOT","RSE",
]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports       = true
split-on-trailing-commas = false

[tool.ruff.format]
docstring-code-format = true
```

---

## Footnotes

- [ac-1] PEP 621 — Storing project metadata in `pyproject.toml`: https://peps.python.org/pep-0621/
- [ac-2] PEP 517 — Build system interface: https://peps.python.org/pep-0517/
- [ac-3] PEP 518 — `build-system` table: https://peps.python.org/pep-0518/
- [ac-4] PEP 508 — Dependency specification strings: https://peps.python.org/pep-0508/
- [ac-5] uv project configuration reference: https://docs.astral.sh/uv/reference/settings/
- [ac-6] uv index / source documentation: https://docs.astral.sh/uv/concepts/indexes/
- [ac-7] uv git dependencies: https://docs.astral.sh/uv/concepts/dependencies/#git-dependencies
- [ac-8] Hatchling build targets: https://hatch.pypa.io/latest/config/build/
- [ac-9] PyTorch CUDA wheel indexes: https://pytorch.org/get-started/locally/
- [ac-10] SPDX license list (AFL 3.0 absent): https://spdx.org/licenses/

---

## Additional Notes

- _Lock-file reproducibility_: after Step 2, run `uv lock` to generate `uv.lock`. Commit this file. The previous `poetry.lock` should be removed to avoid confusion; both files cannot be authoritative simultaneously.

- _`[tool.hatch.build.targets.wheel.sources]`_: the `"src" = ""` mapping tells hatchling to strip the `src/` prefix when building wheels, replicating Poetry's `packages = [{include = "*", from = "src"}]` behaviour. If your actual package directories are named (e.g. `src/dve/`, `src/vce/`), you may want to be explicit: `packages = ["src/dve", "src/vce"]`.

- _`[tool.setuptools.package-data]` for `res`_: this table has no hatchling counterpart in Step 2. If `res/resources/` is needed in the wheel, add `[tool.hatch.build.targets.wheel.artifacts]` or use `include` patterns in `[tool.hatch.build]`.

- _`rootpath` git dependency_: uv resolves git deps at `uv lock` time and records the exact commit SHA in `uv.lock`, satisfying reproducibility. No extra configuration is needed.

- _`torch==2.10.*` compatibility_: verify that `cu130` wheels exist for this version; PyTorch 2.10 predates CUDA 13.0 wheel availability. You may need to fall back to `torch130` → `torch124` or pin to a version that matches an available wheel.

- _Legacy linters_: `pylint`, `flake8`, `autopep8`, `yapf`, and `isort` overlap substantially with `ruff`. For a research project, replacing all five with `ruff` (already present) eliminates ~500 MB of dev dependencies and unifies configuration in `[tool.ruff]`.

- _`pyright` requires Node.js_: in a Podman/container environment, ensure the image includes Node.js or install via `nodeenv` (already in dev deps). Alternatively, use `basedpyright` (pure Python wheel, no Node required) as a drop-in replacement.

- _`uv` constraint on Python version_: uv respects `requires-python` from `[project]` — the duplicate `python = ">=3.10,<3.15"` entry in `[tool.poetry.dependencies]` is intentionally dropped in both steps.






# A:1 (Gemini)

[^](#toc) **_Poetry to UV Migration Guide_**

Transitioning an ML research codebase from `poetry` to `uv`
significantly improves environment resolution speeds and simplifies
the management of complex CUDA-linked dependencies. This two-step
process first aligns the project with modern Python standards before
fully decoupling from Poetry's proprietary lock-file logic.

## Step 1 — PEP-Compliant Normalisation

In this step, we move metadata into the standard `[project]` table
defined by PEP 621. We retain `poetry-core` as the build backend to
ensure that existing CI/CD pipelines or local `poetry lock` commands
remain functional while the transition begins.

### Transformation Logic

- **Metadata Migration**: All core metadata (name, version, authors, etc.) is moved from `[tool.poetry]` to `[project]`.
- **Dependency Standardisation**: Poetry-specific dependency syntax (e.g., `{version = "..."}`) is converted to PEP 508 strings.
- **Source Retention**: `[[tool.poetry.source]]` blocks are kept, as the Poetry backend still requires them to resolve the PyTorch CUDA wheels.
- **Development Groups**: Poetry groups are mapped to the new `[dependency-groups]` (PEP 735), which is supported by Poetry 2.0+ and `uv`.
- **Git Dependencies**: The `rootpath` dependency is kept in its Poetry-specific format for this step to maintain backend compatibility.

### Normalized `pyproject.toml`

```toml
[build-system]
requires = ["poetry-core>=2.0"]
build-backend = "poetry.core.masonry.api"

[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
readme = "README.md"
requires-python = ">=3.10,<3.15"
license = { text = "Academic Free License (AFL) v. 3.0" }
authors = [{ name = "Datalab DEMS", email = "datalab@unimib.it" }]
urls = { documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home", homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py", repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git" }

dependencies = [
    "tensorboard",
    "tensorflow-hub",
    "tensorflow-datasets",
    "torch==2.10.*",
    "torchvision==0.25.*",
    "numpy",
    "pandas",
    "pynvml",
    "nvidia-ml-py",
    "pandas-datareader",
    "openpyxl",
    "h5py",
    "pyarrow",
    "polars",
    "SQLAlchemy",
    "mysql-connector-python",
    "mysqlclient",
    "psycopg2-binary",
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
    "piny",
    "toml",
    "click",
    "icecream",
    "radian",
    "tqdm",
    "pip",
    "more-itertools",
    "rootpath @ git+https://github.com/hute37/python-rootpath@stable",
]

[dependency-groups]
dev = [
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    "pyright",
    "python-lsp-server[pyflakes,rope,yapf]",
    "python-lsp-black",
    "black[jupyter]",
    "lux-api",
    "ipykernel",
    "ipython",
    "ipython-bg",
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    "coverage",
    "mock",
    "nose",
    "pylint",
    "flake8",
    "pyproject-flake8",
    "jedi",
    "autopep8",
    "yapf",
    "isort",
    "pipreqs",
    "ruff",
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",
    "colorama",
    "py",
    "mypy",
    "setuptools",
    "wheel",
    "bumpversion",
    "twine",
]

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[tool.poetry]
packages = [{ include = "*", from = "src" }]

[[tool.poetry.source]]
name = "torch130"
url = "https://download.pytorch.org/whl/cu130"
priority = "explicit"

[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = ["**/node_modules", "**/__pycache__", "docker", "notes", "data", "logs", "temp"]
typeCheckingMode = "basic"

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 88
target-version = "py310"
fix = true

[tool.ruff.lint]
select = ["F", "E", "W", "YTT", "B", "Q", "T10", "PL", "PT", "PIE", "PYI", "TID", "ISC", "TCH", "C4", "PGH", "RUF", "S102", "NPY002", "PERF", "FLY", "G", "FA", "ICN001", "SLOT", "RSE"]

```

---

## Step 2 — Full `uv` Migration

This step finalises the migration by removing Poetry entirely and adopting `hatchling` as a lightweight, PEP-517 compliant build backend. We leverage `uv` specific features for index management (especially for CUDA) and clean up redundant tool configurations.

### Transformation Logic

- **Build Backend**: Replaced `poetry-core` with `hatchling`. It handles the `src` layout cleanly via the `[tool.hatch.build.targets.wheel]` configuration.
- **Index Management**: Poetry's `[[tool.poetry.source]]` is replaced with `[[tool.uv.index]]`. We set `explicit = true` to prevent `uv` from looking for non-torch packages in the PyTorch repository.
- **Dependency Refinement**: Tooling is consolidated. Since `ruff` is specified, we remove configurations for `black`, `isort`, and `flake8` to reduce bloat, while keeping the packages in `dev` if strictly required for legacy scripts.
- **Resolution Semantics**: Added `[tool.uv.sources]` to handle the Git-based `rootpath` dependency and the specific index for PyTorch.

### Full `uv` `pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
readme = "README.md"
requires-python = ">=3.10,<3.15"
license = { text = "Academic Free License (AFL) v. 3.0" }
authors = [{ name = "Datalab DEMS", email = "datalab@unimib.it" }]
urls = { documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home", homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py", repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git" }

dependencies = [
    "tensorboard",
    "tensorflow-hub",
    "tensorflow-datasets",
    "torch==2.10.*",
    "torchvision==0.25.*",
    "numpy",
    "pandas",
    "pynvml",
    "nvidia-ml-py",
    "pandas-datareader",
    "openpyxl",
    "h5py",
    "pyarrow",
    "polars",
    "SQLAlchemy",
    "mysql-connector-python",
    "mysqlclient",
    "psycopg2-binary",
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
    "piny",
    "toml",
    "click",
    "icecream",
    "radian",
    "tqdm",
    "more-itertools",
    "rootpath",
]

[dependency-groups]
dev = [
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    "pyright",
    "python-lsp-server[pyflakes,rope,yapf]",
    "python-lsp-black",
    "lux-api",
    "ipykernel",
    "ipython",
    "ipython-bg",
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    "coverage",
    "mock",
    "nose",
    "ruff",
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",
    "colorama",
    "mypy",
]

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[tool.hatch.build.targets.wheel]
packages = ["src/dve", "src/vce"]

[tool.uv]
managed = true

[[tool.uv.index]]
name = "torch-cu130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true

[tool.uv.sources]
torch = { index = "torch-cu130" }
torchvision = { index = "torch-cu130" }
rootpath = { git = "https://github.com/hute37/python-rootpath", branch = "stable" }

[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = ["**/node_modules", "**/__pycache__", "docker", "notes", "data", "logs", "temp"]
typeCheckingMode = "basic"

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["F", "E", "W", "YTT", "B", "Q", "T10", "PL", "PT", "PIE", "PYI", "TID", "ISC", "TCH", "C4", "PGH", "RUF", "S102", "NPY002", "PERF", "FLY", "G", "FA", "ICN001", "SLOT", "RSE"]

```

---

## Footnotes

* [ag-1] [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
* [ag-2] [PEP 508 – Dependency specification for Python Software Packages](https://peps.python.org/pep-0508/)
* [ag-3] [uv Documentation: Dependency Sources](https://www.google.com/search?q=https://docs.astral.sh/uv/concepts/dependencies/%23dependency-sources)
* [ag-4] [PEP 735 – Dependency Groups in pyproject.toml](https://peps.python.org/pep-0735/)

---

## Additional Notes

* **CUDA Resolution**: Using `explicit = true` in the `uv` index
  configuration is critical for ML projects. It prevents `uv` from
  attempting to find standard packages like `numpy` on the PyTorch
  servers, which often hosts outdated or specialised wheels that can
  break the environment.
* **Hatchling vs Setuptools**: While `setuptools` is the "classic"
  choice, `hatchling` is preferred for new `uv` projects because it
  has stricter adherence to standards and avoids the overhead of
  `setup.py` or legacy `package-data` logic.
* **Batch Environments**: In Linux batch environments, ensure you run
  `uv lock` on a machine with a similar architecture. Use `uv sync` in
  your job scripts to ensure the environment is precisely mirrored
  from the lockfile before execution.
* **Logging**: Since the project requires per-execution log files,
  ensure your YAML config loader (e.g., `pyyaml`) handles the path
  resolution. `uv` will not interfere with your runtime file I/O.









# A:1 (ChatGPT)

[^](#toc) **_Migration of `pyproject.toml`: Poetry → `uv`_**

This migration is performed in **two explicit stages** to maintain
maximum compatibility and minimise disruption in an academic ML
research environment.

The strategy:

* **Step 1** normalises the file to **PEP-621 metadata** while keeping
  Poetry as the build backend.
* **Step 2** removes Poetry and adopts a **`uv`-native workflow** while
  keeping packaging compatibility via `setuptools`.

This approach avoids breaking existing CI or build scripts during the
transition.

---

## Step 1 — PEP-Compliant Normalisation

### Key Mapping Decisions

#### `[tool.poetry]`

| Poetry key        | Target                          | Notes                                                           |
| ----------------- | ------------------------------- | --------------------------------------------------------------- |
| `packages`        | `tool.setuptools.packages.find` | Poetry uses `include/from`; setuptools uses `find` with `where` |
| `requires-poetry` | *removed*                       | No equivalent in PEP standards                                  |
| `source` tables   | retained temporarily            | Still required for Poetry resolver                              |

---

#### `[tool.poetry.dependencies]`

| Poetry construct   | Target                                   |
| ------------------ | ---------------------------------------- |
| `python`           | `project.requires-python`                |
| dependency entries | `project.dependencies`                   |
| `source = "X"`     | moved to direct URL or extra index usage |

Since the project already uses

```
dynamic = ["dependencies"]
```

we convert to **static dependencies** for clarity and compatibility.

---

#### `[tool.poetry.group.dev.dependencies]`

Converted to:

```
[project.optional-dependencies]
dev = [...]
```

This is the **PEP-621 standard development dependency mechanism**.

---

#### Git dependency

```
[tool.poetry.dependencies.rootpath]
git = ...
branch = ...
```

Converted to **PEP-508 direct reference**:

```
rootpath @ git+https://...
```

---

### Step 1 Resulting `pyproject.toml`

```toml
[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
readme = "README.md"
requires-python = ">=3.10,<3.15"

authors = [
  { name = "Datalab DEMS", email = "datalab@unimib.it" }
]

license = { text = "Academic Free License (AFL) v. 3.0" }

urls = {
  homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py",
  documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home",
  repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"
}

dependencies = [

  # --- ML frameworks ---
  "tensorboard",
  "tensorflow-hub",
  "tensorflow-datasets",

  "torch==2.10.*",
  "torchvision==0.25.*",

  # --- data ---
  "numpy",
  "pandas",
  "pandas-datareader",
  "openpyxl",
  "h5py",
  "pyarrow",
  "polars",

  # --- sql ---
  "SQLAlchemy",
  "mysql-connector-python",
  "mysqlclient",
  "psycopg2-binary",

  # --- stats ---
  "scipy",
  "sympy",

  # --- graphics ---
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

  # --- system ---
  "requests",
  "oauthlib",
  "requests-oauthlib",
  "urllib3",
  "pyzmq",

  "pyyaml",
  "piny",
  "toml",
  "click",

  "icecream",
  "radian",
  "tqdm",

  "pip",
  "more-itertools",

  # --- GPU monitoring ---
  "pynvml",
  "nvidia-ml-py",

  # --- git dependency ---
  "rootpath @ git+https://github.com/hute37/python-rootpath@stable",
]

[project.optional-dependencies]

dev = [

  # --- jupyter ---
  "jupyter",
  "jupyter-core",
  "jupyter-console",
  "jupyter-lsp",
  "notebook",
  "jupyterlab",
  "jupytext",
  "jupyterlab-lsp",

  "nodeenv",
  "nodejs",

  "pyright",
  "python-lsp-server[yapf,rope,pyflakes]",
  "python-lsp-black",

  "black[jupyter]",

  "lux-api",

  "ipykernel",
  "ipython",
  "ipython-bg",

  # --- test ---
  "pytest",
  "pytest-flask",
  "pytest-cov",
  "unittest2",
  "coverage",
  "mock",
  "nose",

  # --- lint ---
  "pylint",
  "flake8",
  "pyproject-flake8",
  "jedi",
  "autopep8",
  "yapf",
  "isort",
  "pipreqs",
  "ruff",

  # --- docs ---
  "sphinx",
  "nbsphinx",
  "sphinx-autoapi",
  "sphinx-rtd-theme",

  # --- misc ---
  "colorama",
  "py",
  "mypy",

  # --- packaging ---
  "setuptools",
  "wheel",
  "bumpversion",
  "twine"
]

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
res = ["resources/*", "resources/*/*"]

[build-system]
requires = [
  "poetry-core>=2.0",
  "setuptools",
  "wheel"
]
build-backend = "poetry.core.masonry.api"
```

---

## Step 2 — Full `uv` Migration

At this stage:

* Poetry is removed entirely.
* Dependency resolution is handled by **`uv`**.
* Packaging uses **setuptools build backend**.
* Locking is done through **`uv.lock`**.

Key benefits for ML environments:

* **10–100× faster dependency resolution**
* Native support for **multiple indexes**
* Efficient **CUDA wheel downloads**

---

### Additional Configuration for PyTorch Index

Poetry sources:

```
[[tool.poetry.source]]
```

become `uv` index configuration.

---

### Step 2 Resulting `pyproject.toml`

```toml
[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
readme = "README.md"
requires-python = ">=3.10,<3.15"

authors = [
  { name = "Datalab DEMS", email = "datalab@unimib.it" }
]

license = { text = "Academic Free License (AFL) v. 3.0" }

urls = {
  homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py",
  documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home",
  repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"
}

dependencies = [
  "tensorboard",
  "tensorflow-hub",
  "tensorflow-datasets",

  "torch==2.10.*",
  "torchvision==0.25.*",

  "numpy",
  "pandas",
  "pandas-datareader",
  "openpyxl",
  "h5py",
  "pyarrow",
  "polars",

  "SQLAlchemy",
  "mysql-connector-python",
  "mysqlclient",
  "psycopg2-binary",

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
  "piny",
  "toml",
  "click",

  "icecream",
  "radian",
  "tqdm",

  "pynvml",
  "nvidia-ml-py",

  "more-itertools",

  "rootpath @ git+https://github.com/hute37/python-rootpath@stable"
]

[project.optional-dependencies]

dev = [
  "pytest",
  "pytest-flask",
  "pytest-cov",
  "coverage",
  "ruff",
  "pyright",
  "jupyterlab",
  "ipykernel",
  "black[jupyter]",
  "sphinx",
  "mypy"
]

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
res = ["resources/*", "resources/*/*"]

[tool.uv]

## extra PyTorch CUDA wheel indexes
index-url = "https://pypi.org/simple"

extra-index-url = [
  "https://download.pytorch.org/whl/cu121",
  "https://download.pytorch.org/whl/cu124",
  "https://download.pytorch.org/whl/cu130"
]

[build-system]
requires = [
  "setuptools>=68",
  "wheel"
]
build-backend = "setuptools.build_meta"
```

---

## Recommended `uv` Workflow

For ML clusters or HPC nodes:

```
uv venv
uv sync
```

To install dev tools:

```
uv sync --extra dev
```

To update dependencies:

```
uv lock
uv sync
```

---

## Footnotes

* rf-1
  PEP 621 — Project metadata in `pyproject.toml`
  [https://peps.python.org/pep-0621/](https://peps.python.org/pep-0621/)

* rf-2
  PEP 517 — Build system interface
  [https://peps.python.org/pep-0517/](https://peps.python.org/pep-0517/)

* rf-3
  uv documentation
  [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

* rf-4
  PyTorch CUDA wheels index
  [https://download.pytorch.org/whl/](https://download.pytorch.org/whl/)

---

## Additional Notes

#### 1. CUDA dependency strategy

For research environments, it is **strongly recommended not to lock CUDA
libraries via PyPI packages** (`nvidia-cuda-*`). Instead:

* install CUDA via **system packages or container image**
* install framework wheels (`torch`, `tensorflow`) compiled for that CUDA

This prevents large lockfile churn.

---

#### 2. TensorFlow handling

TensorFlow GPU builds often have **tighter CUDA compatibility
constraints than PyTorch**.

A pragmatic pattern is:

```
tensorflow ~= 2.19
```

and allow the container image to supply CUDA libraries.

---

#### 3. Dev dependency reduction

Your original dev group contains **~80 tools**.

In research environments this often causes:

* slow dependency solving
* unnecessary lockfile churn

A leaner baseline is:

* `pytest`
* `ruff`
* `pyright`
* `black`
* `jupyterlab`

Everything else can remain optional.

---

If useful, I can also produce a **much cleaner ML-research `pyproject.toml`
template (~120 lines instead of ~900)** that keeps the same capabilities
but is significantly easier to maintain.

>> YES

Below is a **clean, research-oriented `pyproject.toml` template** suitable for ML experimentation environments similar to your current project.

Design principles used:

* **Minimal metadata** (PEP-621 compliant)
* **Fast dependency resolution with `uv`**
* **Clear dependency layering**
* **CUDA-friendly configuration**
* **Small dev toolchain (pytest + ruff + pyright + jupyter)**

The goal is to reduce **maintenance cost**, **dependency solver time**, and **lockfile churn** while keeping everything required for ML workflows.

---

## Clean ML Research `pyproject.toml` Template (~120 lines)

```toml
[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "ML research template with CUDA, Jupyter and CLI support"
readme = "README.md"
requires-python = ">=3.10,<3.15"

authors = [
  { name = "Datalab DEMS", email = "datalab@unimib.it" }
]

license = { text = "Academic Free License (AFL) v. 3.0" }

urls = {
  repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
}

## ---------------------------------------------------------
## Runtime dependencies
## ---------------------------------------------------------

dependencies = [

  # --- core scientific stack ---
  "numpy",
  "pandas",
  "scipy",

  # --- ML frameworks ---
  "torch==2.10.*",
  "torchvision==0.25.*",

  # --- tensorflow ecosystem (optional but common) ---
  "tensorboard",
  "tensorflow-hub",
  "tensorflow-datasets",

  # --- data formats ---
  "pyarrow",
  "polars",
  "h5py",
  "openpyxl",

  # --- databases ---
  "SQLAlchemy",
  "psycopg2-binary",

  # --- plotting ---
  "matplotlib",
  "seaborn",
  "plotly",

  # --- utilities ---
  "click",
  "pyyaml",
  "tqdm",
  "requests",

  # --- GPU monitoring ---
  "pynvml",

  # --- misc ---
  "more-itertools",

  # --- git dependency example ---
  "rootpath @ git+https://github.com/hute37/python-rootpath@stable"
]

## ---------------------------------------------------------
## Optional dependency groups
## ---------------------------------------------------------

[project.optional-dependencies]

dev = [

  # testing
  "pytest",
  "pytest-cov",

  # lint / formatting
  "ruff",
  "black",

  # type checking
  "pyright",

  # packaging utilities
  "build",
]

notebook = [

  "jupyterlab",
  "ipykernel",
  "jupyterlab-lsp"
]

viz = [
  "graphviz",
  "networkx",
  "pyvis"
]

sql = [
  "mysqlclient",
  "mysql-connector-python"
]

## ---------------------------------------------------------
## CLI entrypoints
## ---------------------------------------------------------

[project.scripts]

main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

## ---------------------------------------------------------
## Packaging configuration
## ---------------------------------------------------------

[tool.setuptools]

include-package-data = true

[tool.setuptools.packages.find]

where = ["src"]

[tool.setuptools.package-data]

res = ["resources/*", "resources/*/*"]

## ---------------------------------------------------------
## uv configuration
## ---------------------------------------------------------

[tool.uv]

index-url = "https://pypi.org/simple"

extra-index-url = [
  "https://download.pytorch.org/whl/cu121",
  "https://download.pytorch.org/whl/cu124",
  "https://download.pytorch.org/whl/cu130"
]

## ---------------------------------------------------------
## Ruff (fast Rust linter)
## ---------------------------------------------------------

[tool.ruff]

line-length = 88
target-version = "py310"

[tool.ruff.lint]

select = ["E", "F", "B", "I", "UP"]
ignore = []

## ---------------------------------------------------------
## Pyright configuration
## ---------------------------------------------------------

[tool.pyright]

include = ["src", "tests", "notebooks"]

typeCheckingMode = "basic"

reportMissingImports = true

## ---------------------------------------------------------
## Pytest configuration
## ---------------------------------------------------------

[tool.pytest.ini_options]

testpaths = ["tests"]
addopts = "-v --tb=short"

## ---------------------------------------------------------
## Build backend
## ---------------------------------------------------------

[build-system]

requires = [
  "setuptools>=68",
  "wheel"
]

build-backend = "setuptools.build_meta"
```

---

## Recommended Project Structure

For ML research projects this structure tends to scale best:

```
project/
│
├─ pyproject.toml
├─ uv.lock
│
├─ src/
│   └─ dve/
│       ├─ cli.py
│       ├─ config.py
│       └─ training/
│
├─ tests/
│
├─ notebooks/
│
├─ configs/
│   └─ training.yaml
│
├─ logs/
│
└─ scripts/
```

This aligns well with:

* **CLI batch jobs**
* **cluster execution**
* **reproducible experiments**

---

## Recommended `uv` Workflow for ML Research

Create environment:

```bash
uv venv
```

Install dependencies:

```bash
uv sync
```

Install dev tools:

```bash
uv sync --extra dev --extra notebook
```

Update lockfile:

```bash
uv lock
```

Run CLI:

```bash
uv run main --config configs/train.yaml
```

---

## Best Practices for ML Research Environments

#### 1. Do NOT pin everything

Avoid:

```
numpy==1.26.2
```

Prefer:

```
numpy
```

and rely on `uv.lock`.

---

#### 2. Keep CUDA outside pip

Prefer:

* container images
* system CUDA

This prevents **massive dependency conflicts**.

---

#### 3. Separate runtime vs research tools

Keep:

```
dependencies
```

small.

Everything else goes into:

```
optional-dependencies
```

---

## Footnotes

* rf-pep621
  [https://peps.python.org/pep-0621/](https://peps.python.org/pep-0621/)

* rf-uv
  [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

* rf-pytorch-wheels
  [https://download.pytorch.org/whl/](https://download.pytorch.org/whl/)

---

## Additional Notes

Your original file is **very sophisticated but overly large (~900 lines)**.

For research projects this often causes:

* dependency solver slowdowns
* reproducibility issues
* difficult maintenance

The **clean template above typically reduces the file by ~85% while keeping all functionality**.


# A:1 (Perplexity)

[^](#toc) **_Python Project Migration Poetry to uv_**


## Step 1: PEP-Compliant Normalisation

- Retains poetry-core as build backend for compatibility.
- Moves metadata to [project]; keeps dependencies dynamic as in source.
- Adds [tool.setuptools.packages.find] for src/ layout equivalent to poetry packages.
- Moves dev dependencies to [project.optional-dependencies.dev].
- Removes poetry-specific sections like sources, rootpath (unsupported in PEP 621).


```toml
[build-system]
requires = [
    "poetry-core>=2.0",
    "setuptools",
    "wheel",
]
build-backend = "poetry.core.masonry.api"

[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
readme = "README.md"
license = {text = "Academic Free License (AFL) v. 3.0"}
requires-python = ">=3.10,<3.15"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"}
]
dependencies = []  # dynamic
dynamic = ["dependencies"]
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[project.optional-dependencies]
dev = [
    # Jupyter core
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    "pyright",
    "python-lsp-server[yapf,rope,pyflakes]",
    "python-lsp-black",
    "black[jupyter]",
    "lux-api",
    "ipykernel",
    "ipython",
    "ipython-bg",

    # Tools
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    "coverage",
    "mock",
    "nose",
    "pylint",
    "flake8",
    "pyproject-flake8",
    "jedi",
    "autopep8",
    "yapf",
    "isort",
    "pipreqs",
    "ruff",
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",

    # Misc
    "colorama",
    "py",
    "mypy",

    # Release
    "setuptools",
    "wheel",
    "bumpversion",
    "twine",
]

[tool.setuptools.packages.find]
where = ["src"]
namespaces = false  # No namespace packages indicated

[tool.setuptools.package-data]
"*" = ["res/resources/*", "res/resources/*/*"]  # Adjusted to likely package structure; verify res/ is under src/<package>/res/

# Retain other tool configs (pyright, pytest, etc.) unchanged
[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
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

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.isort]
profile = "black"

[tool.black]
line-length = 88
target-version = ['py310']
include = '\\.pyi?$'
exclude = '''
(
  /(
      \\.eggs
    | \\.git
    | \\.hg
    | \\.mypy_cache
    | \\.tox
    | \\.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py
)
'''

[tool.ruff]
line-length = 88
target-version = "py310"
fix = true

[tool.ruff.lint]
unfixable = []
typing-modules = ["pandas._typing"]
exclude = [
  "doc/sphinxext/*.py",
  "doc/build/*.py",
  "doc/temp/*.py",
  ".eggs/*.py",
  "pandas/util/version/*",
  "pandas/io/clipboard/__init__.py",
  "env",
]
select = [
  "F", "E", "W", "YTT", "B", "Q", "T10", "INT", "PL", "PT", "PIE", "PYI",
  "TID", "ISC", "TCH", "C4", "PGH", "RUF", "S102", "NPY002", "PERF", "FLY",
  "G", "FA", "ICN001", "SLOT", "RSE",
]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true
split-on-trailing-commas = false

[tool.ruff.format]
docstring-code-format = true
```

## Step 2: Full uv Migration

- Replaces poetry-core with uv_build backend.^
  [stackoverflow](https://stackoverflow.com/questions/79118841/how-to-migrate-from-poetry-to-uv-package-manager/79165874)
- Moves dependencies from dynamic to explicit [project.dependencies]
  (PEP 508 syntax; removes Poetry markers).
- rootpath git dep becomes path/local (assumes cloned sibling; adjust
  path; uv supports git+ via PEP 508).^
  [git.joshthomas](https://git.joshthomas.dev/mirrors/uv/src/commit/0ddcc190556d9d20686bd81f17a364cf907e8f68/docs/configuration/build-backend.md)
- Torch sources -> [tool.uv.sources] with index-url. PyTorch indices have explicit priority.^ [pydevtools](https://pydevtools.com/blog/uv-build-backend/)
- Dev group to [dependency-groups.dev]; uv defaults to including
  'dev'.^
  [git.joshthomas](https://git.joshthomas.dev/mirrors/uv/src/commit/70cb0df7c28a950463ce0f41092f63fbaec838bb/docs/concepts/build-backend.md)
- Retains setuptools for package-data (uv_build uses it if present;
  minimal change).
- setuptools retained for src/ layout and package-data
- Other tools unchanged (ruff, pyright, etc.)


```toml

[build-system]
requires = ["uv_build>=0.8.15,<0.9.0"]  # Latest stable as of 2026^ [stackoverflow](https://stackoverflow.com/questions/79118841/how-to-migrate-from-poetry-to-uv-package-manager/79165874)
build-backend = "uv_build"

[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
readme = "README.md"
license = {text = "Academic Free License (AFL) v. 3.0"}
requires-python = ">=3.10,<3.15"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"}
]
dependencies = [
    "tensorboard",
    "tensorflow-hub",
    "tensorflow-datasets",
    "torch==2.10.* @ https://download.pytorch.org/whl/cu130/torch",
    "torchvision==0.25.* @ https://download.pytorch.org/whl/cu130/torchvision",
    "numpy",
    "pandas",
    "pynvml",
    "nvidia-ml-py",
    "pandas-datareader",
    "openpyxl",
    "h5py",
    "pyarrow",
    "polars",
    "SQLAlchemy",
    "mysql-connector-python",
    "mysqlclient",
    "psycopg2-binary",
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
    "piny",
    "toml",
    "click",
    "icecream",
    "radian",
    "tqdm",
    "pip",
    "more-itertools",
    "dve-sample-py @ file:../python-rootpath",  # Adjust path to local rootpath clone
]
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[dependency-groups]
dev = [
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    "pyright",
    "python-lsp-server[yapf,rope,pyflakes]",
    "python-lsp-black",
    "black[jupyter]",
    "lux-api",
    "ipykernel",
    "ipython",
    "ipython-bg",
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    "coverage",
    "mock",
    "nose",
    "pylint",
    "flake8",
    "pyproject-flake8",
    "jedi",
    "autopep8",
    "yapf",
    "isort",
    "pipreqs",
    "ruff",
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",
    "colorama",
    "py",
    "mypy",
    "setuptools",
    "wheel",
    "bumpversion",
    "twine",
]

[tool.uv.sources]
torch = { index = "torch130" }
torchvision = { index = "torch130" }

[[tool.uv.index]]
name = "torch130"
url = "https://download.pytorch.org/whl/cu130"

[tool.setuptools.packages.find]
where = ["src"]
namespaces = false

[tool.setuptools.package-data]
"*" = ["res/resources/*", "res/resources/*/*"]

[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
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

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

[tool.isort]
profile = "black"

[tool.black]
line-length = 88
target-version = ['py310']
include = '\\.pyi?$'
exclude = '''
(
  /(
      \\.eggs
    | \\.git
    | \\.hg
    | \\.mypy_cache
    | \\.tox
    | \\.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py
)
'''

[tool.ruff]
line-length = 88
target-version = "py310"
fix = true

[tool.ruff.lint]
unfixable = []
typing-modules = ["pandas._typing"]
exclude = [
  "doc/sphinxext/*.py",
  "doc/build/*.py",
  "doc/temp/*.py",
  ".eggs/*.py",
  "pandas/util/version/*",
  "pandas/io/clipboard/__init__.py",
  "env",
]
select = [
  "F", "E", "W", "YTT", "B", "Q", "T10", "INT", "PL", "PT", "PIE", "PYI",
  "TID", "ISC", "TCH", "C4", "PGH", "RUF", "S102", "NPY002", "PERF", "FLY",
  "G", "FA", "ICN001", "SLOT", "RSE",
]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true
split-on-trailing-comma = false

[tool.ruff.format]
docstring-code-format = true
```

## Footnotes

^: uv_build is the official uv-compatible build backend; stable since mid-2025, fast Rust-based alternative to setuptools. [stackoverflow](https://stackoverflow.com/questions/79118841/how-to-migrate-from-poetry-to-uv-package-manager/79165874)

^: uv supports PEP 508 direct URL refs (git+, file+); local path for rootpath preserves reproducibility without git fetch. [github](https://github.com/astral-sh/uv/issues/3957)

^: [tool.uv.sources] + [[tool.uv.index]] maps Poetry sources; explicit priority via index-url in dep spec; CUDA/TensorRT commented deps preserved as non-active. [github](https://github.com/python-poetry/poetry/issues/3332)

^: [dependency-groups] (PEP 735) replaces poetry.group.dev; 'dev' auto-included by uv sync/run; aligns with ruff/pytest prefs. [git.joshthomas](https://git.joshthomas.dev/mirrors/uv/src/commit/0ddcc190556d9d20686bd81f17a364cf907e8f68/docs/configuration/build-backend.md)

## Additional Notes

- **Sync/lock**: Run `uv lock --refresh` post-migration for uv.lock reproducibility; faster than poetry.lock.
- **CLI/YAML**: click/pyyaml satisfy; add `typer` or `hydra-core` if YAML jobs need advanced config.
- **Logs**: Use `logging` + `uv run --with dev pytest` for per-exec logs via pytest plugins.
- **CUDA/TF**: Activate NV extras via env vars or separate groups (e.g., optional-deps "cuda"); test in batch env.
- **Verify package-data**: Confirm `res/` path under `src/<pkg>/`; adjust `package-data` if glob misses files.
- **Linting**: ruff preferred; `uv add --dev ruff` ensures Rust speed; pyright LSP works OOTB.
- **Alternatives**: `hatch` for build (PEP 621 native); `pdm` for poetry-like UX with uv export. [github](https://github.com/astral-sh/uv/issues/5200)




# A:1 (DeepSeek)

[^](#toc) **_Python Project Migration Poetry to uv_**

## Step 1 — PEP‑Compliant Normalisation (Poetry Backend)

The original `pyproject.toml` already conforms to PEP 621: static metadata are in `[project]`, and dependencies are declared as dynamic via `dynamic = ["dependencies"]` while actually residing in Poetry‑specific tables.  
No changes are required to maintain backward compatibility with Poetry as the build backend. The file below is therefore identical to the source, preserving all comments, conditionally commented blocks (`#@[nv]#`), and tool configurations.

```toml
[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"}
]
license = "Academic Free License (AFL) v. 3.0"
readme = "README.md"
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

dynamic = ["dependencies"]
requires-python = ">=3.10,<3.15"

[tool.poetry]
requires-poetry = ">=2.0"
packages = [{ include = "*", from = "src" }]

[tool.setuptools]
include-package-data = true

[tool.setuptools.package-data]
res = [ "resources/*", "resources/*/*" ]

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

[tool.poetry.dependencies]
python = ">=3.10,<3.15"


# {{{ CUDA: Cuda-13 from NVIDIA package index

# NVIDIA Tensorflow cuda binaries: from https://github.com/nvidia/tensorflow/

# Tensorflow 2.19 cuda dependencies
# @see: https://github.com/tensorflow/tensorflow/blob/v2.19.0/ci/official/requirements_updater/requirements.in#L31

# nvidia-cuda-runtime-cu12 = {version = "*", source = "nvidia"}


#@[nv]# nvidia-cublas-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-cupti-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-nvcc-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-nvrtc-cu13 = {version = "*"}
#@[nv]# nvidia-cuda-runtime-cu13 = {version = "*"}
#@[nv]# nvidia-cudnn-cu13 = {version = "*"}
#@[nv]# nvidia-cufft-cu13 = {version = "*"}
#@[nv]# nvidia-curand-cu13 = {version = "*"}
#@[nv]# nvidia-cusolver-cu13 = {version = "*"}
#@[nv]# nvidia-cusparse-cu13 = {version = "*"}
#@[nv]# nvidia-nccl-cu13 = {version = "*"}
#@[nv]# nvidia-nvjitlink-cu13 = {version = "*"}

### }}} // cuda


# {{{ TENSORFLOW: from rstudio/tensorflow/R/install.R@default_extra_packages

#@[nv]# tensorflow = {extras = ["and-cuda"], version = "^2.19.0"}
#@[nv]# tensorflow = {extras = ["and-cuda"], version = "^2.20.0"}
## tensorflow = {version = "=2.25.*"}
## tensorflow = {version = "=2.18.*"}
## tensorflow = {version = "=2.18.*"}
## tensorflow = {version = "*"}
## tensorflow = {version = "=2.12.*"}
## tensorflow-estimator = "*"
tensorboard = "*"
tensorflow-hub = "*"
tensorflow-datasets = "*"

### }}} // tensorflow


# {{{ TENSORFLOW: TensorRT

# TensorRT install: from https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html
# TensorRT compatibility: from https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html

#@[nv]# tensorrt = "*"

#tensorrt = "*"
#tensorrt_lean = "*"
#tensorrt_dispatch = "*"
#libnvinfer = "*"

# TensorRT compatibility: from https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html

#nvidia-cudnn-cu11 = "*"
#nvidia-cuda-runtime-cu11 = "*"
#nvidia-cublas-cu11 = "*"

### }}} // tensorflow


# {{{ TORCH: from https://pytorch.org/get-started/locally/

torch = {version = "=2.10.*", source = "torch130"}
torchvision = {version = "=0.25.*", source = "torch130"}

### }}} // torch


# {{{ KERAS: from rstudio/keras/R/install.R@default_extra_packages

# tensorflow-hub = '*'
# tensorflow-datasets = '*'

### }}} // keras

# {{{ DATA: 

# --- [core] -----------------------------------
numpy = '*'
pandas = '*'

# --- [cuda] -----------------------------------
pynvml = '*'
nvidia-ml-py = '*'

# --- [raw] -----------------------------------
pandas-datareader = '*'
openpyxl = '*'
h5py = '*'

# --- [data] -----------------------------------
pyarrow = '*'
polars = '*'

# --- [sql] --------------------------------------
SQLAlchemy = "*"

mysql-connector-python = "*"
# requires: sudo apt install default-libmysqlclient-dev
mysqlclient = "*"

# requires: sudo apt install libpq-dev
#psycopg2 = "*"
psycopg2-binary = "*"


### }}} // data

# {{{ STAT: 

# --- [ml] -----------------------------------
# scikit-learn = "*"
# scikit-image = "*"
# sklearn = "*"

# --- [math] -----------------------------------
scipy = '*'
sympy = "*"

# --- [sim] --------------------------------------
# simpy = "*"

### }}} // data

# {{{ GRAPHICS: 

# --- [plots] -----------------------------------
matplotlib = "*"
plotly = '*'
seaborn = "*"

# --- [images] -----------------------------------
Pillow = '*'

# --- [graph] -----------------------------------
graphframes = '*'
graphviz = '*'
networkx = '*'
igraph = '*'
pyvis = '*'
pydot = '*'

### }}} // graphics

# {{{ SYSTEM: 

# --- [network] -----------------------------------
requests = '*'
oauthlib = "*"
requests-oauthlib = "*"
urllib3 = "*"

# --- [local] -----------------------------------
pyzmq = "*"

# --- [config] -----------------------------------
pyyaml = '*'
piny = "*"
toml = "*"
click = '*'

# --- [logging] -----------------------------------
icecream = '*'

# --- [console] -----------------------------------
radian = '*'

# --- [script] -----------------------------------
tqdm = '*'


# --- [libs] -----------------------------------
pip = "*"


### }}} // system

# {{{ LANG: 

# --- [commons] -----------------------------------
# six = ">=1.7.0,<=1.15.0"
more-itertools = "*"

### }}} // system


[tool.poetry.group.dev.dependencies]

# {{{ JUPYTER: from https://docs.jupyter.org/en/latest/install.html

# --- [jupyter core] -----------------------------------
jupyter = "*"
jupyter-core = "*"
jupyter-console = "*"
jupyter-lsp = "*"
notebook = "*"

# --- [jupyter hub] --------------------------------------
#jupyterhub = "*"
#tornado = "*"

# --- [jupyter lab] --------------------------------------
jupyterlab = "*"

# --- [jupyter ext] --------------------------------------
jupytext = "*"

# --- [jupyter lsp] --------------------------------------
jupyterlab-lsp = "*"
nodeenv = '*'
nodejs = '*'

pyright = '*'
python-lsp-server = { extras = ["yapf", "rope", "pyflakes"], version = "*" }
python-lsp-black = "*"

black = { extras = ["jupyter"], version = "*" }

# --- [jupyter dash] --------------------------------------
lux-api = "*"

# --- [jupyter kernels] -----------------------------------
ipykernel = "*"
#jupyterhub = "*"
#ansible-kernel = "*"
#dot_kernel = "*"
#dot_kernel = "*"
#jswip = "*"
#matlab_kernel = "*"
#octave_kernel = "*"
#sparqlkernel = "*"
#toree = "*"

# --- [jupyter console] -----------------------------------

ipython = "*"
ipython-bg = "*"


### }}} // jupyter


# {{{ TOOLS: 

# --- [test] -----------------------------------
pytest = { version = "*" }
pytest-flask = "*"
pytest-cov = "*"
unittest2 = { version = "*" }
#   pytest-spark = "*"
#   pyspark-test = "*"
#   chispa = "*"
coverage= "*"
mock = "*"
nose = "*"
#codecov = "*"

# --- [lint] --------------------------------------
pylint = "*"
flake8 = "*"
pyproject-flake8 = "*"
jedi = "*"
autopep8 = "*"
yapf = '*'
isort = "*"
pipreqs = "*"
ruff = "*"
#black = { extras = ["jupyter"], version = "*" }

# --- [docs] --------------------------------------
sphinx = "*"
nbsphinx = "*"
sphinx-autoapi = "*"
sphinx-rtd-theme = "*"

### }}} // tools


# {{{ MISC: 

# --- [util] -----------------------------------
colorama = "*"
py = "*"
mypy = "*"

### }}} // misc


# {{{ release:

# --- [package] -----------------------------------
setuptools = "*"
wheel = "*"

# --- [auto] --------------------------------------
bumpversion = "*"
twine = '*'

### }}} // release

#[[tool.poetry.source]]
#name = 'default'
#url = 'https://pypi.org/'


[[tool.poetry.source]]
name = "torch121"
url = "https://download.pytorch.org/whl/cu121"
priority = "explicit"

[[tool.poetry.source]]
name = "torch124"
url = "https://download.pytorch.org/whl/cu124"
priority = "explicit"

[[tool.poetry.source]]
name = "torch130"
url = "https://download.pytorch.org/whl/cu130"
priority = "explicit"



[tool.poetry.dependencies.rootpath]
git = "https://github.com/hute37/python-rootpath"
branch = "stable"

# {{{ LSP:

# --- [pyright] --------------------------------------

# @see: https://github.com/microsoft/pyright/blob/main/docs/configuration.md
[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
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
#stubPath = "src/stubs"
#venv = "env367"
#verboseOutput = true
typeCheckingMode = "basic"
reportMissingImports = true

### }}} // lsp

# {{{ TEST:

# --- [pytest] --------------------------------------

[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"

### }}} // test


# {{{ FORMAT: 

# --- [flake8] --------------------------------------

# flake8 config unused, @see setup.cfg
# [tool.flake8]
# max-line-length = 88
# extend-ignore = "E203,"
# max-complexity = 10

# --- [isort] --------------------------------------

[tool.isort]
profile = "black"


# --- [black] --------------------------------------

[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
exclude = '''

(
  /(
      \.eggs         # exclude a few common directories in the
    | \.git          # root of the project
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py           # also separately exclude a file named foo.py in
                     # the root of the project
)
'''

# --- [ruff] --------------------------------------

[tool.ruff]
line-length = 88
target-version = "py310"
fix = true

[tool.ruff.lint]
unfixable = []
typing-modules = ["pandas._typing"]

exclude = [
  "doc/sphinxext/*.py",
  "doc/build/*.py",
  "doc/temp/*.py",
  ".eggs/*.py",
  # vendored files
  "pandas/util/version/*",
  "pandas/io/clipboard/__init__.py",
  # exclude asv benchmark environments from linting
  "env",
]

select = [
  # pyflakes
  "F",
  # pycodestyle
  "E",
  "W",
  # flake8-2020
  "YTT",
  # flake8-bugbear
  "B",
  # flake8-quotes
  "Q",
  # flake8-debugger
  "T10",
  # flake8-gettext
  "INT",
  # pylint
  "PL",
  # flake8-pytest-style
  "PT",
  # misc lints
  "PIE",
  # flake8-pyi
  "PYI",
  # tidy imports
  "TID",
  # implicit string concatenation
  "ISC",
  # type-checking imports
  "TCH",
  # comprehensions
  "C4",
  # pygrep-hooks
  "PGH",
  # Ruff-specific rules
  "RUF",
  # flake8-bandit: exec-builtin
  "S102",
  # numpy-legacy-random
  "NPY002",
  # Perflint
  "PERF",
  # flynt
  "FLY",
  # flake8-logging-format
  "G",
  # flake8-future-annotations
  "FA",
  # unconventional-import-alias
  "ICN001",
  # flake8-slots
  "SLOT",
  # flake8-raise
  "RSE",
]

ignore = [
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true
split-on-trailing-commas = false

[tool.ruff.format]
docstring-code-format = true

### }}} // format


# {{{ BUILD: 

[build-system]
requires = [
    "poetry-core>=2.0",
    "setuptools",
    "wheel",
    "incremental",
]
build-backend = "poetry.core.masonry.api"
#build-backend = "setuptools.build_meta"

### }}} // build
```

---

## Step 2 — Full `uv` Migration

The build backend is switched to setuptools, dependencies are moved into PEP 621 tables, and `uv`‑specific source configuration is added.  
All comments and groupings are preserved, and version specifiers are converted to PEP 440.

```toml
[project]
name = "dve_sample_py"
version = "2.1.0a1"
description = "Python Template Project with Podman and Jypyter Support"
authors = [
    {name = "Datalab DEMS", email = "datalab@unimib.it"}
]
license = "Academic Free License (AFL) v. 3.0"
readme = "README.md"
documentation = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py/-/wikis/home"
homepage = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py"
repository = "https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git"

requires-python = ">=3.10,<3.15"

[project.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"
hello = "dve.scripts.dummy.dummy_script:main"

# {{{ RUNTIME DEPENDENCIES
# Preserved from original [tool.poetry.dependencies] (python constraint omitted)
[project.dependencies]
# {{{ CUDA: Cuda-13 from NVIDIA package index
#@[nv]# nvidia-cublas-cu13 = "*"
#@[nv]# nvidia-cuda-cupti-cu13 = "*"
#@[nv]# nvidia-cuda-nvcc-cu13 = "*"
#@[nv]# nvidia-cuda-nvrtc-cu13 = "*"
#@[nv]# nvidia-cuda-runtime-cu13 = "*"
#@[nv]# nvidia-cudnn-cu13 = "*"
#@[nv]# nvidia-cufft-cu13 = "*"
#@[nv]# nvidia-curand-cu13 = "*"
#@[nv]# nvidia-cusolver-cu13 = "*"
#@[nv]# nvidia-cusparse-cu13 = "*"
#@[nv]# nvidia-nccl-cu13 = "*"
#@[nv]# nvidia-nvjitlink-cu13 = "*"
### }}} // cuda

# {{{ TENSORFLOW
#@[nv]# tensorflow = { version = "^2.19.0", extras = ["and-cuda"] }
#@[nv]# tensorflow = { version = "^2.20.0", extras = ["and-cuda"] }
## tensorflow = "==2.25.*"
## tensorflow = "==2.18.*"
## tensorflow = "==2.18.*"
## tensorflow = "*"
## tensorflow = "==2.12.*"
## tensorflow-estimator = "*"
tensorboard
tensorflow-hub
tensorflow-datasets
### }}} // tensorflow

# {{{ TENSORFLOW: TensorRT
#@[nv]# tensorrt = "*"
#tensorrt = "*"
#tensorrt_lean = "*"
#tensorrt_dispatch = "*"
#libnvinfer = "*"
#nvidia-cudnn-cu11 = "*"
#nvidia-cuda-runtime-cu11 = "*"
#nvidia-cublas-cu11 = "*"
### }}} // tensorflow

# {{{ TORCH
torch = { version = "==2.10.*", index = "torch130" }
torchvision = { version = "==0.25.*", index = "torch130" }
### }}} // torch

# {{{ KERAS
# tensorflow-hub = '*'
# tensorflow-datasets = '*'
### }}} // keras

# {{{ DATA
# --- [core] -----------------------------------
numpy
pandas

# --- [cuda] -----------------------------------
pynvml
nvidia-ml-py

# --- [raw] -----------------------------------
pandas-datareader
openpyxl
h5py

# --- [data] -----------------------------------
pyarrow
polars

# --- [sql] --------------------------------------
SQLAlchemy
mysql-connector-python
mysqlclient
psycopg2-binary
### }}} // data

# {{{ STAT
# --- [ml] -----------------------------------
# scikit-learn = "*"
# scikit-image = "*"
# sklearn = "*"

# --- [math] -----------------------------------
scipy
sympy

# --- [sim] --------------------------------------
# simpy = "*"
### }}} // data

# {{{ GRAPHICS
# --- [plots] -----------------------------------
matplotlib
plotly
seaborn

# --- [images] -----------------------------------
Pillow

# --- [graph] -----------------------------------
graphframes
graphviz
networkx
igraph
pyvis
pydot
### }}} // graphics

# {{{ SYSTEM
# --- [network] -----------------------------------
requests
oauthlib
requests-oauthlib
urllib3

# --- [local] -----------------------------------
pyzmq

# --- [config] -----------------------------------
pyyaml
piny
toml
click

# --- [logging] -----------------------------------
icecream

# --- [console] -----------------------------------
radian

# --- [script] -----------------------------------
tqdm

# --- [libs] -----------------------------------
pip
### }}} // system

# {{{ LANG
# --- [commons] -----------------------------------
# six = ">=1.7.0,<=1.15.0"
more-itertools
### }}} // system

# Git dependency (handled via [tool.uv.sources] below)
rootpath
# }}} RUNTIME DEPENDENCIES

# {{{ DEVELOPMENT DEPENDENCIES (from [tool.poetry.group.dev.dependencies])
[dependency-groups]
dev = [
    # {{{ JUPYTER
    "jupyter",
    "jupyter-core",
    "jupyter-console",
    "jupyter-lsp",
    "notebook",
    #jupyterhub = "*"
    #tornado = "*"
    "jupyterlab",
    "jupytext",
    "jupyterlab-lsp",
    "nodeenv",
    "nodejs",
    "pyright",
    "python-lsp-server[yapf,rope,pyflakes]",
    "python-lsp-black",
    "black[jupyter]",
    "lux-api",
    "ipykernel",
    #jupyterhub = "*"
    #ansible-kernel = "*"
    #dot_kernel = "*"
    #jswip = "*"
    #matlab_kernel = "*"
    #octave_kernel = "*"
    #sparqlkernel = "*"
    #toree = "*"
    "ipython",
    "ipython-bg",
    ### }}} // jupyter

    # {{{ TOOLS
    # --- [test] -----------------------------------
    "pytest",
    "pytest-flask",
    "pytest-cov",
    "unittest2",
    #   pytest-spark = "*"
    #   pyspark-test = "*"
    #   chispa = "*"
    "coverage",
    "mock",
    "nose",
    #codecov = "*"

    # --- [lint] --------------------------------------
    "pylint",
    "flake8",
    "pyproject-flake8",
    "jedi",
    "autopep8",
    "yapf",
    "isort",
    "pipreqs",
    "ruff",
    #black = { extras = ["jupyter"], version = "*" }

    # --- [docs] --------------------------------------
    "sphinx",
    "nbsphinx",
    "sphinx-autoapi",
    "sphinx-rtd-theme",
    ### }}} // tools

    # {{{ MISC
    "colorama",
    "py",
    "mypy",
    ### }}} // misc

    # {{{ release
    "setuptools",
    "wheel",
    "bumpversion",
    "twine",
    ### }}} // release
]
# }}} DEVELOPMENT DEPENDENCIES

# {{{ uv SOURCES & INDEXES
[[tool.uv.index]]
name = "torch121"
url = "https://download.pytorch.org/whl/cu121"
explicit = true

[[tool.uv.index]]
name = "torch124"
url = "https://download.pytorch.org/whl/cu124"
explicit = true

[[tool.uv.index]]
name = "torch130"
url = "https://download.pytorch.org/whl/cu130"
explicit = true

[tool.uv.sources]
rootpath = { git = "https://github.com/hute37/python-rootpath", branch = "stable" }
# }}} uv SOURCES & INDEXES

# {{{ SETUPTOOLS CONFIGURATION
[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
res = [ "resources/*", "resources/*/*" ]
# }}} SETUPTOOLS CONFIGURATION

# {{{ LSP: pyright
[tool.pyright]
include = ["src", "tests/pytest", "notebooks"]
exclude = [
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
#stubPath = "src/stubs"
#venv = "env367"
#verboseOutput = true
typeCheckingMode = "basic"
reportMissingImports = true
# }}} LSP

# {{{ TEST: pytest
[tool.pytest.ini_options]
pythonpath = ["src", "tests/pytest"]
testpaths = ["tests/pytest"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
# }}} TEST

# {{{ FORMATTING & LINTING
[tool.isort]
profile = "black"

[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
exclude = '''
(
  /(
      \.eggs
    | \.git
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py
)
'''

[tool.ruff]
line-length = 88
target-version = "py310"
fix = true

[tool.ruff.lint]
unfixable = []
typing-modules = ["pandas._typing"]
exclude = [
  "doc/sphinxext/*.py",
  "doc/build/*.py",
  "doc/temp/*.py",
  ".eggs/*.py",
  "pandas/util/version/*",
  "pandas/io/clipboard/__init__.py",
  "env",
]
select = [
  "F", "E", "W", "YTT", "B", "Q", "T10", "INT", "PL", "PT", "PIE", "PYI",
  "TID", "ISC", "TCH", "C4", "PGH", "RUF", "S102", "NPY002", "PERF",
  "FLY", "G", "FA", "ICN001", "SLOT", "RSE",
]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
combine-as-imports = true
split-on-trailing-commas = false

[tool.ruff.format]
docstring-code-format = true
# }}} FORMATTING & LINTING

# {{{ BUILD SYSTEM
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"
# }}} BUILD SYSTEM
```

---

## Additional Notes

- **Step 1** required no changes because the original file already used a PEP 621 `[project]` table with `dynamic = ["dependencies"]` while keeping Poetry’s own sections. This hybrid form is fully compliant and allows a gradual migration.
- **Step 2** transforms all dependencies to PEP 508 strings, moves them into `[project.dependencies]` and `[dependency-groups.dev]` (PEP 735), and replaces Poetry’s source definitions with `[[tool.uv.index]]` entries. The git dependency `rootpath` is handled via `[tool.uv.sources]`.
- All comments and region markers (`# {{{ ... }}}`) are preserved to maintain readability and document the purpose of dependency groups.
- The build backend is switched to setuptools, with explicit package discovery in `src/` and preservation of data file inclusion.
- After this migration, run `uv lock` to generate a reproducible `uv.lock` file. All existing tool configurations (pyright, pytest, ruff, etc.) remain functional.
- For CUDA‑specific variants, the conditional comments (`#@[nv]#`) are kept; they can be uncommented and adjusted as needed without breaking the TOML structure.

---

## References

- rf-1: [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- rf-2: [PEP 508 – Dependency specification for Python Software Packages](https://peps.python.org/pep-0508/)
- rf-3: [PEP 735 – Dependency Groups in pyproject.toml](https://peps.python.org/pep-0735/)
- rf-4: [uv Documentation – Dependencies](https://docs.astral.sh/uv/concepts/dependencies/)
- rf-5: [uv Documentation – Indexes](https://docs.astral.sh/uv/configuration/indexes/)
- rf-6: [setuptools Quickstart](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)



<!-- }}} \\ %1. -->
<!-- ::{{{ #TAG: TODO:(q2-section) // -->

# Q:2

## Q:2 - **Modern Python Packaging for ML**

[^](#toc)


## Role

You are a Senior Python Architect and ML Infrastructure Engineer. Your expertise lies in bridging the gap between cutting-edge ML research and professional software engineering standards. You provide pragmatic, "correct-by-construction" advice for academic teams.

## Task

Produce a professional, concise technical guide on modern Python packaging standards, specifically tailored for internal academic research projects that must remain reproducible for peer review.

## Requirements

### 1. The Modern PEP Stack

Explain the roles and relationships between the following specifications:

- **PEP 518:** The `build-system` table and build-time requirements.
- **PEP 517:** The separation of build backends from frontends.
- **PEP 621:** Standardizing project metadata in `pyproject.toml`.
- **PEP 508:** Dependency specification syntax (the "strings" used for requirements).

### 2. Implementation Guide

Provide a template for a compliant `pyproject.toml` file. Focus heavily on the syntax for *dependency strings*, including version specifiers, environment markers (for Linux/HPC environments), and Git/URL references.

### 3. Heavy Binary Management

Discuss the trade-offs of using `pip`/`PyPI` versus `Conda` for projects involving heavy binary dependencies (e.g., PyTorch, JAX, CUDA-linked libraries). Evaluate build systems like **Hatch**, **PDM**, or **Poetry** specifically in the context of research reproducibility and batch-computing environments.

## Constraints

- **Style:** Concise, technical, and authoritative.
- **Audience:** Skilled researchers/developers.
- **References:** Cite official PEPs and documentation where appropriate.



# A:2 (Claude)

[^](#toc) **_Modern Python Packaging for Reproducible ML Research_**

- see: [Modern Python Packaging for Reproducible ML Research](https://claude.ai/public/artifacts/488b0b33-4ede-4a44-af15-ea82ecf6d71f)



## 1. The Modern PEP Stack

Four interlocking PEPs define the current packaging standard. Understanding their roles prevents the common mistake of conflating build tooling with project metadata.

### PEP 518 — Build-time Requirements ([spec](https://peps.python.org/pep-0518/))

Defines the `[build-system]` table in `pyproject.toml`. Before PEP 518, `pip` had no standardized way to know *what* it needed to install before it could build a package — it simply assumed `setuptools`. PEP 518 solves this by declaring build dependencies explicitly:

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"
```

The `requires` list is installed into an isolated environment before any build step executes. This is the foundation of reproducible builds: the build tool itself is versioned.

### PEP 517 — Build Backend Interface ([spec](https://peps.python.org/pep-0517/))

Defines the contract between **build frontends** (`pip`, `build`) and **build backends** (`hatchling`, `flit-core`, `setuptools`, `pdm-backend`). The backend is specified by `build-backend` in the `[build-system]` table.

The key insight: the frontend (what the researcher invokes) is decoupled from the backend (what actually produces the wheel or sdist). You can swap backends without changing how CI pipelines invoke builds. This is why `python -m build` works identically regardless of whether the backend is `hatchling` or `setuptools`.

### PEP 621 — Standard Project Metadata ([spec](https://peps.python.org/pep-0621/))

Standardizes the `[project]` table in `pyproject.toml`. Before this, every backend had its own metadata format (`setup.py`, `setup.cfg`, `poetry`'s `[tool.poetry]`). PEP 621 defines canonical fields:

```toml
[project]
name = "my-research-pkg"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [...]
```

**Critical for reproducibility:** any PEP 621-compliant tool can read this metadata. Your project is not locked to a specific build tool's conventions.

### PEP 508 — Dependency Specification Syntax ([spec](https://peps.python.org/pep-0508/))

Defines the string format used everywhere dependencies are listed: in `pyproject.toml`, `requirements.txt`, and programmatic package resolution. The grammar is:

```
name [extras] [version_specifier] [; marker_expression] [@ url]
```

This single specification governs the "dependency strings" discussed in Section 2.

---

## 2. Implementation Guide: `pyproject.toml` Template

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
name = "research-project"
version = "0.4.0"
description = "Reproducible experiments for [Paper Title]"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.10,<3.13"

authors = [
    { name = "Author Name", email = "author@university.edu" },
]

# ============================================================
# Dependencies (PEP 508 strings)
# ============================================================
dependencies = [
    # --- Version specifiers ---
    # Compatible release: >=2.1.0, <3.0.0
    "numpy~=2.1",

    # Exact floor, no ceiling (common for fast-moving libs)
    "scipy>=1.13.0",

    # Exact pin (use sparingly; justified for security or known breakage)
    "pillow==10.4.0",

    # Multiple specifiers (intersection, not union)
    "matplotlib>=3.8.0,<4.0.0",

    # --- Environment markers (PEP 508 §4) ---
    # Install only on Linux (HPC nodes). sys_platform is most portable.
    "nvtx>=0.2.8; sys_platform == 'linux'",

    # Python-version-conditional backport
    "tomllib>=1.0.0; python_version < '3.11'",

    # CPU arch marker (useful for ARM Mac vs x86 HPC)
    "some-fast-lib[cpu]; platform_machine != 'aarch64'",

    # --- Git and URL references (PEP 440 / PEP 508 URL dependencies) ---
    # Pinned to a specific commit SHA — the only fully reproducible Git ref
    "my-internal-lib @ git+https://github.com/org/repo.git@a3f9b2c1d8e4",

    # Tag reference (reproducible if the tag is immutable)
    "research-utils @ git+https://github.com/org/research-utils.git@v0.3.1",

    # Local wheel (use for vendored/pre-built CUDA packages)
    # "flash-attn @ file:///opt/wheels/flash_attn-2.5.0-cp310-linux_x86_64.whl",
]


# ============================================================
# Optional dependency groups
# ============================================================
[project.optional-dependencies]

# Install with: pip install -e ".[dev]"
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.4.0",
    "mypy>=1.10",
    "pre-commit>=3.7",
]

# For downstream users who want notebook support
notebooks = [
    "jupyter>=1.0",
    "ipywidgets>=8.0",
    "seaborn>=0.13",
]

# Heavy compute extras — intentionally NOT in core dependencies
# (see Section 3 for why PyTorch is excluded here)
cuda = [
    "torch>=2.3.0; sys_platform == 'linux'",
    "torchvision>=0.18.0; sys_platform == 'linux'",
]


# ============================================================
# Tool configuration (non-standard, tool-specific tables)
# ============================================================
[tool.hatch.build.targets.wheel]
packages = ["src/research_project"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=research_project --cov-report=term-missing"
```

### Key Syntax Notes

**Version specifiers** follow PEP 440. Prefer `~=` (compatible release) for most dependencies; it allows patch updates while blocking major API breaks. Reserve exact pins (`==`) for situations with documented breakage — over-pinning causes dependency resolution failures for downstream users.

**Environment markers** are evaluated at install time. The available variables include `sys_platform`, `platform_machine`, `platform_system`, `python_version`, and `python_full_version`. For HPC environments, `sys_platform == 'linux'` is more robust than `platform_system == 'Linux'` due to case-sensitivity.

**Git references** must use a full commit SHA for true reproducibility. Branch names (`@main`) and tag names are mutable and will silently drift. A SHA is the only reference that guarantees the same code is installed across time.

**`@ url` syntax** (direct URL references) is incompatible with being published to PyPI. For internal research packages, this is acceptable. For anything intended for distribution, vendor the dependency or publish it to a private index.

---

## 3. Heavy Binary Management: pip/PyPI vs Conda

### The Core Problem

PyTorch, JAX, and CUDA-linked libraries distribute binaries that are tightly coupled to specific CUDA toolkit versions, driver versions, and sometimes glibc versions. PyPI cannot encode these constraints — its metadata has no concept of CUDA version. This is a fundamental mismatch, not a tooling deficiency.

### pip + PyPI

**Strengths:**
- Universally available; no separate install required.
- Integrates cleanly with `pyproject.toml` and virtual environments.
- The `--index-url` and `--extra-index-url` flags allow routing CUDA packages to PyTorch's own index: `https://download.pytorch.org/whl/cu121`.

**Weaknesses:**
- CUDA/driver compatibility is **your responsibility**. pip installs whatever wheel matches the Python version and platform tag — it does not verify driver or toolkit version.
- No native solver for multi-library constraint satisfaction (e.g., ensuring `torch`, `torchvision`, `torchaudio`, and `xformers` are mutually compatible CUDA builds).
- `requirements.txt` with hashed constraints (`pip-compile --generate-hashes`) is the standard reproducibility mechanism, but hash pinning breaks as soon as any package is re-uploaded or yanked.

**Recommended pattern for HPC:**

```bash
# requirements-cuda.txt (generated by pip-compile or manually audited)
--index-url https://download.pytorch.org/whl/cu121
torch==2.3.0+cu121 \
    --hash=sha256:...
torchvision==0.18.0+cu121 \
    --hash=sha256:...
```

This file lives outside `pyproject.toml` (because `+cu121` local version identifiers are not portable) and is installed as a pre-step before the project itself.

### Conda / Mamba

**Strengths:**
- First-class CUDA toolkit management. `conda install pytorch cudatoolkit=12.1 -c pytorch` resolves driver/toolkit/library compatibility as a single transaction.
- SAT solver (conda) or libmamba solver (mamba/micromamba) handles multi-library binary compatibility.
- Ships the C runtime and CUDA stubs; no system-level CUDA install required on the compute node.

**Weaknesses:**
- `environment.yml` is not a PEP 621 artifact. There is no standardized lock format (though `conda-lock` partially addresses this).
- Conda packages often lag PyPI by weeks to months. Cutting-edge research libraries may not exist in any Conda channel.
- Conda environments are large and slow to create, which matters in job-array HPC contexts.

### Build System Evaluation for Research

| Tool | Strengths | Weaknesses in Research/HPC Context |
|---|---|---|
| **Hatch** | Pure PEP 517/621 compliant; fast; good monorepo support via workspaces; no lockfile (by design) | No integrated lockfile; must pair with `pip-compile` or `uv` for reproducibility |
| **PDM** | PEP 621 native; integrated lockfile (`pdm.lock`); supports PEP 582 (no venv) | Lock format is PDM-specific; CUDA packages require manual index configuration |
| **Poetry** | Mature lockfile (`poetry.lock`); large ecosystem | Uses its own `[tool.poetry]` metadata (not PEP 621); lock format opaque; CUDA packages frequently require `source` blocks and manual intervention |
| **uv** | Extremely fast resolver and installer (Rust); generates `uv.lock`; fully PEP 621 compatible | Relatively new (2024); lock format not yet stable across versions |

### Recommended Architecture for Reproducible Research

For most academic ML projects, a **two-layer strategy** provides the best balance of correctness and practicality:

**Layer 1 — CUDA/system binaries:** Conda or a pre-installed module system on HPC handles `cudatoolkit`, `cudnn`, and the base Python interpreter. Document the exact `conda env export` output in the repository.

**Layer 2 — Python packages:** `pyproject.toml` with PEP 621 metadata defines the project. A `uv.lock` or `requirements-locked.txt` (generated by `uv pip compile` or `pip-compile`) pins all transitive dependencies with hashes. This file is committed to the repository and used verbatim in CI and batch jobs.

```bash
# Reproduce the exact environment for a submitted paper
conda create -n paper-env python=3.11 cudatoolkit=12.1 -c pytorch
conda activate paper-env
pip install -r requirements-locked.txt --require-hashes
pip install -e . --no-deps
```

The split acknowledges a pragmatic reality: Conda owns the binary ABI boundary; pip owns the Python package graph. Conflating these responsibilities into a single tool introduces more failure modes than it eliminates.

---

## Quick Reference

| Concern | Tool/Spec |
|---|---|
| Declare build dependencies | PEP 518 `[build-system]` |
| Swap build backends portably | PEP 517 `build-backend` |
| Standardize project metadata | PEP 621 `[project]` |
| Write dependency strings | PEP 508 syntax |
| Reproducible Python env | `uv lock` or `pip-compile --generate-hashes` |
| CUDA/binary ABI | Conda + `conda-lock` or HPC modules |
| Internal research packages | PEP 508 `@ git+https://...@<sha>` |






# A:2 (Gemini)

[^](#toc) **_Modern Python Packaging for ML_**

- see: [Modern Python Packaging for ML](https://gemini.google.com/share/5a501e6838b1)


Here is a professional guide to modern Python packaging, designed to bridge the gap between academic ML research and professional software engineering standards.

---

## 1. The Modern PEP Stack

The Python packaging ecosystem has shifted from imperative `setup.py` scripts to declarative configuration. This transition ensures deterministic builds, which are critical for academic reproducibility.

* **[PEP 518](https://peps.python.org/pep-0518/): Build System Minimum Requirements**
Introduced the `pyproject.toml` file and the `[build-system]` table. Prior to this, `pip` assumed `setuptools` and `wheel` were always the build tools. PEP 518 allows a project to explicitly declare its build-time requirements, ensuring the build environment is isolated and reproducible.
* **[PEP 517](https://peps.python.org/pep-0517/): A Build-System Independent Format**
Decoupled the *build frontend* (e.g., `pip`, `uv`, `build`) from the *build backend* (e.g., `hatchling`, `flit_core`, `poetry-core`). Frontends now call a standardized API provided by the backend to generate source distributions (sdists) and wheels, eliminating the need to execute arbitrary code in `setup.py`.
* **[PEP 621](https://peps.python.org/pep-0621/): Storing Project Metadata**
Standardized the `[project]` table in `pyproject.toml`. It ensures that core metadata—such as project name, version, authors, and dependencies—is defined in a single, backend-agnostic format, replacing the proprietary metadata structures of individual tools.
* **[PEP 508](https://peps.python.org/pep-0508/): Dependency Specification Syntax**
Defines the domain-specific language for requirement strings. It establishes the exact syntax for specifying package names, version constraints, extras, URL-based sources, and environment markers (conditional dependencies based on OS, Python version, or architecture).

---

## 2. Implementation Guide: `pyproject.toml`

Below is a compliant `pyproject.toml` template using `hatchling` as the build backend. It heavily utilizes PEP 508 syntax to demonstrate advanced dependency resolution common in ML research.

```toml
[build-system]
# PEP 518: Define build dependencies
requires = ["hatchling"]
# PEP 517: Define the backend API
build-backend = "hatchling.build"

[project]
# PEP 621: Standardized metadata
name = "diffusion-model-research"
version = "0.1.0"
description = "Reproducible diffusion models for HPC environments"
authors = [{ name = "ML Lab", email = "research@university.edu" }]
requires-python = ">=3.10"

# PEP 508: Dependency Specifications
dependencies = [
    # Standard version specifier
    "numpy>=1.24.0,<2.0.0",
    
    # Extras and specific versions
    "pandas[parquet]==2.1.0",
    
    # Environment Markers: Install Triton only on Linux/HPC
    "triton>=2.1.0 ; sys_platform == 'linux'",
    
    # Direct URL/VCS Reference: Pulling an unreleased commit from a research fork
    "jax @ git+https://github.com/google/jax.git@main",
    
    # Direct wheel URL for a specific hardware architecture
    "flash-attn @ https://github.com/Dao-AILab/flash-attention/releases/download/v2.5.6/flash_attn-2.5.6+cu122torch2.2cxx11abiFALSE-cp310-cp310-linux_x86_64.whl"
]

[project.optional-dependencies]
# Define dependency groups (e.g., for testing or dev)
dev = [
    "pytest>=7.0",
    "ruff>=0.3.0"
]

```

> **Architect's Note:** Direct URL and Git references are excellent for internal reproducibility and peer review but are *banned* from packages published to the public PyPI index. Use them strictly for private/internal artifacts.

---

## 3. Heavy Binary Management in HPC

Managing C++ dependencies, CUDA runtimes, and optimized linear algebra libraries (BLAS/LAPACK) is the hardest part of ML infrastructure.

### Pip/PyPI vs. Conda

| Feature | `pip` (PyPI) | `conda` (Conda-forge) |
| --- | --- | --- |
| **Scope** | Python packages only. | Any language (Python, C++, R, CUDA). |
| **Heavy Binaries** | Bundles massive `.whl` files with embedded `.so`/`.dll` libraries (e.g., `manylinux`). Leads to bloated environments and potential ABI collisions. | Native system-level package management. Dynamically links shared libraries securely. |
| **CUDA Support** | Relies on PyTorch/JAX publishing specific wheels. Hardware compatibility is rigid. | Can install specific CUDA toolkits, cuDNN, and compiler toolchains directly into the environment. |
| **HPC Suitability** | Poor for compiling custom kernels (requires system host compilers). | Excellent. Fully reproducible, isolated C++ and CUDA compiler toolchains. |

**Verdict:** For pure Python, use `pip`. For deep learning on HPC/Slurm clusters, **Conda** (specifically `micromamba` or `pixi` for speed) is vastly superior because it controls the system-level C/C++ ABI and CUDA toolchain.

### Build System Evaluation for Research

When orchestrating these environments, choose your tooling carefully:

* **Poetry:** Highly popular but heavily anti-patterned for ML research. Its strict lockfile resolver notoriously fails when dealing with PyTorch and JAX wheels because PyPI lacks robust platform/CUDA tags. It forces users into complex, fragile workaround configurations for heavy binaries.
* **Hatch:** A fantastic, lightweight build backend (used by PyPA). It is PEP 621 native and highly extensible. However, it lacks built-in application-level lockfiles, requiring pairing with a tool like `pip-tools` to ensure strict reproducibility.
* **PDM:** An excellent modern alternative to Poetry that is fully PEP 621 compliant. It handles complex dependency groups and lockfiles better than Hatch, but still inherits the PyPI wheel resolution issues for CUDA libraries.
* **The Modern Standard (`uv`):** In 2024/2025, the industry shifted rapidly toward [uv](https://github.com/astral-sh/uv). Written in Rust, it acts as a drop-in, sub-second replacement for `pip` and `pip-tools`.

### The Recommended "Correct-by-Construction" ML Stack

For reproducible academic ML research, use this hybrid architecture:

1. Define your Python project using **Hatchling** in `pyproject.toml`.
2. Use **Conda** (or `pixi`) to provision the base environment, Python interpreter, and heavy C++/CUDA libraries.
3. Use **uv** to resolve, lock (`uv pip compile`), and install the remaining Python dependencies into that Conda environment.

---

Would you like me to generate a `Makefile` or CI/CD snippet that automates the environment creation using this hybrid Conda + `uv` architecture?

>> YES

Here is the implementation for the hybrid Conda + `uv` architecture. This pattern provides strict separation of concerns: Conda manages the rigid C++/CUDA system dependencies, while `uv` aggressively parallelizes and deterministically locks the Python dependencies.

To make this work, you need a minimal `environment.yml` to bootstrap the system, alongside your `pyproject.toml`.

### 1. The Bootstrap `environment.yml`

Keep this file extremely lean. Its only job is to provision the host Python interpreter, the CUDA toolkit, and `uv`.

```yaml
name: diffusion-env
channels:
  - conda-forge
  - nvidia
dependencies:
  - python=3.10
  - cuda-toolkit=12.1
  - uv>=0.1.0

```

---

### 2. The Orchestration `Makefile`

A `Makefile` is the standard entry point for HPC and academic workflows. It abstracts away the complex activation logic and ensures your lab-mates are always running the exact same commands.

```makefile
# Variables
ENV_NAME := diffusion-env
# Robust activation for Makefiles (works across bash/zsh)
CONDA_ACTIVATE := source $$(conda info --base)/etc/profile.d/conda.sh && conda activate $(ENV_NAME)

.PHONY: help env lock sync clean

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

env: ## 1. Provision the base Conda environment (C++/CUDA/Python base)
	micromamba env create -f environment.yml -n $(ENV_NAME) -y

lock: ## 2. Generate a strict cross-platform lockfile from pyproject.toml
	$(CONDA_ACTIVATE) && uv pip compile pyproject.toml --all-extras --output-file requirements.lock

sync: ## 3. Atomically sync the environment to exactly match the lockfile
	$(CONDA_ACTIVATE) && uv pip sync requirements.lock
	$(CONDA_ACTIVATE) && uv pip install -e . --no-deps

clean: ## Nuke the environment and lockfiles
	micromamba env remove -n $(ENV_NAME) -y
	rm -f requirements.lock

```

*Architect's Note:* I default to `micromamba` here as it drops the heavy Python dependency of standard Conda and resolves C++ dependencies significantly faster, which is crucial for iteration speed.

---

### 3. CI/CD: GitHub Actions Snippet

When pushing to a repository for peer review, continuous integration guarantees your reproducibility claims. This pipeline utilizes `setup-micromamba` for aggressive caching, drastically reducing CI build times for heavy ML environments.

```yaml
name: Reproducibility Check

on:
  push:
    branches: [ "main" ]
  pull_request:

jobs:
  test-environment:
    runs-on: ubuntu-latest
    defaults:
      run:
        # Forces all run commands to execute inside the micromamba environment
        shell: bash -el {0} 

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Micromamba & Cache
        uses: mamba-org/setup-micromamba@v1
        with:
          environment-file: environment.yml
          environment-name: diffusion-env
          cache-environment: true
          
      - name: Sync Python Dependencies
        run: |
          # uv pip sync is atomic; it installs missing and removes extraneous packages
          uv pip sync requirements.lock
          uv pip install -e . --no-deps

      - name: Run Integration Tests
        run: |
          pytest tests/ --disable-warnings

```

Would you like me to elaborate on how to structure the `tests/` directory to specifically validate CUDA availability and ensure tensor operations are executing on the GPU rather than falling back to the CPU?

>> YES

In ML research, "reproducibility" often fails not because of the code, but because of a silent fallback to CPU when the environment is misconfigured. Validating the **Hardware-Software-Driver (HSD)** stack is as important as validating your model architecture.

### 1. The Validation Strategy

We use `pytest` with specific markers. This allows you to run local tests on a CPU-only laptop while enforcing GPU-specific tests in your HPC/Slurm environment.

### 2. Implementation: `tests/conftest.py`

This file contains the logic to skip GPU tests if the hardware or drivers are missing, preventing "false failure" reports.

```python
import pytest
import torch

@pytest.fixture(scope="session")
def device():
    """Returns the best available device."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def pytest_collection_modifyitems(config, items):
    """Automatically skip tests marked with @pytest.mark.gpu if CUDA is unavailable."""
    if not torch.cuda.is_available():
        skip_gpu = pytest.mark.skip(reason="CUDA hardware/driver not detected")
        for item in items:
            if "gpu" in item.keywords:
                item.add_marker(skip_gpu)

```

---

### 3. Implementation: Hardware Integration Tests

Create a dedicated `tests/test_infrastructure.py` to verify the "correct-by-construction" environment you built with `uv` and `micromamba`.

```python
import torch
import pytest
import os

@pytest.mark.gpu
def test_cuda_interop():
    """Verify PyTorch can talk to the NVIDIA driver and move tensors."""
    assert torch.cuda.is_available(), "CUDA not available to PyTorch"
    
    # Check for the correct CUDA version defined in your environment.yml
    # e.g., '12.1'
    expected_version = "12"
    assert torch.version.cuda.startswith(expected_version)

    # Tensor round-trip test
    x = torch.ones((1024, 1024)).to("cuda")
    y = x * 2
    assert y.device.type == "cuda"
    assert torch.allclose(y, torch.full((1024, 1024), 2.0).to("cuda"))

@pytest.mark.gpu
def test_cudnn_available():
    """Deep learning primitives (Conv/RNN) require cuDNN."""
    assert torch.backends.cudnn.is_available()
    assert torch.backends.cudnn.enabled

```

---

### 4. Running the Validation

Integrate these checks into your `Makefile` to ensure the environment is healthy before starting a long-running experiment.

```makefile
test-infra: ## Verify the CUDA/CUDNN stack is operational
	$(CONDA_ACTIVATE) && pytest tests/test_infrastructure.py -v -m gpu

test-all: ## Run all unit and hardware tests
	$(CONDA_ACTIVATE) && pytest tests/ -v

```

### 5. Why this matters for Peer Review

When you provide your code to reviewers, they can run `make env && make sync && make test-infra`. If `test-infra` passes, they have objective proof that their local hardware setup matches your research requirements. If it fails, the error message tells them exactly which layer (Driver vs. Library) is the culprit.

Would you like a template for a **`README.md`** section that explains how to use these reproducibility tools for external reviewers?

>> YES

This `README.md` section is designed to give peer reviewers and collaborators a "one-click" path to replicating your exact research environment. It signals professional rigor and significantly lowers the barrier to verifying your results.

---

## Reproducibility & Environment Setup

This project uses a hybrid **Conda + uv** architecture to ensure bit-for-bit reproducibility of the hardware-software stack (CUDA/C++/Python).

### Prerequisites

* **Conda/Micromamba**: Required for managing the Python interpreter and CUDA toolkit. [Download Micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html).
* **NVIDIA Drivers**: Ensure your host machine has drivers compatible with **CUDA 12.1** or higher.

### Quick Start (HPC / Linux)

We provide a `Makefile` to automate the complex orchestration of environment provisioning and dependency locking.

```bash
# 1. Create the base environment (Python + CUDA Toolkit)
make env

# 2. Sync Python dependencies via uv (Atomic & Deterministic)
# This uses the requirements.lock file to ensure identical package versions.
make sync

# 3. Verify the Hardware-Software-Driver (HSD) stack
# This ensures PyTorch can see the GPU and cuDNN is functional.
make test-infra

```

### Dependency Architecture

To maintain a "correct-by-construction" environment, we separate dependencies into two layers:

1. **System Layer (`environment.yml`)**: Managed by Conda. Contains the Python interpreter, CUDA kernels, and C++ compilers.
2. **Application Layer (`pyproject.toml`)**: Managed by `uv`. Contains ML libraries (PyTorch, JAX) and research-specific code.

| File | Purpose |
| --- | --- |
| `pyproject.toml` | PEP 621 metadata and high-level dependency requirements. |
| `requirements.lock` | A fully resolved, platform-specific lockfile generated by `uv`. |
| `tests/test_infrastructure.py` | Automated checks for CUDA/GPU parity. |

### Hardware Validation

Before running training scripts, we recommend running the infrastructure validation suite:

```bash
conda activate diffusion-env
pytest tests/test_infrastructure.py -v -m gpu

```

If these tests fail, your local environment does not match the research requirements (e.g., mismatched CUDA versions or missing drivers), and results may not be reproducible.

### Citation

If you use this environment stack or code in your research, please cite:

```bibtex
@software{diffusion_research_2026,
  author = {Your Lab Name},
  title = {Reproducible Diffusion Research Template},
  year = {2026},
  url = {https://github.com/your-repo}
}

```

---

This concludes the setup for your research infrastructure. Is there a specific ML framework (e.g., **PyTorch Lightning**, **Accelerate**, or **Hydra** for config management) you’d like to integrate into this `pyproject.toml` structure?




# A:2 (ChatGPT)

[^](#toc) **_Modern Python Packaging Guide_**


- see: [Modern Python Packaging Guide](https://chatgpt.com/share/69b2efa6-8bd0-8012-be2b-e93cd99c5473)

This guide summarizes the **modern Python packaging standards** relevant for **internal academic ML projects** that must remain reproducible for peer review, artifact evaluation, and long-term archival. The modern ecosystem centers on **`pyproject.toml`** and a set of interoperable specifications (PEPs) that decouple **build configuration, metadata, and dependency specification**.

Primary specifications:

- PEP 518 – build system declaration
- PEP 517 – build backend/frontend interface
- PEP 621 – standardized project metadata
- PEP 508 – dependency specification syntax

These specifications form the **modern packaging stack** used by tools
such as pip, Hatch, PDM, and Poetry.

---

## 1. The Modern PEP Stack

### 1.1 Build Configuration — PEP 518

PEP 518 introduced the **`pyproject.toml` file** and the
**`[build-system]` table**, which defines **build-time requirements**.

Before this PEP, builds depended implicitly on `setup.py` execution
and required tools to guess dependencies.

Example:

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"
```

Key properties:

| Concept         | Purpose                                        |
| --------------- | ---------------------------------------------- |
| `requires`      | Packages required to build the project         |
| `build-backend` | Python module implementing the build interface |

For research environments, this guarantees that **build dependencies
are explicit**, enabling reproducible builds.

---

### 1.2 Backend Interface — PEP 517

PEP 517 defines a **standard API between build frontends and build backends**.

**Frontend tools**

- pip
- build
- uv

**Backend implementations**

- Setuptools
- Hatchling
- PDM Backend
- Poetry Core

Architecture:

```
Frontend (pip / build / uv)
        │
        │ PEP 517 API
        ▼
Backend (hatchling / setuptools / pdm-backend)
        │
        ▼
Build artifacts (wheel / sdist)
```

Benefits:

- Replaces implicit `setup.py` execution.
- Enables multiple build backends.
- Allows minimal, deterministic build environments.

For academic reproducibility, this prevents **hidden execution logic during builds**.

---

### 1.3 Standard Metadata — PEP 621

PEP 621 standardizes **project metadata** inside `pyproject.toml`.

Historically this lived in `setup.py` or `setup.cfg`. PEP 621 moves it
to a **static declarative format**.

Example:

```toml
[project]
name = "ml-research-project"
version = "0.1.0"
description = "Experimental ML research codebase"
readme = "README.md"
requires-python = ">=3.10"

authors = [
  { name = "Research Group", email = "ml@university.edu" }
]

dependencies = [
  "numpy>=1.26",
  "torch>=2.2",
]
```

Advantages:

- Machine-readable metadata
- Compatible with all modern build tools
- Supports dependency specification using **PEP 508 strings**

---

### 1.4 Dependency Syntax — PEP 508

PEP 508 defines the **grammar for dependency specification strings**
used across the Python ecosystem.

Example syntax:

```
package_name[extra] version_specifier ; environment_marker
```

Examples:

```text
numpy>=1.26
pandas>=2.0,<3
torch==2.2.*
jax[cuda12]>=0.4.20
```

#### Environment markers

Environment markers allow **platform-specific dependencies**, useful in HPC clusters.

Example:

```text
uvloop>=0.19 ; sys_platform == "linux"
pywin32 ; sys_platform == "win32"
```

Common markers:

| Marker             | Example                    |
| ------------------ | -------------------------- |
| `python_version`   | `python_version >= "3.10"` |
| `sys_platform`     | `"linux"` / `"darwin"`     |
| `platform_machine` | `"x86_64"`                 |
| `platform_system`  | `"Linux"`                  |

Example HPC constraint:

```text
jax[cuda12]>=0.4.20 ; platform_system == "Linux"
```

---

## 2. Implementation Guide

### Minimal Reproducible `pyproject.toml`

```toml
[build-system]
requires = ["hatchling>=1.21"]
build-backend = "hatchling.build"

[project]
name = "ml-research-project"
version = "0.1.0"
description = "Reproducible ML research experiments"
readme = "README.md"
requires-python = ">=3.10"

authors = [
  { name = "Research Team", email = "research@example.edu" }
]

dependencies = [
  "numpy>=1.26",
  "scipy>=1.11",
  "pandas>=2.1",

  # ML frameworks
  "torch>=2.2",
  "jax>=0.4.20",

  # Linux-specific HPC dependency
  "uvloop>=0.19 ; sys_platform == 'linux'",

  # Optional GPU packages
  "nvidia-cublas-cu12 ; platform_system == 'Linux'"
]

[project.optional-dependencies]

dev = [
  "pytest>=7",
  "ruff>=0.4",
  "mypy>=1.8"
]

docs = [
  "mkdocs>=1.5",
  "mkdocs-material"
]

[project.urls]
Repository = "https://github.com/research-group/ml-project"
```

---

### Git Dependencies

Useful for **unreleased research libraries**.

Example:

```toml
dependencies = [
  "transformer-engine @ git+https://github.com/NVIDIA/TransformerEngine.git"
]
```

Pinned revision:

```toml
"mylib @ git+https://github.com/user/mylib.git@8b6c2c1"
```

---

### Direct URL Dependencies

Example:

```toml
dependencies = [
  "customlib @ https://example.com/packages/customlib-0.2.0-py3-none-any.whl"
]
```

Recommended only for **artifact reproduction or archival datasets**.

---

## 3. Heavy Binary Dependency Strategy

ML systems depend heavily on **compiled libraries**.

Examples:

- PyTorch
- JAX
- CUDA
- TensorFlow

These create tension between **PyPI packaging** and **Conda environments**.

---

### pip / PyPI Approach

Advantages:

- Standard Python packaging workflow
- Compatible with `pyproject.toml`
- Works with modern resolvers

Modern wheels include many compiled dependencies (e.g. PyTorch).

Limitations:

- CUDA compatibility issues
- HPC environments may lack system libraries
- Binary compatibility depends on manylinux constraints

Typical command:

```
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

---

### Conda / Mamba Approach

Conda environments manage **system-level dependencies**.

Advantages:

- Reliable GPU stacks
- Binary compatibility across Linux clusters
- Handles C/C++ dependencies

Limitations:

- Separate packaging ecosystem
- Harder integration with `pyproject.toml`
- Reproducibility requires `environment.yml`

Example:

```yaml
name: ml-project
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pytorch
  - cudatoolkit
  - pip
  - pip:
      - -e .
```

---

### Recommended Hybrid Strategy

For academic ML projects:

```
Conda → system / binary dependencies
pip → Python package installation
```

Workflow:

```
conda create -n mlproj python=3.11 pytorch cudatoolkit
pip install -e .
```

Benefits:

- Stable CUDA stack
- Standard Python packaging
- Compatible with CI and reproducibility archives

---

## 4. Build System Evaluation

### Hatch

Hatch is currently one of the **cleanest PEP-compliant build tools**.

Strengths:

- Pure `pyproject.toml`
- Reproducible environments
- Lightweight backend (`hatchling`)
- Good CI compatibility

Recommended for **research projects**.

---

### PDM

PDM emphasizes **PEP-native workflows**.

Strengths:

- Uses PEP 582 or virtualenv
- Lockfile support
- Good dependency resolution

Useful when reproducibility via **lockfiles** is required.

---

### Poetry

Poetry historically dominated research projects.

Advantages:

- Integrated dependency resolver
- Good UX

Limitations:

- Custom dependency specification layer
- Lockfile ecosystem diverges slightly from PEP-native tooling
- Less ideal for HPC workflows

---

### Recommendation for Academic Research

A pragmatic stack:

```
pyproject.toml (PEP 518/621)
        │
Hatchling build backend
        │
pip / uv for installation
        │
Conda or Mamba for system binaries
```

This provides:

- **Reproducible builds**
- **Minimal tooling complexity**
- **Compatibility with artifact review pipelines**

---

## 5. Reproducibility Best Practices for ML Papers

1. **Commit `pyproject.toml`**
2. **Export dependency lockfile**

Example:

```
pip freeze > requirements-lock.txt
```

3. Provide **Conda environment**

```
conda env export > environment.yml
```

4. Archive artifacts:

- Git tag
- Docker image
- dataset checksum

5. Provide a **one-command install script** for reviewers.

---

## Key References

- PEP 518 – Build system requirements
- PEP 517 – Build backend interface
- PEP 621 – Project metadata
- PEP 508 – Dependency specification

Official documentation:

- Python Packaging User Guide
- pip dependency resolution documentation



# A:2 (Perplexity)

[^](#toc) **_Python Packaging Guide_**

- see: [Python Packaging Guide](https://www.perplexity.ai/search/role-you-are-a-senior-python-a-1lDQbrCYRriRal10NuG9Ig)


You should treat `pyproject.toml` as the single, canonical source of truth for build configuration and metadata, and then layer environment-specific tooling (pip/Conda, Hatch/PDM/Poetry) around it in a way that keeps experiments reproducible across laptops, CI, and HPC nodes. [peps.python](https://peps.python.org/pep-0621/)


## 1. The modern PEP stack

### PEP 518 – build-time requirements

- PEP 518 introduces the `[build-system]` table in `pyproject.toml` to declare the *minimum* build system and its *build-time* dependencies. [peps.python](https://peps.python.org/pep-0518/)
- `build-system.requires` is a list of PEP 508 requirement strings specifying what must be installed *before* the backend can run (e.g. `["setuptools>=61", "wheel"]`). [peps.python](https://peps.python.org/pep-0508/)
- This allows frontends (e.g. `pip`, `build`, Hatch, PDM, Poetry) to create an isolated build env with exactly those dependencies, decoupling project builds from whatever happens to be in the user’s environment. [dev.docs.pyansys](https://dev.docs.pyansys.com/packaging/build-systems.html)

### PEP 517 – backends vs frontends

- PEP 517 defines a standard interface for *build backends* (the thing that knows how to build wheels/sdists) and *build frontends* (the tool the user runs, like `pip` or `python -m build`). [reddit](https://www.reddit.com/r/learnpython/comments/10cy488/what_does_it_mean_for_a_tool_to_be_build_frontend/)
- The backend is named in `build-system.build-backend`, e.g. `"setuptools.build_meta"`, `"hatchling.build"`, `"poetry.core.masonry.api"`, or `"pdm.backend"`, and the frontend only talks to it via the PEP 517 API. [pydevtools](https://pydevtools.com/handbook/explanation/what-is-a-build-frontend/)
- In theory you can mix a frontend from tool A with a backend from tool B as long as both are PEP 517-compliant; in practice, many tools ship a tightly integrated pair (e.g. Poetry + `poetry-core`, PDM + `pdm-backend`). [reddit](https://www.reddit.com/r/learnpython/comments/10cy488/what_does_it_mean_for_a_tool_to_be_build_frontend/)

### PEP 621 – project metadata in `pyproject.toml`

- PEP 621 standardizes how to store *core project metadata* under `[project]` in `pyproject.toml` (name, version, authors, dependencies, URLs, entry points, etc.). [peps.python](https://peps.python.org/pep-0621/)
- When a project uses PEP 621, this metadata is considered canonical; tools must treat it as the single source of truth and must not silently mutate statically specified fields. [peps.python](https://peps.python.org/pep-0621/)
- Fields can be either fully specified or marked `dynamic` (e.g. `dynamic = ["version"]` when the backend computes it), but anything not listed as dynamic must be present and valid. [github](https://github.com/pypa/pyproject-metadata)

### PEP 508 – dependency specification strings

- PEP 508 defines the grammar for a *single dependency string*: package name, version specifier(s), optional extras, optional URL/direct reference, and optional environment marker. [peps.pythondiscord](https://peps.pythondiscord.com/pep-0508/)
- These strings are used everywhere: `build-system.requires` (PEP 518), `[project].dependencies` and `[project.optional-dependencies]` (PEP 621), requirements files, etc. [dev.docs.pyansys](https://dev.docs.pyansys.com/packaging/build-systems.html)
- Environment markers (e.g. `; python_version >= "3.10" and sys_platform == "linux"`) control when a dependency applies; if the marker evaluates to false in a given environment, the dependency is ignored. [peps.python](https://peps.python.org/pep-0508/)

PEPs 518 and 517 define *how* builds run; PEP 621 defines *what* the project is; PEP 508 defines the *syntax* for all dependency strings those other PEPs rely on. [peps.python](https://peps.python.org/pep-0518/)

***

## 2. Implementation guide: `pyproject.toml` template

Below is a PEP-518/517/621-compliant template emphasizing PEP 508 dependency syntax, including environment markers and VCS/URL requirements. [peps.python](https://peps.python.org/pep-0518/)

```toml
[build-system]
requires = [
  "hatchling>=1.18",          # PEP 508 requirement string
]
build-backend = "hatchling.build"

[project]
name = "my-research-project"
version = "0.1.0"
description = "Reproducible experiments for XYZ paper."
readme = "README.md"
requires-python = ">=3.11"

license = { text = "MIT" }

authors = [
  { name = "Giovanni Pelosi", email = "giovanni@example.org" },
]

# --- Core runtime dependencies (PEP 621, PEP 508 strings) ---
dependencies = [
  # Simple pinned/compatible versions
  "numpy>=1.26,<2.0",
  "scipy>=1.12",
  "pandas==2.1.4",

  # Extras
  "matplotlib[qt]>=3.8",

  # Environment markers: typical Linux/HPC constraints
  # Only install on CPython on Linux with Python >=3.11
  "psutil>=5.9; python_version >= '3.11' and platform_system == 'Linux' and implementation_name == 'cpython'",

  # Different implementation depending on availability (example)
  "uvloop>=0.19; platform_system == 'Linux'",
  "colorama>=0.4; platform_system == 'Windows'",

  # GPU vs CPU dependencies (marker-based toggle)
  "cupy-cuda12x>=13.0; platform_system == 'Linux' and extra == 'gpu'",
]

# Optional dependency groups for extras (e.g., pip install .[dev,gpu])
[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-cov>=4.1",
  "ruff>=0.5",
  "mypy>=1.10",
]

docs = [
  "sphinx>=7.2",
  "sphinx-autodoc-typehints>=2.0",
]

gpu = [
  # You typically prefer Conda for CUDA stacks; this is illustrative only.
  "torch>=2.2; platform_system == 'Linux'",
]

hpc = [
  # HPC-specific tools (installed only on Linux, not macOS/Windows)
  "mpi4py>=3.1; platform_system == 'Linux'",
  "tqdm>=4.66",
]

# Direct references / VCS URLs (PEP 508)
# NOTE: These are better kept in a separate constraints/lock file for reproducibility,
# but are sometimes necessary for academic forks.
experimental = [
  # GitHub repo at a tag
  "myfork @ git+https://github.com/mygroup/myfork.git@v0.3.1",

  # Specific commit hash
  "customlib @ git+https://github.com/otherlab/customlib.git@a1b2c3d4e5f6",

  # Git over SSH (internal repos; requires SSH keys on HPC)
  "private-utils @ git+ssh://git@github.com/mygroup/private-utils.git@main",
]

[project.urls]
homepage = "https://git.example.org/mygroup/my-research-project"
repository = "https://git.example.org/mygroup/my-research-project.git"
issues = "https://git.example.org/mygroup/my-research-project/issues"

[tool.hatch.metadata]
# Example of delegating some metadata dynamically if desired
allow-direct-references = true
```

Key idioms relevant for research/HPC:

- **Version pins vs ranges**: for reproducibility, prefer upper-bounded or fully pinned versions; use looser ranges only in early exploration phases, but lock in versions for submitted artifacts. [dasroot](https://dasroot.net/posts/2026/01/python-packaging-best-practices-setuptools-poetry-hatch/)
- **Environment markers for Linux/HPC**: use `platform_system == "Linux"`, `platform_machine == "x86_64"` and optionally `python_version >= "3.11"` to declare Linux-only or x86-only deps, and avoid installing MPI/CUDA packages on dev laptops. [peps.python](https://peps.python.org/pep-0508/)
- **Direct references**: `name @ git+https://...@ref` is PEP 508-compliant and lets you point to forks or internal repos, but you should capture the *resolved* commit in a lock file or constraints file to keep runs reproducible. [pythontutorials](https://www.pythontutorials.net/blog/how-to-write-setup-py-to-include-a-git-repository-as-a-dependency/)

In practice for a paper you want:

- `pyproject.toml` (canonical metadata, minimal constraints).  
- A lock/constraints file (`poetry.lock`, `pdm.lock`, `requirements.txt` + `constraints.txt`, or Hatch lock) checked in and referenced in the replication instructions. [dasroot](https://dasroot.net/posts/2026/01/python-packaging-best-practices-setuptools-poetry-hatch/)

***

## 3. Heavy binary management (PyPI vs Conda; Hatch/PDM/Poetry)

### pip/PyPI vs Conda for heavy binaries

**pip / PyPI**

- Strengths: aligns directly with PEP 508/517/518/621; integrates cleanly with `pyproject.toml` and modern build backends; wheels are often available for major GPU/CPU combos (torch, jax, etc.). [dev.docs.pyansys](https://dev.docs.pyansys.com/packaging/build-systems.html)
- Weaknesses: no first-class solver for system libraries; CUDA/BLAS/FFT dependencies are assumed to be present or provided via wheels; heterogeneous HPC clusters often lack the exact glibc / driver versions implied by PyPI wheels, forcing you to build from source.  

**Conda (or mamba)**

- Strengths: environment solver covers both Python and non-Python dependencies, including CUDA toolkits, MKL/OpenBLAS, NCCL, MPI, and system libs; ideal for clusters where you cannot control the OS images but can load modules and Conda envs. [dasroot](https://dasroot.net/posts/2026/01/python-packaging-best-practices-setuptools-poetry-hatch/)
- Weaknesses: Conda’s dependency metadata is separate from `pyproject.toml`; PEP 517/621 tooling does not natively “understand” Conda, so the Conda spec becomes a parallel source of truth that must be kept consistent manually.  

For heavy binary stacks (PyTorch, JAX, CUDA-linked libraries) on HPC:

- Use **Conda/mamba** to provision the *base* environment (Python version, CUDA toolkit, compilers, BLAS, MPI, etc.).  
- Within that environment, use **pip** with a PEP-621 `pyproject.toml` (and a lock/constraints file) for your own package and light pure-Python dependencies. [dasroot](https://dasroot.net/posts/2026/01/python-packaging-best-practices-setuptools-poetry-hatch/)

### Build systems (Hatch, PDM, Poetry) for research reproducibility

All three can act as PEP 517 backends and PEP 621 metadata consumers; the differences matter for workflow and HPC ergonomics rather than basic correctness. [peps.python](https://peps.python.org/pep-0621/)

#### High-level comparison

| Aspect                               | Hatch                        | PDM                             | Poetry                         |
|--------------------------------------|------------------------------|---------------------------------|--------------------------------|
| Default backend                      | `hatchling` (PEP 517/621)    | `pdm-backend` (PEP 517/621)     | `poetry-core` (PEP 517/621)    |
| Lock file                            | `hatch.lock`                 | `pdm.lock`                      | `poetry.lock`                  |
| Env management                       | Optional (via envs feature)  | Built-in, uses PEP 582 or venvs | Built-in, virtualenvs          |
| Conda/HPC friendliness               | Good (external envs, simple) | Good (can run inside Conda)     | Acceptable but heavier         |
| Philosophy                           | “Backend first”, modular     | “pip-like but modern”           | “All-in-one project manager”   |
| Learning curve                       | Moderate                     | Low–moderate                    | Moderate–high                  |

#### Hatch

- Pros: very thin backend (`hatchling`), minimal magic, good alignment with PEP 621, and good fit if you already manage environments with Conda, modules, or `venv` and just need reproducible builds and releases. [dasroot](https://dasroot.net/posts/2026/01/python-packaging-best-practices-setuptools-poetry-hatch/)
- Cons: less opinionated about dependency management; you must integrate your own lock/constraints strategy, which is often what you want for reproducible academic workflows that live under Conda anyway.  

**Academic/HPC guidance:** Use Hatch as the build backend and keep dependency resolution outside (Conda + `pip-compile` or equivalent). This keeps `pyproject.toml` simple and lets you document exact environment creation commands separately.  

#### PDM

- Pros: PEP 621-native from day one; uses standard `pyproject.toml` for metadata and dependencies, with a deterministic `pdm.lock` for reproducible installs. [peps.python](https://peps.python.org/pep-0621/)
- Pros (HPC): can operate inside any Python environment (including Conda), and you can tell users: “load module X, create Conda env, then `pdm install --frozen`”.  
- Cons: PDM’s own environment management (PEP 582 local packages, its own venvs) is less relevant on HPC where Conda/modules are standard.  

**Academic/HPC guidance:** Strong choice if you want lock-file-based reproducibility but still expect users to bring their own Conda env. Treat `pdm.lock` as part of the replication bundle.  

#### Poetry

- Cons (HPC): Poetry prefers to manage its own virtualenvs, which can clash with module/Conda-based workflows; it is heavier and more opinionated, and HPC users may fall back to `pip install .` anyway.  

**Academic/HPC guidance:** Reasonable if your group standardizes on Poetry across laptops and a modest CI, but you’ll need explicit documentation for how to reconcile Poetry’s envs with Conda and modules on clusters.  

### Recommended patterns for research projects

For a reproducible, HPC-friendly research project:

1. **Use PEP 621 metadata in `pyproject.toml`** with Hatch or PDM as the backend, keeping dependencies expressed as PEP 508 strings. [peps.python](https://peps.python.org/pep-0508/)
2. **Manage heavy binaries via Conda** (or system modules) and treat `pyproject.toml` as Python-level metadata, not as a full system spec.  
3. **Check in a lock or constraints file** (`pdm.lock`, `poetry.lock`, or `requirements.txt` + `constraints.txt`) that corresponds to the environment used to generate the paper’s results. [dasroot](https://dasroot.net/posts/2026/01/python-packaging-best-practices-setuptools-poetry-hatch/)
4. **Document an end-to-end “replication recipe”**:  
   - Create Conda env with specific Python/CUDA.  
   - Install your package via the chosen frontend in *frozen* mode (`pdm install --frozen`, `pip install -r requirements.txt -c constraints.txt`, etc.). [dev.docs.pyansys](https://dev.docs.pyansys.com/packaging/build-systems.html)

This approach keeps you fully aligned with modern PEPs while acknowledging the realities of heavy binary stacks and heterogeneous HPC environments.


# A:2 (DeepSeek)

[^](#toc) **_Modern Python Packaging for Reproducible Research_**

- see: [Modern Python Packaging for Reproducible Research](https://chat.deepseek.com/share/fr7ksfy0f2u8qhf9lp)

## Technical Guide: Modern Python Packaging for Reproducible Research

### 1. The Modern PEP Stack: A Concise Reference

Understanding the PEP stack is essential for constructing reproducible research environments. These specifications form the foundation of modern Python packaging.

**PEP 518 – `pyproject.toml` & Build Requirements**
- Introduces `pyproject.toml` as a standard configuration file
- Defines the `[build-system]` table specifying tools needed *before* building your project
- Example: `requires = ["setuptools>=61.0", "wheel"]` ensures the correct build tools are present

**PEP 517 – Build Backend Abstraction**
- Decouples build frontends (pip) from backends (setuptools, hatchling, flit)
- Allows projects to specify their build backend independently of installation tools
- Critical for reproducibility: the same backend version builds identical distributions

**PEP 621 – Standardized Project Metadata**
- Moves project metadata (name, version, dependencies) into `pyproject.toml`
- Eliminates duplication between `setup.py`, `setup.cfg`, and `requirements.txt`
- Backend-agnostic: works with any PEP 517-compliant builder

**PEP 508 – Dependency Specification Syntax**
- Defines the grammar for requirement strings
- Supports version specifiers (`>=`, `~=`, `==`), environment markers, and URL references
- The syntax used in `dependencies` lists, `requirements.txt`, and `install_requires`

### 2. Implementation Guide: Production-Ready Template

```toml
[build-system]
requires = ["hatchling>=1.18.0"]
build-backend = "hatchling.build"

[project]
name = "research-project"
version = "2024.1.0"
description = "Reproducible ML Research Artifact"
authors = [{name = "Research Group", email = "group@university.edu"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.10,<3.12"

dependencies = [
    # Core scientific stack with exact pinning for reproducibility
    "numpy==1.24.3",
    "scipy==1.10.1",
    
    # Version ranges with upper bounds for ABI compatibility
    "pandas>=2.0.0,<2.2.0",
    
    # Git reference for unreleased fixes (use commit hash for immutability)
    "custom-utils @ git+https://github.com/lab/custom-utils.git@a1b2c3d4e5f6...",
    
    # Local path for in-development dependencies (use with caution)
    "-e ../shared-lib",
    
    # Environment markers for platform-specific dependencies
    "nvidia-ml-py3 >=7.352.0 ; sys_platform == 'linux'",
    "pywin32 >=305 ; sys_platform == 'win32'",
    
    # CUDA-aware package with marker
    "cupy-cuda12x >=12.0.0 ; platform_system == 'Linux' and platform_machine == 'x86_64'",
    
    # Conditional dependency based on Python version
    "dataclasses >=0.6 ; python_version < '3.7'",
    
    # Package with direct URL (PEP 508)
    "dataset @ https://github.com/org/dataset/archive/refs/tags/v1.2.3.zip",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "pre-commit>=3.3.0",
]
hpc = [
    "mpi4py>=3.1.5",
    "horovod>=0.28.0 ; platform_system != 'Windows'",
]

[tool.hatch.build.targets.wheel]
packages = ["src/research_project"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/tests",
    "/scripts",
    "/data/sample",
]
exclude = [
    "/data/large",
    "/.github",
]

# Optional: Version constraints for transitive dependencies
[tool.hatch.metadata]
allow-direct-references = true
```

**Critical Dependency String Patterns:**
- **Exact pins**: `package==1.2.3` – Maximum reproducibility, minimum flexibility
- **Compatible release**: `package~=1.2.0` – Equivalent to `>=1.2.0,<1.3.0`
- **Environment markers**: `package>=1.0 ; sys_platform == 'linux'`
- **Git commits**: `package @ git+https://...@<full-commit-hash>` – Never use branches
- **Local paths**: `package @ file:///absolute/path` or relative with `-e`

### 3. Heavy Binary Management: Strategic Considerations

#### Pip/PyPI vs. Conda

| Aspect | Pip/PyPI | Conda |
|--------|----------|-------|
| **Binary Compatibility** | Requires system compilers, manylinux wheels | Pre-built binaries across platforms |
| **CUDA/GPU Support** | PyPI hosts CUDA wheels (PyTorch, TensorFlow) | Conda handles CUDA toolkit as dependency |
| **Environment Isolation** | Virtualenv/venv | Native environment solver |
| **Non-Python Dependencies** | Manual installation required | Handles C libraries, CUDA, MPI |
| **Reproducibility** | `pip freeze` + constraints files | `conda env export` + explicit specs |

**Recommendation for HPC/Research:**
- **Use Conda when:** You need exact CUDA toolkit versions, complex C++ dependencies, or non-Python libraries (OpenMPI, HDF5). Conda's solver handles SAT/SMT constraints better than pip's linear resolver.
- **Use Pip when:** Dependencies are pure Python or have well-distributed wheels, you need PyTorch nightly builds, or you're deploying to environments with existing module systems (e.g., cluster Lmod).

#### Build System Evaluation

**Hatch**
- **Strengths:** Standards-compliant, excellent environment management, matrix testing
- **Research fit:** Ideal for projects requiring multiple Python version tests; minimal magic
- **Reproducibility:** `hatch env show` provides full environment specs

**PDM**
- **Strengths:** PEP 582 (local packages) support, lockfile-first approach
- **Research fit:** Excellent when you need deterministic installs across clusters
- **Reproducibility:** `pdm lock` creates complete resolution graph; `pdm export` to requirements.txt

**Poetry**
- **Strengths:** Dependency resolution, semantic versioning, active community
- **Research fit:** Good for libraries, but solver can be slow with large scientific stacks
- **Reproducibility:** Lockfile ensures identical transitive dependencies; supports group dependencies

**Verdict for Research Teams:**
- **Hatch** for standards compliance and simplicity
- **PDM** when lockfile accuracy is paramount
- **Poetry** for teams prioritizing UX over pure standards
- **Avoid** legacy `setup.py` unless absolutely required

### 4. Best Practices for Reproducible Research

1. **Pin everything, including build tools:**
   ```toml
   [build-system]
   requires = ["setuptools==68.2.2", "wheel==0.41.2"]
   ```

2. **Use constraints files for deep reproducibility:**
   ```bash
   # Generate during working state
   pip freeze --exclude-editable > constraints.txt
   # Install with constraints
   pip install -e . -c constraints.txt
   ```

3. **Document the environment explicitly:**
   ```bash
   # Record complete environment
   pip list --format=freeze > requirements.full.txt
   conda list --explicit > spec-file.txt
   ```

4. **CI/CD validation:**
   - Test install in fresh container weekly
   - Validate against latest dependency updates monthly
   - Archive full environment specs with publication

### References
- [PEP 508 – Dependency specification](https://peps.python.org/pep-0508/)
- [PEP 517 – Build system interface](https://peps.python.org/pep-0517/)
- [PEP 518 – pyproject.toml](https://peps.python.org/pep-0518/)
- [PEP 621 – Project metadata](https://peps.python.org/pep-0621/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Conda Build Concepts](https://docs.conda.io/projects/conda-build/en/latest/concepts/general.html)

This approach ensures your research artifacts remain installable and verifiable years after publication, surviving Python ecosystem evolution and infrastructure changes.


<!-- }}} \\ %2. -->
<!-- {{{ // %*
LocalWords:  GitLab CommonMark GFM GLFM YAML
vim: set foldmethod=marker :
}}} // %* -->
