from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    path("barang/", include("barang.urls")),

    path("inspection/", include("inspection.urls")),

    path("reports/", include("reports.urls")),

    path("server/", include("server.urls")),

    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )