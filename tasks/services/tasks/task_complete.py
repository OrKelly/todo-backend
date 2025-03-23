import datetime
from typing import NoReturn

from rest_framework import status
from rest_framework.validators import ValidationError

from tasks.models import Task, TaskStatusChoices
from users.models import User


class TaskCompleteService:
    def __init__(self, task: Task, user: User):
        self._task = task
        self._user = user

    def execute(self) -> Task:
        self._validate()
        return self._change_status()

    def _validate(self) -> NoReturn:
        if self._task.user.user_id != self._user.user_id:
            raise ValidationError(
                code=status.HTTP_403_FORBIDDEN,
                detail="Редактирование чужой задачи запрещено",
            )
        if self._task.status == TaskStatusChoices.DONE:
            raise ValidationError(
                code=status.HTTP_400_BAD_REQUEST, detail="Задача уже завершена"
            )

    def _change_status(self) -> Task:
        self._task.status = TaskStatusChoices.DONE
        self._task.completed_at = datetime.datetime.today().date()
        self._task.save(update_fields=["status", "completed_at"])
        return self._task
