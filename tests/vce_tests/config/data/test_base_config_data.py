import logging
import os
import sys
import unittest

from vce.config.data import cfd

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)

CHECK_EXISTING = False


class ConfigDataTest(unittest.TestCase):
    warnings_no = 0

    # noinspection PyUnusedLocal
    def verify_dir(self, name, path, exists, isdir):
        if not (exists and isdir):
            self.warnings_no = self.warnings_no + 1
        return not CHECK_EXISTING or (exists and isdir)

    def log_dir(self, name, path):
        exists = os.path.exists(path)
        isdir = os.path.isdir(path)

        mess = "+++ {}: {} -> {}".format(name, path, os.path.realpath(path))

        if exists and isdir:
            log.debug(mess)
        else:
            log.warning(mess + "!NOTFND")
        return self.verify_dir(name, path, exists, isdir)

    def test_default_data_home_defined(self):
        log.debug("+++ DATA_HOME:" + cfd().DATA_HOME)
        self.assertIsNotNone(cfd().DATA_HOME)

    def test_default_data_home(self):
        self.assertTrue(self.log_dir("DATA_HOME", cfd().DATA_HOME))

    def test_default_data_work_defined(self):
        log.debug("+++ DATA_WORK:" + cfd().DATA_WORK)
        self.assertIsNotNone(cfd().DATA_WORK)

    def test_default_data_work(self):
        self.assertTrue(self.log_dir("DATA_WORK", cfd().DATA_WORK))

    def test_default_data_logs_defined(self):
        log.debug("+++ DATA_LOGS:" + cfd().DATA_LOGS)
        self.assertIsNotNone(cfd().DATA_LOGS)

    def test_default_data_logs(self):
        self.assertTrue(self.log_dir("DATA_LOGS", cfd().DATA_LOGS))

    def test_default_data_host_defined(self):
        log.debug("+++ DATA_HOST:" + cfd().DATA_HOST)
        self.assertIsNotNone(cfd().DATA_HOST)

    def test_default_data_host(self):
        self.assertTrue(self.log_dir("DATA_HOST", cfd().DATA_HOST))

    def test_default_data_user_defined(self):
        log.debug("+++ DATA_USER:" + cfd().DATA_USER)
        self.assertIsNotNone(cfd().DATA_USER)

    def test_default_data_user(self):
        self.assertTrue(self.log_dir("DATA_USER", cfd().DATA_USER))

    def test_default_data_desk_defined(self):
        log.debug("+++ DATA_DESK:" + cfd().DATA_DESK)
        self.assertIsNotNone(cfd().DATA_DESK)

    def test_default_data_desk(self):
        self.assertTrue(self.log_dir("DATA_DESK", cfd().DATA_DESK))

    def test_default_data_test_defined(self):
        log.debug("+++ DATA_TEST:" + cfd().DATA_TEST)
        self.assertIsNotNone(cfd().DATA_TEST)

    def test_default_data_test(self):
        self.assertTrue(self.log_dir("DATA_TEST", cfd().DATA_TEST))

    def test_default_data_temp_defined(self):
        log.debug("+++ DATA_TEMP:" + cfd().DATA_TEMP)
        self.assertIsNotNone(cfd().DATA_TEMP)

    def test_default_data_temp(self):
        self.assertTrue(self.log_dir("DATA_TEMP", cfd().DATA_TEMP))

    def test_config_loader(self):
        o = cfd()
        self.assertIsNotNone(o)
        log.debug("+++ cfd: " + str(o))

    def setUp(self):
        # self.conf_dir = os.environ['CONFIG_DIR']
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
