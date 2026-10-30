import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from backend.constatations.models import Constatation


class BackofficeProcedureFilterSet(django_filters.FilterSet):
    cas_reels = django_filters.CharFilter(method="filter_cas_reels")
    casReels = django_filters.CharFilter(method="filter_cas_reels")
    auteur_identifie = django_filters.CharFilter(method="filter_auteur_identifie")
    auteurIdentifie = django_filters.CharFilter(method="filter_auteur_identifie")
    besoin_accompagnement = django_filters.CharFilter(method="filter_besoin_accompagnement")
    besoinAccompagnement = django_filters.CharFilter(method="filter_besoin_accompagnement")
    etape = django_filters.CharFilter(method="filter_etape")
    traitement = django_filters.CharFilter(field_name="suivi_procedure__statut_traitement")
    assignee = django_filters.CharFilter(method="filter_assignee")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Constatation
        fields = [
            "cas_reels",
            "casReels",
            "auteur_identifie",
            "auteurIdentifie",
            "besoin_accompagnement",
            "besoinAccompagnement",
            "etape",
            "traitement",
            "assignee",
            "search",
        ]

    def filter_boolean_field(self, queryset, field_name, value):
        if value == "Oui":
            return queryset.filter(**{field_name: True})
        elif value == "Non":
            return queryset.filter(**{field_name: False})
        return queryset

    def filter_cas_reels(self, queryset, name, value):
        if value == "Oui":
            return queryset.filter(ceci_est_un_test=False)
        elif value == "Non":
            return queryset.filter(ceci_est_un_test=True)
        return queryset

    def filter_auteur_identifie(self, queryset, name, value):
        return self.filter_boolean_field(queryset, "auteur_identifie", value)

    def filter_besoin_accompagnement(self, queryset, name, value):
        return self.filter_boolean_field(queryset, "besoin_accompagnement", value)

    def filter_etape(self, queryset, name, value):
        if value and value != "Tous" and value.isdigit():
            etape_int = int(value)
            if etape_int >= 5:
                return queryset.filter(suivi_procedure__etape_en_cours__gte=5)
            return queryset.filter(suivi_procedure__etape_en_cours=etape_int)
        return queryset

    def filter_assignee(self, queryset, name, value):
        if not value or value == "Tous":
            return queryset
        if value in ("None", "null"):
            return queryset.filter(suivi_procedure__personne_assignee__isnull=True)
        elif value.isdigit():
            return queryset.filter(suivi_procedure__personne_assignee_id=int(value))
        return queryset

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(commune__icontains=value)
                | Q(constatant_nom__icontains=value)
                | Q(constatant_prenom__icontains=value)
                | Q(user__email__icontains=value)
            )
        return queryset


class BackofficeUserFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    procedures_count = django_filters.CharFilter(method="filter_procedures_count")
    has_procedures = django_filters.CharFilter(method="filter_has_procedures")
    has_proconnect = django_filters.CharFilter(method="filter_has_proconnect")

    class Meta:
        model = get_user_model()
        fields = [
            "search",
            "procedures_count",
            "has_procedures",
            "has_proconnect",
        ]

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(email__icontains=value)
                | Q(first_name__icontains=value)
                | Q(last_name__icontains=value)
                | Q(proconnect_profile__siret__icontains=value)
                | Q(proconnect_profile__siren__icontains=value)
                | Q(proconnect_profile__organization_label__icontains=value)
            )
        return queryset

    def filter_procedures_count(self, queryset, name, value):
        if value == "0" or value == "zero":
            return queryset.filter(procedures_count=0)
        elif value == ">0" or value == "gt0":
            return queryset.filter(procedures_count__gt=0)
        return queryset

    def filter_has_procedures(self, queryset, name, value):
        if value == "Oui" or value == "true" or value == "1":
            return queryset.filter(procedures_count__gt=0)
        elif value == "Non" or value == "false" or value == "0":
            return queryset.filter(procedures_count=0)
        return queryset

    def filter_has_proconnect(self, queryset, name, value):
        if value == "Oui" or value == "true" or value == "1":
            return queryset.filter(proconnect_profile__isnull=False)
        elif value == "Non" or value == "false" or value == "0":
            return queryset.filter(proconnect_profile__isnull=True)
        return queryset
