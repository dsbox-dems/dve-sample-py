import logging
import re
import os
import sys
import unittest
import json

from dve.config import conf
from dve.common.util import environ

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)

CHECK_EXISTING = False


class ConfigModelTest(unittest.TestCase):
    warnings_no = 0

    def dump_config(self, config):
        msg = json.dumps(config, indent=4, sort_keys=False, default=str)
        result = re.sub('"password": *"[^"]*",','"password": "***"', msg)
        return result

    def test_config_name(self):
        actual_name = conf.config_name()
        log.debug("+++ CONFIG NAME (default):" + actual_name)
        self.assertIsNotNone(actual_name)

    def test_config_path(self):
        actual_path = conf.config_path()
        log.debug("+++ CONFIG PATH (default):" + actual_path)
        self.assertIsNotNone(actual_path)
        self.assertTrue(os.path.isfile(actual_path))

    def test_load_config(self):
        actual_config = conf.load_config()
        self.assertIsNotNone(actual_config)
        log.debug("+++ CONFIG MODEL (default):" + self.dump_config(actual_config))

    def test_get_config(self):
        actual_config = conf.get_config()
        cached_config = conf.get_config()
        self.assertEqual(actual_config, cached_config)
        log.debug(f'+++ CONFIG MODEL ID (default): {id(actual_config)}, {id(cached_config)}')

    def test_get_demo_my(self):
        config = conf.get_config()
        db_config = config["data"]["db"]["demo_my"]
        self.assertIsNotNone(db_config)
        log.debug(f'+++ CONFIG DB (demo.my): {self.dump_config(db_config)} ')

    def test_env_my_defaults(self):
        exp = {
           'host':  "localhost",
           'port':  "3306",
           'user':  "demo",
           'database':  "demo",
        }
        config = conf.get_config()
        act = config["data"]["db"]["demo_my"]
        log.debug(f'+++ CONFIG DB (demo.my): {self.dump_config(act)} ')
        self.assertEqual(exp['host'],act['host'])
        self.assertEqual(exp['port'],act['port'])
        self.assertEqual(exp['user'],act['user'])
        self.assertEqual(exp['database'],act['database'])

    def test_env_pg_defaults(self):
        exp = {
           'host':  "localhost",
           'port':  "5432",
           'user':  "demo",
           'database':  "demo",
        }
        config = conf.get_config()
        act = config["data"]["db"]["demo_pg"]
        log.debug(f'+++ CONFIG DB (demo.pg): {self.dump_config(act)} ')
        self.assertEqual(exp['host'],act['host'])
        self.assertEqual(exp['port'],act['port'])
        self.assertEqual(exp['user'],act['user'])
        self.assertEqual(exp['database'],act['database'])

    def test_env_my_override(self):
        exp = {
           'host':  "_host_",
           'port':  "_port_",
           'user':  "_user_",
           'password':  "_password_",
           'database':  "_database_"
        }
        with environ.modified_environ(
            X_DB_DEMO_HOST=exp['host'],
            X_DB_DEMO_PORT=exp['port'],
            X_DB_DEMO_USER=exp['user'],
            X_DB_DEMO_PASSWORD=exp['password'],
            X_DB_DEMO_DATABASE=exp['database']
        ):

            config = conf.get_config()
            act = config["data"]["db"]["demo_my"]
            log.debug(f'+++ CONFIG DB (demo.my): {self.dump_config(act)} ')
            self.assertEqual(exp['host'],act['host'])
            self.assertEqual(exp['port'],act['port'])
            self.assertEqual(exp['user'],act['user'])
            self.assertEqual(exp['password'],act['password'])
            self.assertEqual(exp['database'],act['database'])

    def test_env_pg_override(self):
        exp = {
           'host':  "_host_",
           'port':  "_port_",
           'user':  "_user_",
           'password':  "_password_",
           'database':  "_database_"
        }
        with environ.modified_environ(
            X_DB_DEMO_HOST=exp['host'],
            X_DB_DEMO_PORT=exp['port'],
            X_DB_DEMO_USER=exp['user'],
            X_DB_DEMO_PASSWORD=exp['password'],
            X_DB_DEMO_DATABASE=exp['database']
        ):

            config = conf.get_config()
            act = config["data"]["db"]["demo_pg"]
            log.debug(f'+++ CONFIG DB (demo.pg): {self.dump_config(act)} ')
            self.assertEqual(exp['host'],act['host'])
            self.assertEqual(exp['port'],act['port'])
            self.assertEqual(exp['user'],act['user'])
            self.assertEqual(exp['password'],act['password'])
            self.assertEqual(exp['database'],act['database'])


    def setUp(self):
        conf.config_unload_all()
        pass

    def tearDown(self):
        conf.config_unload_all()
        pass


if __name__ == "__main__":
    unittest.main()


