import logging

from django.conf import settings
from django.core.mail import send_mail
from django_tasks import task

logger = logging.getLogger(__name__)


@task(queue_name="emails")
def send_proconnect_access_request_notification_task(validated_data: dict, admin_link: str) -> None:
    try:
        siret = validated_data.get("siret", "")
        siren = validated_data.get("siren", "")
        organization_label = validated_data.get("organization_label", "")
        email = validated_data.get("email", "")
        name = validated_data.get("name", "")
        message = validated_data.get("message", "")
        admin_email = getattr(
            settings,
            "ADMIN_EMAIL",
            getattr(settings, "DEFAULT_FROM_EMAIL", "contact@depots-sauvages.beta.gouv.fr"),
        )
        subject = f"[Stop Déchets Sauvages] Demande d'accès ProConnect : {organization_label or siren or email}"
        content = (
            f"Une demande d'ouverture d'accès ProConnect a été déposée sur Stop Déchets Sauvages.\n\n"
            f"--- Détails du demandeur ---\n"
            f"Nom : {name or 'Non précisé'}\n"
            f"Email : {email}\n"
            f"Organisme : {organization_label or 'Non précisé'}\n"
            f"SIREN : {siren or 'Non précisé'}\n"
            f"SIRET : {siret or 'Non précisé'}\n"
            f"Commentaire de l'agent :\n{message or 'Aucun'}\n\n"
            f"--- Action administrateur ---\n"
            f"Pour autoriser cet établissement, vous pouvez ajouter le SIREN '{siren}' "
            f"dans la liste blanche de configuration ProConnect via le lien suivant :\n"
            f"{admin_link}\n"
        )
        from_email = getattr(
            settings,
            "SERVER_EMAIL",
            getattr(settings, "DEFAULT_FROM_EMAIL", "contact@depots-sauvages.beta.gouv.fr"),
        )
        send_mail(
            subject=subject,
            message=content,
            from_email=from_email,
            recipient_list=[admin_email],
            fail_silently=True,
        )
        logger.info(f"Demande d'accès ProConnect envoyée avec succès pour {email} ({siren})")
    except Exception as exc:
        logger.error(
            f"Erreur inattendue lors de l'envoi de la demande d'accès : {exc}", exc_info=True
        )
