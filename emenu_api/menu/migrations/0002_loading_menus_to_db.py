from django.core.management import call_command
from django.db import migrations


def load_menu_data(apps, schema_editor):
    call_command("loaddata", "menu/menus.json")


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0001_initial"),
        ("dish", "0002_loading_dishes_to_db"),
    ]

    operations = [
        migrations.RunPython(load_menu_data),
    ]
