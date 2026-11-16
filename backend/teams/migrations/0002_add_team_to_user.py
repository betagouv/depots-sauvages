from django.db import migrations


def add_team_to_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Team = apps.get_model("teams", "Team")
    from django.db import models

    field = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        verbose_name="Organisation / Équipe",
    )
    field.set_attributes_from_name("team")
    schema_editor.add_field(User, field)


def remove_team_from_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    field = User._meta.get_field("team")
    schema_editor.remove_field(User, field)


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(add_team_to_user, remove_team_from_user),
    ]
