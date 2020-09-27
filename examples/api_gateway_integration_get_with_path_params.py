import requests
from marshmallow import Schema, fields

from lamper import core
from lamper import decorators
from lamper.exceptions import HttpBaseException
from lamper.https import HttpResponse
from lamper.config import get_logger

logger = get_logger(__name__, level='DEBUG')

#MODELS
class ExamplePathParam(Schema):
    customer_id = fields.Str()
    name = fields.Str()


class ExampleResponse(Schema):
    customer = fields.Str()
    name = fields.Str()

#SERVICE
def example_service(event):
    return core.callapi(
        path_param_schema=ExamplePathParam,
        response_schema=ExampleResponse,
        http_method=core.HttpMethod.GET,
        api_url='http://echo.jsontest.com/customer/{customer_id}/name/{name}',
        event=event)


# ROUTES
routes = decorators.Mapping()


@routes.get('/example')
def my_example(event, context):
    try:
        response = example_service(event)
    except HttpBaseException as e:
        return e.get_response()

    return HttpResponse.success(response)


def lambda_handler(event, context):
    return core.registry_components(event=event,
                                    context=context,
                                    routes=routes, )

#TEST LAMBDA HANDLER
if __name__ == '__main__':
    event = {
        'resource': '/example',
        'httpMethod': 'GET',
        'pathParameters': {'customer_id': '1', 'name': 'EPOPEIA'}
    }

    result = lambda_handler(event, None)


# 2020-09-27:08:19:54,937 INFO     [core.py:72] calling url:http://echo.jsontest.com/customer/1/name/EPOPEIA
# 2020-09-27:08:19:54,937 INFO     [core.py:73] with headers:
# 2020-09-27:08:19:54,937 INFO     [core.py:74] None
# 2020-09-27:08:19:54,937 INFO     [core.py:75] with payload:
# 2020-09-27:08:19:54,940 DEBUG    [connectionpool.py:226] Starting new HTTP connection (1): echo.jsontest.com:80
# send: b'GET /customer/1/name/EPOPEIA HTTP/1.1\r\nHost: echo.jsontest.com\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
# reply: 'HTTP/1.1 200 OK\r\n'
# header: Access-Control-Allow-Origin: *
# header: Content-Type: application/json
# header: X-Cloud-Trace-Context: 6e1a7b378c247fa827bff0494fcc4a7a
# header: Date: Sun, 27 Sep 2020 11:19:55 GMT
# header: Server: Google Frontend
# header: Content-Length: 45
# 2020-09-27:08:19:55,296 DEBUG    [connectionpool.py:433] http://echo.jsontest.com:80 "GET /customer/1/name/EPOPEIA HTTP/1.1" 200 45
# 2020-09-27:08:19:55,297 INFO     [core.py:88] request : <PreparedRequest [GET]>
# 2020-09-27:08:19:55,298 INFO     [core.py:89] response text: {
#    "name": "EPOPEIA",
#    "customer": "1"
# }
#
# 2020-09-27:08:19:55,298 INFO     [core.py:97] response:
# 2020-09-27:08:19:55,299 INFO     [core.py:98] {'name': 'EPOPEIA'}
# 2020-09-27:08:19:55,299 INFO     [https.py:22] response to api gateway:
# 2020-09-27:08:19:55,299 INFO     [https.py:23] {'body': '{"name": "EPOPEIA"}', 'statusCode': 200}
