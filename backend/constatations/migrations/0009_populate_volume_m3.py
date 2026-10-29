from decimal import Decimal
from django.db import migrations

LEGACY_VOLUME_MAPPING = {
    "Moins de 1m3": Decimal("0.5"),
    "Entre 1 et 3m3": Decimal("2.0"),
    "Entre 3 et 10m3": Decimal("6.0"),
    "Entre 10 et 100m3": Decimal("50.0"),
    "Plus de 100m3": Decimal("150.0"),
}


def populate_volume_m3(apps, schema_editor):
    Constatation = apps.get_model("constatations", "Constatation")
    for legacy_text, numeric_val in LEGACY_VOLUME_MAPPING.items():
        Constatation.objects.filter(
            volume_depot=legacy_text, volume_m3__isnull=True
        ).update(volume_m3=numeric_val)


def reverse_populate_volume_m3(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("constatations", "0008_constatation_volume_m3"),
    ]

    operations = [
        migrations.RunPython(populate_volume_m3, reverse_populate_volume_m3),
    ]
