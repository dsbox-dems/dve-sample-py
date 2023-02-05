import sys
import logging

from vce.cli.ctl import std_main
from vce.cli.xargs import get_runner_argparser

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


def parse_args(argv=None, **kwargs):
    parser = get_runner_argparser()
    result = parser.parse_args(argv, **kwargs)
    return result


def exec(xargs, argv=None, **kwargs):
    cmd = xargs.cmd
    if cmd == "_":
        cmd = "auto"

    if cmd == "auto":
        import vce.demo.demo_auto as script

        RC = script.main(argv, **kwargs)
    elif cmd == "numa":
        import vce.demo.demo_numa as script

        RC = script.main(argv, **kwargs)
    elif cmd == "test":
        msg = f"#<test>: argv:<{str(argv)}>, args:<{str(args)}>, kwargs:<{str(kwargs)}>"
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
    RC = exec(xargs, argv, **kwargs)
    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


if __name__ == "__main__":
    main(sys.argv[1:])
