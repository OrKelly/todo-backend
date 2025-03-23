from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_v1_urlpatterns = [
    path("tasks/", include("tasks.api.v1.urls")),
    path("users/", include("users.api.v1.urls")),
]

swagger_urlpatterns = [
    path("", SpectacularAPIView.as_view(), name="swagger"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="swagger"),
        name="api-docs",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", include(swagger_urlpatterns)),
    path("api/v1/", include(api_v1_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
