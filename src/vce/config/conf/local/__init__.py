from pathlib import Path
from typing import Any
from abc import abstractmethod

from vce.config.conf.base import BaseConfig
from vce.config.data import cfd


class LocalConfigConsts(object):
    CONFIG_F_ROOT = cfd().DATA_WORK
    CONFIG_F_MAIN = "./config.yaml"

    CONFIG_S_MAIN = "main"
    CONFIG_S_DEFAULT = CONFIG_S_MAIN

    CONFIG_C_PATH_SEP = "/"

    CONFIG_L_PROJECT_FILE = "pyproject.toml"
    CONFIG_L_SECTION_PARENT = "tool"
    CONFIG_L_SECTION_NAME = "local"
    CONFIG_L_ENV_PREFIX = "X_RUN_"
    CONFIG_L_KEY_CONFIG = "config"
    CONFIG_L_DEF_CONFIG = "config.yaml"
    CONFIG_L_KEY_HAS_CONFIG = "has_config"
    CONFIG_L_DEF_HAS_CONFIG = True

    CFG_TYPE_GENERIC = "generic"
    CFG_TYPE_YAML = "yaml"
    CFG_TYPE_ERROR = "error"

    DB_S_DEMO = "demo"
    DB_S_DATA = "data"
    DB_S_DEFAULT = DB_S_DATA


class ProjectConfig(BaseConfig):
    @property
    @abstractmethod
    def section(self) -> str:
        pass

    @property
    @abstractmethod
    def base_path(self) -> Path:
        pass

    @property
    @abstractmethod
    def project_path(self) -> Path:
        pass

    @property
    @abstractmethod
    def config_path(self) -> Path:
        pass

    @property
    @abstractmethod
    def has_project(self) -> bool:
        pass

    @property
    @abstractmethod
    def has_config(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_config_defined(self) -> bool:
        pass

    @property
    @abstractmethod
    def local(self) -> dict[str, Any]:
        pass


def get_local_config(section: str = LocalConfigConsts.CONFIG_L_SECTION_NAME) -> ProjectConfig:
    # ruff: noqa: PLC0415
    from vce.config.conf.local.local_config import ProjectConfigStoreGlobals

    result = ProjectConfigStoreGlobals.store.get_local(section)
    return result


#  LocalWords:  PLC, noqa
