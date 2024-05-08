---
title: python setup
subtitle: install pyenv, pipenv, pipx, ipython, jupyter, cookiecutter
author: gp
date: 15/06/2021
---




REFERENCES
==========

* [Python Packages](https://py-pkgs.org/)
* [Poetry](https://python-poetry.org/)
* [Pipenv: Python Dev Workflow for Human](https://pipenv.pypa.io/en/latest/)
* [Installing Pythons with PyEnv](https://medium.com/@Joachim8675309/installing-pythons-with-pyenv-54cca2196cd3)
* [Managing Multiple Python Versions With pyenv](https://realpython.com/intro-to-pyenv/)
* [What Are Python Wheels and Why Should You Care?](https://realpython.com/python-wheels/)
* [Python on Wheels](https://lucumr.pocoo.org/2014/1/27/python-on-wheels/)
* [Poetry PyCharm Plugin](https://plugins.jetbrains.com/plugin/14307-poetry)
* [VS Code Python Tooling Gets 'Most Requested' Feature: Poetry Support](https://visualstudiomagazine.com/articles/2021/04/20/vscode-python-421.aspx)
* [Python projects with Poetry and VSCode](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1/)
* [Python Environment](https://xkcd.com/1987/)

PYENV
=====

Build Dependencies
------------------

```
# python build-deps

sudo apt install -y \
    make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

```

Install
-------

```

# ===( install )===========================

[ -d ~/.pyenv ] || curl https://pyenv.run | bash
( cd ~/.pyenv   && git  pull )


# ===( profile )===========================

#WARN: source ~/.bashrc at end

cat >> ~/.profile <<\EOF
#!/bin/sh
# -*- mode: shell-script;-*-
export PY_RC_PROFILE=1

##
#  pyenv environment
#
if [ ! -f ~/.py-env.off ]; then
if [ -d $HOME/.pyenv ]; then    
    export PY_RC_ENV=1
py_rc_env_sh() {
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
}
py_rc_env_sh
fi
fi

##
#  poetry environment
#
if [ ! -f ~/.py-poetry.off ]; then
if [ -d $HOME/.poetry ]; then    
    export PY_RC_POETRY=1
py_rc_poetry_sh() {
export PATH="$HOME/.poetry/bin:$PATH"
}
py_rc_poetry_sh
fi
fi

EOF



# ===( rc )===========================

cat >> ~/.bashrc <<\EOF

# ---(pyenv:begin)-----
if [ ! -f ~/.py-env.off ]; then
if [ -d $HOME/.pyenv ]; then
   eval "$(pyenv init -)"
fi
fi
# ---(pyenv:end)-----

EOF


cat >> ~/.zshrc <<\EOF

# ---(pyenv:begin)-----
if [ ! -f ~/.py-env.off ]; then
if [ -d $HOME/.pyenv ]; then
   eval "$(pyenv init -)"
fi
fi
# ---(pyenv:end)-----

EOF



# ===( reload )===========================

exec $SHELL --login


```

Version
-------

```

# ===( install )===========================

eval "$(pyenv init -)"

pyenv --version

pyenv versions

: ${PYRC_PY_VERSION:=3.7.6}; export PYRC_PY_VERSION
[ -f ~/.python-version ] || echo "${PYRC_PY_VERSION}" > ~/.python-version


pyenv install $(cat ~/.python-version)

pyenv versions


# ===( activate )===========================

exec $SHELL --login

eval "$(pyenv init -)"
pyenv versions

pyenv shell $(cat ~/.python-version)

which python
python --version

pyenv global $(cat ~/.python-version)


```

Tools
-----

```
exec $SHELL --login

which python
python --version

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pipenv
python3 -m pip install --upgrade setuptools wheel

python3 -m pip install --upgrade ipython
python3 -m pip install --upgrade cookiecutter

pyenv    rehash
pipenv --version


python3 -m pip install --upgrade pipx
python3 -m pipx ensurepath


# pipx

ssh localhost 

pipx install pycowsay
pipx list
pipx run pycowsay 'moooo!'

exit

# rehash

pycowsay 'moooo!'




```

POETRY
======


Install
-------

```

# ===( get )===========================

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python 


# ===( reload )===========================

exec $SHELL --login

# ===( check )===========================

poetry --version
poetry self update


```

Build
-----

```
#   cd ~/work/vs/dve-sample-py


cat ./pyproject.toml


#eval "$(pyenv init -)"

[ -f ./.python-version ]   && pyenv shell $(cat ./.python-version)
[ ! -f ./.python-version ] && pyenv shell $(cat ~/.python-version)


which python
pyenv versions
python --version
pipenv --version
poetry --version

poetry env list
poetry env info
poetry env use -- $(which python)
poetry env list
poetry env info


# poetry lock

poetry install

poetry show


```

ACTIVATE
--------

```

#eval "$(pyenv init -)"

[ -f ./.python-version ]   && pyenv shell $(cat ./.python-version)
[ ! -f ./.python-version ] && pyenv shell $(cat ~/.python-version)

poetry shell

which python
which jupyter

python --version
jupyter --version



```

JUPYTER
-------

```

alias jupyter='eval "$(pyenv init -)"; pyenv exec poetry run jupyter'

jupyter --version
jupyter kernelspec list

[ -d ./notebooks ] && cd ./notebooks; \
jupyter notebook


[ -d ./notebooks ] && cd ./notebooks; \
jupyter notebook test/pyenv-verify/pyenv-check.ipynb



##
#
#

cd ~/work/bp/...


(poetry run jupyter notebook --notebook-dir=./notebooks --no-browser)



```




