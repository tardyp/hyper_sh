import os
import subprocess
from unittest.case import SkipTest

from hypercompose.api import Hyper


def assertSetup():
    try:
        Hyper.guess_config()
    except RuntimeError:
        raise SkipTest("no default config is detected")


def test_simple_compose():
    assertSetup()
    cwd = os.path.dirname(__file__)
    subprocess.check_call(["hyper-compose", "up", '-d'], cwd=cwd)
    subprocess.check_call(["hyper-compose", "down"], cwd=cwd)
    subprocess.check_call(["hyper-compose", "rm"], cwd=cwd)
