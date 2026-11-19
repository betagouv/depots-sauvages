import pytest
from django.urls import reverse
from rest_framework import status

from backend.activity_logs.models import ActivityLog
from backend.constatations.models import Constatation
from backend.stats.anonymizer import anonymize_user_hash
from backend.unit_tests.factories import UserFactory


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_user_action_authenticated(client):
    user = UserFactory(is_staff=False)
    client.force_login(user)
    constatation = Constatation.objects.create(
        user=user,
        commune="Lyon",
    )
    url = reverse("track-user-action")
    payload = {
        "action": "notification_auteur_envoyee",
        "object": str(constatation.id),
        "data": {
            "date_envoi": "2026-08-05",
            "actor_role": "agent",
        },
    }

    response = client.post(url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    log = ActivityLog.objects.using("stats_db").get(action="notification_auteur_envoyee")
    assert log.actor == anonymize_user_hash(user.id)
    assert log.target == "suivi_procedure"
    assert log.session_id == client.session.session_key
    assert log.constatation_id == constatation.id
    assert log.suivi_procedure_id == constatation.suivi_procedure.id
    assert log.data["date_envoi"] == "2026-08-05"
    assert log.data["est_staff"] is False


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_user_action_unrelated_object(client):
    user = UserFactory(is_staff=False)
    client.force_login(user)
    url = reverse("track-user-action")
    payload = {
        "action": "etape_guidee_consultee",
        "object": "123",
        "data": {"guidance_step": 2},
    }
    response = client.post(url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    log = ActivityLog.objects.using("stats_db").get(action="etape_guidee_consultee")
    assert log.object == "123"
    assert log.constatation_id is None
    assert log.suivi_procedure_id is None


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_user_action_anonymous(client):
    url = reverse("track-user-action")
    payload = {"action": "etape_guidee_consultee"}
    response = client.post(url, payload, content_type="application/json")
    assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_user_action_missing_action(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse("track-user-action")
    payload = {"data": {"foo": "bar"}}
    response = client.post(url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "action" in response.data


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_user_action_idempotent_duplicate(client):
    user = UserFactory(is_staff=False)
    client.force_login(user)
    constatation = Constatation.objects.create(user=user, commune="Lyon")
    url = reverse("track-user-action")
    payload = {
        "action": "notification_auteur_envoyee",
        "object": str(constatation.id),
        "data": {"date_envoi": "2026-08-05"},
    }
    # Premier appel
    res1 = client.post(url, payload, content_type="application/json")
    assert res1.status_code == status.HTTP_201_CREATED

    # Deuxième appel identique durant la même session
    payload_updated = {
        "action": "notification_auteur_envoyee",
        "object": str(constatation.id),
        "data": {"date_envoi": "2026-08-06"},
    }
    res2 = client.post(url, payload_updated, content_type="application/json")
    assert res2.status_code == status.HTTP_201_CREATED
    # Vérification qu'il n'y a qu'UN seul log en base (avec la donnée mise à jour)
    logs = ActivityLog.objects.using("stats_db").filter(
        action="notification_auteur_envoyee",
        constatation_id=constatation.id,
    )
    assert logs.count() == 1
    assert logs.first().data["date_envoi"] == "2026-08-06"


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_user_action_with_team(client):
    from backend.teams.models import Team

    team = Team.objects.create(name="Brigade Verte", siret="99999999900099")
    user = UserFactory(is_staff=False, team=team)
    client.force_login(user)

    url = reverse("track-user-action")
    payload = {
        "action": "etape_guidee_consultee",
        "object": "456",
        "data": {"step": 1},
    }
    response = client.post(url, payload, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED

    log = ActivityLog.objects.using("stats_db").get(action="etape_guidee_consultee", object="456")
    assert log.data["team_id"] == team.id
    assert log.data["est_staff"] is False
    assert log.data["step"] == 1


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_track_activity_mixin_with_team(rf):
    from backend.activity_logs.views import TrackActivityMixin
    from backend.teams.models import Team

    team = Team.objects.create(name="Police Municipale", siret="88888888800088")
    user = UserFactory(is_staff=True, team=team)

    request = rf.get("/dummy/")
    request.user = user
    request.session = type("Session", (), {"session_key": "fake-session-123"})()

    view = TrackActivityMixin()
    view.request = request

    view._track(action="test_action", target="test_target", custom_field="hello")

    log = ActivityLog.objects.using("stats_db").get(action="test_action")
    assert log.target == "test_target"
    assert log.data["team_id"] == team.id
    assert log.data["est_staff"] is True
    assert log.data["custom_field"] == "hello"
