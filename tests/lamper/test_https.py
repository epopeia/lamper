import unittest

from lamper.https import HttpResponse


class TestHttpResponse(unittest.TestCase):

    def test_return_ok_success(self):
        self.assertEqual(dict(statusCode=200, body=None), HttpResponse.success())

    def test_return_created_success(self):
        self.assertEqual(dict(statusCode=201, body=None), HttpResponse.created())

    def test_return_no_content_success(self):
        self.assertEqual(dict(statusCode=204, body=None), HttpResponse.no_content())

    def test_return_bad_request_success(self):
        self.assertEqual(dict(statusCode=400, body=None), HttpResponse.bad_request())

    def test_return_unauthorized_success(self):
        self.assertEqual(dict(statusCode=401, body=None), HttpResponse.unauthorized())

    def test_return_forbidden_success(self):
        self.assertEqual(dict(statusCode=403, body=None), HttpResponse.forbidden())

    def test_return_not_found_success(self):
        self.assertEqual(dict(statusCode=404, body=None), HttpResponse.not_found())

    def test_return_unprocessable_success(self):
        self.assertEqual(dict(statusCode=422, body=None), HttpResponse.unprocessable())

    def test_return_error_success(self):
        self.assertEqual(dict(statusCode=500, body=None), HttpResponse.error())

    def test_build_success(self):
        self.assertEqual(dict(statusCode=999, body=None), HttpResponse.build(999))

    def test_build_status_code_is_required(self):
        with self.assertRaises(TypeError):
            HttpResponse.build()

    def test_build_with_body_success(self):
        self.assertEqual(
            dict(statusCode=999, body='Build Example'), HttpResponse.build(999, 'Build Example'))
