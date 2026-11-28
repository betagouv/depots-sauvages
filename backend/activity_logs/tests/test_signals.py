import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

from backend.activity_logs.models import ActivityLog
from backend.activity_logs.utils import resolve_auth_method
from backend.unit_tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db(databases=["default", "stats_db"])
def test_user_logged_in_signal_tracking(rf):
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )
    request = rf.get("/")
    request.session = {"_auth_user_backend": "django.contrib.auth.backends.ModelBackend"}

    user_logged_in.send(sender=User, request=request, user=user)

    log = ActivityLog.objects.using("stats_db").get(action="utilisateur_connecte")
    assert log.target == "auth"
    assert log.data["est_staff"] is False
    assert log.data["methode_auth"] == "password"
    assert "team_id" not in log.data

    # Test user with team
    from backend.teams.models import Team

    team = Team.objects.create(name="Team Alpha", siret="12312312300012")
    user_with_team = UserFactory(
        username="teamuser", email="teamuser@example.com", password="password", team=team
    )
    user_logged_in.send(sender=User, request=request, user=user_with_team)
    log_team = ActivityLog.objects.using("stats_db").filter(action="utilisateur_connecte").last()
    assert log_team.data["team_id"] == team.id


def test_resolve_auth_method(rf):
    request = rf.get("/")

    request.session = {"_auth_user_backend": "backend.proconnect.auth.ProConnectOIDCBackend"}
    assert resolve_auth_method(request) == "proconnect"

    request.session = {"_auth_user_backend": "backend.bypass_auth.auth.BypassAuthBackend"}
    assert resolve_auth_method(request) == "demo"

    request.session = {"_auth_user_backend": "django.contrib.auth.backends.ModelBackend"}
    assert resolve_auth_method(request) == "password"
