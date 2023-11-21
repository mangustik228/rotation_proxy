import os


def test_MODE():
    assert os.getenv("MODE") == "TEST"
