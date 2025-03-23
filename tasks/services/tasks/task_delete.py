from typing import NoReturn

from rest_framework import status
from rest_framework.exceptions import ValidationError

from tasks.models import Task
from users.models import User


class TaskDeleteService:
    def __init__(self, task: Task, user: User):
        self._task = task
        self._user = user

    def execute(self) -> NoReturn:
        self._validate()
        self._delete()

    def _validate(self) -> NoReturn:
        if self._task.user.user_id != self._user.user_id:
            raise ValidationError(
                code=status.HTTP_403_FORBIDDEN,
                detail="Удаление чужой задачи запрещено",
            )

    def _delete(self) -> NoReturn:
        self._task.delete()
