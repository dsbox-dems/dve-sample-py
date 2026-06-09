import os.path
from pathlib import Path
from typing import Any, Self, cast
from piny import YamlLoader
from abc import abstractmethod
import toml

from vce.config.conf.db import DbConfig
from vce.config.conf import AppConfigConsts, BaseConfig, AppConfig, AppConfigEx, ProjectConfig
from vce.common.util.file import find_file_upwards
from vce.common.util.format import dump_object, dump_object_uri


class BaseConfigMixin(BaseConfig):
    @abstractmethod
    def get_value(self, key: str) -> Any:
        pass

    @abstractmethod
    def has_value(self, key: str) -> bool:
        pass

    @abstractmethod
    def dump(self, full: bool = False) -> str:
        pass

    def dump_object(self, obj: Any) -> str:
        return dump_object(obj)

    def dump_object_uri(self, uri: str) -> str:
        return dump_object_uri(uri)

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


class ProjectConfigImpl(ProjectConfig, BaseConfigMixin):
    @classmethod
    def create(cls, section: str = AppConfigConsts.CONFIG_L_SECTION_NAME) -> Self:
        try:
            result = cls(section=section)
            result.setup()
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

    def __init__(self, section: str = AppConfigConsts.CONFIG_L_SECTION_NAME):
        self._section = section
        self._base_path = None
        self._project_path = None
        self._config_path = None
        self._local = {}

    def setup(self) -> Self:
        self._project_path = find_file_upwards(AppConfigConsts.CONFIG_L_ENV_PREFIX)
        if not self.has_project:
            return self

        assert self._project_path is not None
        self._base_path = self._project_path.parent
        self._local = self.load_local_config()
        if not self.is_config_defined:
            return self

        self._config_path = self.resolve_config_path()
        return self

    def load_local_config(self) -> dict[str, Any]:
        """Load configuration from pyproject.toml.

        Returns:
        Configuration dictionary with tool.local settings
        """
        try:
            pyproject_path = self.project_path

            data = toml.load(pyproject_path)
            tools = data.get(AppConfigConsts.CONFIG_L_SECTION_PARENT, {})
            section = tools.get(AppConfigConsts.CONFIG_L_SECTION_NAME, {})
            result = cast("dict[str, Any]", section)
            return result
        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

    def resolve_config_path(self) -> Path:
        """Find config.yaml from current dir and parents,
           in not found try path relative to pyproject.toml

        Returns:
        Path of resolved config
        """
        try:
            config_filename = self.get_value(
                AppConfigConsts.CONFIG_L_KEY_CONFIG, AppConfigConsts.CONFIG_L_DEF_CONFIG
            )
            config_path = find_file_upwards(config_filename)

            if config_path is None:
                config_path = find_file_upwards(config_filename, self.base_path)

            if config_path is None:
                msg = f"config file not found: {config_filename} in dir: {Path.cwd()}"
                raise ValueError(msg)

            if not config_path.exists():
                msg = f"config file not found: {config_filename} in dir: {Path.cwd()}"
                raise ValueError(msg)

            return config_path

        except Exception as ex:
            print(type(ex))
            print(ex.args)
            print(ex)
            raise ex

    @property
    def section(self) -> str:
        return self._section

    @property
    def base_path(self) -> Path:
        if self._base_path is None:
            raise ValueError("base_path is None")
        return self._base_path

    @property
    def project_path(self) -> Path:
        if self._project_path is None:
            raise ValueError("project_path is None")
        return self._project_path

    @property
    def config_path(self) -> Path:
        if self._config_path is None:
            raise ValueError("config_path is None")
        return self._config_path

    @property
    def has_project(self) -> bool:
        return self._project_path is not None and self._project_path.exists()

    @property
    def has_config(self) -> bool:
        return self._config_path is not None and self._config_path.exists()

    @property
    def is_config_defined(self) -> bool:
        return self.local.get(
            AppConfigConsts.CONFIG_L_KEY_HAS_CONFIG, AppConfigConsts.CONFIG_L_DEF_HAS_CONFIG
        )

    @property
    def local(self) -> dict[str, Any]:
        return self._local

    def get_value(self, key: str, default_value: Any = None) -> Any:
        env_key = AppConfigConsts.CONFIG_L_ENV_PREFIX + key.upper()
        env_value = os.getenv(env_key)
        if env_value:
            return env_value
        result = self._local.get(key, default_value)
        return result

    def has_value(self, key: str) -> bool:
        try:
            self.get_value(key)
            return True
        except ValueError:
            return False

    def dump(self, full: bool = False) -> str:
        result = dump_object(self)
        return result


class ProjectConfigStore(object):
    def __init__(self):
        self._local = {}

    def get_local(self, section: str = AppConfigConsts.CONFIG_L_SECTION_NAME) -> ProjectConfig:
        result = self._local.get(section)
        if result:
            return result
        result = ProjectConfigImpl.create(section)
        self._local[section] = result
        return result


class ProjectConfigStoreGlobals(object):
    store = ProjectConfigStore()


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
        # ruff: noqa: PERF203
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


class ErrAbsConfig(AbsAppConfig):
    cfg_type = AppConfigConsts.CFG_TYPE_ERROR

    def __init__(self, name: str, ex: Exception):
        super().__init__(name, {"ex": ex})
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
        self._config = {}

    @classmethod
    def config_name(cls, what=AppConfigConsts.CONFIG_S_DEFAULT) -> str:
        result = None
        if what == AppConfigConsts.CONFIG_S_MAIN:
            result = AppConfigConsts.CONFIG_F_MAIN
        if result is None:
            raise ValueError(f'Config Name unknown: "{what}", cannot load')
        return result

    @classmethod
    def config_path(cls, what=AppConfigConsts.CONFIG_S_DEFAULT) -> str:
        name = cls.config_name(what)
        fn = os.path.join(AppConfigConsts.CONFIG_F_ROOT, name)
        result = os.path.normpath(fn)
        return result

    def load_config(self, what=AppConfigConsts.CONFIG_S_DEFAULT) -> AppConfig:
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


class AppConfigStoreGlobals:
    store = AppConfigStore()


def unload_all_configs():
    AppConfigStoreGlobals.store = AppConfigStore()


def get_config_store() -> AppConfigStore:
    return AppConfigStoreGlobals.store
