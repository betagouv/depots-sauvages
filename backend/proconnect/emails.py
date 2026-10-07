import logging

from django.conf import settings
from django.core.mail import EmailMessage
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
        subject_org = f"{organization_label} ({siren})" if organization_label and siren else (organization_label or siren or email)
        subject = f"[Stop Déchets Sauvages] Demande d'accès ProConnect : {subject_org}"
        content = (
            "Une demande d'ouverture d'accès ProConnect a été déposée sur Stop Déchets Sauvages.\n\n"
            "--- Détails du demandeur ---\n"
            f"Nom : {name or 'Non précisé'}\n"
            f"Email : {email}\n"
            f"Organisme : {organization_label or 'Non précisé'}\n"
            f"SIREN : {siren or 'Non précisé'}\n"
            f"SIRET : {siret or 'Non précisé'}\n\n"
            f"Commentaire de l'agent :\n{message or 'Aucun'}\n\n"
            "--- Action administrateur ---\n"
            "Pour autoriser cet établissement, accédez à la gestion des accès ProConnect dans le back-office :\n"
            f"{admin_link}\n\n"
            "Actions possibles :\n"
            f"1. Ajouter le SIREN '{siren}' dans la liste blanche (dérogation spécifique).\n"
            "2. Ou ajouter la catégorie juridique correspondante pour autoriser l'ensemble des structures similaires.\n\n"
            f"Pour répondre directement à l'agent une fois l'accès configuré, vous pouvez répondre à ce message ou lui écrire à : {email}\n"
        )
        from_email = getattr(
            settings,
            "SERVER_EMAIL",
            getattr(settings, "DEFAULT_FROM_EMAIL", "contact@depots-sauvages.beta.gouv.fr"),
        )
        mail_obj = EmailMessage(
            subject=subject,
            body=content,
            from_email=from_email,
            to=[admin_email],
            reply_to=[email] if email else None,
        )
        mail_obj.send(fail_silently=True)
        logger.info(f"Demande d'accès ProConnect envoyée avec succès pour {email} ({siren})")
    except Exception as exc:
        logger.error(
            f"Erreur inattendue lors de l'envoi de la demande d'accès : {exc}", exc_info=True
        )
