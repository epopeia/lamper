from collections import OrderedDict

from lamper import exceptions
from lamper.https import HttpResponse, HttpStatusCode


def test_get_response():
    response = exceptions.HttpBaseException(HttpResponse.success()).get_response()
    assert response == {'statusCode': 200, 'body': None}


def test_get_response_with_body():
    response = exceptions.HttpBaseException(HttpResponse.success(), body={'message': 'ok'}).get_response()
    assert response == {'statusCode': 200, 'body': '{"message": "ok"}'}


def test_get_response_bad_request():
    response = exceptions.HttpBaseException(HttpResponse.bad_request()).get_response()
    assert response.get('statusCode') == 400


def test_get_response_unauthorized():
    response = exceptions.HttpBaseException(HttpResponse.unauthorized()).get_response()
    assert response.get('statusCode') == 401

def test_get_response_error():
    response = exceptions.HttpBaseException(HttpResponse.error()).get_response()
    assert response.get('statusCode') == 500

def test_custom_exception():
    response = exceptions.CustomException(HttpStatusCode.ERROR, None).get_response()
    assert response.get('statusCode') == 500

def test_badrequest_exception():
    response = exceptions.BadRequestException().get_response()
    assert response.get('statusCode') == 400

def test_unauthorized_exception():
    response = exceptions.UnauthorizedException().get_response()
    assert response.get('statusCode') == 401

def test_forbidden_exception():
    response = exceptions.ForbiddenException().get_response()
    assert response.get('statusCode') == 403

def test_error_exception():
    response = exceptions.ErrorException().get_response()
    assert response.get('statusCode') == 500
