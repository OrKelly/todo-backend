import hashlib

from django.db import models

from .choices import TaskStatusChoices
from .managers import TaskQuerySet


class Task(models.Model):
    id = models.CharField(
        db_index=True,
        primary_key=True,
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Время добавления"
    )
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Пользователь",
        db_index=True,
    )
    categories = models.ManyToManyField(
        to="tasks.Category",
        related_name="tasks",
        blank=True,
        verbose_name="Категории",
    )
    title = models.CharField(
        verbose_name="Наименование задачи", max_length=100, db_index=True
    )
    description = models.TextField(
        verbose_name="Описание задачи",
        null=True,
        blank=True,
        max_length=250,
    )
    deadline = models.DateTimeField(verbose_name="Дедлайн выполнения задачи")
    status = models.PositiveIntegerField(
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.ACTIVE,
        verbose_name="Статус задачи",
    )
    completed_at = models.DateTimeField(
        verbose_name="Выполнена", null=True, blank=True
    )

    objects = TaskQuerySet().as_manager()

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def save(self, *args, **kwargs):
        if not self.id:
            unique_string = (
                f"{self.user.username}{self.title}{self.created_at}"
            )
            self.id = hashlib.sha256(unique_string.encode()).hexdigest()[:16]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_active_task(self):
        return self.status != TaskStatusChoices.DONE
