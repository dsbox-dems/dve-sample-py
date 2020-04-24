from datetime import datetime
import unittest
from common.common import *
import os


class CommonTest(unittest.TestCase):

    def test_config_loader(self):
        self.assertIsNotNone(True)


    def setUp(self):
        self.conf_dir = os.environ['CONFIG_DIR']

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
