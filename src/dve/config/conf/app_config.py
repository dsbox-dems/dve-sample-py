import os.path
from typing import Any, cast, override

from dve.config.conf.db import DbConfig
from dve.config.conf import AppConfigConsts, AppConfig, AppConfigEx

import vce.config.conf as vce_conf
import vce.config.conf.db as vce_conf_db
import vce.config.conf.app_config as vce_conf_impl


# ruff: noqa: PLC0415
class AppConfigImpl(AppConfigEx):
    def __init__(self, name: str, inner: vce_conf.AppConfigEx):
        super().__init__(name)
        self.inner = inner
        self._db_config_cache = {}

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

    def dump_object(self, obj: Any) -> str:
        return self.inner.dump_object(obj)

    def dump_object_uri(self, uri: str) -> str:
        return self.inner.dump_object_uri(uri)

    def dump(self, full: bool = False) -> str:
        return self.inner.dump(full)

    @classmethod
    def create(cls, name: str, config: vce_conf.AppConfig) -> AppConfig:
        try:
            inner = cast("vce_conf.AppConfigEx", config)
            result = AppConfigImpl(name, inner)
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex


class AppConfigStore(vce_conf_impl.BaseConfigStore[AppConfig]):
    def __init__(self):
        super().__init__(AppConfig)

    @override
    def load_config(self, what=AppConfigConsts.CONFIG_S_DEFAULT) -> AppConfig:
        config_path = self.config_path(what)
        if not os.path.exists(config_path):
            raise ValueError(f"Config Name {what} file not found: {config_path}")
        try:
            from vce.config import conf

            inner = cast("vce_conf.AppConfigEx", conf.get_config())
            result = AppConfigImpl.create(what, inner)
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex


class AppConfigStoreGlobals:
    _store = AppConfigStore()


def unload_all_configs():
    AppConfigStoreGlobals._store = AppConfigStore()
    vce_conf_impl.unload_all_configs()


def get_config_store() -> AppConfigStore:
    return AppConfigStoreGlobals._store
