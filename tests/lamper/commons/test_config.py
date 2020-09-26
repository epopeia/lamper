import logging
from unittest import TestCase
from lamper.config import get_logger


class TestConfig(TestCase):

    def test_config_default_logger(self):
        my_logger = get_logger(__name__)
        self.assertEqual(logging.INFO, my_logger.level)

    def test_config_change_level(self):
        my_logger = get_logger(__name__, logging.WARNING)
        self.assertEqual(logging.WARNING, my_logger.level)
