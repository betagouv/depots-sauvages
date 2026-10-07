import csv
import io
import logging
import tempfile
import urllib.request
import zipfile
from typing import Iterator

from django.core.management.base import BaseCommand

from backend.proconnect.models import PublicEntitySirene

logger = logging.getLogger(__name__)

DEFAULT_SIRENE_URL = (
    "https://www.data.gouv.fr/api/1/datasets/r/825f4199-cadd-486c-ac46-a65a8ea1a047"
)
BATCH_SIZE = 5000


def parse_csv_stream(file_stream: Iterator[str], batch_size: int = BATCH_SIZE) -> int:
    reader = csv.DictReader(file_stream)
    batch = []
    total_saved = 0
    for row in reader:
        cat = str(row.get("categorieJuridiqueUniteLegale") or "").strip()
        if not cat.startswith("7"):
            continue
        siren = str(row.get("siren") or "").strip()
        if not siren or len(siren) != 9:
            continue
        denomination = str(
            row.get("denominationUniteLegale") or row.get("denominationUsuelle1UniteLegale") or ""
        ).strip()
        batch.append(
            PublicEntitySirene(
                siren=siren,
                categorie_juridique=cat,
                denomination=denomination,
            )
        )
        if len(batch) >= batch_size:
            PublicEntitySirene.objects.bulk_create(
                batch,
                update_conflicts=True,
                unique_fields=["siren"],
                update_fields=["categorie_juridique", "denomination", "modified"],
            )
            total_saved += len(batch)
            batch = []
    if batch:
        PublicEntitySirene.objects.bulk_create(
            batch,
            update_conflicts=True,
            unique_fields=["siren"],
            update_fields=["categorie_juridique", "denomination", "modified"],
        )
        total_saved += len(batch)
    return total_saved


def process_zip_file(zip_path: str) -> int:
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_filenames = [n for n in zf.namelist() if n.endswith(".csv")]
        if not csv_filenames:
            return 0
        with zf.open(csv_filenames[0], "r") as f:
            text_stream = io.TextIOWrapper(f, encoding="utf-8")
            return parse_csv_stream(text_stream)


class Command(BaseCommand):
    help = "Importe les unités légales publiques (catégorie 7xxx) depuis le fichier StockUniteLegale Sirene"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Chemin vers un fichier CSV ou ZIP local StockUniteLegale",
        )
        parser.add_argument(
            "--url",
            type=str,
            default=DEFAULT_SIRENE_URL,
            help=f"URL du fichier ZIP StockUniteLegale (défaut: {DEFAULT_SIRENE_URL})",
        )

    def handle(self, *args, **options):
        local_path = options.get("file")
        url = options.get("url")
        if local_path:
            self.stdout.write(f"Lecture du fichier local : {local_path}")
            if local_path.endswith(".zip"):
                total = process_zip_file(local_path)
            else:
                with open(local_path, "r", encoding="utf-8") as f:
                    total = parse_csv_stream(f)
        else:
            self.stdout.write(f"Téléchargement depuis : {url}")
            req = urllib.request.Request(
                url, headers={"User-Agent": "depots-sauvages-sirene-import"}
            )
            with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
                with urllib.request.urlopen(req) as resp:
                    while chunk := resp.read(1024 * 1024 * 8):
                        tmp.write(chunk)
                tmp.flush()
                self.stdout.write("Téléchargement terminé, traitement des unités publiques...")
                total = process_zip_file(tmp.name)
        self.stdout.write(
            self.style.SUCCESS(f"Import terminé avec succès : {total} entités enregistrées.")
        )
