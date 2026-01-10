from django.urls import path
from .views import (
    leave_dashboard,
    leave_apply,
    leave_team_requests,
    approve_leave,
    reject_leave,
)

urlpatterns = [
    path(
        "",
        leave_dashboard,
        name="leave_dashboard"
    ),
    path(
        "apply/",
        leave_apply,
        name="leave_apply"
    ),
    path(
        "team/",
        leave_team_requests,
        name="leave_team_requests"
    ),
    path(
        "team/<int:pk>/approve/",
        approve_leave,
        name="approve_leave"
    ),
    path(
        "team/<int:pk>/reject/",
        reject_leave,
        name="reject_leave"
    ),
]
