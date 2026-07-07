from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure


class BackofficeSuiviProcedureSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.filter(is_staff=True),
        allow_null=True,
        required=False,
    )
    anomalie = serializers.SerializerMethodField()

    class Meta:
        model = SuiviProcedure
        fields = [
            "etape_en_cours",
            "preuves_fournies",
            "constatation_signee",
            "lettre_signe",
            "identification_reussie",
            "observations_internes",
            "assigned_to",
            "assigned_at",
            "anomalie",
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
            "date_recouvrement_effective",
            "titre_recette_confirme",
            "montant_recouvre",
            "dossier_archive",
            "statut_traitement",
        ]

    def get_anomalie(self, obj):
        return ""


class BackofficeProcedureSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    suivi_procedure = serializers.SerializerMethodField()

    class Meta:
        model = Constatation
        fields = [
            "id",
            "commune",
            "date_constat",
            "constatant_role",
            "volume_depot",
            "nature_terrain",
            "ceci_est_un_test",
            "user_email",
            "agent",
            "auteur_identifie",
            "suivi_procedure",
            "localisation_depot",
            "heure_constat",
            "constatant_civilite",
            "constatant_nom",
            "constatant_prenom",
            "proprietaire_terrain_prive",
            "types_depot",
            "precisions_depot",
            "photo_dispo",
            "risque_ecoulement",
            "statut_auteur",
            "auteur_civilite",
            "auteur_nom",
            "auteur_prenom",
            "auteur_adresse",
            "auteur_siret",
            "entreprise_francaise",
            "plainte_etat",
            "indices_disponibles",
            "precisions_indices",
            "prejudice_montant_connu",
            "prejudice_montant",
            "prejudice_nombre_personnes",
            "prejudice_nombre_heures",
            "prejudice_nombre_vehicules",
            "prejudice_kilometrage",
            "prejudice_autres_couts",
            "contact_nom",
            "contact_prenom",
            "contact_email",
            "contact_telephone",
            "accepte_accompagnement",
            "doc_constat_generated_at",
            "lettre_info_generated_at",
        ]

    def get_user_email(self, obj):
        return obj.user.email if obj.user else ""

    def get_agent(self, obj):
        if obj.constatant_prenom or obj.constatant_nom:
            return f"{obj.constatant_prenom} {obj.constatant_nom}".strip()
        return obj.user.email if obj.user else ""

    def get_suivi_procedure(self, obj):
        sp = getattr(obj, "suivi_procedure", None)
        if sp:
            return BackofficeSuiviProcedureSerializer(sp).data
        return BackofficeSuiviProcedureSerializer(SuiviProcedure()).data


class StaffUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "name", "email"]

    def get_name(self, obj):
        full_name = obj.get_full_name()
        return full_name if full_name else obj.email
