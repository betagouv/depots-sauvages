from django.db import migrations
from django.db.models.signals import post_save

from backend.constatations.models import Constatation
from backend.signalements.signals import (
    generate_doc_constat,
    generate_document,
    generate_lettre_info,
)


def recalculate_prejudice_and_regenerate_docs(apps, schema_editor):
    # Filter only constatations with plainte and unknown prejudice amount
    qs = Constatation.objects.filter(
        plainte_etat__in=["Déposée", "Sera déposée"],
        prejudice_montant_connu=False,
    )

    for c in qs:
        # Disconnect signals to prevent enqueuing tasks during migrations
        post_save.disconnect(generate_doc_constat, sender=Constatation)
        post_save.disconnect(generate_lettre_info, sender=Constatation)
        try:
            # c.save() will recalculate the prejudice using our save() override
            c.save()
        finally:
            post_save.connect(generate_doc_constat, sender=Constatation)
            post_save.connect(generate_lettre_info, sender=Constatation)

        # Generate documents synchronously
        try:
            generate_document(c.id, "doc_constat", "constatations.constatation")
        except Exception:
            pass

        if c.auteur_identifie:
            try:
                generate_document(c.id, "lettre_info", "constatations.constatation")
            except Exception:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ("constatations", "0002_alter_constatation_prejudice_autres_couts_and_more"),
    ]

    operations = [
        migrations.RunPython(recalculate_prejudice_and_regenerate_docs),
    ]
