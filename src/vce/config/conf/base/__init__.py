from typing import Any
from abc import ABC, abstractmethod

from vce.config.data import cfd


from vce.config.data import cfd


class BaseConfigConsts(object):
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


class BaseConfig(ABC):
    @abstractmethod
    def get_value(self, key: str) -> Any:
        pass

    @abstractmethod
    def has_value(self, key: str) -> bool:
        pass

    @abstractmethod
    def dump_value(self, key: str) -> str:
        pass

    @abstractmethod
    def get_bool(self, key: str, defValue: bool = False) -> bool:
        pass

    @abstractmethod
    def get_int(self, key: str, defValue: int = 0) -> int:
        pass

    @abstractmethod
    def get_float(self, key: str, defValue: float = 0.0) -> float:
        pass

    @abstractmethod
    def get_str(self, key: str, defValue: str = "") -> str:
        pass

    @abstractmethod
    def dump_object(self, obj: Any) -> str:
        pass

    @abstractmethod
    def dump_object_uri(self, uri: str) -> str:
        pass

    @abstractmethod
    def dump(self, full: bool = False) -> str:
        pass


class BaseConfigEx(BaseConfig):
    @abstractmethod
    def data(self) -> dict:
        pass

    @abstractmethod
    def db_config(self, db_name: str) -> dict:
        pass
