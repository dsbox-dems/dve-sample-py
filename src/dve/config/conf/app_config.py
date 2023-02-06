import os.path
from typing import Any, cast

from dve.config.conf.db import DbConfig
from dve.config.conf import AppConfigConsts, AppConfig, AppConfigEx

import vce.config.conf as vce_conf
import vce.config.conf.db as vce_conf_db
import vce.config.conf.app_config as vce_conf_impl


class AppConfigImpl(AppConfigEx):
    def __init__(self, name: str, inner: vce_conf.AppConfigEx):
        super().__init__(name)
        self.inner = inner
        self._db_config_cache = dict()

    def db_config_cache(self) -> dict:
        return self._db_config_cache

    def db_config(self, db_name: str) -> dict:
        return self.inner.db_config(db_name)

    def db_inner(self, db_name: str) -> vce_conf_db.DbConfig:
        return self.inner.db(db_name)

    def db(self, db_name: str) -> DbConfig:
        from dve.config.conf.db.db_config import DbConfigFactory

        result = DbConfigFactory.get_instance(self, db_name)
        return result

    def data(self) -> dict:
        return self.inner.data()

    def get_value(self, key: str) -> Any:
        return self.inner.get_value(key)

    def has_value(self, key: str) -> bool:
        return self.inner.has_value(key)

    def dump_value(self, key: str) -> str:
        return self.inner.dump_value(key)

    def get_int(self, key: str, defValue: int = 0) -> int:
        return self.inner.get_int(key, defValue)

    def get_bool(self, key: str, defValue: bool = False) -> bool:
        return self.inner.get_bool(key, defValue)

    def get_float(self, key: str, defValue: float = 0.0) -> float:
        return self.inner.get_float(key, defValue)

    def get_str(self, key: str, defValue: str = "") -> str:
        return self.inner.get_str(key, defValue)

    def dump(self) -> str:
        return self.inner.dump()

    @classmethod
    def create(cls, name: str, config: vce_conf.AppConfig) -> AppConfig:
        try:
            from vce.config import conf

            inner = cast(vce_conf.AppConfigEx, config)
            result = AppConfigImpl(name, inner)
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
            from vce.config import conf

            inner = cast(vce_conf.AppConfigEx, conf.get_config())
            result = AppConfigImpl.create(what, inner)
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
            handle["data"] = None
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
    vce_conf_impl.unload_all_configs()


def get_config_store() -> AppConfigStore:
    global _store
    return _store
