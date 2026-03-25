import logging

from subprocess import run
from textwrap import dedent

import vce.common.util.time as tm

# import vce.common.util.file as fu

log = logging.getLogger(__name__)


def to_oneline(command_line):
    return dedent(command_line).replace("\n", " ").replace("; ", ";")


def to_manylines(command_lines):
    return dedent(command_lines)


proc_num = 0
init_timer = tm.timer()


def new_proc_id():
    global proc_num
    proc_num = proc_num + 1
    return proc_num


def run_context(
    command, script=None, name=None, parms=None, xargs=None, argv=None, *args, **kwargs
):
    conf = None
    proc_id = new_proc_id()
    timer = tm.timer()
    prefix = f"//run({proc_id},{init_timer}):"
    ctx = dict(
        command=command,
        script=script,
        proc_id=proc_id,
        timer=timer,
        prefix=prefix,
        mp_conf=conf,
        parms=parms,
        name=name,
        xargs=xargs,
        args=args,
        argv=argv,
    )
    return ctx


def run_command(
    command, script=None, name=None, parms=None, xargs=None, argv=None, *args, **kwargs
):
    ctx = run_context(command, script, name, parms, xargs, argv, *args, **kwargs)
    log.info(f"> {ctx['prefix']} {command}")

    # TODO: multi-process config <c:NUMA>

    # if ctx["mp_conf"].enable:
    #     rc = run_para(ctx, command)
    # else:
    #     rc = run_proc(ctx, command)

    rc = run_proc(ctx, command)

    log.info(f"< {ctx['prefix']}  (rc:{rc},elapsed{ctx['timer']})")
    return rc


def run_proc(ctx, command):
    command_line = command
    log.info(f"* {ctx['prefix']} {command_line}")
    rp = run(command_line, shell=True, check=True)
    rc = rp.returncode
    return rc


def cmd_args(
    script=None, name=None, parms=None, xargs=None, argv=None, *args, **kwargs
):
    # result = [
    #     "--jobname",
    #     parms["job"],
    #     "--group",
    #     parms["group"],
    #     "--filename",
    #     parms["filename"],
    # ]
    # s = join(result)

    s_argv = " ".join(argv) if argv else ""
    s = " ".join([s_argv])
    return s


def cmd_script(
    script=None, name=None, parms=None, xargs=None, argv=None, *args, **kwargs
):
    result = (
        f"python {script} {cmd_args(script, name, parms, xargs,argv, *args, **kwargs)}"
    )
    return result


def call_command(command, name, xargs, argv=None, **kwargs):
    parms = dict()
    run_command(command, parms, name, xargs, argv)


def call_script(script=None, name=None, xargs=None, argv=None, *args, **kwargs):
    # TODO: spawn process parms <c:NUMA c:PARMS>
    # parm = DD_PARMS[name]
    parms = dict()
    command = cmd_script(script, name, parms, xargs, argv, *args, **kwargs)
    rc = run_command(command, script, name, parms, xargs, argv, *args, **kwargs)
    return rc
