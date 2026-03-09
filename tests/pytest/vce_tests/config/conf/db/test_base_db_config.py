import logging
import sys
import unittest

from vce.config import conf

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)


class ConfigDbTest(unittest.TestCase):
    warnings_no = 0

    def test_config_demo(self):
        actual_db_config = conf.get_config().db("demo")
        self.assertIsNotNone(actual_db_config)
        actual_config = actual_db_config.config
        self.assertIsNotNone(actual_config)
        actual_uri = actual_db_config.uri()
        self.assertRegex(actual_uri, "://")
        log.debug("+++ CONFIG MODEL (demo):" + actual_db_config.dump(True))
        log.debug("+++ CONFIG URI   (demo):" + actual_db_config.dump())

    def test_config_demo_my(self):
        actual_db_config = conf.get_config().db("demo_my")
        self.assertIsNotNone(actual_db_config)
        actual_config = actual_db_config.config
        self.assertIsNotNone(actual_config)
        actual_uri = actual_db_config.uri()
        self.assertRegex(actual_uri, "://")
        self.assertRegex(actual_uri, "^mysql")
        log.debug("+++ CONFIG MODEL (demo_my):" + actual_db_config.dump(True))
        log.debug("+++ CONFIG URI   (demo_my):" + actual_db_config.dump())

    def test_config_demo_pg(self):
        actual_db_config = conf.get_config().db("demo_pg")
        self.assertIsNotNone(actual_db_config)
        actual_config = actual_db_config.config
        self.assertIsNotNone(actual_config)
        actual_uri = actual_db_config.uri()
        self.assertRegex(actual_uri, "://")
        self.assertRegex(actual_uri, "^postgresql")
        log.debug("+++ CONFIG MODEL (demo_pg):" + actual_db_config.dump(True))
        log.debug("+++ CONFIG URI   (demo_pg):" + actual_db_config.dump())

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
