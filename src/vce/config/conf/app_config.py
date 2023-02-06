import os.path
from typing import Any
from piny import YamlLoader

from vce.config.conf.db import DbConfig
from vce.config.conf import AppConfigConsts, AppConfig, AppConfigEx


class AbsAppConfig(AppConfigEx):
    def __init__(self, name: str, conf: dict):
        super().__init__(name)
        self.conf = conf
        self.path_separator = AppConfigConsts.CONFIG_C_PATH_SEP

    def db_config(self, db_name: str) -> dict:
        result = self.conf["data"]["db"][db_name]
        return result

    def db(self, db_name: str) -> DbConfig:
        from vce.config.conf.db.db_config import DbConfigFactory

        result = DbConfigFactory.get_instance(self, db_name)
        return result

    def data(self) -> dict:
        return self.conf

    def key_path(self, key: str) -> list:
        result = key.split(self.path_separator)
        return result

    def get_value(self, key: str) -> Any:
        keys = self.key_path(key)
        cfg = self.conf
        ks = []
        for k in keys:
            try:
                ks.append(k)
                cfg = cfg[k]
            except:
                raise ValueError(f"config key not found: {ks} in key: {key}")
        return cfg

    def has_value(self, key: str) -> bool:
        try:
            self.get_value(key)
            return True
        except ValueError:
            return False

    def dump_value(self, key: str) -> str:
        try:
            obj = self.get_value(key)
            result = self.dump_object(obj)
            return result
        except ValueError:
            return ""

    def get_int(self, key: str, defValue: int = 0) -> int:
        obj = None
        try:
            obj = self.get_value(key)
        except ValueError:
            return defValue
        result = int(obj)
        return result

    def get_float(self, key: str, defValue: float = 0) -> float:
        obj = None
        try:
            obj = self.get_value(key)
        except ValueError:
            return defValue
        result = float(obj)
        return result

    def get_bool(self, key: str, defValue: bool = False) -> bool:
        obj = None
        try:
            obj = self.get_value(key)
        except ValueError:
            return defValue
        s = str(obj).lower()
        result = s in {"y", "yes", "t", "true", "1"}
        return result

    def get_str(self, key: str, defValue: str = "") -> str:
        obj = None
        try:
            obj = self.get_value(key)
        except ValueError:
            return defValue
        result = str(obj)
        return result

    def dump(self) -> str:
        result = self.dump_object(self.conf)
        return result


class ErrAbsConfig(AbsAppConfig):
    cfg_type = AppConfigConsts.CFG_TYPE_ERROR

    def __init__(self, name: str, ex: Exception):
        super().__init__(name, dict(ex=ex))
        self.ex = ex


class YamlAppConfig(AbsAppConfig):
    cfg_type = AppConfigConsts.CFG_TYPE_YAML

    def __init__(self, name: str, conf: Any):
        super().__init__(name, conf)

    @classmethod
    def create(cls, name: str, config_path: str) -> AbsAppConfig:
        try:
            conf = YamlLoader(path=config_path).load()
            result = YamlAppConfig(name, conf)
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex


class AppConfigStore(object):
    def __init__(self):
        self._config = dict()

    @classmethod
    def config_name(cls, what=AppConfigConsts.CONFIG_S_DEFAULT):
        result = None
        if what == AppConfigConsts.CONFIG_S_MAIN:
            result = AppConfigConsts.CONFIG_F_MAIN
        if result is None:
            raise ValueError(f'Config Name unknown: "{what}", cannot load')
        return result

    @classmethod
    def config_path(cls, what=AppConfigConsts.CONFIG_S_DEFAULT):
        name = cls.config_name(what)
        fn = os.path.join(AppConfigConsts.CONFIG_F_ROOT, name)
        result = os.path.normpath(fn)
        return result

    def load_config(self, what=AppConfigConsts.CONFIG_S_DEFAULT):
        config_path = self.config_path(what)
        if not os.path.exists(config_path):
            raise ValueError(f"Config Name {what} file not found: {config_path}")
        try:
            result = YamlAppConfig.create(what, config_path)
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

    def get_config(self, what=AppConfigConsts.CONFIG_S_DEFAULT) -> AppConfig:
        if what in self._config:
            handle = self._config[what]
            result = handle["data"]
            return result

        handle = {
            "what": what,
            "loaded": True,
            "failed": False,
            "error": None,
            "data": None,
        }
        self._config[what] = handle
        try:
            handle["data"] = self.load_config(what)

        except Exception as ex:
            handle["failed"] = True
            handle["error"] = ex
            handle["data"] = ErrAbsConfig(what, ex)
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

        h = self._config[what]
        result = h["data"]

        if result is None:
            ex = h["error"]
            raise ValueError(f"Config Name {what} not loaded: {type(ex)} {ex.args}")

        return result


_store = AppConfigStore()


def unload_all_configs():
    global _store
    _store = AppConfigStore()


def get_config_store() -> AppConfigStore:
    global _store
    return _store
