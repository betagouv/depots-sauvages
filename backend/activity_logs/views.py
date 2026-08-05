from trackman.tracking import TrackingHandler

from backend.stats.anonymizer import anonymize_user_hash


class TrackActivityMixin:
    def _track(self, action, object_id, target, **data):
        TrackingHandler().track_action(
            {
                "action": action,
                "actor": anonymize_user_hash(self.request.user.id),
                "object": str(object_id),
                "target": target,
                "data": {
                    "user_is_staff": self.request.user.is_staff,
                    **data,
                },
            },
            model_alias="activity_log",
        )
