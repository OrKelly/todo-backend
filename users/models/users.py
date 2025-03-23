from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    user_id = models.CharField(
        verbose_name="ID пользователя " "(ID пользователя в ТГ)",
        unique=True,
        db_index=True,
        primary_key=True,
    )
    username = models.CharField(
        null=True, verbose_name="Никнейм пользователя", max_length=100
    )
    email = models.EmailField(
        verbose_name="Эл.почта пользователя (для регистрации в админке)",
        null=True,
        blank=True,
        unique=True,
    )
    registered_at = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
