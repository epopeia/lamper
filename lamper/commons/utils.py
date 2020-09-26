import json
import re

from requests import Response
from requests.structures import CaseInsensitiveDict

from lamper import config
from lamper.exceptions import UnprocessableException, BadRequestException, CustomException

"""
Converters Helpers
"""


# convert string to json, case has any failure on json decoding,
# we will return JSONDecodeError
def str_to_json(text):
    if text:
        return json.loads(text)
    return text


"""
HTTP Helpers
"""


# return query string parameters from event variable
def get_query_string_parameters(event, required=True):
    ret = event.get('queryStringParameters', None)
    if required and not ret:
        raise BadRequestException()
    return CaseInsensitiveDict(ret) or {}


# return path parameters from event variable
def get_path_parameters(event, required=True):
    ret = event.get('pathParameters', None)
    if required and not ret:
        raise BadRequestException()
    return CaseInsensitiveDict(ret) or {}


# return body from event variable
def get_body(event, required=True):
    ret = event.get('body', None)
    if required and not ret:
        raise BadRequestException()
    return CaseInsensitiveDict(ret) or {}


# customize a response.text to json. If a 204 status_code founded return ''
# case not success response, return a ErrorException
def customize_response(response: Response, logger=config.get_logger(__name__), show_reason=False):
    if response.ok:
        if response.status_code == 204:
            return ''
        return response.json()
    else:
        logger.error(f'status_code: {response.status_code}, reason: {response.reason}')
        raise CustomException(
            response.status_code,
            show_reason and response.reason or None)


"""
Validators Helpers
"""


# check if exists any errors and return a UnprocessableException
def check_errors(errors, logger=config.get_logger(__name__)):
    if errors:
        logger.info("SOME FIELDS CONTAINS ERRORS")
        raise UnprocessableException(errors)


# marshmallow only number validation. ex.: `validate=check_only_numbers`
def check_only_numbers(value, msg=None):
    if not re.match(r"^[0-9]*$", value):
        raise ValidationError(msg or 'Is not a valid number.')
