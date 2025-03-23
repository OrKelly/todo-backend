from django.db.models import BooleanField, Case, Q, QuerySet, Value, When

from tasks.models import TaskStatusChoices


class TaskQuerySet(QuerySet):
    def with_is_active_annotation(self):
        return self.annotate(
            is_active=Case(
                When(Q(status=TaskStatusChoices.DONE), then=Value(False)),
                default=Value(True),
                output_field=BooleanField(),
            )
        )
