import requests_mock
from marshmallow import Schema, fields

from lamper import core


def test_callapi(requests_mock):
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
