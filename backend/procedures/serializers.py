from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.procedures.models import SuiviProcedure


class SuiviProcedureResumeSerializer(serializers.ModelSerializer):
    """
    Summary of procedure follow-up sent with the list of procedures
    (dashboard "Mes procédures"). Contains fields needed to determine which
    sections are completed and place each file in its corresponding column.
    """

    class Meta:
        model = SuiviProcedure
        fields = [
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
            "titre_recette_confirme",
            "montant_recouvre",
            "dossier_archive",
        ]


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
            "numero_suivi_lettre",
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
            "date_recouvrement_effective",
            "titre_recette_confirme",
            "montant_recouvre",
            "dossier_archive",
            "observations_internes",
        ]

        read_only_fields = ("created", "modified")


class SuiviProcedureStaffSerializer(SuiviProcedureSerializer):
    personne_assignee = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        allow_null=True,
        required=False,
    )

    class Meta(SuiviProcedureSerializer.Meta):
        fields = SuiviProcedureSerializer.Meta.fields + [
            "statut_traitement",
            "personne_assignee",
            "date_pilotage",
            "notes_traitement",
        ]
        read_only_fields = ("created", "modified", "date_pilotage")
