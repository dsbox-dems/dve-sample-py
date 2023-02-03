import logging

from vce.cli.ctl import std_main
from vce.cli.xargs import get_main_argparser

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
        entry = "demo"

    if entry == "demo":
        import vce.demo.demo_runner as runner

        RC = runner.main(argv, *args, **kwargs)
    else:
        raise ValueError(f"invalid command: {entry}!")
    return RC


@std_main(debug=True)
def main(argv=None, *args, **kwargs):
    """Process command line arguments."""
    xargs = parse_args(argv, *args, **kwargs)
    RC = exec(xargs, argv=argv, *args, **kwargs)
    return RC


if __name__ == "__main__":
    main()
