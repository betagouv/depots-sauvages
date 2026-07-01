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
        }
