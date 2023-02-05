import sys
import logging

from vce.cli.ctl import std_main
from vce.cli.xargs import get_test_argparser

import vce.cli.parms as sp

from dve.config.data import cfd

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

RC_C_FAIL = 1
RC_C_OK = 0

RC = RC_C_OK


def do_process(xargs, argv=None, **kwargs):
    msgs = [
        f">> @{__name__}.proc(argv=<{str(argv)}>)",
        f">> @{__name__}.proc(args=<{str(args)}>)",
        f">> @{__name__}.proc(kwargs=<{str(kwargs)}>)",
    ]
    msg = " ".join(msgs)

    log.info(msgs[0])
    log.debug(msgs[0])
    log.debug(msgs[0])

    print(msg)

    return RC


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def parse_args(argv=None, **kwargs):
    parser = get_test_argparser()
    result = parser.parse_args(argv, **kwargs)
    return result


def exec(xargs, argv=None, **kwargs):
    RC = do_process(xargs=xargs, argv=argv, **kwargs)
    return RC


@std_main(log=log, debug=True)
def main(argv=None, **kwargs):
    log.info(">> ### " + __name__ + ".main(argv=" + str(argv) + ")")
    kwargs['argvx']  = argv
    xargs = parse_args(argv=argv, **kwargs)
    kwargs['xargs']  = xargs
    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


if __name__ == "__main__":
    main(sys.argv[1:])
