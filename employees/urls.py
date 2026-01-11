from django.urls import path
from .views import (
    hr_dashboard,
    teamlead_dashboard,
    employee_dashboard,
    hr_employee_list,
    hr_employee_create,
    hr_employee_edit,
    hr_employee_delete,
    hr_employee_credentials,
    team_members,
    my_profile,
)
from .department_views import create_department


urlpatterns = [
    path("hr/dashboard/", hr_dashboard, name="hr_dashboard"),
    path("teamlead/dashboard/", teamlead_dashboard, name="teamlead_dashboard"),
    path("employee/dashboard/", employee_dashboard, name="employee_dashboard"),

    path("hr/", hr_employee_list, name="hr_employee_list"),
    path("hr/create/", hr_employee_create, name="hr_employee_create"),
    path("hr/credentials/", hr_employee_credentials, name="hr_employee_credentials"),
    path("hr/<int:pk>/edit/", hr_employee_edit, name="hr_employee_edit"),
    path("hr/<int:pk>/delete/", hr_employee_delete, name="hr_employee_delete"),

    path("hr/departments/create/", create_department, name="create_department"),

    path("team/", team_members, name="team_members"),
    path("me/", my_profile, name="my_profile"),
]
