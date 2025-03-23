from typing import NoReturn

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError

from tasks.models import Task
from users.models import User


class TaskUpdateService:
    def __init__(self, task: Task, user: User, validated_data: dict):
        self._task = task
        self._user = user
        self._validated_data = validated_data

    def execute(self) -> Task:
        self._validate()
        return self._create()

    def _validate(self) -> NoReturn:
        deadline = self._validated_data.get("deadline")
        title = self._validated_data.get("title", self._task.title)
        now_date = timezone.now()
        if self._task.user.user_id != self._user.user_id:
            raise ValidationError(
                code=status.HTTP_403_FORBIDDEN,
                detail="Редактирование чужой задачи запрещено",
            )
        if deadline and now_date > deadline:
            raise ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Дедлайн не может быть раньше сегодняшней " "даты",
            )
        deadline = deadline if deadline else self._task.deadline
        if (
            Task.objects.filter(
                deadline=deadline, title=title, user=self._user
            )
            .exclude(id=self._task.id)
            .exists()
        ):
            raise ValidationError(
                code=status.HTTP_409_CONFLICT,
                detail="Такая задача уже существует",
            )

    @transaction.atomic
    def _create(self) -> Task:
        categories = self._validated_data.pop("categories", None)
        for attr, value in self._validated_data.items():
            if hasattr(self._task, attr):
                setattr(self._task, attr, value)
        self._task.save()
        if categories:
            self._task.categories.set(categories)
        return self._task
