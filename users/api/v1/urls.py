from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.api.v1.views import UserViewSet

router = SimpleRouter()

router.register("", UserViewSet, "users")

urlpatterns = [
    path(r"", include(router.urls)),
]
