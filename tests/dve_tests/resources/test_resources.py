import unittest

from dve_tests.resources.sql.test_resources_sql import ResourcesSqlTest


def load_test(c):
    return unittest.defaultTestLoader.loadTestsFromTestCase(c)


def all_tests():
    test_suite = unittest.TestSuite()
#    test_suite.addTest(load_test(ResourcesSqlTest))
    return test_suite


if __name__ == "__main__":
    suite = all_tests()
    runner = unittest.TextTestRunner()
    runner.run(suite)
