import sentry_sdk
from django.http import HttpResponse


def sentry_debug_view(request):
    """
    Diagnostic view for verifying Sentry configuration and exception capturing.
    Enabled only when SENTRY_DEBUG is True.
    """
    client = sentry_sdk.Hub.current.client
    if not client or not sentry_sdk.is_initialized():
        return HttpResponse(
            "❌ Sentry is NOT initialized. Check SENTRY_ENABLED and SENTRY_DSN in your environment.",
            status=500,
            content_type="text/plain; charset=utf-8",
        )

    # 1. Capture an explicit message and flush immediately
    event_id = sentry_sdk.capture_message(
        "Test message manually triggered from /sentry-debug/",
        level="warning",
    )
    sentry_sdk.flush(timeout=5.0)

    # 2. Trigger an unhandled exception to test automatic Django exception capturing
    if request.GET.get("raise", "true").lower() in ("true", "1"):
        division_by_zero = 1 / 0  # noqa: F841

    return HttpResponse(
        f"✅ Sentry test message sent successfully! Event ID: {event_id}\n"
        f"Environment: {getattr(client.options, 'get', lambda k: getattr(client.options, k, ''))('environment')}",
        status=200,
        content_type="text/plain; charset=utf-8",
    )
