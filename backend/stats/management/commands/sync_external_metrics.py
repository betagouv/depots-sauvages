import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from backend.stats.collectors import tally
from backend.stats.db import get_stats_db_alias, stats_are_enabled, stats_db_is_configured
from backend.stats.models import ExternalMetric

COLLECTORS = {
    "tally": tally.collect,
}

DEFAULT_WINDOW_DAYS = 7


class Command(BaseCommand):
    help = (
        "Collecte les agrégats journaliers des sources externes (Tally aujourd'hui, "
        "Matomo et RDV Service Public ensuite) dans la base de statistiques."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            action="append",
            choices=sorted(COLLECTORS),
            help="Limite la collecte à cette source (répétable). Par défaut, toutes.",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=DEFAULT_WINDOW_DAYS,
            help=(
                "Nombre de jours à recalculer, en comptant aujourd'hui "
                f"(défaut {DEFAULT_WINDOW_DAYS}). Sert aussi au rattrapage historique."
            ),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Affiche ce qui serait écrit, sans rien écrire en base.",
        )

    def handle(self, *args, **options):
        if not stats_are_enabled():
            self.stdout.write(
                self.style.WARNING(
                    "Stats feature is disabled (STATS_ENABLED=False). Skipping collection."
                )
            )
            return

        target_db = get_stats_db_alias()
        if not stats_db_is_configured():
            self.stdout.write(
                self.style.WARNING(
                    f"Database alias '{target_db}' is not configured in DATABASES. "
                    "Skipping collection."
                )
            )
            return

        days = options["days"]
        if days < 1:
            raise CommandError("--days doit valoir au moins 1.")

        dry_run = options["dry_run"]
        sources = options["source"] or sorted(COLLECTORS)
        end_date = timezone.localdate()
        start_date = end_date - datetime.timedelta(days=days - 1)

        self.stdout.write(
            self.style.SUCCESS(
                f"Collecte des métriques externes du {start_date} au {end_date} "
                f"(sources={', '.join(sources)}, dry_run={dry_run}, target_db={target_db})"
            )
        )

        failures = []
        for source in sources:
            try:
                self.collect_source(source, start_date, end_date, target_db, dry_run)
            except Exception as error:  # noqa: BLE001 - une source en échec n'arrête pas les autres
                failures.append(source)
                self.stderr.write(self.style.ERROR(f"Source '{source}' en échec : {error}"))

        if failures and len(failures) == len(sources):
            raise CommandError(f"Aucune source n'a pu être collectée : {', '.join(failures)}.")

        if failures:
            self.stdout.write(
                self.style.WARNING(f"Collecte terminée avec des échecs : {', '.join(failures)}.")
            )
            return

        self.stdout.write(self.style.SUCCESS("External metrics collection finished successfully."))

    def collect_source(self, source, start_date, end_date, target_db, dry_run):
        points = COLLECTORS[source](start_date, end_date)

        if not points:
            self.stdout.write(f"{source} : aucune donnée sur la période.")
            return

        if dry_run:
            for point in points:
                self.stdout.write(
                    f"  [dry-run] {point.date} {point.source}.{point.metric}"
                    f"[{point.dimension}] = {point.value}"
                )
            self.stdout.write(f"{source} : {len(points)} ligne(s) — rien n'a été écrit.")
            return

        ExternalMetric.objects.using(target_db).bulk_create(
            [
                ExternalMetric(
                    source=point.source,
                    metric=point.metric,
                    date=point.date,
                    dimension=point.dimension,
                    value=point.value,
                    details=point.details,
                )
                for point in points
            ],
            update_conflicts=True,
            unique_fields=["source", "metric", "date", "dimension"],
            update_fields=["value", "details", "collected_at"],
        )
        self.stdout.write(self.style.SUCCESS(f"{source} : {len(points)} ligne(s) synchronisée(s)."))
