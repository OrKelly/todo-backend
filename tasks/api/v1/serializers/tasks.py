from rest_framework import serializers

from tasks.api.v1.serializers.categories import CategorySerializer
from tasks.models import Category, Task
from users.api.v1.serializers.users import UserSerializer


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all()
        ),
        required=False,
    )

    class Meta:
        model = Task
        fields = ["categories", "title", "description", "deadline"]


class TaskRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "categories",
            "title",
            "description",
            "deadline",
            "status",
            "created_at",
            "completed_at",
        ]


class TaskListSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "deadline", "created_at", "is_active"]

    def get_is_active(self, obj: Task) -> bool:
        if hasattr(obj, "is_active"):
            return obj.is_active
        return obj.is_active_task
