from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from core.services.notifications.factory import (
    NotificationMessageCreateFactory,
)
from tasks.models import Task, TaskStatusChoices
from tasks.models.choices import TaskNotificationKindChoices

# from .notifications import send_notification


@shared_task()
def check_tasks_for_today():
    now = timezone.now()
    end_of_day = now.replace(hour=23, minute=59, second=59)

    tasks_today = Task.objects.filter(deadline__range=(now, end_of_day))

    for task in tasks_today:
        reminder_time = task.deadline - timedelta(hours=1)
        if reminder_time > now:
            send_task_reminder.apply_async((task.id,), eta=reminder_time)

        status_check_time = task.deadline
        check_task_status.apply_async((task.id,), eta=status_check_time)


@shared_task()
def send_task_reminder(task_id):
    task = Task.objects.get(id=task_id)
    notification_service = NotificationMessageCreateFactory(
        kind=TaskNotificationKindChoices.REMINDER, task=task
    ).execute()
    notification_service.notify()


@shared_task()
def check_task_status(task_id):
    task = Task.objects.get(id=task_id)

    if not task.status != TaskStatusChoices.DONE:
        task.status = TaskStatusChoices.OVERDUE
        task.save()
    notification_service = NotificationMessageCreateFactory(
        kind=TaskNotificationKindChoices.OVERDUE, task=task
    ).execute()
    notification_service.notify()
