import pytest
from trackman.tracking import TrackingHandler
from backend.activity_logs.models import ActivityLog


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_activity_log_creation():
    handler = TrackingHandler()
    handler.track_action(
        {
            "action": "test_action",
            "actor": "user_hash_123",
            "target": "app",
            "object": "object_456",
            "data": {"key": "value"},
        },
        model_alias="activity_log",
    )

    log = ActivityLog.objects.using("stats_db").get(action="test_action")
    assert log.actor == "user_hash_123"
    assert log.target == "app"
    assert log.object == "object_456"
    assert log.data == {"key": "value"}
