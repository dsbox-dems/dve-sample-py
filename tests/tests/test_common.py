import logging

import unittest
import os

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


def conf_dir(env_key, default_value):
    return os.path.expanduser(os.getenv(env_key, default_value))


data_dir = conf_dir('PC_DATA_DIR', "~/work/vs/dve/sample-py/data/def")


class CommonTest(unittest.TestCase):

    def test_default_data_path_defined(self):
        log.debug("+ data_dir:"+data_dir)
        self.assertIsNotNone(data_dir)

    def test_default_data_path(self):
        self.assertIsNotNone(os.path.exists(data_dir))
        self.assertIsNotNone(os.path.isdir(data_dir))
        log.debug("+ data_dir: {} -> {}".format(data_dir, os.path.realpath(data_dir)))

    def test_config_loader(self):
        self.assertIsNotNone(True)

    def setUp(self):
        # self.conf_dir = os.environ['CONFIG_DIR']
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
