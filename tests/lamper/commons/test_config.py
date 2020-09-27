import logging

from lamper.config import get_logger


def test_config_default_logger():
    my_logger = get_logger(__name__)
    assert logging.INFO == my_logger.level


def test_config_change_level():
    my_logger = get_logger(__name__, logging.WARNING)
    assert logging.WARNING == my_logger.level
