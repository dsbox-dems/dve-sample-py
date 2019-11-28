#!/bin/bash


PYE_VERSION=3.7.4


exit_usage() {

    cat <<EOF

usage: $0 $@


EOF

    exit 1


}





pyenv_config() {

cat >> ~/.bashrc <<\EOF

# ---(pyenv:begin)-----
if [ -d ~/.pyenv ]; then
if [ ! -f ~/.pyenv.off ]; then

export PATH=~/.pyenv/bin:$PATH
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"


fi
fi
# ---(pyenv:end)-----

EOF


. ~/.bashrc



}


pyenv_reload() {


export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv rehash


}




pyenv_setup() {

    curl https://pyenv.run | bash

}


pyenv_install() {

    pyenv install

}


pyenv_status() {
    
    set +x

    pyenv_reload
    pyenv --version
    pyenv versions
    which python
    python --version

}


pipenv_status() {

    pyenv_status
    pipenv --version
    
}



pipenv_setup() {

    python -m pip install --upgrade pip
    python -m pip install --upgrade pipenv
    python -m pip install --upgrade setuptools wheel

}


pipenv_install() {

    pipenv install $PYPENV_VERBOSE --dev --python $(which python)

}

pipenv_update() {

    pipenv update $PYPENV_VERBOSE

}




py_sh() {

    pipenv shell $@

}


py_run() {

    pipenv run $@

}


py_note() {

# alias jupyter='eval "$(pyenv init -)"; pyenv exec pipenv run \jupyter'

[ -d ./notebooks ] && NB_HOME=./notebooks

# ${NB_OPTS:=' --no-browser'}
: ${NB_OPTS:=''}
: ${NB_ARGS:=""}

(pipenv run jupyter notebook --notebook-dir=${NB_HOME:-'.'} $NB_OPTS $NB_ARGS $@)

}



py_status() {

    pipenv_status

    which python
    which jupyter
    python --version
    jupyter --version
    jupyter kernelspec list
    
}






main() {

    cmd="$1"
    shift

    set -x

    case "$cmd" in

        pyenv.setup)    pyenv_setup $@ ;;
        pyenv.install)  pyenv_install $@ ;;
        pyenv.status)   pyenv_status $@ ;;

        pipenv.setup)   pipenv_setup $@ ;;
        pipenv.install) pipenv_install $@ ;;
        pipenv.update)  pipenv_update $@ ;;
        pipenv.status)  pipenv_status $@ ;;

        py.sh)          py_sh $@ ;;
        py.run)         py_run $@ ;;
        py.note)        py_note $@ ;;
        
        py.status)      py_status $@ ;;
        
        
        *) echo "# maker args? $0 $@"; exit_usage;;

    esac

    exit $?

}




main $@
