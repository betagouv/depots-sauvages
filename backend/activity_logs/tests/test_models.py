import pytest

from backend.activity_logs.models import ActivityLog
from backend.activity_logs.tracking import IdempotentTrackingHandler
from backend.stats.models import StatsConstatation, StatsSuiviProcedure


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_activity_log_creation():
    stats_c = StatsConstatation.objects.using("stats_db").create(commune="Lyon")
    stats_sp = StatsSuiviProcedure.objects.using("stats_db").create(constatation=stats_c)
    ActivityLog.objects.create(
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


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_idempotent_tracking_handler():
    handler = IdempotentTrackingHandler()
    action_details = {
        "action": "constatation_demarree",
        "actor": "user_hash_999",
        "target": "app",
        "session_id": "sess_abc_123",
        "object": "42",
        "data": {"step": 1},
    }
    log1 = handler.track_action(action_details)
    assert ActivityLog.objects.using("stats_db").filter(session_id="sess_abc_123").count() == 1
    assert log1.data["step"] == 1
    # Deuxième appel avec mise à jour des données
    action_details_2 = {
        "action": "constatation_demarree",
        "actor": "user_hash_999",
        "target": "app",
        "session_id": "sess_abc_123",
        "object": "42",
        "data": {"step": 2},
    }
    log2 = handler.track_action(action_details_2)
    assert log2.id == log1.id
    assert ActivityLog.objects.using("stats_db").filter(session_id="sess_abc_123").count() == 1
    assert log2.data["step"] == 2


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_idempotent_tracking_handler_data_merge():
    handler = IdempotentTrackingHandler()
    action_details_1 = {
        "action": "sanction_decidee",
        "actor": "user_hash_777",
        "target": "suivi_procedure",
        "session_id": "sess_xyz_456",
        "object": "100",
        "data": {"est_staff": False, "montant_amende": None},
    }
    log1 = handler.track_action(action_details_1)
    assert log1.data["montant_amende"] is None
    assert log1.data["est_staff"] is False

    # Second call updates montant_amende to 500 without losing est_staff
    action_details_2 = {
        "action": "sanction_decidee",
        "actor": "user_hash_777",
        "target": "suivi_procedure",
        "session_id": "sess_xyz_456",
        "object": "100",
        "data": {"montant_amende": 500},
    }
    log2 = handler.track_action(action_details_2)
    assert log2.id == log1.id
    assert log2.data["montant_amende"] == 500
    assert log2.data["est_staff"] is False

