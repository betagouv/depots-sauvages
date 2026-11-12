import re

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure

# Patterns pour le nettoyage des PII
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_REGEX = re.compile(r"\b(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}\b")
SIRET_SIREN_REGEX = re.compile(r"\b\d{3}\s*\d{3}\s*\d{3}(?:\s*\d{5})?\b")
IMMATRICULATION_REGEX = re.compile(
    r"\b[A-Z]{2}[-\s]?\d{3}[-\s]?[A-Z]{2}\b|\b\d{1,4}[-\s]?[A-Z]{2,3}[-\s]?\d{2}\b"
)


def scrub_pii(text):
    """
    Supprime ou masque les informations nominatives et sensibles (emails, téléphones,
    sirets, plaques d'immatriculation) d'un texte avant envoi au LLM.
    """
    if not text or not isinstance(text, str):
        return ""

    scrubbed = EMAIL_REGEX.sub("[EMAIL_MASQUÉ]", text)
    scrubbed = PHONE_REGEX.sub("[TÉL_MASQUÉ]", scrubbed)
    scrubbed = SIRET_SIREN_REGEX.sub("[SIRET/SIREN_MASQUÉ]", scrubbed)
    scrubbed = IMMATRICULATION_REGEX.sub("[IMMATRICULATION_MASQUÉE]", scrubbed)
    return scrubbed


def _resolve_etape_metier(suivi, procedure):
    """
    Détermine l'étape métier lisible pour l'agent (miroir des colonnes du tableau de bord).
    """
    if procedure.is_draft:
        return "Brouillon à finaliser"

    if not procedure.auteur_identifie:
        if suivi and suivi.dossier_archive:
            return "Clôturé (Auteur non identifié)"
        if suivi and suivi.identification_reussie is False:
            return "Identification infructueuse (prêt pour clôture)"
        return "Recherche de l'auteur présumé"

    if not suivi:
        return "Pièces de procédure à signer"

    # Vérification des étapes
    if not (suivi.preuves_fournies and suivi.constatation_signee and suivi.lettre_signe):
        return "Documents à signer (Rapport et/ou Lettre d'information)"

    if not suivi.lettre_envoyee:
        return "Lettre d'information prête à être envoyée (LRAR)"

    if not (suivi.ar_recu and (suivi.ar_statut == "npai" or suivi.ar_presentation_date)):
        return "En attente de retour de l'accusé de réception (AR)"

    if suivi.ar_statut == "npai":
        if suivi.decision_poursuite == "abandon":
            return "Abandon validé (Auteur introuvable NPAI)"
        return "Courrier retourné NPAI - Recherche d'adresse nécessaire"

    if suivi.decision_poursuite == "sanction":
        if suivi.dossier_archive:
            return "Dossier clôturé (Sanction)"
        if suivi.notification_sanction_envoyee and suivi.titre_recette_emis:
            return "Amende notifiée et titre émis (en attente recouvrement Trésor public)"
        return "Action de sanction en cours (Arrêté et Titre à finaliser)"

    if suivi.decision_poursuite == "abandon":
        return "Dossier en cours d'abandon de poursuites"

    return "Période du contradictoire ou décision de poursuite à prendre"


def build_safe_user_context(user, current_path="", form_context=None):
    """
    Construit un dictionnaire de contexte strictement anonymisé et sécurisé (Zero-PII)
    à destination du prompt système de l'assistant IA.
    Prend en compte également l'état en cours du formulaire de constatation si transmis.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return {
            "is_authenticated": False,
            "profil_usager": "anonyme",
            "procedures_count": 0,
            "dossiers": [],
        }

    procedures_qs = Constatation.objects.filter(user=user).select_related("suivi_procedure")
    procedures_count = procedures_qs.count()

    # Détection de l'ID d'un dossier actif depuis le chemin
    # ex: /suivi-procedure/14 ou /constatation/14
    active_id_match = re.search(r"/(?:suivi-procedure|constatation)/(\d+)", current_path or "")
    active_procedure_id = int(active_id_match.group(1)) if active_id_match else None

    # Extraction des 5 dossiers les plus récents
    recent_procedures = list(procedures_qs.order_by("-id")[:5])

    dossiers_summary = []
    dossier_actif_summary = None

    for proc in recent_procedures:
        suivi = getattr(proc, "suivi_procedure", None)
        etape_metier = _resolve_etape_metier(suivi, proc)

        item = {
            "id": proc.id,
            "est_brouillon": proc.is_draft,
            "etape_metier": etape_metier,
            "volume_estime": proc.volume_depot
            or (f"{proc.volume_m3} m³" if proc.volume_m3 else "Inconnu"),
            "volume_m3": float(proc.volume_m3) if proc.volume_m3 is not None else None,
            "types_depot": proc.types_depot or [],
            "nature_terrain": proc.nature_terrain or ["non renseigné"],
            "auteur_identifie": proc.auteur_identifie is True,
            "statut_auteur": proc.statut_auteur
            or ("Entreprise" if proc.entreprise_francaise else "Particulier"),
            "ar_statut": getattr(suivi, "ar_statut", None) if suivi else None,
            "ar_presentation_date": (
                str(suivi.ar_presentation_date) if suivi and suivi.ar_presentation_date else None
            ),
            "decision_poursuite": getattr(suivi, "decision_poursuite", None) if suivi else None,
            "montant_amende": (
                float(suivi.montant_amende) if suivi and suivi.montant_amende is not None else None
            ),
            "dossier_archive": getattr(suivi, "dossier_archive", False) if suivi else False,
        }

        dossiers_summary.append(item)
        if active_procedure_id and proc.id == active_procedure_id:
            dossier_actif_summary = item

    profil_usager = (
        "primo_utilisateur_sans_procedure"
        if procedures_count == 0
        else "utilisateur_avec_procedures"
    )

    # Nettoyage et assainissement strict Zero-PII des informations du formulaire en cours
    safe_form_data = None
    if isinstance(form_context, dict) and form_context:
        safe_form_data = {}
        if commune := form_context.get("commune"):
            safe_form_data["commune"] = str(commune).strip()
        if localisation := form_context.get("localisationDepot"):
            safe_form_data["localisationDepot"] = scrub_pii(str(localisation).strip())
        if form_context.get("volumeM3") is not None:
            try:
                safe_form_data["volumeM3"] = float(form_context["volumeM3"])
            except (ValueError, TypeError):
                pass
        elif volume_depot := form_context.get("volumeDepot"):
            safe_form_data["volumeDepot"] = str(volume_depot)
        if types := form_context.get("typesDepot"):
            if isinstance(types, list):
                safe_form_data["typesDepot"] = [str(t) for t in types if t]
        if terrain := form_context.get("natureTerrain"):
            if isinstance(terrain, list):
                safe_form_data["natureTerrain"] = [str(t) for t in terrain if t]
        if isinstance(form_context.get("auteurIdentifie"), bool):
            safe_form_data["auteurIdentifie"] = form_context["auteurIdentifie"]
        if precisions := form_context.get("precisionsDepot"):
            safe_form_data["precisionsDepot"] = scrub_pii(str(precisions).strip())

    return {
        "is_authenticated": True,
        "profil_usager": profil_usager,
        "procedures_count": procedures_count,
        "current_path": current_path,
        "form_context": safe_form_data,
        "dossier_actif": dossier_actif_summary,
        "dossiers_recents": dossiers_summary,
    }
