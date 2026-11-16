import json
from pathlib import Path

from django.db import migrations


def load_initial_exclusions(apps, schema_editor):
    TeamAutoCreationExclusion = apps.get_model("teams", "TeamAutoCreationExclusion")
    fixture_path = (
        Path(__file__).resolve().parent.parent
        / "fixtures"
        / "initial_team_autocreation_exclusions.json"
    )
    if fixture_path.exists():
        with open(fixture_path, encoding="utf-8") as f:
            exclusions_data = json.load(f)

        for item in exclusions_data:
            fields = item.get("fields", {})
            siren = fields.get("siren", "")
            siret = fields.get("siret", "")
            label = fields.get("label", "")
            reason = fields.get("reason", "")

            # Avoid duplicates if fixture was partially or already loaded
            if siren:
                TeamAutoCreationExclusion.objects.get_or_create(
                    siren=siren,
                    siret=siret,
                    defaults={"label": label, "reason": reason},
                )
            elif siret:
                TeamAutoCreationExclusion.objects.get_or_create(
                    siret=siret,
                    defaults={"siren": siren, "label": label, "reason": reason},
                )


def populate_and_migrate_teams(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Team = apps.get_model("teams", "Team")
    TeamAutoCreationExclusion = apps.get_model("teams", "TeamAutoCreationExclusion")
    Constatation = apps.get_model("constatations", "Constatation")
    SuiviProcedure = apps.get_model("procedures", "SuiviProcedure")
    ProConnectProfile = apps.get_model("proconnect", "ProConnectProfile")

    # 0. Ensure initial exclusions are loaded
    load_initial_exclusions(apps, schema_editor)

    # 1. Backfill created_by and updated_by on Constatation from existing user
    for c in Constatation.objects.filter(user__isnull=False):
        c.created_by_id = c.user_id
        c.updated_by_id = c.user_id
        c.save(update_fields=["created_by", "updated_by"])

    # 2. Backfill updated_by on SuiviProcedure from constatation.updated_by
    for sp in SuiviProcedure.objects.filter(constatation__isnull=False):
        if sp.constatation.updated_by_id:
            sp.updated_by_id = sp.constatation.updated_by_id
            sp.save(update_fields=["updated_by"])

    # 3. Retrieve excluded SIREN and SIRET sets
    excluded_sirens = set(
        TeamAutoCreationExclusion.objects.exclude(siren="").values_list("siren", flat=True)
    )
    excluded_sirets = set(
        TeamAutoCreationExclusion.objects.exclude(siret="").values_list("siret", flat=True)
    )

    # 4. Migrate users with eligible ProConnect profiles to Teams
    for profile in ProConnectProfile.objects.select_related("user"):
        siret = (profile.siret or "").strip()
        siren = (profile.siren or "").strip() or (siret[:9] if len(siret) >= 9 else "")
        user = profile.user

        if not siret or len(siret) != 14:
            continue
        if siret in excluded_sirets or siren in excluded_sirens:
            continue

        team_name = (profile.organization_label or "").strip() or f"Organisation {siret}"
        team, _ = Team.objects.get_or_create(
            siret=siret,
            defaults={"name": team_name, "siren": siren},
        )

        if not user.team_id:
            user.team = team
            user.save(update_fields=["team"])

        # Associate historical user's constatations with the team
        Constatation.objects.filter(user=user, team__isnull=True).update(team=team)


def reverse_populate(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0002_add_team_to_user"),
        ("constatations", "0010_constatation_created_by_constatation_team_and_more"),
        ("procedures", "0009_suiviprocedure_updated_by"),
        ("proconnect", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_and_migrate_teams, reverse_populate),
    ]
