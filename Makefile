##
#{{{ Makefile: project global/standard actions
#
# @see: ./notes/usage/readme.md for usage info
#
#}}} \\\


#{{{ [ VARS.* ] /////////////////////////////////////////////////////////////////



# ---(base)------------------------------------------------

ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))


# ---(project)------------------------------------------------

PACKAGE := $(shell ls src | grep -v -e egg -e '\.py$$' | head -n 1)
PYMODULE ?= ${PACKAGE}

SRC := 'src'
TESTS := 'tests'

# ---(IMAGES)------------------------------------------------

IMG_MAKE_DIR ?= 'docker/r-images'


# ---(DOCS)------------------------------------------------

DOC_MAKE_DIR ?= 'doc'


# ---(paths)------------------------------------------------

LOGS_DIR ?= ${ROOT_DIR}/logs
TEMP_DIR ?= ${ROOT_DIR}/temp

BUILD_DIRS = ${TEMP_DIR} ${LOGS_DIR}
CLEAN_DIRS = ${TEMP_DIR}

# ---(progs)------------------------------------------------

SHELL := /bin/bash
#POETRY := poetry
POETRY := $(shell command -v poetry 2> /dev/null)
PY_RUN := ${POETRY} run


#}}} \\\

#{{{ [ COMMANDS.* ] /////////////////////////////////////////////////////////////////

# ---(commands)------------------------------------------------

.PHONY: all test check docs man vignettes readme format build install clean init


all: # @HELP/base make: "init,check,test,docs,build"  targets
all: init check test docs build

test: # @HELP/base runs: `devtools::test()`
test: init
	${PY_RUN} pytest


check: # @HELP/base runs: mypy, pflake8, pylint
check: init
	@echo "+++ {{{ CHECK /////////";
	@echo "+++ Running Poetry Check..."; $(POETRY) check || true
	@echo "+++ Running Mypy..."; $(POETRY) run mypy $(SRC) $(TESTS) || true
	@echo "+++ Running Flake8..."; $(POETRY) run pflake8  || true # This is not a typo
	@echo "+++ Running Pylint..."; $(POETRY) run pylint $(SRC) || true
	@echo "+++ }}} CHECK \\\\\\\\\ ";

docs: # @HELP/base make: "man,readme,vignettes"  targets
docs: man readme vignettes

man: # @HELP/base runs: make sphinx
man: init
	cd ${DOC_MAKE_DIR} && $(MAKE) $@

vignettes: # @HELP/base runs: `devtools::build_vignettes()`
vignettes: 
	cd ${DOC_MAKE_DIR} && $(MAKE) $@

README.rst: 

readme: # @HELP/base runs: `knitr::knit("README.Rmd")` 
readme: README.rst

format: # @HELP/baseformat code with black
format: 
	${POETRY} run black $(SRC) $(TESTS)



#requirements: .requirements.txt
#env: .venv/bin/activate
#.requirements.txt: requirements.txt
#	$(shell . .venv/bin/activate && pip install -r requirements.txt)
#.PHONY: update
#update: env
#	.venv/bin/python3 -m pip install -U pip
#	poetry update
#	poetry export -f requirements.txt --output requirements.txt --without-hashes
#.PHONY: format
#format: env
#	$(shell . .venv/bin/activate && isort ./)
#	$(shell . .venv/bin/activate && black ./)


build: # @HELP/base runs: `devtools::build()`
build: 
	${POETRY} build

install: # @HELP/base runs: `devtools::install()`
install:
	${RSCRIPT} -e 'devtools::install()'

uninstall: # @HELP/base runs: `devtools::uninstall()`
uninstall:
	${RSCRIPT} -e 'devtools::uninstall()'

clean: # @HELP/base clean all files in .gitignore
	@echo "+++ {{{ CLEAN /////////";
	@echo "+++ Running  py3clean..."; $(POETRY) run py3clean -v $(SRC) $(TESTS) || true
	@echo "+++ Cleaning pytest cache..."; [ -d .pytest_cache ] && rm -rf .pytest_cache || true
	@echo "+++ NOT Cleaning build, dist ..."; echo "rm -rf ./build ./dist"  || true
	@echo "+++ NOT Running git clean ..."; echo "git clean -Xdf"  || true
	@echo "+++ }}} CLEAN \\\\\\\\\ ";



init: # @HELP/base initialize local (temp,logs) directories
	@mkdir -p ${LOGS_DIR}
	@mkdir -p ${TEMP_DIR}

#}}} \\\

#{{{ [ CUSTOMIZATION.* ] /////////////////////////////////////////////////////////////////

# ---(custom)------------------------------------------------

.PHONY: custom custom-help

custom: # @HELP/custom runs: ./etc/custom/custom.sh for initial project customization
custom: init
	bash ./etc/custom/custom.sh

custom-help: help/custom

#}}} \\\

#{{{ [ ENVIRONMENT.* ] /////////////////////////////////////////////////////////////////

# ---(build)------------------------------------------------

.PHONY: setup prepare update upgrade build-help

prepare: init

setup: # @HELP/build initial build of all podman images
setup:  init prepare build-setup build-validate

update: # @HELP/build rebuild of modified podman images
update: init prepare build-update

upgrade: # @HELP/build fresh rebuild of all podman images (pull)
update: init prepare build-upgrade

build-help: help/build

#}}} \\\

#{{{ [ CONTAINERS.* ] /////////////////////////////////////////////////////////////////

# ---(images)------------------------------------------------

.PHONY: build-setup build-update build-upgrade

build-setup:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

build-update:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

build-upgrade:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@


# ---(inner check)------------------------------------------------

.PHONY: build-validate

build-validate:
	./runtime.sh build all


# ---(run)------------------------------------------------

.PHONY: runtime-repl runtime-cli runtime-shell runtime-build runtime-command runtime-term runtime-rstudio runtime-help

runtime-repl: # @HELP/runtime ...
runtime-repl:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

runtime-cli: # @HELP/runtime ...
runtime-cli:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

runtime-shell: # @HELP/runtime ...
runtime-shell:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

runtime-build: # @HELP/runtime ...
runtime-build:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

runtime-command: # @HELP/runtime ...
runtime-command:
	@cd ${IMG_MAKE_DIR} && $(MAKE) --silent $@

runtime-term: # @HELP/runtime ...
runtime-term:
	@cd ${IMG_MAKE_DIR} && $(MAKE) --silent $@

runtime-rstudio: # @HELP/runtime ...
runtime-rstudio:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

runtime-help: help/runtime

# ---(worker)------------------------------------------------

.PHONY: worker-pack worker-push worker-pull
.PHONY: worker-make worker-test worker-check worker-docs
.PHONY: worker-build worker-install
.PHONY: worker-exec worker-shell

worker-pack: # @HELP/worker ...
worker-pack:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-push: # @HELP/worker ...
worker-push:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-pull: # @HELP/worker ...
worker-pull:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-make: # @HELP/worker ...
worker-make:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-test: # @HELP/worker ...
worker-test:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-check: # @HELP/worker ...
worker-check:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-docs: # @HELP/worker ...
worker-docs:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-build: # @HELP/worker ...
worker-build:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-install: # @HELP/worker ...
worker-install:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-exec: # @HELP/worker ...
worker-exec:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-shell: # @HELP/worker ...
worker-shell:
	cd ${IMG_MAKE_DIR} && $(MAKE) $@

worker-help:  help/worker

#}}} \\\

#{{{ [ UTILS.* ] /////////////////////////////////////////////////////////////////

# ---(debug)------------------------------------------------

.PHONY: print-%

# Display the value.
# ex. $ make print-REPORT_SOURCE_DIR
# ex. $ make print-IMAGE_REVISION
print-%:
	@echo $* = $($*)

# ---(help)------------------------------------------------

.PHONY: help help%

help/%:
	@echo "NOTE: Use BUILDARCH/BUILDOS variables to override OS/ARCH"
	@echo
	@echo "VARIABLES:"
	@echo "  BINS = $(BINS)"
	@echo "  OS = $(OS)"
	@echo "  ARCH = $(ARCH)"
	@echo "  REGISTRY = $(REGISTRY)"
	@echo "  HOSTARCH = $(HOSTARCH)"
	@echo
	@echo "TARGETS:"
	@grep -E '^.*: *# *@HELP/$*' $(MAKEFILE_LIST) \
	    | awk '                                   \
	        BEGIN {FS = ": *# *@HELP/$*"};        \
	        { sub(/$*-/,"",$$1); printf "  %-30s %s\n", $$1, $$2 };  \
	    '

help: # @HELP/base prints this message
help:  help/base help/build 


#}}} \\\
# vim: set foldmethod=marker :
