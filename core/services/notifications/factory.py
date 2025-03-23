from core.services.notifications.overdue_notification import (
    OverdueNotificationMessageCreateService,
)
from core.services.notifications.reminder_notification import (
    ReminderNotificationMessageCreateService,
)
from tasks.models import Task
from tasks.models.choices import TaskNotificationKindChoices


class NotificationMessageCreateFactory:
    kind_map = {
        TaskNotificationKindChoices.REMINDER: ReminderNotificationMessageCreateService,
        TaskNotificationKindChoices.OVERDUE: OverdueNotificationMessageCreateService,
    }

    def __init__(self, task: Task, kind: TaskNotificationKindChoices):
        self.kind = kind
        self.task = task

    def execute(self):
        return self.kind_map.get(self.kind)(self.task)
