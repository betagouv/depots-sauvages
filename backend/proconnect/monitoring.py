import logging

from backend.activity_logs.tracking import IdempotentTrackingHandler

logger = logging.getLogger(__name__)


def track_proconnect_activity(
    action,
    actor,
    session_id=None,
    data=None,
    target="auth",
):
    try:
        IdempotentTrackingHandler().track_action(
            {
                "action": action,
                "actor": actor,
                "target": target,
                "session_id": session_id,
                "data": data or {},
            },
            model_alias="activity_log",
        )
    except Exception as exc:
        logger.debug(f"Failed to record ProConnect activity log: {exc}")


def record_proconnect_sentry_event(
    event_type,
    siren="",
    reason="",
    organization_label="",
    extra=None,
):
    try:
        import sentry_sdk

        with sentry_sdk.isolation_scope() as scope:
            scope.set_tag("auth.provider", "proconnect")
            scope.set_tag("auth.event", event_type)
            if reason:
                scope.set_tag("auth.rejection_reason", reason)
            if siren:
                scope.set_tag("auth.siren", siren)
            scope.add_breadcrumb(
                category="auth.proconnect",
                message=f"ProConnect {event_type}: reason={reason}, siren={siren}",
                level="warning" if "refuse" in event_type else "info",
            )
            sentry_data = {
                "siren": siren,
                "reason": reason,
                "organization_label": organization_label,
                **(extra or {}),
            }
            for k, v in sentry_data.items():
                if v:
                    scope.set_extra(k, v)
            if "refuse" in event_type:
                sentry_sdk.capture_message(
                    f"ProConnect access denied: {reason} (SIREN: {siren or 'N/A'})",
                    level="warning",
                )
            elif event_type == "proconnect_demande_acces_envoyee":
                sentry_sdk.capture_message(
                    f"ProConnect access requested: {organization_label or 'N/A'} (SIREN: {siren or 'N/A'})",
                    level="warning",
                )
            elif event_type == "proconnect_config_modifiee":
                sentry_sdk.capture_message(
                    "ProConnect configuration modified",
                    level="info",
                )
    except Exception as exc:
        logger.debug(f"Failed to record ProConnect sentry event: {exc}")
