from enum import Enum
import json
from pprint import pformat
from lamper import config

default_response_headers = None

logger = config.get_logger(__name__)


def _custom_response(status_code, body=None):
    if isinstance(status_code, HttpStatusCode):
        status_code = status_code.value

    if isinstance(body, dict):
        body = json.dumps(body)
    response = dict(statusCode=status_code,  body=body)
    if default_response_headers:
        response['headers'] = default_response_headers

    if status_code < 400:
        logger.info('response to api gateway:')
        logger.info(pformat(response))
    return response


class HttpResponse(object):

    @staticmethod
    def success(body=None):
        return _custom_response(HttpStatusCode.OK, body)

    @staticmethod
    def created(body=None):
        return _custom_response(HttpStatusCode.CREATED, body)

    @staticmethod
    def no_content(body=None):
        return _custom_response(HttpStatusCode.NO_CONTENT, body)

    @staticmethod
    def bad_request(body=None):
        return _custom_response(HttpStatusCode.BAD_REQUEST, body)

    @staticmethod
    def unauthorized(body=None):
        return _custom_response(HttpStatusCode.UNAUTHORIZED, body)

    @staticmethod
    def forbidden(body=None):
        return _custom_response(HttpStatusCode.FORBIDDEN, body)

    @staticmethod
    def not_found(body=None):
        return _custom_response(HttpStatusCode.NOT_FOUND, body)

    @staticmethod
    def unprocessable(body=None):
        return _custom_response(HttpStatusCode.UNPROCESSABLE, body)

    @staticmethod
    def error(body=None):
        return _custom_response(HttpStatusCode.ERROR, body)

    @staticmethod
    def build(status_code, body=None):
        return _custom_response(status_code, body)


class HttpStatusCode(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    UNPROCESSABLE = 422
    ERROR = 500


class HttpMethod(Enum):
    DELETE = 'DELETE'
    GET = 'GET'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'
    POST = 'POST'
    PUT = 'PUT'
