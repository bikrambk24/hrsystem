from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", dashboard_view, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("employees/", include("employees.urls")),
    path("leave/", include("leaveapp.urls")),
    path("checks/", include("checks.urls")),
    path("attendance/", include("attendance.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
