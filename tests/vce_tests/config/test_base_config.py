import unittest

from dve_tests.config.data.test_config_data import ConfigDataTest
from dve_tests.config.conf.test_config_model import ConfigModelTest


def load_test(c):
    return unittest.defaultTestLoader.loadTestsFromTestCase(c)


def all_tests():
    test_suite = unittest.TestSuite()
    #    test_suite.addTest(load_test(ConfigDataTest))
    #    test_suite.addTest(load_test(ConfigModelTest))
    return test_suite


if __name__ == "__main__":
    suite = all_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)
