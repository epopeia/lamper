import json
from enum import Enum
from pprint import pformat

import marshmallow
import requests
from marshmallow import Schema

from lamper import exceptions, https, config
from marshmallow.utils import get_value

logger = config.get_logger(__name__)


def registry_components(event=None, context=None, routes=None, default_response_headers=None):
    https.default_response_headers = default_response_headers
    resource = event.get('resource', None)
    assert resource, 'resource is required'

    method = event.get('httpMethod', None)
    assert method, 'httpMethod is required'

    function = routes.routes.get(resource + method, None)
    assert function, 'Invalid resource path resource %s method %s' % (resource, method)

    return function(event, context)


class HttpMethod(Enum):
    GET = requests.get
    POST = requests.post
    PUT = requests.put
    DELETE = requests.delete


def callapi(request_schema: Schema = None,
            response_schema: Schema = None,
            path_param_schema: Schema = None,
            querystring_schema: Schema = None,
            api_url: str = None,
            http_method: HttpMethod = None,
            request_headers: dict = None,
            event: dict = None):
    """
    :param request_schema: marshmallow schema to be used request body
    :param response_schema: marshmallow schema to be used response body
    :param path_param_schema: marshmallow schema with values to be replaced in api_url param
    :param querystring_schema: marshmallow schema to be used querystring
    :param api_url: url with address api, placeholders {xxx}  to be replaced to path_params_schema values
    :param http_method: method for api request
    :param request_headers: request headers to request
    :param event: original event from api gateway proxy integration
    :return:
    """
    payload = None
    params = {'params': None}
    text_body = get_value(event, 'body')
    if path_param_schema:
        api_url = get_url_with_params(api_url, event, path_param_schema)

    if querystring_schema:
        params = get_querystring_params(event, querystring_schema)

    if request_schema:
        params = get_json_body_payload(request_schema, text_body)

    logger.info(f'calling url:{api_url}')
    logger.info('with headers:')
    logger.info(pformat(request_headers))

    res = http_method(api_url, **params, headers=request_headers)

    logger.info(f'request : {res.request}')
    logger.info(f'response text: {res.text}')
    try:
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        if res.status_code == 404:
            raise exceptions.NotFoundException()
        raise exceptions.UnprocessableException(res.text)

    if response_schema:
        result = response_schema().dump(res.json())
        logger.info('response:')
        logger.info(pformat(result))
        return result


def get_json_body_payload(request_schema, text_body):
    if not text_body:
        text_body = '{}'
    data = json.loads(text_body)
    schema = request_schema()
    try:
        params = {'json': schema.load(data)}
    except marshmallow.ValidationError as e:
        raise exceptions.UnprocessableException(e.messages)
    logger.info(pformat(f'with payload: {params}'))
    return params


def get_querystring_params(event, querystring_schema):
    qs_schema = querystring_schema()
    qs_params = get_value(event, 'queryStringParameters')
    try:
        params = {'params': qs_schema.load(qs_params)}
    except marshmallow.ValidationError as e:
        raise exceptions.UnprocessableException(e.messages)
    return params


def get_url_with_params(api_url, event, path_param_schema):
    param_schema = path_param_schema()
    event_params = get_value(event, 'pathParameters', {})

    try:
        params_data = param_schema.load(event_params)
    except marshmallow.ValidationError as e:
        raise exceptions.UnprocessableException(e.messages)

    for param, value in params_data.items():
        api_url = api_url.replace(f'{{{param}}}', value)
    return api_url
