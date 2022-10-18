import logging
import re
import os
import sys
import unittest
import json

from dve.config.conf.db import db_config
from dve.common.util import environ

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)

CHECK_EXISTING = False


class ConfigDbTest(unittest.TestCase):
    warnings_no = 0

    def dump_config(self, config):
        msg = json.dumps(config, indent=4, sort_keys=False, default=str)
        result = re.sub('"password": *"[^"]*",','"password": "***"', msg)
        return result

    def dump_uri(self, uri):
        result = re.sub('://([^:]*):([^@]*)@',r"://\1:***@", uri)
        return result

    def test_config_demo(self):
        actual_db_config = db_config.get_db_config("demo")
        self.assertIsNotNone(actual_db_config)
        actual_config = actual_db_config.config
        self.assertIsNotNone(actual_config)
        actual_uri = actual_db_config.uri()
        self.assertRegex(actual_uri,'://')
        log.debug("+++ CONFIG MODEL (demo):" + self.dump_config(actual_config))
        log.debug("+++ CONFIG URI   (demo):" + self.dump_uri(actual_uri))

    def test_config_demo_my(self):
        actual_db_config = db_config.get_db_config("demo_my")
        self.assertIsNotNone(actual_db_config)
        actual_config = actual_db_config.config
        self.assertIsNotNone(actual_config)
        actual_uri = actual_db_config.uri()
        self.assertRegex(actual_uri,'://')
        self.assertRegex(actual_uri,'^mysql')
        log.debug("+++ CONFIG MODEL (demo_my):" + self.dump_config(actual_config))
        log.debug("+++ CONFIG URI   (demo_my):" + self.dump_uri(actual_uri))

    def test_config_demo_pg(self):
        actual_db_config = db_config.get_db_config("demo_pg")
        self.assertIsNotNone(actual_db_config)
        actual_config = actual_db_config.config
        self.assertIsNotNone(actual_config)
        actual_uri = actual_db_config.uri()
        self.assertRegex(actual_uri,'://')
        self.assertRegex(actual_uri,'^postgresql')
        log.debug("+++ CONFIG MODEL (demo_pg):" + self.dump_config(actual_config))
        log.debug("+++ CONFIG URI   (demo_pg):" + self.dump_uri(actual_uri))



    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()


