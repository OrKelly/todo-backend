from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.mixins import SerializerMapMixin
from tasks.api.v1.filters import TaskFilterSet
from tasks.api.v1.serializers import (
    CategorySerializer,
    TaskCreateUpdateSerializer,
    TaskListSerializer,
    TaskRetrieveSerializer,
)
from tasks.models import Category, Task
from tasks.services.tasks.task_complete import TaskCompleteService
from tasks.services.tasks.task_create import TaskCreateService
from tasks.services.tasks.task_delete import TaskDeleteService
from tasks.services.tasks.task_update import TaskUpdateService


class TaskViewSet(
    RetrieveModelMixin, ListModelMixin, SerializerMapMixin, GenericViewSet
):
    serializer_map = {
        "list": TaskListSerializer,
        "retrieve": TaskRetrieveSerializer,
        "create": TaskCreateUpdateSerializer,
        "partial_update": TaskCreateUpdateSerializer,
    }
    serializer_class = TaskListSerializer
    queryset = (
        Task.objects.with_is_active_annotation()
        .select_related("user")
        .prefetch_related("categories")
        .all()
    )
    filterset_class = TaskFilterSet

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = TaskCreateService(
            user=request.current_user, validated_data=serializer.validated_data
        ).execute()
        response_serializer = self.serializer_class(task)
        return Response(
            status=status.HTTP_201_CREATED, data=response_serializer.data
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "id",
                type=str,
                location=OpenApiParameter.PATH,
                description="ID задачи",
            )
        ]
    )
    def partial_update(self, request, pk):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = TaskUpdateService(
            task=task,
            validated_data=serializer.validated_data,
            user=request.current_user,
        ).execute()
        response_serializer = self.serializer_class(task)
        return Response(response_serializer.data)

    @extend_schema(request=None)
    @action(
        methods=["POST"], detail=True, url_name="complete", url_path="complete"
    )
    def complete(self, request, pk):
        task = self.get_object()
        task = TaskCompleteService(
            task=task, user=request.current_user
        ).execute()
        response_serializer = self.serializer_class(task)
        return Response(response_serializer.data)

    def destroy(self, request, pk):
        task = self.get_object()
        TaskDeleteService(task=task, user=request.current_user).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
