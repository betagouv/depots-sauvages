from django.conf import settings


class StagingNoIndexMiddleware:
    """
    Adds X-Robots-Tag: noindex, nofollow to all HTTP responses
    if the environment is not production, preventing indexing of all pages and assets.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(settings, "ENV_NAME", "") != "prod":
            response["X-Robots-Tag"] = "noindex, nofollow"
        return response
