import sys
import logging

from vce.cli.ctl import std_main
from dve.cli.xargs import get_test_argparser

import vce.cli.parms as sp

from dve.config.data import cfd

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

RC_C_FAIL = 1
RC_C_OK = 0

RC = RC_C_OK


def do_process(xargs, argv=None, *args, **kwargs):
    log.info(">> @" + __name__ + ".proc(argv=" + str(argv) + ")")

    return RC


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def parse_args(argv=None, *args, **kwargs):
    parser = get_test_argparser()
    result = parser.parse_args(argv, *args, **kwargs)
    return result


def exec(xargs, argv=None, *args, **kwargs):
    RC = do_process(xargs, argv=argv, *args, **kwargs)
    return RC


@std_main(log=log, debug=True)
def main(argv=None, *args, **kwargs):
    log.info(">> ### " + __name__ + ".main(argv=" + str(argv) + ")")
    xargs = parse_args(argv, *args, **kwargs)
    RC = exec(xargs, argv, *args, **kwargs)
    log.info("<< ###" + __name__ + ".main => (rc=" + str(RC) + ")")
    return RC


if __name__ == "__main__":
    main(sys.argv[1:])
