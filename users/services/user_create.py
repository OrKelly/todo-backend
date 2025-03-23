from typing import NoReturn

from rest_framework.exceptions import ValidationError

from users.models import User


class UserCreateService:
    def __init__(self, validated_data: dict):
        self._validated_data = validated_data

    def execute(self) -> User:
        self._validate()
        return self._create()

    def _validate(self) -> NoReturn:
        if User.objects.filter(
            user_id=self._validated_data.get("user_id")
        ).exists():
            raise ValidationError("Пользователь уже зарегистрирован")

    def _create(self) -> User:
        return User.objects.create(**self._validated_data)
