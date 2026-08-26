import django_filters
from django.db.models import Q

from backend.constatations.models import Constatation


class BackofficeProcedureFilterSet(django_filters.FilterSet):
    cas_reels = django_filters.CharFilter(method="filter_cas_reels")
    casReels = django_filters.CharFilter(method="filter_cas_reels")
    auteur_identifie = django_filters.CharFilter(method="filter_auteur_identifie")
    auteurIdentifie = django_filters.CharFilter(method="filter_auteur_identifie")
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
            "etape",
            "traitement",
            "assignee",
            "search",
        ]

    def filter_cas_reels(self, queryset, name, value):
        if value == "Oui":
            return queryset.filter(ceci_est_un_test=False)
        elif value == "Non":
            return queryset.filter(ceci_est_un_test=True)
        return queryset

    def filter_auteur_identifie(self, queryset, name, value):
        if value == "Oui":
            return queryset.filter(auteur_identifie=True)
        elif value == "Non":
            return queryset.filter(auteur_identifie=False)
        return queryset

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
