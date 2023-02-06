import sys
import logging

from vce.cli.ctl import std_main
from dve.cli.xargs import get_runner_argparser

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


def parse_args(argv, **kwargs):
    parser = get_runner_argparser()
    result = parser.parse_args(argv, **kwargs)
    return result


def exec(argv, xargs, **kwargs):
    cmd = xargs.cmd
    if cmd == "_":
        cmd = "auto"

    if cmd == "auto":
        import dve.scripts.auto as script

        RC = script.main(argv, **kwargs)
    elif cmd == "test":
        msg = f"#<runner.test>: cmd={cmd}, xargs:<{str(xargs)}>, argv:<{str(argv)}>, kwargs:<{str(kwargs)}>"
        log.info(msg)
        print(msg)
        RC = 0
    else:
        raise ValueError(f"invalid command: {cmd}!")
    return RC


@std_main(log=log, debug=True)
def main(argv=None, **kwargs):
    log.info(">> ### " + __name__ + ".main(argv=" + str(argv) + ")")
    xargs = parse_args(argv, **kwargs)
    RC = exec(argv, xargs, **kwargs)
    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


if __name__ == "__main__":
    main(sys.argv[1:])
