from django.core.management import call_command
from django.db import migrations


def load_dish_data(apps, schema_editor):
    call_command("loaddata", "dish/dishes.json")


class Migration(migrations.Migration):
    dependencies = [
        ("dish", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_dish_data),
    ]
