---
title: jupyter setup
subtitle: install pyenv, pipenv, jupyter, pandas
author: gp
date: 03/05/2019
---





PYENV
=====

* https://realpython.com/intro-to-pyenv/
* https://medium.com/@Joachim8675309/installing-pythons-with-pyenv-54cca2196cd3


BUILD DEPS
----------

```

# @runas(root)

apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl



```


Virtual Display
---------------

* https://pypi.org/project/PyVirtualDisplay/
* https://github.com/ponty/pyscreenshot
* 


```

# pyvirtualdisplay xvfbwrapper

Y='-y'

apt install $Y xvfb xserver-xephyr vnc4server
apt install $Y freeglut3-dev ffmpeg


# pip install pyvirtualdisplay xvfbwrapper





```





INSTALL
-------

```

# @runas(user)

curl https://pyenv.run | bash


# install pyenv
PROJ=pyenv-installer
SCRIPT_URL=https://github.com/pyenv/$PROJ/raw/master/bin/$PROJ
curl -L $SCRIPT_URL | bash

# update pyenv
( cd ~/.pyenv; git pull )

# setup
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"


# config

cat >> ~/.bashrc <<\EOF

# ---(pyenv:begin)-----

export PATH=~/.pyenv/bin:$PATH
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# ---(pyenv:end)-----

EOF


. ~/.bashrc


```

VERSION
-------

```

eval "$(pyenv init -)"

pyenv --version

pyenv versions

: ${PYRC_PY_VERSION:=3.8.0}; export PYRC_PY_VERSION
[ -f ~/.python-version ] || echo "${PYRC_PY_VERSION}" > ~/.python-version


pyenv install $(cat ~/.python-version)

pyenv versions



```



PIPENV
=====


ACTIVATE
--------

```

eval "$(pyenv init -)"
pyenv versions

pyenv shell $(cat ~/.python-version)

which python
python --version

pyenv global $(cat ~/.python-version)


```



```

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pipenv
python3 -m pip install --upgrade setuptools wheel

pyenv    rehash
pipenv --version




```


```


(mkdir -p ~/work/vs; cd  ~/work/vs; [ -d dve-sample-py ] || git clone https://gitlab.com/ub-dems-public/ds-labs/dve-sample-py.git )

cd ~/work/vs/dve-sample-py
git pull

ls -l ./Pipfile*
# cat   ./Pipfile


#eval "$(pyenv init -)"

[ -f ./.python-version ]   && pyenv shell $(cat ./.python-version)
[ ! -f ./.python-version ] && pyenv shell $(cat ~/.python-version)


which python
python --version
pipenv --version


pipenv --rm

pipenv install --dev --python $(which python)


# pipenv install -v --dev --python $(which python)

```


ACTIVATE
--------

```

#eval "$(pyenv init -)"

[ -f ./.python-version ]   && pyenv shell $(cat ./.python-version)
[ ! -f ./.python-version ] && pyenv shell $(cat ~/.python-version)

pipenv shell

which python
which jupyter

python --version


jupyter --version

python -m site

#pycharm

```




JUPYTER
-------

```

alias jupyter='eval "$(pyenv init -)"; pyenv exec pipenv run \jupyter'

jupyter --version
jupyter kernelspec list

[ -d ./notebooks ] && cd ./notebooks; \
jupyter notebook


[ -d ./notebooks ] && cd ./notebooks; \
jupyter notebook test/pyenv-verify/pyenv-check.ipynb



##
#
#

cd ~/work/vs/dve-sample-py

(pipenv run jupyter notebook --notebook-dir=./notebooks --no-browser)



```




PYCHARM
-------

```

##
# (@runas: root)
#


mount /vol/glob/dvd

# rm -rf /opt/local/tools/pycharm/
mkdir -p /opt/local/tools/pycharm/
cd       /opt/local/tools/pycharm/

tar xvzf /vol/glob/dvd/tools/intellij/pycharm/pycharm-community-*.tar.gz

ls -l

[ -h ./pycharm-ce ] && rm -f ./pycharm-ce

chgrp -R users pycharm-community-*
chmod -R g+w pycharm-community-*

ls -ld $(ls -dt pycharm-community-* | tail -n 1)
ln -s  $(ls -dt pycharm-community-* | tail -n 1) pycharm-ce
ls -l 


ls -l /usr/bin/*charm*
ls -l /usr/local/bin/*charm*
[ -f /usr/bin/pycharm ] && [ ! -f /usr/bin/pycharm-36 ] && mv /usr/bin/pycharm /usr/bin/pycharm-36
ln -s /usr/local/bin/charm /usr/local/bin/pycharm
ls -l /usr/bin/*charm*
ls -l /usr/local/bin/*charm*


ls -l /usr/share/applications/*charm*
ls -l /usr/local/share/applications/*charm*
mkdir -p /usr/local/doc/pycharm-36
[ -f /usr/share/applications/pycharm.desktop ] && mv /usr/share/applications/pycharm.desktop /usr/local/doc/pycharm-36
ls -l /usr/share/applications/*charm*
ls -l /usr/local/share/applications/*charm*


##
# (@runas: sudoer)
#

rm -rf ~/.PyCharm*

/opt/local/tools/pycharm/pycharm-ce/bin/pycharm.sh

##
# - create system script:
# /usr/local/bin/charm
#
# - create desktop entry:
# file:///usr/local/share/applications/jetbrains-pycharm-ce.desktop
#


##
# (@runas: root)
#


#ln -s /usr/local/share/applications/jetbrains-pycharm-ce.desktop /usr/share/applications/jetbrains-pycharm-ce.desktop


# clear; ls /home | grep -v -e lost -e dsbox -e dsuser -e dsguest | xargs -I{} echo 'sudo -u {} cp -rv /etc/skel/.config/xfce4/panel/launcher-9 .config/xfce4/panel/'


```


