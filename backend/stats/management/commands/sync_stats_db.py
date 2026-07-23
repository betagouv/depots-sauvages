from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Max

from backend.constatations.models import Constatation
from backend.procedures.models import SuiviProcedure
from backend.stats.models import StatsConstatation, StatsSuiviProcedure

SYNC_REGISTRY = [
    (Constatation, StatsConstatation),
    (SuiviProcedure, StatsSuiviProcedure),
]


class Command(BaseCommand):
    help = (
        "Synchronizes production data to the stats database with anonymization and field exclusion."
    )

    @property
    def stats_db_alias(self):
        return getattr(settings, "STATS_DATABASE_ALIAS", "stats_db")

    def add_arguments(self, parser):
        parser.add_argument(
            "--full-reset",
            action="store_true",
            help="Force full re-synchronization of all records.",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=500,
            help="Batch size for bulk insertion/update operations.",
        )

    def handle(self, *args, **options):
        if not getattr(settings, "STATS_ENABLED", True):
            self.stdout.write(
                self.style.WARNING(
                    "Stats feature is disabled (STATS_ENABLED=False). Skipping synchronization."
                )
            )
            return

        if self.stats_db_alias not in settings.DATABASES:
            self.stdout.write(
                self.style.WARNING(
                    f"Database alias '{self.stats_db_alias}' is not configured in DATABASES. Skipping synchronization."
                )
            )
            return
        full_reset = options["full_reset"]
        batch_size = options["batch_size"]
        self.stdout.write(
            self.style.SUCCESS(
                f"Starting stats sync (full_reset={full_reset}, batch_size={batch_size}, target_db={self.stats_db_alias})"
            )
        )
        for prod_model, stats_model in SYNC_REGISTRY:
            self.sync_model_pair(
                prod_model, stats_model, full_reset=full_reset, batch_size=batch_size
            )
        self.stdout.write(
            self.style.SUCCESS("Stats database synchronization finished successfully.")
        )

    def sync_model_pair(self, prod_model, stats_model, full_reset=False, batch_size=500):
        model_name = prod_model._meta.model_name
        stats_exclude = getattr(stats_model, "stats_exclude", set())
        stats_anonymize = getattr(stats_model, "stats_anonymize", {})
        prod_fields = {f.name for f in prod_model._meta.fields}
        exclude_fields = stats_exclude.intersection(prod_fields)
        qs = prod_model.objects.using("default").order_by("id")
        if exclude_fields:
            qs = qs.defer(*exclude_fields)
        target_db = self.stats_db_alias
        if not full_reset:
            last_modified = stats_model.objects.using(target_db).aggregate(Max("modified"))[
                "modified__max"
            ]
            if last_modified is not None:
                qs = qs.filter(modified__gte=last_modified)
                self.stdout.write(f"Syncing {model_name} incremental since {last_modified}")
            else:
                self.stdout.write(f"Syncing {model_name} full (no previous records found)")
        else:
            self.stdout.write(f"Syncing {model_name} full (--full-reset)")
        total_count = qs.count()
        if total_count == 0:
            self.stdout.write(f"No records to sync for {model_name}.")
            return
        processed = 0
        stats_meta_fields = stats_model._meta.fields
        update_fields = [f.name for f in stats_meta_fields if not f.primary_key]
        instances_batch = []
        for prod_obj in qs.iterator(chunk_size=batch_size):
            data = {}
            for field in stats_meta_fields:
                if field.name in stats_exclude or field.attname in stats_exclude:
                    continue
                val = getattr(prod_obj, field.attname, getattr(prod_obj, field.name, None))
                if val is None and field.name == "user_hash":
                    val = getattr(prod_obj, "user_id", None)
                if field.name in stats_anonymize:
                    anonymizer_func = stats_anonymize[field.name]
                    val = anonymizer_func(val, record_id=getattr(prod_obj, "id", None))
                elif field.attname in stats_anonymize:
                    anonymizer_func = stats_anonymize[field.attname]
                    val = anonymizer_func(val, record_id=getattr(prod_obj, "id", None))
                data[field.attname] = val
            instances_batch.append(stats_model(**data))
            if len(instances_batch) >= batch_size:
                stats_model.objects.using(target_db).bulk_create(
                    instances_batch,
                    update_conflicts=True,
                    unique_fields=["id"],
                    update_fields=update_fields,
                    batch_size=batch_size,
                )
                processed += len(instances_batch)
                instances_batch.clear()
        if instances_batch:
            stats_model.objects.using(target_db).bulk_create(
                instances_batch,
                update_conflicts=True,
                unique_fields=["id"],
                update_fields=update_fields,
                batch_size=batch_size,
            )
            processed += len(instances_batch)
            instances_batch.clear()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully synced {processed} records for {model_name}.")
        )
