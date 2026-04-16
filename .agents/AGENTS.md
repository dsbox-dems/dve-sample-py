# AGENTS instructions

<!-- markdownlint-disable MD013 -->

## Environment

- Language Tools: assume installed under user home and in path:
  - `uv`
  - `uvx`
  - `npm`
  - `npx`
- Language Tools: assume installed under project virtual environment (`uv` or `yarn`)
  - `python`
  - `ruff`
  - `pyright`
  - `jupyter`
  - `jlpm` (yarn)
- System Utilities
  - all `coreutils`: `cat`, `grep`, `awk`, `find`, `sed`, `cut`, ...
  - basic `perl`
  - rust utilities: `rg` (rip-grep), `fdfind`, `exa`
  - network tools: `curl`, `wget`, `ftp`, `scp`
  - misc tools: `markdownlint-cli2`, `jq`, `yq`
  
- **Never run pytest, python, pyright, ruff, yarn commands directly on the host**: always use `uv`
  
## Commands

- **Run a single test:** `uv run pytest path/to/test.py::TestClass::test_method -xvs`
- **Run a test file:** `uv run  pytest path/to/test.py -xvs`
- **Run all tests in package:** `uv run pytest path/to/package -xvs`
- **Run a Python script:** `uv run python dev/my_script.py`
- **Run Jupyter CLI:** `uv run jupyter --notebook-dir=notebooks --no-browser`
- **Type-check:** `uv run pyright path/to/code`
- **Lint with ruff only:** `uv run ruff --check`
- **Format with ruff only:** `uv run ruff --format`
- **Install Python Packages with:** `uv lock && uv sync --all-extras --all-groups`
- **Install Node modules with:** `uv run jlpm up && uv run jlpm install`
- **Run manual (slower) checks:** `prek run --from-ref <target_branch> --stage manual`
- **Build docs:** `bash ./build.sh docs`

## Project Scopes

- Project scope is data-science and statistics reserch experiments.
- Mixed language project (Python, R, Javascript, Markdown)
- Two runtime contexts: "Native" and "containerized" ("rootless" `podman`)
- Virtual environments: `uv` for Python, `renv` (explicit) for R, `jlpm` (yarn) for Javascript (Jupyter lab)

## Project Directories

### Mixed Language support

#### Python language

**Important**: To be considered for Python development

- `src/`: Python application code
- `src/*/cli/__main__.py`: main appliction CLI entrypoint (in `pyproject.toml`, `[project.scripts]`)
- `src/*/scripts`: alternative scripts entrypoints (in `pyproject.toml`, `[project.scripts]`)
- `src/vce`: library of utility functions
- `notebooks/`: `jupyter` notebooks
- `tests/pytest/`: `pytest` unit tests
- `doc`: sphinx documantation in `*.rst` format
- `pyproject.toml/`: `uv` based, PEP 621 compliant, Python project definition
- `.venv/`, `.venv.cdk/`: `uv` virual environments (native and containerized), to be ignored

#### R language

**Important**: To be considered for R development

- `R/`: R package functions
- `exec/`: R executable scripts
- `etc/R/Makevars`: mapped as `~/.R/Makevars` in containers
- `man/`: R generated documentation
- `vignettes/`: R vignettes
- `tests/testthat/`: R unit tests for `testthat` execution.
- `renv/`: renv configuration
- `DESCRIPTION`: R package description

#### Javascript (node-js) language

**Important**: Used for Jupyter-lab runtime, To be considered also for skill scripts

- `package.json`: jupyter lab (and optionally SKILLS scripts) module dependencies
- `.yarnrc.yml`: `jlpm` (yarn) configuration

### Containerization

**Important**: **Exclusively** used for `podman` / `docker` image
building and container execution (Dockerfiles), container scripts, and
compose specifications. Do not mix application logic here.

- `docker/`: base directory for all containerization support
- `docker/r-image`: default image definition
- `docker/r-image/dockerfiles`: OCI Compliant image dokerfiles
- `docker/r-image/mamba`: micromamba environment for CUDA installation
- `docker/r-image/scripts`: image setup scripts
- `docker/r-image/scripts/setup`: post image runtime setup on persistent mounted volume (under `home/`)
- `docker/r-image/*.conf`: built time/runtime customization
- `docker/r-image/Makefile`: main `podman` interface, invoked by root `Makefile` by `build.sh` and `runtime.sh` scripts

### Working Directories

**Important**: Excluded in `.gitignore`, can be used if needed

- `data/`: Local storage for datasets (Python Layout)
- `inst/extdata/ext`: Local storage for datasets (R Layout)
- `temp/`: temporary data.
- `logs/`: Loglife destination

### Ignored Directories

**Important**: Ignone all other non-versioned files following `.gitignore`

- `home/`: Never access this directory for security reasons.
- `.venv*/`: python virtual environents (`uv venv`)
- `node_modules/`: node installed modules (Jupyter)

### Documentation

#### Internal Documentation

- `notes/`: base directory for all internal documentation

##### AI Generated Documents

**Important**: In valid GLFM markdown, sometimes translated in PDF form

- `notes/agents/`: directory for agent generated documentation (**USE THIS FOT GENERATED DOCS**)
- `notes/howtos/`: directory for saved LLM queries, for analysis and project usage

##### Manual Edited Documents

- `notes/custom/`: emacs `org-mode` customization source for project cloning
- `notes/ref/`: for bibliograpy in BibLaTeX format
- `notes/nat/`: for `denote` emacs annotations in `org-mode` format
- `notes/setup/`: initial python toolchain setup
- `notes/samples/`: dorectory for additiona code samples and optional features
- `notes/styles/`: directory for pandoc markdown to PDF rendering pipeline

#### Public Project Documentation

- `doc/`: sphinx documantation in `*.rst` format
- `man/`: generated documentation for R functions
- `vignettes/`: R documentation in `knitr` format

#### Public Project Reference

- `CITATION.cff`: project and related papers references

## Project Scripts

Project script logic is implemented in:

- `Makefile`: root command interface
- `docker/r-image`: `podman` command implementation

### Build Commands

- `build.sh`: (see `--help` output) build commands interface

### Container Image Build

- `build.sh setup`: initial image creation
- `build.sh update`: update images
- `build.sh upgrade`: remove `uv.lock` and `renv.lock` to force package upgrade
- `build.sh full`: after a `build.sh setup`, invoke `runtime.sh` for virtuual environment installation in persistent volume (mapped under `home/`) directory

### Native/Containerized Project build commands

- `build.sh build`: project build  (Python/R)
- `build.sh test`: run project tests  (Python/R)
- `build.sh check`: run project linters and checks  (Python/R)
- `build.sh docs`: generate project documentation  (Python/R)

### Containerized Only Runtime Commands

- `runtime.sh`: (see `--help` output) container runtime control interface

### Initial Setup Commands

- `runtime.sh environment`:import `~/.config` and `ssh` keys in mapped home (`home/user/`) inside a container
- `runtime.sh setup`: runs `setup.sh`, inside a container, to initialize and populate virtual environments

### Interactive Commands

- `runtime.sh sh`: run interactive `bash` inside a container via `uv run bash`
- `runtime.sh python|R`: `ipython`, `R` repl
- `runtime.sh term|xterm`: attach interactive term or `xterm` to running container

### Batch Commands

- `runtime.sh pyrun`: runns `uv run python` with the arguments
- `runtime.sh rs`: runns `uv run Rscript` with the arguments

### Wrapper Commands

- `runtime.sh build|test|check`: wraps equivalent `build.sh` or `setup.sh` command executed inside a container

### Server Commands

- `runtime.sh rstudio`: runs `rstudio-server`, forwarding ports at `28787`
- `runtime.sh lab|notebook`: runs `jupyterr`, forwarding ports at `28888`

### IDE Commands

- `runtime.sh code`: runs `code-server`, inside a container
- `runtime.sh cursor`: runs `cursor`, inside a container, with `X-Window` support
- `runtime.sh antigravity`: runs `antigravity`, inside a container, with `X-Window` support

## Coding Standards

- **Always format and check Python files with ruff immediately after
  writing or editing them:
  - `uv run ruff format <file_path>`
  - `uv run ruff check --fix <file_path>`
  Do this for every Python file you create or modify, before moving on to the next step.
- Invoke static type checking code with `uv run pyright <file_path>`
- Imports at top of file. Valid exceptions: circular imports, lazy loading for worker isolation, `TYPE_CHECKING` blocks.
- see `/python-code-style` for python formatting

## Testing Standards

- Add tests for new behavior — cover success, failure, and edge cases.
- Use pytest patterns, not `unittest.TestCase`.
- Use `spec`/`autospec` when mocking.
- Use `@pytest.mark.parametrize` for multiple similar inputs.
- Use `@pytest.mark.db_test` for tests that require database access.
- Test fixtures: `/test/pytest/dve/tests/pytest_plugin.py`.

## Commits and PRs

Write commit messages focused on user impact, not implementation details.

- **Good:** `Fix airflow dags test command failure without serialized Dags`
- **Good:** `UI: Fix Grid view not refreshing after task actions`
- **Bad:** `Initialize DAG bundles in CLI get_dag function`

## Boundaries

- **Ask first**
  - Large cross-package refactors.
  - New dependencies with broad impact.
  - Destructive data or migration changes.
- **Never**
  - Commit secrets, credentials, or tokens.
  - Edit generated files by hand when a generation workflow exists.
  - Use destructive git operations unless explicitly requested.
