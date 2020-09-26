import unittest

from lamper.commons import constant


class TestConstant(unittest.TestCase):

    def test_correct_pi(self):
        self.assertEqual(3.14159265359, constant.PI)

    def test_correct_gravity(self):
        self.assertEqual(9.81, constant.GRAVITY)
