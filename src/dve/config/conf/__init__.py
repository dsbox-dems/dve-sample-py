import re
import json
from typing import Any
from abc import ABC, abstractmethod

from dve.config.conf.db import DbConfig

import vce.config.conf as vce_conf
import vce.config.conf.db as vce_conf_db


class AppConfigConsts(object):
    CONFIG_F_ROOT = vce_conf.AppConfigConsts.CONFIG_F_ROOT
    CONFIG_F_MAIN = vce_conf.AppConfigConsts.CONFIG_F_MAIN

    CONFIG_S_MAIN = vce_conf.AppConfigConsts.CONFIG_S_MAIN
    CONFIG_S_DEFAULT = vce_conf.AppConfigConsts.CONFIG_S_DEFAULT

    CONFIG_C_PATH_SEP = vce_conf.AppConfigConsts.CONFIG_C_PATH_SEP

    CFG_TYPE_GENERIC = vce_conf.AppConfigConsts.CFG_TYPE_GENERIC
    CFG_TYPE_YAML = vce_conf.AppConfigConsts.CFG_TYPE_YAML
    CFG_TYPE_ERROR = vce_conf.AppConfigConsts.CFG_TYPE_ERROR

    DB_S_DEMO = vce_conf.AppConfigConsts.DB_S_DEMO
    DB_S_DATA = vce_conf.AppConfigConsts.DB_S_DATA
    DB_S_DEFAULT = vce_conf.AppConfigConsts.DB_S_DEFAULT


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

    @abstractmethod
    def db_inner(self, db_name: str) -> vce_conf_db.DbConfig:
        pass

    @abstractmethod
    def db_config_cache(self) -> dict:
        pass


# ruff: noqa: PLC0415
class AppConfigs(object):
    @staticmethod
    def unload_all():
        from dve.config.conf.app_config import unload_all_configs

        unload_all_configs()

    @staticmethod
    def get(what=AppConfigConsts.CONFIG_S_DEFAULT) -> AppConfig:
        from dve.config.conf.app_config import get_config_store

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
