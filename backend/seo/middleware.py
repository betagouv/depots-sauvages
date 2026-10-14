from backend.seo.seo_metadata import is_production


class NonProductionNoIndexMiddleware:
    """
    Adds X-Robots-Tag: noindex, nofollow to all HTTP responses
    if the environment is not production, preventing indexing of all pages and assets.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not is_production():
            response["X-Robots-Tag"] = "noindex, nofollow"
        return response
