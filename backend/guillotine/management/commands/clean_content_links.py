from django.apps import apps
from django.core.management.base import BaseCommand

from backend.guillotine.link_utils import clean_blocks_content
from backend.guillotine.models import BlockContent


class Command(BaseCommand):
    help = (
        "Nettoie les liens dans les contenus riches de tous les modèles BlockContent (blog, FAQ, etc.) : "
        "retire target='_blank' et rel='nofollow' sur les liens internes, convertit les URLs "
        "absolues du site en chemins relatifs, et normalise les liens externes avec rel='noopener noreferrer'."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Affiche les modifications prévues sans les sauvegarder en base de données.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        if dry_run:
            self.stdout.write(
                self.style.WARNING("--- MODE DRY-RUN ACTIF (aucune écriture en base) ---")
            )
        total_models_scanned = 0
        total_items_updated = 0
        for model in apps.get_models():
            if issubclass(model, BlockContent) and not model._meta.abstract:
                total_models_scanned += 1
                model_name = model._meta.verbose_name or model.__name__
                self.stdout.write(f"Vérification de {model_name}...")
                updated_count = 0
                for item in model.objects.all():
                    cleaned_content, changed = clean_blocks_content(item.content)
                    if changed:
                        updated_count += 1
                        title = getattr(item, "title", str(item.pk))
                        self.stdout.write(
                            f"  - {model.__name__} ID {item.pk} ('{title}') : liens modifiés"
                        )
                        if not dry_run:
                            item.content = cleaned_content
                            item.save(update_fields=["content"])
                total_items_updated += updated_count
        summary = f"Terminé. Modèles inspectés : {total_models_scanned}, Éléments modifiés : {total_items_updated}"
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] {summary}"))
        else:
            self.stdout.write(self.style.SUCCESS(summary))
