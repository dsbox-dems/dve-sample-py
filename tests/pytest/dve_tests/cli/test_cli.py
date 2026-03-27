import logging
import sys
import io
import pytest
import unittest
from contextlib import redirect_stdout

from dve.cli import main

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)


class CliTest(unittest.TestCase):
    warnings_no = 0

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    def test_runner_args(self):
        argv = ["-v", "--exec", "main", "--cmd", "test"]
        log.debug("+++ cli.main: %s", str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        s = out.getvalue()
        assert argv[0] in s

    def test_auto_check(self):
        argv = ["--name", "test-01"]
        log.debug("+++ cli.main: %s", str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        s = out.getvalue()
        assert "'job_name': 'test-01'" in s

    def test_runner_check(self):
        argv = ["-v", "--exec", "main", "--cmd", "auto", "--name", "test-01"]
        log.debug("+++ cli.main: %s", str(argv))
        out = io.StringIO()
        with redirect_stdout(out):
            main(argv)
        s = out.getvalue()
        assert "'job_name': 'test-01'" in s

    def setUp(self):
        # self.conf_dir = os.environ['CONFIG_DIR']
        logging.getLogger(__name__)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
