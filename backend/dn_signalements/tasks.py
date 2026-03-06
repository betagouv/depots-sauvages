import logging

from django.contrib.auth import get_user_model
from django_tasks import task

logger = logging.getLogger(__name__)
User = get_user_model()


@task()
def sync_user_dossiers(user_id: int):
    """
    Synchronize user dossiers from Démarches Simplifiées.
    """
    try:
        user = User.objects.get(pk=user_id)
        logger.info(f"Task sync_user_dossiers started for user: {user.email} (ID: {user_id})")
        logger.info(f"Task sync_user_dossiers completed successfully for user: {user.email}")
    except User.DoesNotExist:
        logger.error(f"Task sync_user_dossiers failed: User with ID {user_id} does not exist.")
    except Exception as e:
        logger.exception(f"Unexpected error in sync_user_dossiers for user ID {user_id}: {e}")
