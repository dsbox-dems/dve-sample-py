import unittest

from vce_tests.common.test_common import CommonTest
from dve_tests.config import test_config
from dve_tests.cli.test_cli import CliTest
from dve_tests.resources import test_resources


def load_test(c):
    return unittest.defaultTestLoader.loadTestsFromTestCase(c)


def all_tests():
    test_suite = unittest.TestSuite()
    #    test_suite.addTests(load_test(CommonTest))
    #    test_suite.addTests(load_test(test_config.all_tests))
    #    test_suite.addTests(load_test(CliTest))
    #    test_suite.addTests(load_test(test_resources.all_tests))
    return test_suite


if __name__ == "__main__":
    suite = all_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)
