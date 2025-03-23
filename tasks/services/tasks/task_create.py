from typing import NoReturn

from dateutil import parser
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.validators import ValidationError

from tasks.models import Task
from users.models import User


class TaskCreateService:
    def __init__(self, user: User, validated_data: dict):
        self._user = user
        self._validated_data = validated_data

    def execute(self) -> Task:
        self._validate()
        return self._create()

    def _validate(self) -> NoReturn:
        deadline = self._validated_data.get("deadline")
        now_date = timezone.now()
        if now_date > deadline:
            raise ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Дедлайн не может быть раньше сегодняшней даты",
            )
        if Task.objects.filter(
            user=self._user,
            title=self._validated_data.get("title"),
            deadline=deadline,
        ):
            raise ValidationError(
                code=status.HTTP_409_CONFLICT,
                detail="Такая задача уже существует",
            )

    @transaction.atomic
    def _create(self) -> Task:
        categories = self._validated_data.pop("categories", None)
        deadline = self._validated_data.pop("deadline")

        if isinstance(deadline, str):
            deadline = parser.isoparse(deadline)
        if timezone.is_aware(deadline):
            deadline = deadline.astimezone(timezone.get_current_timezone())
        else:
            deadline = timezone.make_aware(
                deadline, timezone=timezone.get_current_timezone()
            )

        task = Task.objects.create(
            user=self._user, deadline=deadline, **self._validated_data
        )
        if categories:
            task.categories.set(categories)
        return task
