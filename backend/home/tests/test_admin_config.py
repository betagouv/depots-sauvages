import sys
from importlib import reload

import pytest
from django.conf import settings
from django.test import override_settings
from django.urls import clear_url_caches

from backend.unit_tests.factories import UserFactory

pytestmark = pytest.mark.django_db(databases=settings.DATABASES.keys())


def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    clear_url_caches()


def test_admin_url_is_accessible_when_enabled(client):
    user = UserFactory(is_staff=True, is_superuser=True)
    client.force_login(user)
    with override_settings(ENABLE_ADMIN=True, ADMIN_URL_NAME="admin"):
        reload_urlconf()
        url = "/admin/"
        response = client.get(url)
        assert response.status_code == 200


def test_admin_url_is_not_found_when_disabled(client):
    # We use a unique URL name to avoid conflicts with previous tests if reload fails
    with override_settings(ENABLE_ADMIN=False, ADMIN_URL_NAME="disabled-admin"):
        reload_urlconf()
        url = "/disabled-admin/"
        response = client.get(url)
        # Excluded from catch-all, and not in urlpatterns
        assert response.status_code == 404


def test_custom_admin_url_is_accessible(client):
    user = UserFactory(is_staff=True, is_superuser=True)
    client.force_login(user)
    with override_settings(ENABLE_ADMIN=True, ADMIN_URL_NAME="secret-admin"):
        reload_urlconf()
        url = "/secret-admin/"
        response = client.get(url)
        assert response.status_code == 200
        # Original admin should now be caught by frontend catch-all (returns 200)
        # because "admin" is no longer excluded by the dynamic regex
        response_old = client.get("/admin/")
        assert response_old.status_code == 200
