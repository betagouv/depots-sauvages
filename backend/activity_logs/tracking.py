from trackman.tracking import TrackingHandler

from backend.activity_logs.models import ActivityLog


class IdempotentTrackingHandler(TrackingHandler):
    """
    Extending TrackingHandler to do a update_or_create instead of a create when a session_id
    is provided along with a constatation_id, suivi_procedure_id or object.
    """

    def _update_or_create_action(self, action_details):
        session_id = action_details.get("session_id")
        actor = action_details.get("actor")
        action = action_details.get("action")
        constatation_id = action_details.get("constatation_id")
        suivi_procedure_id = action_details.get("suivi_procedure_id")
        obj = action_details.get("object")
        lookup_kwargs = {
            "actor": actor,
            "action": action,
            "session_id": session_id,
        }
        if constatation_id:
            lookup_kwargs["constatation_id"] = constatation_id
        elif suivi_procedure_id:
            lookup_kwargs["suivi_procedure_id"] = suivi_procedure_id
        elif obj:
            lookup_kwargs["object"] = obj
        defaults = {
            "target": action_details.get("target"),
            "data": action_details.get("data", {}),
        }
        if constatation_id:
            defaults["constatation_id"] = constatation_id
        if suivi_procedure_id:
            defaults["suivi_procedure_id"] = suivi_procedure_id
        if obj:
            defaults["object"] = obj
        log, _ = ActivityLog.objects.using("stats_db").update_or_create(
            **lookup_kwargs,
            defaults=defaults,
        )
        return log

    def track_action(self, action_details, model_alias="activity_log"):
        session_id = action_details.get("session_id")
        actor = action_details.get("actor")
        action = action_details.get("action")
        constatation_id = action_details.get("constatation_id")
        suivi_procedure_id = action_details.get("suivi_procedure_id")
        obj = action_details.get("object")
        if session_id and actor and action and (constatation_id or suivi_procedure_id or obj):
            return self._update_or_create_action(action_details)
        return super().track_action(action_details, model_alias=model_alias)
