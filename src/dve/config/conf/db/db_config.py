from dve.config.conf.db import DbConfig
from dve.config.conf import AppConfigEx

import vce.config.conf.db as vce_conf_db


class DbConfigImpl(DbConfig):
    def __init__(self, name: str, inner: vce_conf_db.DbConfig):
        super().__init__(name)
        self.inner = inner

    def uri(self) -> str:
        return self.inner.uri()

    def dump(self, full: bool = False) -> str:
        return self.inner.dump(full)

    @classmethod
    def create(cls, name: str, inner: vce_conf_db.DbConfig) -> DbConfig:
        result = DbConfigImpl(name, inner)
        return result


class DbConfigFactory(object):
    @classmethod
    def get_instance(cls, app_config: AppConfigEx, name: str) -> DbConfig:
        db_config_cache = app_config.db_config_cache()
        if name in db_config_cache:
            return db_config_cache[name]
        else:
            inner = app_config.db_inner(name)
            db_config = DbConfigImpl.create(name, inner)
            db_config_cache[name] = inner
            return db_config
