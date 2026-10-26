import logging

from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from backend.proconnect.models import ProConnectAccessConfig, ProConnectProfile, PublicEntitySirene
from backend.proconnect.monitoring import record_proconnect_sentry_event, track_proconnect_activity
from backend.stats.anonymizer import anonymize_user_hash

logger = logging.getLogger(__name__)


def resolve_nature_juridique(siren: str) -> str:
    if not siren:
        return ""
    entity = PublicEntitySirene.objects.filter(siren=siren).first()
    return entity.categorie_juridique if entity else ""


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
    def check_proconnect_eligibility(self, claims):
        if not getattr(settings, "PROCONNECT_ACCESS_RESTRICTIONS_ENABLED", True):
            return True, "", {}
        roles = claims.get("roles") or []
        if isinstance(roles, str):
            roles = [roles]
        if "agent_public" not in roles:
            logger.info("ProConnect access denied: 'agent_public' role missing")
            return False, "role_invalide", {}
        siret = str(claims.get("siret") or "").strip()
        siren = siret[:9] if len(siret) >= 9 else ""
        if not siren:
            logger.info("ProConnect access denied: no SIRET/SIREN provided")
            return False, "siren_manquant", {}
        config = ProConnectAccessConfig.get_solo()
        if config.is_siren_allowed(siren):
            return True, "", {"siren": siren}
        nature_juridique = resolve_nature_juridique(siren)
        if nature_juridique and config.is_legal_category_allowed(nature_juridique):
            return True, "", {"siren": siren, "nature_juridique": nature_juridique}
        logger.info(
            f"ProConnect access denied: SIREN {siren} "
            f"(nature juridique: {nature_juridique}) unauthorized"
        )
        return (
            False,
            "etablissement_non_autorise",
            {"siren": siren, "nature_juridique": nature_juridique},
        )

    def is_eligible_proconnect_user(self, claims):
        eligible, _, _ = self.check_proconnect_eligibility(claims)
        return eligible

    def authenticate(self, request, **kwargs):
        return super().authenticate(request, **kwargs)

    def get_or_create_user(self, access_token, id_token, payload):
        user_info = self.get_userinfo(access_token, id_token, payload)
        eligible, reason, context = self.check_proconnect_eligibility(user_info)
        if not eligible:
            if hasattr(self, "request") and self.request and hasattr(self.request, "session"):
                siret = str(user_info.get("siret") or "").strip()
                siren = siret[:9] if len(siret) >= 9 else ""
                first_name = user_info.get("given_name", "")
                last_name = user_info.get("usual_name") or user_info.get("family_name") or ""
                full_name = f"{first_name} {last_name}".strip()
                org_label = str(user_info.get("organization_label") or "")
                email = str(user_info.get("email") or "")
                self.request.session["proconnect_rejected_info"] = {
                    "siret": siret,
                    "siren": siren,
                    "organization_label": org_label,
                    "email": email,
                    "name": full_name,
                }
                self.request.session.save()
                session_key = getattr(self.request.session, "session_key", None)
                sub_or_email = user_info.get("sub") or email
                track_proconnect_activity(
                    action="proconnect_acces_refuse",
                    actor=anonymize_user_hash(sub_or_email),
                    session_id=session_key,
                    target="auth",
                    data={
                        "motif_refus": reason,
                        "siren": siren,
                        "nature_juridique": context.get("nature_juridique", ""),
                        "organization_label": org_label,
                    },
                )
                record_proconnect_sentry_event(
                    event_type="proconnect_acces_refuse",
                    siren=siren,
                    reason=reason,
                    organization_label=org_label,
                    extra={"nature_juridique": context.get("nature_juridique", "")},
                )
            return None
        return super().get_or_create_user(access_token, id_token, payload)

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
