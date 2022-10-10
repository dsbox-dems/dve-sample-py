import logging
import re
import os
import sys
import unittest
import json

from dve.config import conf

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



    def setUp(self):
        # self.conf_dir = os.environ['CONFIG_DIR']
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()


