import logging
import functools
import time

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


class StdMain(object):
    LOG_PREFIX = "#++ "

    def __init__(self, func, log=logging.getLogger(__name__), debug=False, **kwargs):
        functools.update_wrapper(self, func)
        self.func = func
        self.debug = debug
        self.extra = kwargs
        self.log = log
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        if self.debug:
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            self.trace(f"Calling {self.func.__name__}({signature})")

        start_time = time.perf_counter()

        self.info(f"Started {self.func.__name__!r}")

        result = self.func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        if self.debug:
            self.trace(f"{self.func.__name__!r} returned {result!r}")

        self.info(f"Finished {self.func.__name__!r} in {run_time:.4f} secs")
        return result

    def error(self, message):
        self.log.error(StdMain.LOG_PREFIX + message)

    def warn(self, message):
        self.log.warning(StdMain.LOG_PREFIX + message)

    def info(self, message):
        self.log.info(StdMain.LOG_PREFIX + message)

    def trace(self, message):
        self.log.debug(StdMain.LOG_PREFIX + message)


def std_main(log=logging.getLogger(__name__), debug=False, **kwargs):
    def _std_main(func):
        return StdMain(func, log, debug, **kwargs)

    return _std_main
