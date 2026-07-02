from rest_framework import serializers

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure


class BackofficeSuiviProcedureSerializer(serializers.ModelSerializer):
    charge_deploiement = serializers.SerializerMethodField()
    date_assigned = serializers.SerializerMethodField()
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
            "charge_deploiement",
            "date_assigned",
            "anomalie",
            # New follow-up fields
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
        ]

    def get_charge_deploiement(self, obj):
        return "Non assigné"

    def get_date_assigned(self, obj):
        return None

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
            # New details fields
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
        return {
            "etape_en_cours": 1,
            "preuves_fournies": False,
            "constatation_signee": False,
            "lettre_signe": False,
            "identification_reussie": None,
            "observations_internes": "",
            "charge_deploiement": "Non assigné",
            "date_assigned": None,
            "anomalie": "",
            "lettre_envoyee": False,
            "lettre_envoyee_date": None,
            "copie_archives": False,
            "ar_recu": False,
            "ar_statut": "",
            "ar_presentation_date": None,
            "decision_poursuite": "",
            "montant_fixe": False,
            "montant_amende": None,
            "arrete_redige": False,
            "titre_recette_emis": False,
            "notification_sanction_envoyee": False,
            "motif_abandon": "",
            "souhaite_notifier_abandon": None,
            "notification_abandon_envoyee": False,
            "nettoyage_fait": None,
            "nettoyage_par": "",
            "date_recouvrement_effective": None,
            "titre_recette_confirme": False,
            "montant_recouvre": False,
            "dossier_archive": False,
        }
