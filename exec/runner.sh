#!/bin/bash
##{{{
# runner.sh: Python script launcher
# ====================================
#
#  Python script runner via poetry
#
#  "./exec/runner.sh help" for usage info
#

E_ROOT_DIR="$(realpath $(dirname $0)/..)"
E_EXEC_DIR="${E_ROOT_DIR}/exec"

export PATH=$E_EXEC_DIR:$PATH

. $(dirname $0)/../functions.sh

#}}} \\\    
#{{{ [ DOCS ] /////////////////////////////////////////////////////////////////

# ---(usage)------------------------------------------------

exit_usage() {

cat <<EOF | $PAGER   

usage $0 [--name poetry-script] [args ...]

runs python script in project via "poetry run"


where "poetry-script" is a project Python script name,
defined in pyproject.toml:

...

[tool.poetry.scripts]
main = "dve.cli:main"
demo = "vce.cli:main"

...




NOTE
====

the scripts will be executerd from project root working directory 
and should be placed in the ./src/<pkg>/scripts directory



ENVIRONMENNT
============

inherited env:
 
- E_SCRIPT_NAME: script name (defaults to 'main')
- E_SCRIPT_FILE: script path (defaults to $E_EXEC_NAME)
- E_SCRIPT_ARGS: script arguments

exported env:

- E_ROOT_DIR: project base directory (working directory)
- E_EXEC_DIR: executable scripts directory ( $E_ROOT_DIR'/exec' )

- PATH: $E_EXEC_DIR:$PATH


EOF

exit 1

}


#}}} \\\
#{{{ [ MAIN ] /////////////////////////////////////////////////////////////////

# ---(args)------------------------------------------------

parse_args_run() {

    args="$@"
    log ">(args.run):" "$args"

    cmds=""

    while [ $# -gt 0 ]; do
        case "$1" in
            --help|-h)
                exit_usage $@
                ;;
            -e)
                E_SCRIPT_NAME="$2"
                shift
                ;;
            -n|--name)
                [ -z "$2" ] && exit_usage $@
                E_SCRIPT_JOB_NAME="$2"
                O_SCRIPT_JOB_NAME=1
                cmds="$cmds --name $E_SCRIPT_JOB_NAME" 
                shift
                ;;
            *)
                cmds="$cmds $1" 
                ;;
        esac
        shift
    done

: ${E_SCRIPT_NAME:="main"}
: ${E_SCRIPT_FILE:="$E_SCRIPT_NAME"}
: ${E_SCRIPT_ARGS:=$cmds}

    

    log "<(args.sub):" "cmds: $cmds"
            
    
}



# ---(call)------------------------------------------------

run_call() {
   #set -x 
   poetry run ${E_SCRIPT_FILE} ${E_SCRIPT_ARGS}
   rc=$?
   #set +x
   return $rc
}

do_call() {
    info "> exec::($E_SCRIPT_NAME, $E_SCRIPT_ARGS) -- ${E_SCRIPT_FILE}"
    run_call
    info "< exec::($E_SCRIPT_NAME, $E_SCRIPT_ARGS) (rc: $rc)"

}

# ---(main)------------------------------------------------

main() {

    parse_args_run $@

export E_SCRIPT_NAME
export E_SCRIPT_FILE
export E_SCRIPT_ARGS


#cd $E_ROOT_DIR

do_call $@
exit $rc

}

main $@

#}}} \\\

