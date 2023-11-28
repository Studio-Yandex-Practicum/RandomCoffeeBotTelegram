from controlcenter.views import ControlCenter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import DashView

urlpatterns = [
    path("admin_user/", include("admin_user.urls"), name="admin_user"),
    path("admin/dashboard/", ControlCenter("controlcenter", DashView).urls),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
