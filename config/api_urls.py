from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from employees.api_views import (
    DepartmentViewSet,
    EmployeeViewSet,
    MeViewSet,
    TeamViewSet,
)
from leaveapp.api_views import LeaveRequestViewSet
from checks.api_views import (
    DBSCheckAPI,
    BankCheckAPI,
    HomeOfficeCheckAPI,
    CreditCheckAPI,
)
from attendance.api_views import (
    MyAttendanceList,
    ClockInAPI,
    ClockOutAPI,
    HRUserAttendance,
)
from accounts.api_views import ForceChangePasswordAPI


router = DefaultRouter()
router.register(r"departments", DepartmentViewSet, basename="departments")
router.register(r"employees", EmployeeViewSet, basename="employees")
router.register(r"me", MeViewSet, basename="me")
router.register(r"team", TeamViewSet, basename="team")
router.register(r"leave", LeaveRequestViewSet, basename="leave")


urlpatterns = [
    path("auth/token/", obtain_auth_token),
    path(
        "auth/force-change-password/",
        ForceChangePasswordAPI.as_view(),
    ),
    path("", include(router.urls)),

    path("checks/dbs/", DBSCheckAPI.as_view()),
    path("checks/bank/", BankCheckAPI.as_view()),
    path("checks/home-office/", HomeOfficeCheckAPI.as_view()),
    path("checks/credit/", CreditCheckAPI.as_view()),

    path("attendance/me/", MyAttendanceList.as_view()),
    path("attendance/clock-in/", ClockInAPI.as_view()),
    path("attendance/clock-out/", ClockOutAPI.as_view()),
    path(
        "attendance/users/<int:user_id>/",
        HRUserAttendance.as_view(),
    ),
]