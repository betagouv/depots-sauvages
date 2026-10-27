from django.core.exceptions import RequestDataTooBig
from django.http import JsonResponse


class RequestDataTooBigMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def build_error_response(self):
        return JsonResponse(
            {
                "error": "request_data_too_big",
                "detail": "Request body exceeded the maximum allowed size.",
            },
            status=400,
        )

    def __call__(self, request):
        try:
            return self.get_response(request)
        except RequestDataTooBig:
            return self.build_error_response()

    def process_exception(self, request, exception):
        if isinstance(exception, RequestDataTooBig):
            return self.build_error_response()
        return None
