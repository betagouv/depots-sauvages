from trackman.db_routers import TrackingDatabaseRouter


class StatsRouter(TrackingDatabaseRouter):
    """
    Custom router extending Trackman's TrackingDatabaseRouter to ensure strict migration
    isolation on stats_db.
    """

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == self.database_alias:
            return app_label in self.tracking_app_labels
        if app_label in self.tracking_app_labels:
            return False
        return None
