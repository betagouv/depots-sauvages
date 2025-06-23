import logging

from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from backend.antispam_timer.timer import FormTimer

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    """
    Serve Vue Application
    """

    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        logger.debug(f"Starting timer for session: {request.session.session_key}")
        FormTimer.start_timer(request, settings.TIMER_BASE_NAME)
        return super().get(request, *args, **kwargs)


index_view = never_cache(IndexView.as_view())
