import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("configs")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()
CELERY_IMPORTS = ("tasks",)

app.conf.beat_schedule = {
    "check-tasks-every-day": {
        "task": "core.celery_tasks.check_tasks_for_today",
        "schedule": crontab(hour="0", minute="0"),
    },
}
