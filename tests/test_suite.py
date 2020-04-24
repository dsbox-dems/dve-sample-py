import unittest

from tests.test_common import CommonTest


def all_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(CommonTest())
    return test_suite


if __name__ == '__main__':
    suite = all_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)
