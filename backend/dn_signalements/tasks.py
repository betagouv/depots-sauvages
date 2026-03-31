import logging

from django.contrib.auth import get_user_model
from django_tasks import task

from backend.dn.fields import DNField
from backend.dn.client import DNGraphQLClient
from backend.dn.queries import GET_DEMARCHE_DOSSIERS_LEAN_QUERY
from backend.dn_signalements.dn_mappings import CHAMP_ID_ADRESSE_DEPOT, DATE_CONSTAT_CHAMP_ID
from backend.dn_signalements.models import DNSignalement


logger = logging.getLogger(__name__)
User = get_user_model()


@task()
def sync_user_dossiers(user_id: int):
    return sync_user_dossiers_func(user_id)


def sync_user_dossiers_func(user_id: int):
    """
    Synchronize user dossiers from Démarches Simplifiées.
    """
    try:
        user = User.objects.get(pk=user_id)
        logger.info(f"Task sync_user_dossiers started for user: {user.email} (ID: {user_id})")
        dn_client = DNGraphQLClient()
        user_email = user.email or user.username
        if not user_email:
            logger.warning(f"User {user_id} has no email or username, skipping sync.")
            return
        dossiers = dn_client.get_dossiers_for_user(
            user_email, query=GET_DEMARCHE_DOSSIERS_LEAN_QUERY
        )
        for dossier in dossiers:
            dn_field = DNField(dossier)
            fields_data = dn_field.get_data()
            datetime_constat = fields_data.get(DATE_CONSTAT_CHAMP_ID)
            localisation_depot = None
            address_data = fields_data.get(CHAMP_ID_ADRESSE_DEPOT)
            if address_data and isinstance(address_data, dict):
                localisation_depot = address_data.get("label")
            DNSignalement.objects.update_or_create(
                dn_numero_dossier=dossier["number"],
                defaults={
                    "user": user,
                    "dn_date_creation": dossier.get("dateDepot"),
                    "dn_date_modification": dossier.get("dateDerniereModification"),
                    "date_constat": datetime_constat,
                    "heure_constat": datetime_constat.time() if datetime_constat else None,
                    "localisation_depot": localisation_depot or "",
                },
            )
        logger.info(f"Task sync_user_dossiers completed successfully for user: {user.email}")
    except User.DoesNotExist:
        logger.error(f"Task sync_user_dossiers failed: User with ID {user_id} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error in sync_user_dossiers for user ID {user_id}: {e}")
