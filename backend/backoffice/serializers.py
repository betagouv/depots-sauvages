from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure
from backend.proconnect.models import ProConnectProfile
from backend.teams.models import Team, TeamAutoCreationExclusion


class BackofficeSuiviProcedureSerializer(serializers.ModelSerializer):
    personne_assignee = serializers.PrimaryKeyRelatedField(
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
            "notes_traitement",
            "personne_assignee",
            "date_pilotage",
            "anomalie",
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
            "statut_traitement",
            "modified",
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
            "volume_m3",
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
            "accepte_traitement_donnees",
            "besoin_accompagnement",
            "doc_constat_generated_at",
            "lettre_info_generated_at",
            "modified",
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


class BackofficeProConnectProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProConnectProfile
        fields = [
            "id",
            "siret",
            "siren",
            "organization_label",
            "roles",
            "sub",
            "created",
            "modified",
        ]


class BackofficeUserSerializer(serializers.ModelSerializer):
    procedures_count = serializers.IntegerField(read_only=True)
    proconnect_profile = serializers.SerializerMethodField()
    has_proconnect = serializers.SerializerMethodField()
    team_id = serializers.IntegerField(source="profile.team.id", read_only=True, default=None)
    team_name = serializers.CharField(source="profile.team.name", read_only=True, default=None)
    team_siret = serializers.CharField(source="profile.team.siret", read_only=True, default=None)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
            "procedures_count",
            "has_proconnect",
            "proconnect_profile",
            "team_id",
            "team_name",
            "team_siret",
        ]

    def get_has_proconnect(self, obj):
        return hasattr(obj, "proconnect_profile") and obj.proconnect_profile is not None

    def get_proconnect_profile(self, obj):
        if hasattr(obj, "proconnect_profile") and obj.proconnect_profile is not None:
            return BackofficeProConnectProfileSerializer(obj.proconnect_profile).data
        return None


class BackofficeTeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "siret",
            "siren",
            "logo",
            "members_count",
            "created",
            "modified",
        ]
        read_only_fields = ["id", "created", "modified", "members_count"]

    def validate_siret(self, value):
        val = (value or "").strip()
        if not val or len(val) != 14 or not val.isdigit():
            raise serializers.ValidationError("Le SIRET doit comporter exactement 14 chiffres.")
        return val

    def validate_siren(self, value):
        val = (value or "").strip()
        if val and (len(val) != 9 or not val.isdigit()):
            raise serializers.ValidationError("Le SIREN doit comporter exactement 9 chiffres.")
        return val

    def validate(self, attrs):
        siret = attrs.get("siret") or (self.instance.siret if self.instance else "")
        siren = attrs.get("siren") or (self.instance.siren if self.instance else "")
        if siret and siren and siret[:9] != siren:
            raise serializers.ValidationError(
                "Le SIREN ne correspond pas aux 9 premiers chiffres du SIRET."
            )
        return attrs


class BackofficeTeamAutoCreationExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamAutoCreationExclusion
        fields = [
            "id",
            "siren",
            "siret",
            "label",
            "reason",
            "created",
            "modified",
        ]
        read_only_fields = ["id", "created", "modified"]

    def validate_siren(self, value):
        val = (value or "").strip()
        if val and (len(val) != 9 or not val.isdigit()):
            raise serializers.ValidationError("Le SIREN doit comporter exactement 9 chiffres.")
        return val

    def validate_siret(self, value):
        val = (value or "").strip()
        if val and (len(val) != 14 or not val.isdigit()):
            raise serializers.ValidationError("Le SIRET doit comporter exactement 14 chiffres.")
        return val

    def validate(self, attrs):
        instance = self.instance or TeamAutoCreationExclusion()
        for attr, value in attrs.items():
            setattr(instance, attr, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(serializers.as_serializer_error(e))
        return attrs
