# Generated manually to fix nature_terrain data migration issue

from django.db import migrations


def convert_nature_terrain_data(apps, schema_editor):
    """
    Convert existing nature_terrain data to proper JSON format.
    This migration is needed because the nature_terrain field was change to a JSONField but
    the values in database was not properly converted to a json objects.
    """
    Signalement = apps.get_model("signalements", "Signalement")
    for signalement in Signalement.objects.all():
        if not signalement.nature_terrain:
            signalement.nature_terrain = []
            signalement.save()
            continue
        # If it's not a string, we suppose it's already a proper JSON object
        if not isinstance(signalement.nature_terrain, str):
            continue
        signalement.nature_terrain = [signalement.nature_terrain]
        signalement.save()


class Migration(migrations.Migration):

    dependencies = [
        ("signalements", "0010_alter_signalement_nature_terrain"),
    ]

    operations = [
        # Convert the data first (working with current JSONField)
        migrations.RunPython(
            convert_nature_terrain_data,
            migrations.RunPython.noop,
        ),
    ]
