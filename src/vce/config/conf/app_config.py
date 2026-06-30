import os.path
from typing import Any, override
from piny import YamlLoader

from vce.config.conf.base.base_config import BaseConfigMixin, BaseConfigStore
from vce.config.conf.db import DbConfig
from vce.config.conf import AppConfigConsts, AppConfigEx
from vce.common.util.format import dump_object


class AbsAppConfig(AppConfigEx, BaseConfigMixin):
    def __init__(self, name: str, conf: dict):
        super().__init__(name)
        self.conf = conf
        self.path_separator = AppConfigConsts.CONFIG_C_PATH_SEP

    def db_config(self, db_name: str) -> dict:
        result = self.conf["data"]["db"][db_name]
        return result

    def db(self, db_name: str) -> DbConfig:
        # ruff: noqa: PLC0415
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
            except KeyError as ex:
                msg = f"config key not found: {ks} in key: {key}"
                raise ValueError(msg) from ex
        return cfg

    def has_value(self, key: str) -> bool:
        try:
            self.get_value(key)
            return True
        except ValueError:
            return False

    def dump(self, full: bool = False) -> str:
        result = dump_object(self.conf)
        return result


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


class AppConfigStore(BaseConfigStore[YamlAppConfig]):
    def __init__(self):
        super().__init__(YamlAppConfig)

    @override
    def load_config(self, what=AppConfigConsts.CONFIG_S_DEFAULT) -> AbsAppConfig:
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


class AppConfigStoreGlobals:
    store = AppConfigStore()


def unload_all_configs():
    AppConfigStoreGlobals.store = AppConfigStore()


def get_config_store() -> AppConfigStore:
    return AppConfigStoreGlobals.store
