import logging
import sys
import io
import pytest
import unittest
from contextlib import redirect_stdout

from vce.cli import main
from vce.config import conf
from vce.common.util import environ

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)


class BaseCliTest(unittest.TestCase):
    warnings_no = 0

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    def x_test_runner_args(self):
        argv = ["-v", "--exec", "demo", "--cmd", "test"]
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        s = out.getvalue()    
        assert argv[0] in out.getvalue()

    def test_auto_default(self):
        argv = []
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        assert "auto:test-00" in out.getvalue()

    def x_test_auto_environ(self):
        with environ.modified_environ(
            X_E_AUTO="auto:test-01",
        ):
            argv = []
            log.debug("+++ cli.main:" + str(argv))
            out = io.StringIO()
            with redirect_stdout(out):
                main(argv)
                assert "auto:test-01" in out.getvalue()

    def x_test_auto_script(self):
        argv = ["--name", "test-02"]
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        assert "auto:test-02" in out.getvalue()

    def x_test_auto_spawn(self):
        argv = ["--name", "demo-01"]
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        assert "auto:spawn" in out.getvalue()

    def setUp(self):
        conf.AppConfigs.unload_all()
        pass

    def tearDown(self):
        conf.AppConfigs.unload_all()
        pass


if __name__ == "__main__":
    unittest.main()
