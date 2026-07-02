from rest_framework import serializers
from backend.procedures.models import SuiviProcedure


class SuiviProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviProcedure
        fields = [
            "id",
            "created",
            "modified",
            "constatation",
            "etape_en_cours",
            "preuves_fournies",
            "constatation_signee",
            "lettre_signe",
            "identification_reussie",
            "lettre_envoyee",
            "lettre_envoyee_date",
            "copie_archives",
            "ar_recu",
            "ar_statut",
            "ar_presentation_date",
            "decision_poursuite",
            "montant_fixe",
            "montant_amende",
            "arrete_redige",
            "titre_recette_emis",
            "notification_sanction_envoyee",
            "motif_abandon",
            "souhaite_notifier_abandon",
            "notification_abandon_envoyee",
            "nettoyage_fait",
            "nettoyage_par",
            "observations_internes",
            "date_recouvrement_effective",
            "titre_recette_confirme",
            "montant_recouvre",
            "dossier_archive",
        ]
        read_only_fields = ("created", "modified")
