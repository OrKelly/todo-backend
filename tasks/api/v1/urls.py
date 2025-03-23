from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tasks.api.v1.views import CategoryViewSet, TaskViewSet

task_router = SimpleRouter()
category_router = SimpleRouter()

task_router.register("", TaskViewSet, "tasks")
category_router.register("categories", CategoryViewSet, "categories")

urlpatterns = [
    path(r"", include(category_router.urls)),
    path(r"", include(task_router.urls)),
]
