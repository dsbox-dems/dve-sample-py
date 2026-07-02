from __future__ import annotations
import os.path
from typing import Any, cast, override, TYPE_CHECKING
from piny import YamlLoader

from vce.config.conf.base.base_config import BaseConfigImpl, BaseConfigStore
from vce.config.conf import AppConfigConsts, AppConfigEx
from vce.config.conf import ProjectConfig, get_local_config

if TYPE_CHECKING:
    from vce.config.conf.db import DbConfig


class AbsAppConfig(
    BaseConfigImpl,
    AppConfigEx,
):
    def __init__(self, name: str, conf: dict | None = None):
        super().__init__(name, conf)

    def db(self, db_name: str) -> "DbConfig":
        # ruff: noqa: PLC0415
        from vce.config.conf.db.db_config import DbConfigFactory

        result = DbConfigFactory.get_instance(self, db_name)
        return result


class YamlAppConfig(AbsAppConfig):
    cfg_type = AppConfigConsts.CFG_TYPE_YAML

    def __init__(self, name: str, conf: dict | None = None):
        super().__init__(name, conf)

    @classmethod
    def create(cls, name: str, config_path: str) -> "YamlAppConfig":
        try:
            raw_conf = YamlLoader(path=config_path).load()
            conf = cast("dict[str, Any]", raw_conf)
            result = YamlAppConfig(name, conf)
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

    @classmethod
    def create_empty(cls, name: str) -> "YamlAppConfig":
        try:
            loc: ProjectConfig = get_local_config()
            conf: dict[str, Any] = loc.local
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
    def load_config(self, what=AppConfigConsts.CONFIG_S_DEFAULT) -> YamlAppConfig:
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
