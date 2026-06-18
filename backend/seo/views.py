from django.conf import settings
from django.views.generic import TemplateView


class RobotsTxtView(TemplateView):
    """
    Serve dynamic robots.txt based on settings.ENV_NAME
    """

    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["env_name"] = settings.ENV_NAME
        context["admin_url"] = f"/{settings.ADMIN_URL_NAME.rstrip('/')}/"
        return context
