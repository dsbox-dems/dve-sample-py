---
trigger: always_on
---

# Project Scopes and Directories

This project enforces strict directory scoping to maintain a clean architecture:

* `src/`: Main Python application logic and modules (e.g. `dve`, `vce`). Do not put container resources or large data files here.
* `tests/pytest/`: Testing structures. Unit and integration tests must mirror the layout of `src/`.
* `docker/`: **Exclusively** used for `podman` / `docker` image building (Dockerfiles), container scripts, and compose specifications. Do not mix Python runtime or build logic here.
* `notebooks/`: Jupyter data science analysis and `.ipynb` experimentation.
* `data/`: Local storage for datasets (should remain ignored in `.gitignore`).

**Important**: When instructed to write containers or Podman-specific assets, operate solely inside `docker/`. When creating standard Python features, stick to `src/`.

## Ignored Directories

**Important**: Ignone all non-versioned files following `.gitignore`
 
* `home/`: Never access this directory for security reasons.
* `.venv*/`: python virtual environents
* `node_modules/`: node installed modules


## Documentation

### Internal Documentation

* `notes/`: base directory for all internal documentation


#### AI Generated Documents

**Important**: In valid GLFM markdown, sometimes in translated in PDF form

* `notes/agents/`: directory for agent generated documentation (**USE THIS FOT GENERATED DOCS**)
* `notes/howtos/`: directory for saved LLM queries, for analysis and project usage 

#### Manual Edited Documents

* `notes/custom/`: emacs `org-mode` customization source for project cloning
* `notes/ref/`: for bibliograpy in BibLaTeX format
* `notes/nat/`: for `denote` emacs annotations in `org-mode` format
* `notes/setup/`: initial python toolchain setup
* `notes/samples/`: dorectory for additiona code samples and optional features
* `notes/styles/`: directory for pandoc markdown to PDF rendering pipeline

### Public Project Documentation

* `doc/`: sphinx documantation in `*.rst` format
* `man/`: generated documentation for R functions
* `vignettes/`: R documentation in `knitr` format

### Public Project Reference

* `CITATION.cff`: project and related papers references



## Mixed Language support

### R language

**Important**: To be considered only for explicit R reference

* `R/`: R package functions
* `exec/`: R executable scripts
* `man/`: R generated documentation
* `vignettes/`: R vignettes
* `tests/testthat/`: R unit tests for `testthat` execution.
* `renv/`: renv configuration
* `DESCRIPTION`: R package description

### Javascript (node-js) language

**Important**: Used for Jupyter-lab runtime, To be considered also for skill scripts

* `package.json`: node (npm/yarn) module dependencies
* `node_modules/`: node-js module environment. To be ignored


