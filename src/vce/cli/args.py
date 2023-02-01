import sys
import argparse
from typing import Optional
from abc import ABC, abstractmethod


class AppArgsConsts(object):

    ARG_TYPE_GENERIC = "generic"
    ARG_TYPE_MAIN = "main"
    ARG_TYPE_RUNNER = "runner"
    ARG_TYPE_AUTO = "auto"

    ARGS_ENV_AUTO = "X_E_AUTO"


class IAppArgs(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_parser(self) -> argparse.ArgumentParser:
        pass

    @abstractmethod
    def parse_args(self, argv=None, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    def get_args(self) -> dict:
        pass


class AppBaseArgs(IAppArgs):

    arg_type = AppArgsConsts.ARG_TYPE_GENERIC

    def __init__(self, parent: Optional[IAppArgs] = None, *args, **kwargs):
        self.parent = parent
        self.xargs = dict()

    def get_args(self) -> dict:
        return self.xargs

    def make_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(add_help=False, conflict_handler="resolve")
        return parser

    def base_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(add_help=False, conflict_handler="resolve")

        parser.add_argument(
            "--verbose",
            "-v",
            action="count",
            default=0,
            help="increase output verbosity",
        )
        return parser

    def handle_unknown(self, xargs, unknown) -> dict:
        """Runner Script Argument Parser."""
        return xargs

    def parse_args(self, argv=None, *args, **kwargs) -> dict:
        """Process command line arguments."""
        if not argv:
            argv = sys.argv[1:]

        parser = self.get_parser()
        args, unknown = parser.parse_known_args(argv)
        result = self.handle_unknown(args, unknown, *args, **kwargs)
        self.xargs = result
        return result


class AppMainArgs(AppBaseArgs):

    arg_type = AppArgsConsts.ARG_TYPE_MAIN

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def base_parser(self) -> argparse.ArgumentParser:
        return super().base_parser()

    def main_parser(self) -> argparse.ArgumentParser:
        parent = self.base_parser()
        parser = argparse.ArgumentParser(parents=[parent], conflict_handler="resolve")
        parser.add_argument(
            "--exec", "-e", type=str, help="command to dispatch", default="_"
        )
        return parser

    def get_parser(self) -> argparse.ArgumentParser:
        return self.main_parser()


def get_main_argparser(*args, **kwargs) -> AppMainArgs:
    result = AppMainArgs(*args, **kwargs)
    return result


class AppRunnerArgs(AppBaseArgs):

    arg_type = AppArgsConsts.ARG_TYPE_RUNNER

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def base_parser(self) -> argparse.ArgumentParser:
        return super().base_parser()

    def runner_parser(self) -> argparse.ArgumentParser:
        """Runner Script Argument Parser."""
        parser = self.base_parser()
        parser.add_argument(
            "--cmd", "-c", type=str, help="script to execute", default="_"
        )
        return parser

    def get_parser(self) -> argparse.ArgumentParser:
        return self.runner_parser()


def get_runner_argparser(*args, **kwargs) -> AppRunnerArgs:
    result = AppRunnerArgs(*args, **kwargs)
    return result


class AppAutoArgs(AppBaseArgs):

    arg_type = AppArgsConsts.ARG_TYPE_AUTO

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def base_parser(self) -> argparse.ArgumentParser:
        return super().base_parser()

    def auto_parser(self) -> argparse.ArgumentParser:
        """Auto Script Argument Parser."""
        parser = self.base_parser()
        parser.add_argument(
            "--name", "-n", type=str, help="job params entry key", default="_"
        )
        return parser

    def get_parser(self) -> argparse.ArgumentParser:
        return self.auto_parser()


def get_auto_argparser(*args, **kwargs) -> AppAutoArgs:
    result = AppAutoArgs(*args, **kwargs)
    return result
