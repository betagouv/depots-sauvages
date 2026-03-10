import logging

from django.contrib.auth import get_user_model
from django_tasks import task

from backend.dn.champs import DNChamp
from backend.dn.client import DNGraphQLClient
from backend.dn.queries import GET_DEMARCHE_DOSSIERS_LEAN_QUERY
from backend.dn_signalements.dn_mappings import ADDRESS_CHAMP_ID, DATE_CONSTAT_CHAMP_ID
from backend.dn_signalements.models import UserDossier

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
            dn_champ = DNChamp(dossier)
            champs_data = dn_champ.get_data()
            datetime_constat = champs_data.get(DATE_CONSTAT_CHAMP_ID)
            localisation_depot = None
            address_data = champs_data.get(ADDRESS_CHAMP_ID)
            if address_data and isinstance(address_data, dict):
                localisation_depot = address_data.get("label")
            UserDossier.objects.update_or_create(
                numero_dossier=dossier["number"],
                defaults={
                    "user": user,
                    "date_creation": dossier.get("dateDepot"),
                    "date_modification": dossier.get("dateDerniereModification"),
                    "date_constat": datetime_constat,
                    "localisation_depot": localisation_depot or "",
                },
            )
        logger.info(f"Task sync_user_dossiers completed successfully for user: {user.email}")
    except User.DoesNotExist:
        logger.error(f"Task sync_user_dossiers failed: User with ID {user_id} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error in sync_user_dossiers for user ID {user_id}: {e}")
