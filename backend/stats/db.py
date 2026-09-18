from django.conf import settings

DEFAULT_STATS_DATABASE_ALIAS = "stats_db"


def get_stats_db_alias():
    """Alias de la base de statistiques.

    `TRACKMAN_DATABASE_ALIAS` est le réglage de référence : c'est celui que lit le
    routeur de django-trackman. `STATS_DATABASE_ALIAS` reste accepté en premier pour
    ne pas casser une configuration qui le définirait.
    """
    return getattr(
        settings,
        "STATS_DATABASE_ALIAS",
        getattr(settings, "TRACKMAN_DATABASE_ALIAS", DEFAULT_STATS_DATABASE_ALIAS),
    )


def stats_are_enabled():
    return getattr(settings, "STATS_ENABLED", True)


def stats_db_is_configured():
    return get_stats_db_alias() in settings.DATABASES
