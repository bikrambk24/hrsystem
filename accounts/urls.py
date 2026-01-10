from django.urls import path
from .views import login_view, logout_view, dashboard, force_change_password

urlpatterns = [
   path("login/", login_view, name="login"),
   path("logout/", logout_view, name="logout"),
   path("force-change-password/", force_change_password, name="force_change_password"),
   path("dashboard/", dashboard, name="dashboard"),
]
