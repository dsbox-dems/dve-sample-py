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
