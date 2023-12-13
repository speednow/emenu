from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

broker_url = "redis://redis:6379/0"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emenu_api.settings")

app = Celery("emenu_api", broker=broker_url)
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "send-dish-report-every-day-at-10am": {
        "task": "dish.tasks.send_dish_report",
        "schedule": crontab(hour=10, minute=0),
    },
}
