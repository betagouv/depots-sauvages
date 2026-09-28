import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from backend.proconnect.models import ProConnectAccessConfig, ProConnectProfile

logger = logging.getLogger(__name__)


def get_nature_juridique_for_siren(siren: str) -> str:
    """Interroge l'API Recherche d'entreprises pour récupérer la catégorie / nature juridique."""
    if not siren:
        return ""
    api_url = getattr(
        settings, "RECHERCHE_ENTREPRISES_API", "https://recherche-entreprises.api.gouv.fr"
    )
    url = f"{api_url}/search?{urllib.parse.urlencode({'q': siren})}"
    req = urllib.request.Request(url, headers={"User-Agent": "depots-sauvages-proconnect-auth"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("results") or []
            if results:
                return str(results[0].get("nature_juridique") or "").strip()
    except Exception as exc:
        logger.warning(
            f"Erreur lors de la récupération de la nature juridique pour le SIREN {siren}: {exc}"
        )
    return ""


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
    def is_eligible_proconnect_user(self, claims) -> bool:
        """Vérifie si l'utilisateur a le rôle agent_public et appartient à un organisme éligible."""
        roles = claims.get("roles") or []
        if isinstance(roles, str):
            roles = [roles]
        if "agent_public" not in roles:
            logger.info("ProConnect accès refusé: rôle 'agent_public' absent")
            return False
        siret = str(claims.get("siret") or "").strip()
        siren = siret[:9] if len(siret) >= 9 else ""
        if not siren:
            logger.info("ProConnect accès refusé: aucun SIRET/SIREN fourni")
            return False
        config = ProConnectAccessConfig.get_solo()
        if config.est_siren_autorise(siren):
            return True
        # Résolution de la catégorie / nature juridique
        nature_juridique = get_nature_juridique_for_siren(siren)
        if nature_juridique and config.est_categorie_juridique_autorisee(nature_juridique):
            return True
        logger.info(
            f"ProConnect refusé: SIREN {siren} (nature juridique: {nature_juridique}) non habilité"
        )
        return False

    def authenticate(self, request, **kwargs):
        return super().authenticate(request, **kwargs)

    def get_or_create_user(self, access_token, id_token, payload):
        user_info = self.get_userinfo(access_token, id_token, payload)
        if not self.is_eligible_proconnect_user(user_info):
            if hasattr(self, "request") and self.request and hasattr(self.request, "session"):
                siret = str(user_info.get("siret") or "").strip()
                siren = siret[:9] if len(siret) >= 9 else ""
                first_name = user_info.get("given_name", "")
                last_name = user_info.get("usual_name") or user_info.get("family_name") or ""
                full_name = f"{first_name} {last_name}".strip()
                self.request.session["proconnect_rejected_info"] = {
                    "siret": siret,
                    "siren": siren,
                    "organization_label": str(user_info.get("organization_label") or ""),
                    "email": str(user_info.get("email") or ""),
                    "name": full_name,
                }
                self.request.session.save()
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
