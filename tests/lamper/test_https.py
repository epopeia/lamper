
from lamper import https

import pytest


def test_return_ok_success():
    assert dict(statusCode=200, body=None) == https.HttpResponse.success()


def test_return_created_success():
    assert dict(statusCode=201, body=None) == https.HttpResponse.created()


def test_return_no_content_success():
    assert dict(statusCode=204, body=None) == https.HttpResponse.no_content()


def test_return_bad_request_success():
    assert dict(statusCode=400, body=None) == https.HttpResponse.bad_request()


def test_return_unauthorized_success():
    assert dict(statusCode=401, body=None) == https.HttpResponse.unauthorized()


def test_return_forbidden_success():
    assert dict(statusCode=403, body=None) == https.HttpResponse.forbidden()


def test_return_not_found_success():
    assert dict(statusCode=404, body=None) == https.HttpResponse.not_found()


def test_return_unprocessable_success():
    assert dict(statusCode=422, body=None) == https.HttpResponse.unprocessable()


def test_return_error_success():
    assert dict(statusCode=500, body=None) == https.HttpResponse.error()


def test_build_success():
    assert dict(statusCode=999, body=None) == https.HttpResponse.build(999)


def test_build_status_code_is_required():
    with pytest.raises(TypeError):
        https.HttpResponse.build()


def test_build_with_body_success():
    assert dict(statusCode=999, body='Build Example') == https.HttpResponse.build(999, 'Build Example')

def test_custom_response_with_body():
    https.default_response_headers = {'MY_CUSTOM_HEADER': '123'}
    res = https.HttpResponse().success({'name': 'willian'})
    assert res['statusCode'] == 200
    assert res['body'] == '{"name": "willian"}'
    assert res['headers'] == {'MY_CUSTOM_HEADER': '123'}


