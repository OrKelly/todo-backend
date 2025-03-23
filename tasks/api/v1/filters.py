from datetime import date, datetime

from django.utils import timezone
from django_filters import rest_framework as filters


class TaskFilterSet(filters.FilterSet):
    user_id = filters.CharFilter(field_name="user_id")
    deadline = filters.DateFilter(method="filter_by_deadline")
    is_active = filters.BooleanFilter(field_name="is_active")
    ordering = filters.OrderingFilter(
        fields={"deadline": "deadline"}, field_labels={"deadline": "Дедлайн"}
    )

    def filter_by_deadline(self, qs, name, value):
        if not value:
            return qs

        if isinstance(value, date):
            # Если это datetime.date, преобразуем его в datetime
            deadline = datetime.combine(value, datetime.min.time())
        else:
            # Если value не является ожидаемым типом, можно обработать это как ошибку
            return qs

            # Если deadline наивный, делаем его осведомленным
        if timezone.is_naive(deadline):
            deadline = timezone.make_aware(deadline)

            # Приводим deadline к текущему часовому поясу
        deadline = deadline.astimezone(timezone.get_current_timezone())

        # Фильтруем по диапазону, чтобы учесть весь день
        start_of_day = deadline.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_of_day = deadline.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

        return qs.filter(deadline__range=(start_of_day, end_of_day))
