import re
import json
from typing import Any
from abc import ABC, abstractmethod

from vce.config.conf.db import DbConfig
from vce.config.data import cfd


class AppConfigConsts(object):
    CONFIG_F_ROOT = cfd().DATA_WORK
    CONFIG_F_MAIN = "./config.yaml"

    CONFIG_S_MAIN = "main"
    CONFIG_S_DEFAULT = CONFIG_S_MAIN

    CONFIG_C_PATH_SEP = "/"

    CFG_TYPE_GENERIC = "generic"
    CFG_TYPE_YAML = "yaml"
    CFG_TYPE_ERROR = "error"

    DB_S_DEMO = "demo"
    DB_S_DATA = "data"
    DB_S_DEFAULT = DB_S_DATA


class AppConfig(ABC):
    cfg_type = AppConfigConsts.CFG_TYPE_GENERIC

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def db(self, db_name: str) -> DbConfig:
        pass

    @abstractmethod
    def data(self) -> dict:
        pass

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
    def dump(self) -> str:
        pass

    @staticmethod
    def dump_object(obj: Any) -> str:
        msg = json.dumps(obj, indent=4, sort_keys=False, default=str)
        result = re.sub('"password": *"[^"]*",', '"password": "***"', msg)
        return result


class AppConfigEx(AppConfig):
    def __init__(self, name: str):
        super().__init__(name)

    @abstractmethod
    def db_config(self, db_name: str) -> dict:
        pass


class AppConfigs(object):
    @staticmethod
    def unload_all():
        # ruff: noqa: PLC0415
        from vce.config.conf.app_config import unload_all_configs

        unload_all_configs()

    @staticmethod
    def get(what=AppConfigConsts.CONFIG_S_DEFAULT) -> AppConfig:
        from vce.config.conf.app_config import get_config_store

        store = get_config_store()
        result = store.get_config(what)
        return result

    @staticmethod
    def db(db_name=AppConfigConsts.DB_S_DEFAULT) -> DbConfig:
        app_config = AppConfigs.get()
        result = app_config.db(db_name)
        return result


def get_config(what=AppConfigConsts.CONFIG_S_DEFAULT) -> AppConfig:
    return AppConfigs.get(what)


def db_config(db_name=AppConfigConsts.DB_S_DEFAULT) -> DbConfig:
    return AppConfigs.db(db_name)
