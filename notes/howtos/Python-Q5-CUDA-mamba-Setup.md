---
title: Rootless Podman CUDA Container with Micromamba and uv
subtitle: |
  A reproducible, system-wide CUDA/cuDNN environment for PyTorch
  in rootless Podman using micromamba for HPC library management
  and uv for Python project orchestration
# {{{ // %+
category: Python-HOWTOs
keywords: [GEN, Podman, CUDA, micromamba, uv, PyTorch, HPC, containers]
abstract: |
  This document presents a technical guide for designing a robust,
  reproducible base container image for rootless Podman environments
  targeting Machine Learning workloads on NVIDIA hardware.
  The architecture separates system-level HPC library management
  from Python project management: `micromamba` governs the CUDA,
  cuDNN, and BLAS stack, while `uv` handles Python versioning and
  virtual environments.

  The setup operates under a strict "No-Home" constraint, requiring
  all persistent toolchains, libraries, and binaries to reside
  under `/usr/local` or `/opt` rather than user home directories.
  This ensures compatibility with rootless Podman workflows where
  `/home` is unavailable at image build time and mounted only at
  runtime.

  Three primary deliverables are specified: a system-level setup
  script (`install_cuda.sh`) that installs `micromamba` globally
  and configures environment variables (`LD_LIBRARY_PATH`,
  `CUDA_HOME`, `PATH`) system-wide; a `conda-env.yaml` environment
  specification targeting `cuda-toolkit=13.1`, `cudnn`, and
  `libblas` for NVIDIA Driver 580+ compatibility; and a
  `pyproject.toml` configuring a `uv`-compatible project with
  `torch` and `torchvision` linked against the system-provided
  CUDA libraries rather than bundled wheels.

  The principal objective is to avoid redundant CUDA library
  downloads by instructing `uv` to resolve PyTorch dependencies
  against the `micromamba`-managed system environment, thereby
  reducing image size and ensuring a consistent, auditable HPC
  software stack suitable for reproducible ML experimentation.
  
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

1. [Q:1 - Rootless Podman CUDA container with micromamba and uv](#q1)
   - see: [Rootless Podman CUDA container with micromamba and uv (Claude)](#a1-claude)
   - see: [HPC Rootless CUDA container with micromamba and uv (Gemini)](#a1-gemini)
   - see: [Reproducible CUDA Base Image for Rootless Podman (Ubuntu + Rocker) (ChatGPT)](#a1-chatgpt)
   - see: [CUDA container with micromamba and uv (Perplexity)](#a1-perplexity)
   - see: [Micromamba uv PyTorch CUDA Container Setup (DeepSeek)](#a1-deepseek)
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

## Q:1 - **Rootless Podman CUDA container with micromamba and uv**

[^](#toc)

## Role

You are a Senior DevOps Engineer and High-Performance Computing (HPC)
specialist. Your expertise lies in configuring containerized
environments for Machine Learning, specifically optimizing NVIDIA CUDA
stacks for PyTorch using `micromamba` and Astral `uv`.

## Objective

Design a robust, reproducible base container image (Ubuntu-based via
Rocker project) for rootless Podman. The primary goal is to provide a
system-wide CUDA/cuDNN/BLAS environment managed by `micromamba` that
acts as the provider for a Python project managed by `uv`.

## Technical Constraints

- **Environment:** Rootless Podman, Ubuntu-based Rocker images.
- **The "No-Home" Rule:** The `/home` directory is unavailable during
  image build and will be mounted as a volume at runtime. All
  persistent toolchains, libraries, and binaries **must** reside in
  `/usr/local` or `/opt`.
- **Privileges:** You have `root (id=0)` access during the build phase.
- **Package Management:** - Use `micromamba` for system-level CUDA, cuDNN, and NVBLAS.
  - Use `uv` for Python version management and virtual environments.
  - **Crucial:** The PyTorch installation via `uv` must utilize the
    system-provided CUDA libraries rather than downloading massive
    CUDA-bundled wheels.

## Deliverables

### 1. System-Level Setup Script (`install_cuda.sh`)

- Install `micromamba` to `/usr/local/bin`.
- Initialize a global environment in `/opt/mamba`.
- Configure environment variables (`LD_LIBRARY_PATH`, `CUDA_HOME`,
  `PATH`) so they are available to all users at runtime without
  requiring `~/.bashrc`.

### 2. Micromamba Environment Specification (`conda-env.yaml`)

- Define an environment containing: `cuda-toolkit=13.1`, `cudnn`, and `libblas`.
- Ensure compatibility for NVIDIA Driver 580+ (CTK).

### 3. Project Configuration (`pyproject.toml`)

- Configure a `uv`-compatible project.
- Specify `torch` and `torchvision` dependencies.
- Include instructions or configurations to ensure `uv` links against
  the `micromamba` system libraries.

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

[^](#toc) **_Rootless Podman CUDA container with micromamba and uv_**

## Architecture Overview

The design separates concerns into three layers:

- _System layer_: micromamba manages CUDA, cuDNN, BLAS — installed
  globally under `/opt/mamba`
- _Runtime layer_: environment variables exposed via `/etc/profile.d/`
  and `/etc/environment` for all users and non-login shells
- _Project layer_: uv manages Python and virtual environments, linking
  against system CUDA via `UV_NO_BUILD_ISOLATION` and index overrides

---

## 1. System-Level Setup Script

### `install_cuda.sh`

```bash
#!/usr/bin/env bash
# install_cuda.sh
# Installs micromamba to /usr/local/bin and bootstraps the global CUDA
# environment under /opt/mamba. Designed for rootless Podman builds
# where /home is unavailable.
set -euo pipefail

# ── Constants ────────────────────────────────────────────────────────────────
MAMBA_VERSION="2.3.0-0"
MAMBA_ARCH="linux-64"
MAMBA_INSTALL_URL="https://micro.mamba.pm/api/micromamba/${MAMBA_ARCH}/${MAMBA_VERSION}"
MAMBA_BIN="/usr/local/bin/micromamba"
MAMBA_ROOT="/opt/mamba"
ENV_NAME="cuda-base"
ENV_PREFIX="${MAMBA_ROOT}/envs/${ENV_NAME}"
CONDA_ENV_FILE="/opt/conda-env.yaml"

# ── 1. Install micromamba binary ─────────────────────────────────────────────
echo "[1/5] Downloading micromamba ${MAMBA_VERSION} (${MAMBA_ARCH})..."
curl -fsSL "${MAMBA_INSTALL_URL}" \
  | tar -xj -C /tmp --strip-components=1 bin/micromamba
install -m 0755 /tmp/micromamba "${MAMBA_BIN}"
rm -f /tmp/micromamba

# ── 2. Initialise the global mamba root ──────────────────────────────────────
echo "[2/5] Initialising MAMBA_ROOT_PREFIX at ${MAMBA_ROOT}..."
mkdir -p "${MAMBA_ROOT}"/{pkgs,envs}

# Provide a minimal .mambarc that is root-owned but world-readable.
# MAMBA_ROOT_PREFIX is exported; no ~/.bashrc manipulation required.
cat > /etc/mambarc <<'EOF'
# System-wide micromamba configuration
# No user-home dependency — compatible with rootless Podman builds.
auto_activate_base: false
always_yes: true
EOF

export MAMBA_ROOT_PREFIX="${MAMBA_ROOT}"

# ── 3. Create the CUDA environment from the spec file ────────────────────────
echo "[3/5] Creating conda environment '${ENV_NAME}' from ${CONDA_ENV_FILE}..."
"${MAMBA_BIN}" env create \
  --root-prefix "${MAMBA_ROOT}" \
  --name "${ENV_NAME}" \
  --file "${CONDA_ENV_FILE}" \
  --yes

# ── 4. Export system-wide environment variables ───────────────────────────────
echo "[4/5] Writing /etc/profile.d/cuda-base.sh ..."
cat > /etc/profile.d/cuda-base.sh <<EOF
# CUDA / micromamba system environment — sourced for all login shells.
export MAMBA_ROOT_PREFIX="${MAMBA_ROOT}"
export CONDA_ENV_PREFIX="${ENV_PREFIX}"
export CUDA_HOME="${ENV_PREFIX}"
export CUDA_ROOT="${ENV_PREFIX}"
export PATH="${ENV_PREFIX}/bin:\${PATH}"
export LD_LIBRARY_PATH="${ENV_PREFIX}/lib:${ENV_PREFIX}/lib/stubs:\${LD_LIBRARY_PATH:-}"
export NVBLAS_CONFIG_FILE="${ENV_PREFIX}/etc/nvblas.conf"
EOF
chmod 0644 /etc/profile.d/cuda-base.sh

# Write the same variables to /etc/environment for non-login, non-interactive
# shells (e.g. systemd units, container entrypoints without a login shell).
# Note: /etc/environment does not support variable expansion — paths are literal.
echo "[4/5] Writing /etc/environment entries..."
{
  echo "MAMBA_ROOT_PREFIX=${MAMBA_ROOT}"
  echo "CONDA_ENV_PREFIX=${ENV_PREFIX}"
  echo "CUDA_HOME=${ENV_PREFIX}"
  echo "CUDA_ROOT=${ENV_PREFIX}"
  # PATH prepend is not honoured by all parsers of /etc/environment;
  # the profile.d entry above is the canonical PATH source.
  echo "LD_LIBRARY_PATH=${ENV_PREFIX}/lib:${ENV_PREFIX}/lib/stubs"
  echo "NVBLAS_CONFIG_FILE=${ENV_PREFIX}/etc/nvblas.conf"
} >> /etc/environment

# ── 5. Verify the CUDA toolkit is present ────────────────────────────────────
echo "[5/5] Verifying installation..."
"${ENV_PREFIX}/bin/nvcc" --version
echo "micromamba env '${ENV_NAME}' ready at ${ENV_PREFIX}"
```

---

## 2. Micromamba Environment Specification

### `conda-env.yaml`

```yaml
# conda-env.yaml
# System-wide CUDA/cuDNN/BLAS environment managed by micromamba.
# Targets NVIDIA driver 580+ (CTK 13.x / CUDA 13.1).
# Installed to /opt/mamba/envs/cuda-base — no user-home dependency.

name: cuda-base

channels:
  - nvidia          # Primary source for CTK 13.x packages
  - conda-forge     # Fallback and cuDNN supplementary builds

dependencies:
  # ── CUDA Toolkit ────────────────────────────────────────────────────────
  # cuda-toolkit is a meta-package that pulls the compiler (nvcc),
  # runtime libraries, and development headers as a matched set.
  - cuda-toolkit=13.1

  # ── cuDNN ───────────────────────────────────────────────────────────────
  # Let the solver pin the cuDNN major version compatible with CUDA 13.1.
  # As of 2025-Q2 that resolves to cuDNN 9.x.
  - cudnn

  # ── BLAS / NVBLAS ───────────────────────────────────────────────────────
  # libblas from conda-forge provides the BLAS API; the solver will
  # select the NVBLAS implementation when the nvidia channel is present.
  - libblas=*=*nvidia   # selects the nvidia NVBLAS build string
  - libcublas           # explicit cuBLAS shared libraries

  # ── Compiler toolchain (required by nvcc at build time) ─────────────────
  - gxx_linux-64>=12

  # ── Runtime utilities ───────────────────────────────────────────────────
  - nccl               # multi-GPU collective communication
  - cuda-nvtx          # NVIDIA Tools Extension (profiling hooks)
```

---

## 3. Project Configuration

### `pyproject.toml`

```toml
# pyproject.toml
# uv-managed Python project.
# PyTorch is installed from the PyTorch +cu128 index so that only the
# thin CUDA-aware wheels are downloaded; runtime linkage is delegated
# to the system CUDA libraries in /opt/mamba/envs/cuda-base.

[project]
name = "ml-project"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
  "torch>=2.7.0",
  "torchvision>=0.22.0",
]

# ── uv configuration ─────────────────────────────────────────────────────────

[tool.uv]
# Use the PyTorch CUDA 12.8-compatible index.
# These wheels are built against CUDA 12.8 symbols but resolve shared
# libraries from LD_LIBRARY_PATH at process start — i.e. from micromamba.
# Do NOT use the default PyPI torch wheels; they bundle their own CUDA.
index-strategy = "unsafe-best-match"

[[tool.uv.index]]
name    = "pytorch-cu128"
url     = "https://download.pytorch.org/whl/cu128"
explicit = true

[tool.uv.sources]
torch       = { index = "pytorch-cu128" }
torchvision = { index = "pytorch-cu128" }

# ── Build system ─────────────────────────────────────────────────────────────

[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"
```

### Linking uv against the micromamba CUDA Libraries

Create a `.env` file at the project root (or set these in the
container `ENV` directives). _uv_ reads `.env` automatically when `uv
run` is invoked:

```dotenv
# .env — project-local environment consumed by `uv run`
# Delegates all CUDA symbol resolution to the micromamba environment.

CUDA_HOME=/opt/mamba/envs/cuda-base
CUDA_ROOT=/opt/mamba/envs/cuda-base

# Prepend mamba libs so the dynamic linker finds them before any bundled path.
LD_LIBRARY_PATH=/opt/mamba/envs/cuda-base/lib:/opt/mamba/envs/cuda-base/lib/stubs

# Instruct PyTorch to locate cuBLAS / cuDNN from CUDA_HOME, not the wheel.
TORCH_CUDA_ARCH_LIST=8.0;8.6;8.9;9.0
```

To create the virtual environment with _uv_ pointing at the system
Python (also managed by micromamba if desired, or Rocker-provided):

```bash
# Run once during image build or first container start.
# CONDA_ENV_PREFIX is exported by /etc/profile.d/cuda-base.sh
uv venv /opt/project/.venv \
  --python "${CONDA_ENV_PREFIX}/bin/python3" \
  --system-site-packages   # allow fallback to system-level C extensions

uv pip install --project /opt/project \
  --no-build-isolation \   # prevents uv from re-fetching CUDA headers
  -e .
```

---

## 4. Containerfile (Podman)

```dockerfile
# Containerfile
# Rootless Podman — Ubuntu-based Rocker image with micromamba CUDA stack.
# /home is NOT available at build time; all toolchains live under /opt or
# /usr/local.

FROM docker.io/rocker/r-ver:4.4

LABEL org.opencontainers.image.title="ml-cuda-base" \
      org.opencontainers.image.description="micromamba CUDA 13.1 + uv base" \
      org.opencontainers.image.licenses="MIT"

# ── System prerequisites ──────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      bzip2 \
      xz-utils \
      tar \
      bash \
    && rm -rf /var/lib/apt/lists/*

# ── Install uv globally ───────────────────────────────────────────────────────
# uv binary goes to /usr/local/bin — no home directory required.
RUN curl -fsSL https://astral.sh/uv/install.sh \
    | env INSTALLER_NO_MODIFY_PATH=1 UV_INSTALL_DIR=/usr/local/bin bash

# ── Copy environment spec and install script ──────────────────────────────────
COPY conda-env.yaml /opt/conda-env.yaml
COPY install_cuda.sh /opt/install_cuda.sh
RUN chmod +x /opt/install_cuda.sh && /opt/install_cuda.sh

# ── Copy project files ────────────────────────────────────────────────────────
COPY pyproject.toml /opt/project/pyproject.toml
COPY .env           /opt/project/.env

# ── Create uv virtualenv and install dependencies ─────────────────────────────
# Source profile.d first so CUDA_HOME / LD_LIBRARY_PATH are populated.
RUN bash -lc "\
    uv venv /opt/project/.venv \
      --python ${CONDA_ENV_PREFIX}/bin/python3 && \
    cd /opt/project && \
    uv sync --no-build-isolation \
  "

# ── Runtime environment ───────────────────────────────────────────────────────
# These ENV directives ensure variables reach non-login container entrypoints.
ENV MAMBA_ROOT_PREFIX=/opt/mamba \
    CONDA_ENV_PREFIX=/opt/mamba/envs/cuda-base \
    CUDA_HOME=/opt/mamba/envs/cuda-base \
    CUDA_ROOT=/opt/mamba/envs/cuda-base \
    PATH="/opt/mamba/envs/cuda-base/bin:/opt/project/.venv/bin:/usr/local/bin:${PATH}" \
    LD_LIBRARY_PATH="/opt/mamba/envs/cuda-base/lib:/opt/mamba/envs/cuda-base/lib/stubs" \
    VIRTUAL_ENV=/opt/project/.venv

WORKDIR /opt/project

# /home is mounted as a volume at runtime by the Podman invocation.
VOLUME ["/home"]

CMD ["bash", "-l"]
```

---

## Additional Notes

#### CUDA 13.1 vs PyTorch cu128 Index Mismatch

The micromamba environment installs _CUDA Toolkit 13.1_ (CTK), while the PyTorch wheel index used is `cu128`. This is _intentional_: PyTorch wheels are ABI-backwards-compatible — a `cu128`-built wheel runs against CUDA 13.x runtime libraries because CUDA maintains minor-version ABI stability. Do _not_ attempt to force a `cu130`/`cu131` index; no such public PyTorch index existed at the time of writing.

#### `/etc/environment` Limitations

`/etc/environment` is parsed by PAM (`pam_env`) and does _not_ support shell variable expansion (`${VAR}`). Every path entry must be _fully literal_. The `PATH` extension is therefore done exclusively through `/etc/profile.d/cuda-base.sh`, which is a POSIX shell script and supports `${PATH}` expansion.

#### `--system-site-packages` Trade-off

Passing `--system-site-packages` to `uv venv` allows the virtual environment to fall back to C extensions installed in the micromamba env (e.g. NumPy built against MKL). Remove this flag if strict isolation between the venv and the conda environment is required.

#### NVBLAS Configuration

`libblas=*=*nvidia` selects the NVBLAS-backed BLAS implementation. NVBLAS requires a `nvblas.conf` file; the path is exported via `NVBLAS_CONFIG_FILE`. Ensure this file exists in the image (micromamba typically places a template at `${ENV_PREFIX}/etc/nvblas.conf`); otherwise NumPy / SciPy BLAS calls will fall back silently to the CPU implementation.

#### Rootless Podman Volume Mount

At runtime, mount `/home` with:

```bash
podman run --rm -it \
  -v "${HOME}:/home/$(id -un):Z" \
  --userns=keep-id \
  ml-cuda-base:latest
```

The `:Z` label relabels the volume for SELinux; omit on non-SELinux hosts.

---

## References

[^ac-1]: micromamba installation guide — https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html
[^ac-2]: conda-forge CUDA packages and channel priority — https://conda-forge.org/docs/user/tipsandtricks/#using-cuda-in-your-package
[^ac-3]: NVIDIA conda channel (CTK 13.x) — https://anaconda.org/nvidia/cuda-toolkit
[^ac-4]: Astral uv — Python project and environment management — https://docs.astral.sh/uv/
[^ac-5]: uv index configuration (`tool.uv.index`) — https://docs.astral.sh/uv/configuration/indexes/
[^ac-6]: uv environment variables and `.env` file loading — https://docs.astral.sh/uv/configuration/environment/
[^ac-7]: PyTorch CUDA-specific wheel indexes — https://pytorch.org/get-started/locally/
[^ac-8]: Rocker Project base images (Ubuntu / R) — https://rocker-project.org/
[^ac-9]: `pam_env` and `/etc/environment` parsing rules — https://www.man7.org/linux/man-pages/man8/pam_env.8.html
[^ac-10]: Rootless Podman user namespace guide — https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
[^ac-11]: NVBLAS configuration reference — https://docs.nvidia.com/cuda/nvblas/index.html
[^ac-12]: OCI `ENV` inheritance and `/etc/profile.d` in containers — https://github.com/opencontainers/image-spec/blob/main/config.md

# A:1 (Gemini)

[^](#toc) **_HPC Rootless CUDA container with micromamba and uv_**


To build a high-performance, rootless-compatible container for Machine
Learning, we must decouple the heavy-duty CUDA toolchain from the
Python application layer. By leveraging `micromamba` in `/opt` for the
system libraries and `uv` for the virtualized Python environment, we
ensure that the container remains lean and reproducible while
respecting the constraints of HPC environments where `/home` is
volatile.


## 1\. Micromamba Environment Specification (`conda-env.yaml`)

This configuration targets the **NVIDIA** channel to obtain the
specific `cuda-toolkit` and `cudnn` versions required for
high-performance workloads. By installing these via `micromamba`, we
provide the shared objects (`.so`) that PyTorch will link against at
runtime.

```yaml
name: hpc_base
channels:
  - nvidia
  - conda-forge
dependencies:
  - python=3.11
  - cuda-toolkit=13.1
  - cudnn
  - libblas
  - libcusolver
  - magma
```

## 2\. System-Level Setup Script (`install_cuda.sh`)

This script must be executed as `root` during the `Containerfile` /
`Dockerfile` build phase. It ensures all binaries are located in
`/opt` or `/usr/local` to comply with the _No-Home_ rule.

```bash
#!/bin/bash
set -e

# Define installation paths
export MAMBA_ROOT_PREFIX=/opt/mamba
export UV_INSTALL_DIR=/usr/local/bin
export ENV_NAME=hpc_base

# 1. Install Micromamba
_msg "Installing Micromamba to /usr/local/bin..."
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj -C /usr/local/bin --strip-components=1 bin/micromamba

# 2. Create the global environment
_msg "Creating system-wide CUDA environment in ${MAMBA_ROOT_PREFIX}..."
micromamba create -y -p "${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}" -f /tmp/conda-env.yaml

# 3. Install Astral uv
_msg "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="${UV_INSTALL_DIR}" sh

# 4. Configure Global Environment Variables
# We place these in /etc/profile.d/ to ensure visibility for rootless users at login
cat <<EOF > /etc/profile.d/hpc_setup.sh
export MAMBA_ROOT_PREFIX=${MAMBA_ROOT_PREFIX}
export PATH="${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}/bin:${UV_INSTALL_DIR}:\$PATH"
export CUDA_HOME="${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}"
export LD_LIBRARY_PATH="${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}/lib:\$LD_LIBRARY_PATH"
export UV_PYTHON="${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}/bin/python"
EOF

# 5. Set permissions for rootless access
chmod -R 755 /opt/mamba
```


## 3\. Project Configuration (`pyproject.toml`)

To prevent `uv` from downloading "fat" wheels containing their own
CUDA binaries, we configure the project to use the **CPU-specialized**
or **unbundled** wheels from the PyTorch index. At runtime, the
`LD_LIBRARY_PATH` set in the previous step will force PyTorch to use
the `micromamba` system libraries.

```toml
[project]
name = "hpc-ml-project"
version = "0.1.0"
description = "HPC Optimized PyTorch Project"
requires-python = ">=3.11"
dependencies = [
    "torch",
    "torchvision",
    "numpy",
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
# We point to the CPU index for the base wheel. 
# Because our environment has the CUDA Toolkit and NVBLAS in LD_LIBRARY_PATH, 
# PyTorch will dynamically load the system-wide CUDA 13.1 libs.
torch = { index = "pytorch-cpu" }
torchvision = { index = "pytorch-cpu" }

[tool.uv]
managed = true
# Ensure uv uses the micromamba-provided python as the base for its venv
system-python = true
```


## Additional Notes /g

- **Dynamic Linking:** The key to this architecture is the
    `LD_LIBRARY_PATH`. When PyTorch (even the "CPU" version in some
    builds, or specific HPC-focused wheels) looks for `libcuda.so` or
    `libcudnn.so`, it will find the high-performance versions managed
    by `micromamba` in `/opt/mamba`.
- **Rootless Podman:** Since the `/home` directory is mounted at
    runtime, any `uv` operations performed during the build (like `uv
    sync`) must use the `--no-install-project` flag or specify a cache
    directory in `/tmp` to avoid writing to a non-existent home.
- **Rocker Compatibility:** When using Rocker, ensure you use the
    `cuda` or `user` extensions carefully. This manual setup is more
    robust because it bypasses the standard apt-based NVIDIA packages
    which often conflict with rootless overlayfs permissions.

## References /g

- [ag-1] [Micromamba Installation & Path Configuration](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
- [ag-2] [Astral uv: Environment Variables for Installation](https://www.google.com/search?q=https://docs.astral.sh/uv/configuration/environment-variables/)
- [ag-3] [PyTorch: Linker and Library Search Paths](https://pytorch.org/docs/stable/notes/cuda.html)
- [ag-4] [Podman Rootless Guide: Handling Persistent Volumes](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md)
- [ag-5] [NVIDIA Conda Channel Documentation](https://anaconda.org/nvidia/cuda-toolkit)

# A:1 (ChatGPT)

[^](#toc) **_Reproducible CUDA Base Image for Rootless Podman (Ubuntu + Rocker)_**

This design provides a **clean separation of concerns**:

- **System layer (`micromamba`)** → CUDA / cuDNN / BLAS (shared, immutable)
- **Project layer (`uv`)** → Python + PyTorch (lightweight, reproducible)
- **Filesystem constraint compliant** → everything under `/opt` or `/usr/local`
- **Rootless-ready** → no reliance on `$HOME`

---

## 1. System-Level Setup Script — `install_cuda.sh`

### Overview

- Installs `micromamba` into `/usr/local/bin`
- Creates a **global environment** in `/opt/mamba`
- Exposes CUDA toolchain system-wide via `/etc/profile.d`

### Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
MAMBA_ROOT_PREFIX="/opt/mamba"
MAMBA_BIN="/usr/local/bin/micromamba"
ENV_NAME="cuda"

# ------------------------------------------------------------------------------
# Install micromamba (static binary)
# ------------------------------------------------------------------------------
echo "[INFO] Installing micromamba..."

curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest \
  | tar -xvj -C /usr/local/bin/ --strip-components=1 bin/micromamba

chmod +x "${MAMBA_BIN}"

# ------------------------------------------------------------------------------
# Initialize root prefix (NO HOME usage)
# ------------------------------------------------------------------------------
echo "[INFO] Initializing micromamba root prefix at ${MAMBA_ROOT_PREFIX}..."

mkdir -p "${MAMBA_ROOT_PREFIX}"
"${MAMBA_BIN}" shell init -s bash -p "${MAMBA_ROOT_PREFIX}"

# ------------------------------------------------------------------------------
# Create CUDA environment
# ------------------------------------------------------------------------------
echo "[INFO] Creating CUDA environment..."

"${MAMBA_BIN}" create -y \
  -p "${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}" \
  -f /tmp/conda-env.yaml

# ------------------------------------------------------------------------------
# Global environment variables (system-wide)
# ------------------------------------------------------------------------------
echo "[INFO] Configuring global environment..."

cat <<EOF >/etc/profile.d/cuda-mamba.sh
export MAMBA_ROOT_PREFIX=${MAMBA_ROOT_PREFIX}
export MAMBA_DEFAULT_ENV=${ENV_NAME}

export CUDA_HOME=${MAMBA_ROOT_PREFIX}/envs/${ENV_NAME}
export PATH=\${CUDA_HOME}/bin:/usr/local/bin:\${PATH}
export LD_LIBRARY_PATH=\${CUDA_HOME}/lib:\${CUDA_HOME}/lib64:\${LD_LIBRARY_PATH:-}

# Optional: NVBLAS (if needed)
export LD_PRELOAD=\${CUDA_HOME}/lib/libnvblas.so:\${LD_PRELOAD:-}
EOF

chmod +x /etc/profile.d/cuda-mamba.sh

# ------------------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------------------
echo "[INFO] Cleaning micromamba caches..."
"${MAMBA_BIN}" clean -a -y

echo "[INFO] CUDA environment successfully installed."
```

---

## 2. Micromamba Environment — `conda-env.yaml`

### Design Notes

- Uses **NVIDIA + conda-forge channels**
- Targets **CUDA Toolkit 13.1**
- Compatible with **Driver ≥ 580 (CTK model)**
- Installs **shared BLAS** (OpenBLAS)

### Specification

```yaml
name: cuda
channels:
  - nvidia
  - conda-forge

dependencies:
  # CUDA stack (CTK model)
  - cuda-toolkit=13.1
  - cudnn

  # Linear algebra
  - libblas=*=*openblas
  - liblapack

  # Runtime essentials
  - libcxx
  - zlib

  # Optional but useful
  - nccl
  - cutensor

  # Debugging / validation
  - cuda-nvcc
  - cuda-cupti
```

---

## 3. Python Project Configuration — `pyproject.toml`

### Strategy

The key challenge:

> Prevent PyTorch from pulling CUDA-bundled wheels.

#### Solution

- Use **CPU / system-linked PyTorch wheels**
- Force runtime linking via:
  - `LD_LIBRARY_PATH`
  - `CUDA_HOME`
- Avoid `+cuXXX` wheels entirely

---

## `pyproject.toml` /t

```toml
[project]
name = "torch-cuda-system"
version = "0.1.0"
description = "PyTorch project using system CUDA via micromamba"
readme = "README.md"
requires-python = ">=3.11"

dependencies = [
  "torch",
  "torchvision",
]

[tool.uv]
# Use uv-managed Python but rely on system CUDA
python-preference = "managed"

# Avoid downloading CUDA wheels
index-strategy = "prefer-default"

[tool.uv.pip]
# Ensure no CUDA wheels sneak in
extra-index-url = []
```

---

### Runtime Activation Pattern

Inside container runtime:

```bash
# Ensure system CUDA is visible
source /etc/profile.d/cuda-mamba.sh

# Create uv environment (no HOME pollution required)
uv venv /opt/venvs/project

source /opt/venvs/project/bin/activate

uv pip install -e .
```

---

### Validation

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Expected:

```text
True
```

---

## 🔧 Container Integration (Rocker + Podman)

### Minimal Containerfile Sketch

```Dockerfile
FROM rocker/r2u:22.04

COPY install_cuda.sh /tmp/install_cuda.sh
COPY conda-env.yaml /tmp/conda-env.yaml

RUN bash /tmp/install_cuda.sh

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

ENV PATH="/usr/local/bin:${PATH}"
```

---

## ⚠️ Critical Design Considerations

### 1. CUDA Compatibility (CTK Model)

- CUDA 12+ uses **forward-compatible driver model**
- Requires:
  - Host driver ≥ container CUDA version

---

### 2. PyTorch Linking Behavior

PyTorch will:

- Dynamically load:

  - `libcuda.so` (host driver)
  - `libcudart.so` (your micromamba env)

✔ This design ensures:

- No duplication of CUDA runtimes
- Smaller images
- Faster builds

---

### 3. Rootless Podman GPU Access

You must run with:

```bash
podman run \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  ...
```

Or via NVIDIA Container Toolkit integration.

---

### 4. No `$HOME` Assumption

This design strictly avoids:

- `~/.bashrc`
- `~/.local`
- user-specific activation

Everything is:

- system-wide
- deterministic
- container-safe

---

## 📌 Additional Notes

### NVBLAS (Optional Acceleration Layer)

- Enabled via `LD_PRELOAD`
- Can accelerate CPU BLAS calls transparently
- Requires tuning via `nvblas.conf` (not included here)

---

### Reproducibility Tips

- Pin exact versions in `conda-env.yaml`
- Consider exporting lock file:

```bash
micromamba env export -p /opt/mamba/envs/cuda > lock.yaml
```

---

### Performance Optimization

- Add:

  - `TORCH_CUDA_ARCH_LIST`
  - `CUDA_VISIBLE_DEVICES`

- For HPC clusters:

  - integrate with SLURM + `--gpus`

---

### Future Enhancements

- Split runtime vs build images (multi-stage)
- Add `triton` for fused kernels
- Integrate `flash-attn` (requires matching CUDA)

---

## 📚 References

- [at-1] Micromamba documentation — [https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)
- [at-2] NVIDIA CUDA Compatibility — [https://docs.nvidia.com/deploy/cuda-compatibility/](https://docs.nvidia.com/deploy/cuda-compatibility/)
- [at-3] PyTorch CUDA semantics — [https://pytorch.org/docs/stable/notes/cuda.html](https://pytorch.org/docs/stable/notes/cuda.html)
- [at-4] Astral uv documentation — [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- [at-5] NVIDIA Container Toolkit — [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)
- [at-6] Conda-forge CUDA packages — [https://conda-forge.org/docs/user/tipsandtricks.html#using-cuda](https://conda-forge.org/docs/user/tipsandtricks.html#using-cuda)




# A:1 (Perplexity)

[^](#toc) **_CUDA container with micromamba and uv_**

## System-Level Setup Script

The `install_cuda.sh` script installs micromamba to `/usr/local/bin`,
creates a global environment in `/opt/mamba`, and sets system-wide
environment variables via `/etc/environment` for runtime availability
without user
shells. [github](https://github.com/mamba-org/micromamba-releases/blob/main/install.sh)

```bash
#!/bin/bash
set -e

# Install micromamba to /usr/local/bin
cd /tmp
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
mkdir -p /usr/local/bin
mv bin/micromamba /usr/local/bin/
chmod +x /usr/local/bin/micromamba
rm -rf bin

# Create global environment directory
mkdir -p /opt/mamba

# Create environment from YAML
micromamba create -p /opt/mamba -f /tmp/conda-env.yaml --yes
micromamba clean --all --yes

# Set system-wide environment variables
CUDA_HOME=/opt/mamba
MAMBA_ROOT_PREFIX=/opt/mamba
PATH="${PATH}:/opt/mamba/bin"
LD_LIBRARY_PATH="/opt/mamba/lib:${LD_LIBRARY_PATH}"

cat > /etc/environment << EOF
PATH="${PATH}"
LD_LIBRARY_PATH="${LD_LIBRARY_PATH}"
CUDA_HOME="${CUDA_HOME}"
MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX}"
EOF
```

Run this script during the Dockerfile build phase: [micromamba-docker.readthedocs](https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html)

```dockerfile
COPY install_cuda.sh /tmp/ && chmod +x /tmp/install_cuda.sh && /tmp/install_cuda.sh
```

## Micromamba Environment Specification

The `conda-env.yaml` specifies CUDA 13.1, cuDNN 9 (compatible with
NVIDIA driver 580+), and BLAS from conda-forge channels for optimal
compatibility in containerized PyTorch
workflows. [ericmjl.github](https://ericmjl.github.io/blog/2024/6/1/how-to-manage-cuda-libraries-within-conda-environments/)

```yaml
name: cuda-base
channels:
  - nvidia
  - conda-forge
dependencies:
  - cuda-toolkit=13.1
  - cudnn
  - libblas
```

This setup provides the runtime libraries (libcudart, cuBLAS, etc.)
needed by PyTorch without the full compiler toolchain, minimizing
image
size. [docs.nvidia](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)

## Project Configuration

The `pyproject.toml` defines a uv-managed Python project with PyTorch
and TorchVision, relying on system CUDA via `LD_LIBRARY_PATH` and
`CUDA_HOME` for linkage—no bundled CUDA wheels
required. [github](https://github.com/BaoNguyen6742/uv-install-torch)

```toml
[project]
name = "pytorch-project"
version = "0.1.0"
description = "PyTorch project using system CUDA"
dependencies = [
    "torch",
    "torchvision",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

To initialize: Place in project root, run `uv init --python 3.12`, `uv
add torch torchvision`, then `uv sync`. PyTorch detects system CUDA
automatically if env vars are
set. [pytorch-geometric.readthedocs](https://pytorch-geometric.readthedocs.io/en/2.4.0/install/installation.html)

## Additional Notes /p

- **Dockerfile Integration**: Base on `rocker/r-base:24.04` or
  `ubuntu:24.04` for Podman rootless compatibility. Mount `/home` at
  runtime: `podman run -v $HOME:/home
  ...`. [github](https://github.com/nuest/rodman)
- **Verification**: Post-build, test with `podman run --rm -e
  NVIDIA_VISIBLE_DEVICES=all ... python -c "import torch;
  print(torch.cuda.is_available())"` (requires host NVIDIA runtime).
- **uv Toolchain**: Install uv system-wide in Dockerfile (`curl -Ls
  https://astral.sh/uv/install.sh | sh`), or let it manage Python
  per-project with system
  libs. [docs.astral](https://docs.astral.sh/uv/guides/projects/)

## References /p

- [^ap-micromamba-install]: Micromamba installation script. [github](https://github.com/mamba-org/micromamba-releases/blob/main/install.sh)
- [^ap-conda-cuda]: Conda CUDA/cuDNN environment example. [ericmjl.github](https://ericmjl.github.io/blog/2024/6/1/how-to-manage-cuda-libraries-within-conda-environments/)
- [^ap-nvidia-cuda13]: CUDA 13.1 driver compatibility. [ssojet](https://ssojet.com/news/cuda-toolkit-131-release-notes-and-advanced-technical-insights)
- [^ap-rocker-podman]: Rocker with rootless Podman. [rocker-project](https://rocker-project.org/use/rootless-podman.html)
- [^ap-uv-projects]: uv pyproject.toml guide. [docs.astral](https://docs.astral.sh/uv/guides/projects/)
- [^ap-pytorch-env]: PyTorch system CUDA detection. [pytorch-geometric.readthedocs](https://pytorch-geometric.readthedocs.io/en/2.4.0/install/installation.html)

> Best Podman flags for rootless CUDA ML containers ?
> YES.

Podman rootless mode excels for secure ML CUDA workloads by avoiding
privileged access while enabling GPU passthrough. Key flags ensure
device visibility, user ID mapping, and volume handling without
compromising
isolation. [redhat](https://www.redhat.com/en/blog/user-flag-rootless-containers)

## Essential Flags

Use these core flags for NVIDIA CUDA in rootless containers.

- `--userns=keep-id`: Maps host UID/GID inside container, vital for
  shared home volumes and avoiding permission issues in HPC/ML
  setups. [github](https://github.com/NousResearch/hermes-agent/issues/4084)
- `--device nvidia.com/gpu=all`: Passes all GPUs; use
  `nvidia.com/gpu=0` for specific ones. Requires NVIDIA Container
  Toolkit (nvidia-ctk) for CDI
  specs. [oneuptime](https://oneuptime.com/blog/post/2026-03-18-use-gpu-passthrough-podman/view)
- `--security-opt=label=disable`: Bypasses SELinux labeling conflicts
  common in rootless GPU
  access. [reddit](https://www.reddit.com/r/podman/comments/g717xb/catch_22_mounting_volumes_while_running_rootless/)
- `-v /home:/home`: Mounts user home for persistence, respecting
  no-home build
  rule. [reddit](https://www.reddit.com/r/podman/comments/g717xb/catch_22_mounting_volumes_while_running_rootless/)

## Full Command Example

```bash
podman run --rm \
  --userns=keep-id \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  -v $HOME:/home \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e CUDA_VISIBLE_DEVICES=0 \
  your-image:latest \
  python your_ml_script.py
```

This setup verifies CUDA with `nvidia-smi` or
`torch.cuda.is_available()`. Add `--network=host` for multi-GPU comms
like
NCCL. [forums.developer.nvidia](https://forums.developer.nvidia.com/t/rootless-podman-container-cuda-operation-not-supported-error-code-801/303699)

## Advanced Optimizations

- `--gpus all`: Podman 4.4+ alias for device passthrough if toolkit installed. [forums.docker](https://forums.docker.com/t/docker-fails-to-launch-gpu-containers-with-nvidia-runtime-but-podman-works/147966)
- `--volume /dev/shm:/dev/shm`: Shares host SHM for PyTorch DataLoader efficiency.
- For MPI/Cray: `--mpi` or `--cuda-mpi` in HPC envs like NERSC. [docs.nersc](https://docs.nersc.gov/development/containers/podman-hpc/overview/)

- [^ap-podman-rootless]: Podman rootless GPU best practices. [redhat](https://www.redhat.com/en/blog/user-flag-rootless-containers)
- [^ap-nvidia-podman]: NVIDIA device passthrough in Podman. [oneuptime](https://oneuptime.com/blog/post/2026-03-18-use-gpu-passthrough-podman/view)
- [^ap-hpc-podman]: HPC Podman GPU flags. [docs.nersc](https://docs.nersc.gov/development/containers/podman-hpc/overview/)


# A:1 (DeepSeek)

[^](#toc) **_Micromamba uv PyTorch CUDA Container Setup_**

I'll provide a complete container environment that integrates
`micromamba` and `uv` for GPU-accelerated PyTorch workloads in
rootless Podman.

## 1. System-Level Setup Script /d

The script below installs `micromamba` system-wide, creates a global
CUDA/cuDNN environment in `/opt/mamba`, and configures environment
variables accessible to all users without requiring `~/.bashrc`.

```bash
#!/bin/bash
# install_cuda.sh - System-wide micromamba setup for CUDA/cuDNN/BLAS
# Target environment: Ubuntu-based Rocker image, rootless Podman
# All artifacts placed in /usr/local or /opt (no /home dependencies)

set -euo pipefail

# ------------------------------------------------------------------------------
# 1. Install micromamba to /usr/local/bin
# ------------------------------------------------------------------------------
echo "[INFO] Installing micromamba..."
cd /tmp
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
mv bin/micromamba /usr/local/bin/
rm -rf bin
chmod 755 /usr/local/bin/micromamba

# ------------------------------------------------------------------------------
# 2. Initialize global environment root prefix
# ------------------------------------------------------------------------------
export MAMBA_ROOT_PREFIX=/opt/mamba
export PATH="/usr/local/bin:$PATH"

# Create root prefix directory
mkdir -p "$MAMBA_ROOT_PREFIX"

# Initialize shell integration (for root user only; container runtime will handle activation)
micromamba shell init --root-prefix="$MAMBA_ROOT_PREFIX" --shell=bash

# ------------------------------------------------------------------------------
# 3. Create global CUDA/cuDNN environment using provided conda-env.yaml
# ------------------------------------------------------------------------------
echo "[INFO] Creating global CUDA environment..."
cp /tmp/conda-env.yaml /tmp/conda-env.yaml
micromamba create -f /tmp/conda-env.yaml -y

# ------------------------------------------------------------------------------
# 4. Configure persistent environment variables (available at runtime)
# ------------------------------------------------------------------------------
# Create profile.d script that sets environment variables for all users
cat > /etc/profile.d/mamba-cuda.sh << 'EOF'
#!/bin/bash
# System-wide environment variables for micromamba CUDA environment
# This file is sourced by all interactive shells (bash)

# Root prefix for micromamba
export MAMBA_ROOT_PREFIX=/opt/mamba

# Add micromamba bin directory to PATH
export PATH="$MAMBA_ROOT_PREFIX/bin:$PATH"

# CUDA environment variables
export CUDA_HOME="$MAMBA_ROOT_PREFIX/envs/cuda-env"
export CUDA_PATH="$CUDA_HOME"
export CUDA_ROOT="$CUDA_HOME"

# Library path for dynamic linking (critical for uv PyTorch linking)
export LD_LIBRARY_PATH="$CUDA_HOME/lib:$CUDA_HOME/lib64:$MAMBA_ROOT_PREFIX/envs/cuda-env/lib:$LD_LIBRARY_PATH"

# Additional paths for binaries
export PATH="$CUDA_HOME/bin:$PATH"

# Micromamba environment activation
# Activate the cuda-env environment for all processes
if [ -f "$MAMBA_ROOT_PREFIX/envs/cuda-env/bin/activate" ]; then
    eval "$(micromamba shell hook --shell=bash)"
    micromamba activate cuda-env
fi
EOF

chmod 644 /etc/profile.d/mamba-cuda.sh

# Also create an ld.so.conf.d entry for system-wide library discovery
cat > /etc/ld.so.conf.d/cuda-mamba.conf << EOF
$MAMBA_ROOT_PREFIX/envs/cuda-env/lib
$MAMBA_ROOT_PREFIX/envs/cuda-env/lib64
EOF
ldconfig

# ------------------------------------------------------------------------------
# 5. Install uv
# ------------------------------------------------------------------------------
echo "[INFO] Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
# Move uv to system location
mv /root/.cargo/bin/uv /usr/local/bin/
mv /root/.cargo/bin/uvx /usr/local/bin/
rm -rf /root/.cargo
chmod 755 /usr/local/bin/uv /usr/local/bin/uvx

# Configure uv to use system site packages for CUDA libraries
mkdir -p /etc/uv
cat > /etc/uv/uv.toml << 'EOF'
[pip]
index-url = "https://pypi.org/simple"
extra-index-url = [
    "https://download.pytorch.org/whl/cu131",
]

[build]
system-site-packages = true
EOF

# ------------------------------------------------------------------------------
# 6. Validation checks
# ------------------------------------------------------------------------------
echo "[INFO] Validating installation..."
micromamba --version
uv --version
test -f "$MAMBA_ROOT_PREFIX/envs/cuda-env/bin/activate" || { echo "ERROR: cuda-env activation script not found"; exit 1; }

# Verify CUDA libraries are present
ls -la "$MAMBA_ROOT_PREFIX/envs/cuda-env/lib/libcuda.so"* || echo "WARNING: libcuda.so not found (expected if driver not mounted)"
ls -la "$MAMBA_ROOT_PREFIX/envs/cuda-env/lib/libcudnn.so"* || echo "WARNING: libcudnn.so not found"

echo "[INFO] Installation complete."
```

## 2. Micromamba Environment Specification /d

Save this as `conda-env.yaml` and place it alongside the installation script.

```yaml
# conda-env.yaml
# Micromamba environment specification for CUDA 13.1 with cuDNN and BLAS
# Compatible with NVIDIA Driver 580+ (r580 series)

name: cuda-env
channels:
  - conda-forge
  - nodefaults
dependencies:
  # CUDA Toolkit 13.1 - fully ABI-compatible with NVIDIA r580 series drivers[reference:0]
  - cuda-toolkit =13.1
  # cuDNN - deep neural network acceleration library
  - cudnn =9.10.1.4
  # BLAS (OpenBLAS backend) - optimized linear algebra
  - libblas =3.9.0
  # OpenMP runtime (required by OpenBLAS threading)
  - libgomp
  # Helper utilities
  - curl
  - ca-certificates
  # (Optional) Python - uv will install its own; this ensures system has base python3
  - python =3.12
```

## 3. Project Configuration (`pyproject.toml`) /d

This configuration ensures `uv` installs PyTorch that links against
the system-provided CUDA libraries from `micromamba`, rather than
downloading bundled CUDA wheels.

```toml
[project]
name = "my-pytorch-project"
version = "0.1.0"
description = "PyTorch project using system CUDA libraries"
requires-python = ">=3.12,<3.13"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "torch>=2.5.0",
    "torchvision>=0.20.0",
]

# Use PyTorch's CUDA 13.1 wheel index
# The +cu131 suffix indicates CUDA 13.1 variant
[[tool.uv.index]]
name = "pytorch-cu131"
url = "https://download.pytorch.org/whl/cu131"
explicit = true

[tool.uv.sources]
torch = {index = "pytorch-cu131"}
torchvision = {index = "pytorch-cu131"}

# Ensure uv uses system site packages to access micromamba's CUDA libraries
[tool.uv]
system-site-packages = true

# Build configuration to link against system libraries
[tool.uv.build]
no-binary-packages = []

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

# Optional: Customize PyTorch build to use system libraries
[tool.setuptools]
packages = ["src"]

[project.scripts]
train = "my_package.cli:train"
infer = "my_package.cli:infer"
```

**Key points for this configuration:**

- `explicit = true` ensures the PyTorch index is only used for `torch`
  and `torchvision`, not for other dependencies[reference:1].
- `system-site-packages = true` allows the Python environment to
  access system (micromamba) libraries at
  `/opt/mamba/envs/cuda-env/lib`[reference:2].
- The PyTorch wheel variant `+cu131` corresponds to CUDA 13.1,
  matching the conda environment.

## Additional Notes /d

### Runtime Requirements

When running the container with rootless Podman, ensure:

1. **NVIDIA Container Toolkit** is installed on the host and configured for rootless mode[reference:3].
2. **CDI (Container Device Interface)** is enabled for seamless GPU access in rootless containers[reference:4].
3. Run container with appropriate GPU flags:

   ```bash
   podman run --rm -it --device nvidia.com/gpu=all --security-opt label=disable \
     -v /home/user/project:/workspace my-pytorch-image
   ```

### CUDA Compatibility

CUDA Toolkit 13.1 is fully ABI-compatible with NVIDIA r580 series
drivers (version 580.95.05+). No driver is installed inside the
container; the host's NVIDIA driver provides the kernel modules, while
CUDA user-space libraries come from the conda
environment[reference:5].

### Verification Steps

After building the container, verify the setup:

```bash
# Activate environment and check CUDA availability
micromamba activate cuda-env
python -c "import torch; print(torch.cuda.is_available()); print(torch.version.cuda)"
```

Expected output: `True` and `13.1` (or compatible version).

### Security Considerations

- The profile.d script sources environment variables for **all**
  interactive users. In containerized environments, this is typically
  acceptable as containers are single-purpose.
- `system-site-packages = true` allows the Python environment to
  access all system libraries; ensure only trusted packages are
  installed.

## References /d

- ad-1 [NVIDIA CUDA Toolkit Documentation - Compatibility Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#compatibility)
- ad-2 [micromamba Installation Guide](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)
- ad-3 [Using uv with PyTorch - Official Documentation](https://docs.astral.sh/uv/guides/integration/pytorch/)
- ad-4 [NVIDIA Container Toolkit for Podman](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- ad-5 [conda-forge cuda-toolkit feedstock](https://github.com/conda-forge/cuda-toolkit-feedstock)
- ad-6 [conda-forge cudnn feedstock](https://github.com/conda-forge/cudnn-feedstock)
- ad-7 [conda-forge libblas](https://anaconda.org/conda-forge/libblas)


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
