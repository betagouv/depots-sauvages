# Generated by Django 5.2 on 2025-04-24 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("signalements", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="signalement",
            name="pdf_document",
            field=models.BinaryField("Document PDF", blank=True, null=True),
        ),
    ]
