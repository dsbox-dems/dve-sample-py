import re
from abc import ABC, abstractmethod


class DbConfigConsts(object):
    DB_TYPE_GENERIC = "generic"
    DB_TYPE_MYSQL = "mysql"
    DB_TYPE_POSTGRESQL = "postgresql"


class DbConfig(ABC):
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

    @staticmethod
    def dump_object_uri(uri: str) -> str:
        result = re.sub("://([^:]*):([^@]*)@", r"://\1:***@", uri)
        return result


class DbConfigs(object):
    pass
