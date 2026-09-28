from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("proconnect", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProConnectAccessConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "categories_juridiques_autorisees",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="Liste JSON des catégories autorisées (ex: [{'code': '72', 'nom': 'Communes...'}])",
                        verbose_name="Catégories juridiques autorisées",
                    ),
                ),
                (
                    "sirens_autorises",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="Liste JSON des SIREN spécifiquement autorisés (ex: [{'siren': '157000019', 'nom': 'Gendarmerie...'}])",
                        verbose_name="SIREN autorisés (liste blanche)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Configuration d'accès ProConnect",
            },
        ),
    ]
