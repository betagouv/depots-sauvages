import logging
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

logger = logging.getLogger(__name__)


class ProConnectOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        logger.info(f"ProConnect create_user called with claims: {claims}")
        user = super(ProConnectOIDCBackend, self).create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("usual_name") or claims.get("family_name") or ""
        # email is handled by default if OIDC_RP_CLIENT_ID matches standard claims
        user.username = user.email
        user.save()
        return user

    def update_user(self, user, claims):
        logger.info(f"ProConnect update_user called with claims: {claims}")
        first_name = claims.get("given_name", "")
        last_name = claims.get("usual_name") or claims.get("family_name") or ""
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        return user
