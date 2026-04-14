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
