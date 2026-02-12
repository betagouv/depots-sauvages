from import_export import resources

from backend.signalements.models import Signalement


class SignalementResource(resources.ModelResource):
    class Meta:
        model = Signalement
        # Exclude binary fields that make no sense in CSV/Excel
        exclude = ("doc_constat", "lettre_info")
        # Define fields to export (optional, but good for explicit ordering)
        # We'll stick to 'exclude' to automatically include new fields unless binary.
