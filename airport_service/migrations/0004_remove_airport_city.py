# Generated by Django 5.0.3 on 2024-03-27 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport_service", "0003_alter_airport_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="airport",
            name="city",
        ),
    ]
