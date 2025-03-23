from django.db import models


class TaskStatusChoices(models.IntegerChoices):
    ACTIVE = 1, "Активная"
    DONE = 2, "Выполнена"
    OVERDUE = 3, "Просрочена"


class TaskNotificationKindChoices(models.IntegerChoices):
    REMINDER = 1, "Напоминание"
    OVERDUE = 2, "Просроченная задача"
