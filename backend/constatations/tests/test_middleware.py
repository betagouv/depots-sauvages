import pytest
from django.core.exceptions import RequestDataTooBig
from django.test import RequestFactory

from backend.constatations.middleware import RequestDataTooBigMiddleware


def test_request_data_too_big_middleware_returns_json_on_exception():
    rf = RequestFactory()
    request = rf.post("/api/constatations/")

    def failing_view(req):
        raise RequestDataTooBig("Request body exceeded DATA_UPLOAD_MAX_MEMORY_SIZE")

    middleware = RequestDataTooBigMiddleware(failing_view)
    response = middleware(request)
    if response.status_code != 400:
        response = middleware.process_exception(
            request, RequestDataTooBig("Request body exceeded DATA_UPLOAD_MAX_MEMORY_SIZE")
        )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert b'"request_data_too_big"' in response.content


def test_request_data_too_big_middleware_passes_through_normal_requests():
    rf = RequestFactory()
    request = rf.get("/api/constatations/")

    def normal_view(req):
        from django.http import HttpResponse

        return HttpResponse("OK")

    middleware = RequestDataTooBigMiddleware(normal_view)
    response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"OK"
