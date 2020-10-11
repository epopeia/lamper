from collections import OrderedDict

from lamper.exceptions import HttpBaseException, CustomException
from lamper.https import HttpResponse, HttpStatusCode


def test_get_response():
    response = HttpBaseException(HttpResponse.success()).get_response()
    assert response == {'statusCode': 200, 'body': None}


def test_get_response_with_body():
    response = HttpBaseException(HttpResponse.success(), body={'message': 'ok'}).get_response()
    assert response == {'statusCode': 200, 'body': '{"message": "ok"}'}


def test_get_response_bad_request():
    response = HttpBaseException(HttpResponse.bad_request()).get_response()
    assert response.get('statusCode') == 400


def test_get_response_unauthorized():
    response = HttpBaseException(HttpResponse.unauthorized()).get_response()
    assert response.get('statusCode') == 401

def test_get_response_error():
    response = HttpBaseException(HttpResponse.error()).get_response()
    assert response.get('statusCode') == 500

def test_custom_exception():
    response = CustomException(HttpStatusCode.ERROR, None).get_response()
    assert response.get('statusCode') == 500

