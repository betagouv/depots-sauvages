from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class ProConnectOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(ProConnectOIDCBackend, self).create_user(claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        # email is handled by default if OIDC_RP_CLIENT_ID matches standard claims
        user.username = user.email
        user.save()
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user
