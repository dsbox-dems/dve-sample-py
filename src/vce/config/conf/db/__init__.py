from abc import abstractmethod
from vce.config.conf import BaseConfig


class DbConfigConsts(object):
    DB_TYPE_GENERIC = "generic"
    DB_TYPE_SQLITE = "sqlite"
    DB_TYPE_MYSQL = "mysql"
    DB_TYPE_POSTGRESQL = "postgresql"


class DbConfig(BaseConfig):
    db_type = DbConfigConsts.DB_TYPE_GENERIC

    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config

    @abstractmethod
    def uri(self) -> str:
        pass

    @abstractmethod
    def dump(self, full: bool = False) -> str:
        pass


class DbConfigs(object):
    pass
