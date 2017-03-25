from unittest.case import SkipTest

from hyper_sh import Client


def assertSetup():
    try:
        Client.guess_config()
    except RuntimeError:
        raise SkipTest("no default config is detected")


def test_list_images():
    assertSetup()
    c = Client("~/.hyper/config.json")  # guess config
    assert len(c.images()) != 0
