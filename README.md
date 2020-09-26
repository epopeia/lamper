[![Build Status](https://travis-ci.org/epopeia/lamper.svg?branch=master)](https://travis-ci.org/epopeia/lamper)
[![Coverage Status](https://coveralls.io/repos/github/epopeia/lamper/badge.svg)](https://coveralls.io/github/epopeia/lamper)

Lambda Helper to Api Gateway Lambda Integration
=======================

This lib provide a way to organize aws lambda integration with aws api gateway
using Models, Services and Controllers. 

Get It Now
==========
```bash
$ pip install lamper
```

```python
import requests
from marshmallow import Schema, fields

from lamper import core
from lamper import decorators
from lamper.exceptions import HttpBaseException
from lamper.https import HttpResponse
from lamper.config import get_logger

logger = get_logger(__name__, level='DEBUG')

#MODELS
class ExampleQueryString(Schema):
    idFromApiGateway = fields.Str(required=True, attribute="id")


class ExampleResponse(Schema):
    one_changed = fields.Str(attribute="one")
    key_changed = fields.Str(attribute="key")

#SERVICE
def example_service(event):
    return core.callapi(
        querystring_schema=ExampleQueryString,
        response_schema=ExampleResponse,
        get=requests.get,
        api_url='http://echo.jsontest.com/key/value/one/two',
        event=event)


# ROUTES /CONTROLLER
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
        'queryStringParameters': {'idFromApiGateway': '1'}
    }

    result = lambda_handler(event, None)


#SUCESS RESPONSE

# 2020-09-26:11:09:48,483 INFO     [core.py:72] calling url:http://echo.jsontest.com/key/value/one/two
# 2020-09-26:11:09:48,483 INFO     [core.py:73] with headers:
# 2020-09-26:11:09:48,483 INFO     [core.py:74] None
# 2020-09-26:11:09:48,483 INFO     [core.py:75] with payload:
# 2020-09-26:11:09:48,483 INFO     [core.py:77] {'id': '1'}
# 2020-09-26:11:09:48,486 DEBUG    [connectionpool.py:226] Starting new HTTP connection (1): echo.jsontest.com:80
# send: b'GET /key/value/one/two?id=1 HTTP/1.1\r\nHost: echo.jsontest.com\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
# reply: 'HTTP/1.1 200 OK\r\n'
# header: Access-Control-Allow-Origin: *
# header: Content-Type: application/json
# header: X-Cloud-Trace-Context: 6943045aaeac18beff6462204546f853
# header: Date: Sat, 26 Sep 2020 14:09:48 GMT
# header: Server: Google Frontend
# header: Content-Length: 39
# {'statusCode': 200, 'body': '{"key_changed": "value", "one_changed": "two"}'}
# 2020-09-26:11:09:48,702 DEBUG    [connectionpool.py:433] http://echo.jsontest.com:80 "GET /key/value/one/two?id=1 HTTP/1.1" 200 39
# 2020-09-26:11:09:48,703 INFO     [core.py:88] request : <PreparedRequest [GET]>
# 2020-09-26:11:09:48,703 INFO     [core.py:89] response text: {
#    "one": "two",
#    "key": "value"
# }
#
# 2020-09-26:11:09:48,703 INFO     [core.py:97] response:
# 2020-09-26:11:09:48,704 INFO     [core.py:98] {'key_changed': 'value', 'one_changed': 'two'}
# 2020-09-26:11:09:48,704 INFO     [https.py:22] response to api gateway:
# 2020-09-26:11:09:48,704 INFO     [https.py:23] {'body': '{"key_changed": "value", "one_changed": "two"}', 'statusCode': 200}
#



#TEST VALIDATES
    event = {
        'resource': '/example',
        'httpMethod': 'GET',
        'queryStringParameters': {'idFromApiGateway': None}
    }

    result = lambda_handler(event, None)

#RESPONSE
# 2020-09-26:11:16:19,832 INFO     [exceptions.py:18] response to api gateway:
# 2020-09-26:11:16:19,833 INFO     [exceptions.py:19] {'body': '{"idFromApiGateway": ["Field may not be null."]}', 'statusCode': 422}

```