from rest_framework import serializers

from backend.constatations.models import Constatation


class ConstatationSerializer(serializers.ModelSerializer):
    souhaite_porter_plainte = serializers.ReadOnlyField()
    date_creation = serializers.DateTimeField(source="created", read_only=True)
    date_modification = serializers.DateTimeField(source="modified", read_only=True)
    suivi_procedure = serializers.SerializerMethodField()

    class Meta:
        model = Constatation
        fields = [
            "id",
            "created",
            "modified",
            "user",
            "commune",
            "localisation_depot",
            "date_constat",
            "heure_constat",
            "constatant_civilite",
            "constatant_role",
            "constatant_nom",
            "constatant_prenom",
            "constatant_est_utilisateur_connecte",
            "nature_terrain",
            "proprietaire_terrain_prive",
            "volume_depot",
            "types_depot",
            "precisions_depot",
            "photo_dispo",
            "risque_ecoulement",
            "auteur_identifie",
            "statut_auteur",
            "auteur_civilite",
            "auteur_nom",
            "auteur_prenom",
            "auteur_adresse",
            "auteur_siret",
            "entreprise_francaise",
            "informations_auteur",
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
            "ceci_est_un_test",
            "doc_constat_should_generate",
            "doc_constat_generated_at",
            "lettre_info_should_generate",
            "lettre_info_generated_at",
            "souhaite_porter_plainte",
            "date_creation",
            "date_modification",
            "suivi_procedure",
        ]

    def get_suivi_procedure(self, obj):
        sp = getattr(obj, "suivi_procedure", None)
        if not sp:
            return {"etape_en_cours": 1}
        return {"etape_en_cours": sp.etape_en_cours}

    def get_docs_generation_flags(self, auteur_identifie):
        return {
            "doc_constat_should_generate": True,
            "lettre_info_should_generate": bool(auteur_identifie),
        }

    def update(self, instance, validated_data):
        auteur_identifie = validated_data.get("auteur_identifie", instance.auteur_identifie)
        validated_data.update(self.get_docs_generation_flags(auteur_identifie))
        return super().update(instance, validated_data)

    def create(self, validated_data):
        auteur_identifie = validated_data.get("auteur_identifie", False)
        validated_data.update(self.get_docs_generation_flags(auteur_identifie))
        return super().create(validated_data)
