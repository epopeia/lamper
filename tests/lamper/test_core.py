import json

import pytest
import requests_mock
from marshmallow import Schema, fields

from lamper import core, exceptions


def test_get_callapi(requests_mock):
    event = {
        'resource': '/example',
        'httpMethod': 'GET',
        'pathParameters': {'customer_id': '1', 'name': 'EPOPEIA'}
    }

    class ExamplePathParam(Schema):
        customer_id = fields.Str()
        name = fields.Str()

    class ExampleResponse(Schema):
        customer = fields.Str()
        name = fields.Str()

    api_url = 'http://echo.jsontest.com/customer/{customer_id}/name/{name}'
    requests_mock.get(api_url.replace('{customer_id}', '1').replace('{name}', 'EPOPEIA'),
                      json={"customer": "1", "name": "EPOPEIA"})
    result = core.callapi(
        path_param_schema=ExamplePathParam,
        response_schema=ExampleResponse,
        http_method=core.HttpMethod.GET,
        api_url=api_url,
        event=event)

    assert result.get('name') == "EPOPEIA"
    assert result.get('customer') == "1"


def test_get_callapi_with_error(requests_mock):
    event = {
        'resource': '/example',
        'httpMethod': 'GET',
        'pathParameters': {'customer_id': None}
    }

    class ExamplePathParam(Schema):
        customer_id = fields.Str()
        name = fields.Str()

    class ExampleResponse(Schema):
        customer = fields.Str()
        name = fields.Str()

    with pytest.raises(exceptions.UnprocessableException):
        api_url = 'http://echo.jsontest.com/customer/'
        requests_mock.get(api_url,
                          json={"customer": "1", "name": "EPOPEIA"})
        result = core.callapi(
            path_param_schema=ExamplePathParam,
            response_schema=ExampleResponse,
            http_method=core.HttpMethod.GET,
            api_url=api_url,
            event=event)


def test_get_callapi_with_error(requests_mock):
    event = {
        'resource': '/example',
        'httpMethod': 'GET',
        'pathParameters': {}
    }

    class ExamplePathParam(Schema):
        customer_id = fields.Str(required=True)
        name = fields.Str(required=True)

    class ExampleResponse(Schema):
        customer = fields.Str()
        name = fields.Str()

    with pytest.raises(exceptions.UnprocessableException):
        api_url = 'http://echo.jsontest.com/customer/'
        requests_mock.get(api_url,
                          json={"customer": "1", "name": "EPOPEIA"})
        core.callapi(
            path_param_schema=ExamplePathParam,
            response_schema=ExampleResponse,
            http_method=core.HttpMethod.GET,
            api_url=api_url,
            event=event)


def test_post_callapi_with_error(requests_mock):
    event = {
        'resource': '/example',
        'httpMethod': 'POST',
        'body': ''
    }

    class ExampleRequest(Schema):
        customer_id = fields.Str(required=True)
        name = fields.Str(required=True)

    class ExampleResponse(Schema):
        customer = fields.Str()
        name = fields.Str()

    with pytest.raises(exceptions.UnprocessableException):
        api_url = 'http://echo.jsontest.com/customer/'
        requests_mock.post(api_url,
                           json={"customer": "1", "name": "EPOPEIA"})
        core.callapi(
            request_schema=ExampleRequest,
            response_schema=ExampleResponse,
            http_method=core.HttpMethod.POST,
            api_url=api_url,
            event=event)
