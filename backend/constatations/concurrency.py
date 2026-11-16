from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response

# Maximum string length for last_synced_modified to prevent ReDoS / CPU exhaustion attacks
MAX_TIMESTAMP_LENGTH = 100
# Grace period (in seconds) to absorb slight network delays or clock drifts between client and server
DEFAULT_TOLERANCE_SECONDS = 1.0


def check_optimistic_lock(
    instance,
    request_data,
    tolerance_seconds=DEFAULT_TOLERANCE_SECONDS,
):
    """
    Check for concurrent edit conflicts using Optimistic Concurrency Control (OCC).
    Clients send the timestamp of the version they started editing (`last_synced_modified`).
    If the server instance was modified more recently by someone else, the edit is rejected
    unless explicitly forced.

    Returns:
        Response(status=409) if a conflict is detected, or None if the modification
        can proceed safely.
    """
    force_value = request_data.get("force", False)
    force = force_value in (True, 1, "1", "true", "True")
    # Bypass optimistic locking if the client explicitly requested to overwrite conflicts
    if force:
        return None
    last_synced_modified_raw = request_data.get("last_synced_modified")
    if not last_synced_modified_raw or not isinstance(last_synced_modified_raw, str):
        return None
    # String length guard (prevents DoS regex/string parsing attacks)
    if len(last_synced_modified_raw) > MAX_TIMESTAMP_LENGTH:
        return None
    client_modified = parse_datetime(last_synced_modified_raw.strip())
    if not client_modified or not getattr(instance, "modified", None):
        return None
    server_modified = instance.modified
    # Timezone normalization: Django parse_datetime returns naive datetime if the input
    # string lacks timezone/offset (e.g. 'YYYY-MM-DDTHH:MM:SS'). Python prevents subtracting
    # aware and naive datetimes (TypeError), so we align client_modified to current timezone.
    if timezone.is_aware(server_modified) and timezone.is_naive(client_modified):
        client_modified = timezone.make_aware(client_modified, timezone.get_current_timezone())
    elif timezone.is_naive(server_modified) and timezone.is_aware(client_modified):
        client_modified = timezone.make_naive(client_modified, timezone.get_current_timezone())
    try:
        diff_seconds = (server_modified - client_modified).total_seconds()
    except (TypeError, ValueError, OverflowError):
        return None
    if diff_seconds > tolerance_seconds:
        updated_by_user = getattr(instance, "updated_by", None)
        if updated_by_user:
            first_name = getattr(updated_by_user, "first_name", "") or ""
            last_name = getattr(updated_by_user, "last_name", "") or ""
            full_name = f"{first_name} {last_name}".strip()
            updated_by_name = (
                full_name or getattr(updated_by_user, "email", "") or "Un autre collègue"
            )
        else:
            updated_by_name = "Un autre utilisateur"
        return Response(
            {
                "error": "CONCURRENT_MODIFICATION",
                "message": f"Ce dossier a été modifié par {updated_by_name} entre-temps.",
                "updated_by": updated_by_name,
                "server_modified": server_modified.isoformat(),
            },
            status=status.HTTP_409_CONFLICT,
        )
    return None
