from dve.config import conf

DB_TYPE_GENERIC = "generic"
DB_TYPE_MYSQL = "mysql"
DB_TYPE_POSTGRESQL = "postgresql"

DB_REG_CLASSES = {
    DB_TYPE_MYSQL: lambda name: MyDbConfig.create(name),
    DB_TYPE_POSTGRESQL: lambda name: PgDbConfig.create(name),
}


class DbConfig(object):

    db_type = DB_TYPE_GENERIC

    @classmethod
    def get_config(cls, name: str) -> dict:
        app_config = conf.get_config()
        db_config = app_config["data"]["db"][name]
        return db_config

    def __init__(self, name: str):
        self.name = name
        self.config = self.get_config(name)

    def uri(self) -> str:
        raise ValueError("abstract")


class AbsDbConfig(DbConfig):
    @classmethod
    def get_direct(cls, name) -> DbConfig:
        db_config = cls.get_config(name)
        db_type = str(db_config["type"]).lower()
        db_create = DB_REG_CLASSES[db_type]
        result = db_create(name)
        return result

    @classmethod
    def get_delegate(cls, name, config) -> DbConfig:
        if not "alias" in config:
            raise ValueError(f"alias not found for db source: {name}")
        db_name = config["alias"]
        result = cls.get_direct(db_name)
        return result

    @classmethod
    def get_instance(cls, name: str) -> DbConfig:
        config = cls.get_config(name)
        if "alias" in config:
            result = RefDbConfig.create(name)
        else:
            result = cls.get_direct(name)
        return result

    def __init__(self, name):
        super().__init__(name)

    def uri(self) -> str:
        cfg = self.config
        if not "uri" in cfg:
            raise ValueError(f"alias not found for db source: {self.name}")
        uri = str(cfg["uri"])
        result = uri.format(cfg)
        return result


def db_config(name: str) -> DbConfig:
    result = AbsDbConfig.get_instance(name)
    return result


class RefDbConfig(AbsDbConfig):

    db_type = DB_TYPE_GENERIC

    def __init__(self, name: str):
        super().__init__(name)
        self.delegate = self.get_delegate(name, self.config)

    @classmethod
    def create(cls, name) -> AbsDbConfig:
        result = RefDbConfig(name)
        return result

    def uri(self) -> str:
        return self.delegate.uri()


class MyDbConfig(AbsDbConfig):

    db_type = DB_TYPE_MYSQL

    def __init__(self, name):
        super().__init__(name)

    @classmethod
    def create(cls, name) -> AbsDbConfig:
        result = MyDbConfig(name)
        return result


class PgDbConfig(AbsDbConfig):

    db_type = DB_TYPE_POSTGRESQL

    def __init__(self, name):
        super().__init__(name)

    @classmethod
    def create(cls, name) -> AbsDbConfig:
        result = PgDbConfig(name)
        return result
