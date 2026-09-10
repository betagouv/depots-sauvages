import logging

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from backend.proconnect.models import ProConnectProfile

logger = logging.getLogger(__name__)


def sync_proconnect_profile(user, claims):
    siret = str(claims.get("siret") or "").strip()
    siren = siret[:9] if len(siret) >= 9 else ""
    roles = claims.get("roles") or []
    if isinstance(roles, str):
        roles = [roles]
    ProConnectProfile.objects.update_or_create(
        user=user,
        defaults={
            "sub": str(claims.get("sub") or ""),
            "siret": siret,
            "siren": siren,
            "organization_label": str(claims.get("organization_label") or ""),
            "roles": roles,
            "raw_claims": claims,
        },
    )


class ProConnectOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        logger.info(f"ProConnect create_user called for sub: {claims.get('sub')}")
        user = super(ProConnectOIDCBackend, self).create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("usual_name") or claims.get("family_name") or ""
        user.username = user.email
        user.save()
        sync_proconnect_profile(user, claims)
        return user

    def update_user(self, user, claims):
        logger.info(f"ProConnect update_user called for sub: {claims.get('sub')}")
        first_name = claims.get("given_name", "")
        last_name = claims.get("usual_name") or claims.get("family_name") or ""
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        sync_proconnect_profile(user, claims)
        return user
