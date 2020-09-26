import json
from pprint import pformat

import marshmallow
import requests
from lamper import exceptions, https, config
from marshmallow.utils import get_value

logger = config.logger(__name__)
def registry_components(event=None, context=None, routes=None, default_response_headers=None):

    https.default_response_headers = default_response_headers
    resource = event.get('resource', None)
    assert resource, 'Resource is required'

    method = event.get('httpMethod', None)
    assert method, 'HttpMethod is required'

    function = routes.routes.get(resource + method, None)
    assert function, 'Invalid resource path resource %s method %s' % (resource, method)

    return function(event, context)


def callapi(request_schema=None,
            response_schema=None,
            path_param_schema=None,
            querystring_schema=None,
            api_url=None,
            post=None,
            get=None,
            put=None,
            delete=None,
            request_headers=None,
            event=None):

    payload = None
    text_body = get_value(event, 'body')
    complete_url = api_url
    if path_param_schema:
        param_schema = path_param_schema()
        event_params = get_value(event, 'pathParameters', {})

        try:
            params_data = param_schema.load(event_params)
        except marshmallow.ValidationError as e:
            raise exceptions.UnprocessableException(e.messages)

        for param, value in params_data.items():
            complete_url = complete_url.replace(f'{{{param}}}', value)

    if querystring_schema:
        qs_schema = querystring_schema()
        qs_params = get_value(event, 'queryStringParameters')

        try:
            payload = qs_schema.load(qs_params)
        except marshmallow.ValidationError as e:
            raise exceptions.UnprocessableException(e.messages)

    if request_schema:
        data = json.loads(text_body)
        schema = request_schema()

        try:
            payload = schema.load(data)
        except marshmallow.ValidationError as e:
            raise exceptions.UnprocessableException(e.messages)

        logger.info(pformat(f'with payload: {payload}'))

    logger.info(f'calling url:{complete_url}')
    logger.info('with headers:')
    logger.info(pformat(request_headers))
    logger.info('with payload:')
    if payload:
        logger.info(pformat(payload))

    if post:
        res = post(complete_url, json=payload, headers=request_headers)
    if put:
        res = put(complete_url, json=payload, headers=request_headers)
    if get:
        res = get(complete_url, params=payload, headers=request_headers)
    if delete:
        res = delete(complete_url, params=payload, headers=request_headers)

    logger.info(f'request : {res.request}')
    logger.info(f'response text: {res.text}')
    try:
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise exceptions.UnprocessableException(res.text)

    if response_schema:
        result = response_schema().dump(res.json())
        logger.info('response:')
        logger.info(pformat(result))
        return result
