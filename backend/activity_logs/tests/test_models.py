import pytest

from backend.activity_logs.models import ActivityLog
from backend.stats.models import StatsConstatation, StatsSuiviProcedure


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_activity_log_creation():
    stats_c = StatsConstatation.objects.using("stats_db").create(commune="Lyon")
    stats_sp = StatsSuiviProcedure.objects.using("stats_db").create(constatation=stats_c)
    log = ActivityLog.objects.create(
        action="test_action",
        actor="user_hash_123",
        target="app",
        constatation=stats_c,
        suivi_procedure=stats_sp,
        data={"key": "value"},
    )
    fetched_log = ActivityLog.objects.get(action="test_action")
    assert fetched_log.actor == "user_hash_123"
    assert fetched_log.target == "app"
    assert fetched_log.constatation == stats_c
    assert fetched_log.suivi_procedure == stats_sp
    assert fetched_log.data == {"key": "value"}
