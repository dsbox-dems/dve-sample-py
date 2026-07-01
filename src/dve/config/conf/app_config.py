import os.path
from typing import cast, override

from dve.config.conf.db import DbConfig
from dve.config.conf import AppConfigConsts, AppConfig, AppConfigEx

import vce.config.conf as vce_conf
import vce.config.conf.base.base_config as vce_base
import vce.config.conf.db as vce_conf_db
import vce.config.conf.app_config as vce_conf_impl


class AppConfigBase(vce_base.BaseConfigWrapper[vce_conf.AppConfigEx]):
    def __init__(self, name: str, inner: vce_conf.AppConfigEx):
        super().__init__(name, inner)


# ruff: noqa: PLC0415
class AppConfigImpl(AppConfigBase, AppConfigEx):
    def __init__(self, name: str, inner: vce_conf.AppConfigEx):
        super().__init__(name, inner)
        self._db_config_cache = {}

    def db_config_cache(self) -> dict:
        return self._db_config_cache

    def db_inner(self, db_name: str) -> vce_conf_db.DbConfig:
        return self.inner.db(db_name)

    def db(self, db_name: str) -> DbConfig:
        from dve.config.conf.db.db_config import DbConfigFactory

        result = DbConfigFactory.get_instance(self, db_name)
        return result

    @classmethod
    def create(cls, name: str, config: vce_conf.AppConfig) -> AppConfig:
        try:
            inner = config.as_ex()
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
