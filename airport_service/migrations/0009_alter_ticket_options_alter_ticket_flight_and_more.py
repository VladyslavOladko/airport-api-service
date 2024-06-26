# Generated by Django 5.0.3 on 2024-04-08 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport_service", "0008_ticket"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
        migrations.AlterField(
            model_name="ticket",
            name="flight",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="airport_service.flight"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("flight", "row", "seat")},
        ),
    ]
