from src.config import settings


def test_mode():
    mode = settings.MODE

    assert mode == "TEST"
