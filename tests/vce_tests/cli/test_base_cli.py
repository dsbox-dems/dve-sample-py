import logging
import sys
import io
import pytest
import unittest
from contextlib import redirect_stdout

from vce.cli import main

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)


class BaseCliTest(unittest.TestCase):
    warnings_no = 0

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    @unittest.skip("cli: not ready yet")
    def test_simple_args(self):
        argv = ["-v", "--exec", "main", "--cmd", "test"]
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        assert argv[0] in out.getvalue()

    @unittest.skip("cli: not ready yet")
    def test_auto_script(self):
        argv = ["-v", "--exec", "main", "--cmd", "auto", "--name", "test"]
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        assert "auto:test" in out.getvalue()

    @pytest.mark.skip(reason="feature delayed: numactl support ...")
    @unittest.skip("feature delayed: numactl support")
    def test_auto_spawn(self):
        argv = ["-v", "--exec", "main", "--cmd", "auto", "--name", "auto"]
        log.debug("+++ cli.main:" + str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        assert "auto:spawn" in out.getvalue()

    def setUp(self):
        # self.conf_dir = os.environ['CONFIG_DIR']
        log = logging.getLogger(__name__)
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
