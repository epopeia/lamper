from json import JSONDecodeError
from unittest import TestCase

from lamper.commons.utils import str_to_json


class TestUtilsConverters(TestCase):
    def setUp(self):
        self.valid_json = '{"id": 1234, "name": "Maicon Keller"}'
        self.expected_json = {'id': 1234, 'name': 'Maicon Keller'}

    def test_str_to_json_when_correct_input(self):
        result = str_to_json(self.valid_json)
        self.assertEqual(self.expected_json, result)

    def test_str_to_json_when_empty_or_none_input(self):
        self.assertEqual('', str_to_json(''))
        self.assertEqual(None, str_to_json(None))

    def test_str_to_json_when_invalid_json(self):
        with self.assertRaises(JSONDecodeError) as context:
            str_to_json('Invalid json object')
        self.assertEqual('Invalid json object', context.exception.doc)
