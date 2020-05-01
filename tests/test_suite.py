import unittest

from tests.test_common import CommonTest


def load_test(c):
    return  unittest.defaultTestLoader.loadTestsFromTestCase(c)


def all_tests():
    test_suite = unittest.TestSuite()
    test_suite.addTest(load_test(CommonTest))
    return test_suite


if __name__ == '__main__':
    suite = all_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)
