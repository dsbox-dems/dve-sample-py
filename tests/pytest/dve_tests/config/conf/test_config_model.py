import logging
import sys
import unittest

from dve.config import conf
from vce.common.util import environ

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)


class ConfigModelTest(unittest.TestCase):
    warnings_no = 0

    def test_config_name(self):
        cfg = conf.get_config()
        actual_name = cfg.name
        log.debug("+++ CONFIG NAME (default):" + actual_name)
        assert actual_name is not None

    def test_load_config(self):
        cfg = conf.get_config()
        assert cfg is not None
        log.debug("+++ CONFIG MODEL (default):" + cfg.dump())

    def test_get_config(self):
        actual_config = conf.get_config()
        cached_config = conf.get_config()
        assert actual_config == cached_config
        log.debug(
            f"+++ CONFIG MODEL ID (default): {id(actual_config)}, {id(cached_config)}"
        )

    def test_get_demo_my(self):
        cfg = conf.get_config()
        db_config = cfg.get_value("data/db/demo_my")
        assert db_config is not None
        log.debug(f'+++ CONFIG DB (demo.my): {cfg.dump_value("data/db/demo_my")} ')

    def test_env_my_defaults(self):
        exp = {
            "host": "localhost",
            "port": "3306",
            "user": "demo",
            "database": "demo",
        }
        cfg = conf.get_config()
        act = cfg.get_value("data/db/demo_my")
        log.debug(f"+++ CONFIG DB (demo.my): {cfg.dump_object(act)}")
        assert exp["host"] == act["host"]
        assert exp["port"] == act["port"]
        assert exp["user"] == act["user"]
        assert exp["database"] == act["database"]

    def test_env_pg_defaults(self):
        exp = {
            "host": "localhost",
            "port": "5432",
            "user": "demo",
            "database": "demo",
        }
        cfg = conf.get_config()
        act = cfg.get_value("data/db/demo_pg")
        log.debug(f"+++ CONFIG DB (demo.pg): {cfg.dump_object(act)}")
        assert exp["host"] == act["host"]
        assert exp["port"] == act["port"]
        assert exp["user"] == act["user"]
        assert exp["database"] == act["database"]

    def test_env_my_override(self):
        exp = {
            "host": "_host_",
            "port": "_port_",
            "user": "_user_",
            "password": "_password_",
            "database": "_database_",
        }
        with environ.modified_environ(
            X_DB_DEMO_HOST=exp["host"],
            X_DB_DEMO_PORT=exp["port"],
            X_DB_DEMO_USER=exp["user"],
            X_DB_DEMO_PASSWORD=exp["password"],
            X_DB_DEMO_DATABASE=exp["database"],
        ):
            cfg = conf.get_config()
            act = cfg.get_value("data/db/demo_my")
            log.debug(f"+++ CONFIG DB(e) (demo.my): {cfg.dump_object(act)}")
            assert exp["host"] == act["host"]
            assert exp["port"] == act["port"]
            assert exp["user"] == act["user"]
            assert exp["password"] == act["password"]
            assert exp["database"] == act["database"]

    def test_env_pg_override(self):
        exp = {
            "host": "_host_",
            "port": "_port_",
            "user": "_user_",
            "password": "_password_",
            "database": "_database_",
        }
        with environ.modified_environ(
            X_DB_DEMO_HOST=exp["host"],
            X_DB_DEMO_PORT=exp["port"],
            X_DB_DEMO_USER=exp["user"],
            X_DB_DEMO_PASSWORD=exp["password"],
            X_DB_DEMO_DATABASE=exp["database"],
        ):
            cfg = conf.get_config()
            act = cfg.get_value("data/db/demo_pg")
            log.debug(f"+++ CONFIG DB(e) (demo.pg): {cfg.dump_object(act)}")
            assert exp["host"] == act["host"]
            assert exp["port"] == act["port"]
            assert exp["user"] == act["user"]
            assert exp["password"] == act["password"]
            assert exp["database"] == act["database"]

    def setUp(self):
        conf.AppConfigs.unload_all()

    def tearDown(self):
        conf.AppConfigs.unload_all()


if __name__ == "__main__":
    unittest.main()
