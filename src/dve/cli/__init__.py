import logging

from vce.cli.ctl import std_main
from dve.cli.xargs import get_main_argparser

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

RC = 0


def parse_args(argv=None, *args, **kwargs):
    parser = get_main_argparser()
    result = parser.parse_args(argv, *args, **kwargs)
    return result


def exec(xargs, argv=None, *args, **kwargs):
    entry = xargs.exec
    if entry == "_":
        entry = "main"

    if entry == "main":
        import dve.scripts.runner as runner

        RC = runner.main(argv, *args, **kwargs)
    else:
        raise ValueError(f"invalid command: {entry}!")
    return RC


@std_main(log=log, debug=True)
def main(argv=None, *args, **kwargs):
    log.info(">> ### " + __name__ + ".main(argv=" + str(argv) + ")")
    xargs = parse_args(argv, *args, **kwargs)
    RC = exec(xargs, argv, *args, **kwargs)
    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


if __name__ == "__main__":
    main()
