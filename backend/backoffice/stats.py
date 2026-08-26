from django.db.models import Count, Q

from backend.constatations.models import Constatation


def get_backoffice_dashboard_stats():
    """Calculate aggregated stats for the backoffice dashboard in a single query."""
    stats = Constatation.objects.aggregate(
        total=Count("id"),
        real=Count("id", filter=Q(ceci_est_un_test=False)),
        test=Count("id", filter=Q(ceci_est_un_test=True)),
        author_identified=Count("id", filter=Q(ceci_est_un_test=False, auteur_identifie=True)),
        author_not_identified=Count(
            "id", filter=Q(ceci_est_un_test=False, auteur_identifie=False)
        ),
        total_active=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                suivi_procedure__etape_en_cours__lt=5,
                suivi_procedure__dossier_archive=False,
            ),
        ),
        ar_waiting=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                suivi_procedure__etape_en_cours__lt=5,
                suivi_procedure__lettre_envoyee=True,
                suivi_procedure__ar_recu=False,
            ),
        ),
        decision_to_take=Count(
            "id", filter=Q(ceci_est_un_test=False, suivi_procedure__etape_en_cours=3)
        ),
        closed=Count(
            "id", filter=Q(ceci_est_un_test=False, suivi_procedure__statut_traitement="Clôturé")
        ),
        step_id_1=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False, auteur_identifie=True, suivi_procedure__etape_en_cours=1
            ),
        ),
        step_id_2=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False, auteur_identifie=True, suivi_procedure__etape_en_cours=2
            ),
        ),
        step_id_3=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False, auteur_identifie=True, suivi_procedure__etape_en_cours=3
            ),
        ),
        step_id_4=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False, auteur_identifie=True, suivi_procedure__etape_en_cours=4
            ),
        ),
        step_id_5=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                auteur_identifie=True,
                suivi_procedure__etape_en_cours__gte=5,
            ),
        ),
        step_not_id_1=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                auteur_identifie=False,
                suivi_procedure__etape_en_cours=1,
            ),
        ),
        step_not_id_2=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                auteur_identifie=False,
                suivi_procedure__etape_en_cours=2,
            ),
        ),
        step_not_id_3=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                auteur_identifie=False,
                suivi_procedure__etape_en_cours__in=[3, 4],
            ),
        ),
        step_not_id_5=Count(
            "id",
            filter=Q(
                ceci_est_un_test=False,
                auteur_identifie=False,
                suivi_procedure__etape_en_cours__gte=5,
            ),
        ),
        status_nouveau=Count(
            "id", filter=Q(ceci_est_un_test=False, suivi_procedure__statut_traitement="Nouveau")
        ),
        status_ouvert=Count(
            "id", filter=Q(ceci_est_un_test=False, suivi_procedure__statut_traitement="Ouvert")
        ),
        status_pause=Count(
            "id",
            filter=Q(ceci_est_un_test=False, suivi_procedure__statut_traitement="En pause"),
        ),
        status_resolu=Count(
            "id", filter=Q(ceci_est_un_test=False, suivi_procedure__statut_traitement="Résolu")
        ),
        status_cloture=Count(
            "id", filter=Q(ceci_est_un_test=False, suivi_procedure__statut_traitement="Clôturé")
        ),
    )

    workload_query = (
        Constatation.objects.filter(ceci_est_un_test=False)
        .values("suivi_procedure__personne_assignee")
        .annotate(count=Count("id"))
    )
    workload = {
        item["suivi_procedure__personne_assignee"]: item["count"] for item in workload_query
    }

    return {
        "totalActive": stats["total_active"],
        "arWaiting": stats["ar_waiting"],
        "decisionToTake": stats["decision_to_take"],
        "closed": stats["closed"],
        "generalStats": {
            "total": stats["total"],
            "real": stats["real"],
            "test": stats["test"],
            "authorIdentified": stats["author_identified"],
            "authorNotIdentified": stats["author_not_identified"],
        },
        "steps": {
            "identified": {
                1: stats["step_id_1"],
                2: stats["step_id_2"],
                3: stats["step_id_3"],
                4: stats["step_id_4"],
                5: stats["step_id_5"],
            },
            "notIdentified": {
                1: stats["step_not_id_1"],
                2: stats["step_not_id_2"],
                3: stats["step_not_id_3"],
                5: stats["step_not_id_5"],
            },
        },
        "byStatus": {
            "Nouveau": stats["status_nouveau"],
            "Ouvert": stats["status_ouvert"],
            "En pause": stats["status_pause"],
            "Résolu": stats["status_resolu"],
            "Clôturé": stats["status_cloture"],
        },
        "workloadByAssigneeId": workload,
    }
