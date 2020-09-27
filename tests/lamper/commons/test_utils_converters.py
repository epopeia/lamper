from json import JSONDecodeError

import pytest

from lamper.commons.utils import str_to_json

valid_json = '{"id": 1234, "name": "Maicon Keller"}'
expected_json = {'id': 1234, 'name': 'Maicon Keller'}


def test_str_to_json_when_correct_input():
    result = str_to_json(valid_json)
    assert expected_json == result


def test_str_to_json_when_empty_or_none_input():
    assert '' == str_to_json('')
    assert None == str_to_json(None)


def test_str_to_json_when_invalid_json():
    with pytest.raises(JSONDecodeError):
        str_to_json('Invalid json object')

