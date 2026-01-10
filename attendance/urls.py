from django.urls import path
from .views import my_attendance, clock_in, clock_out, hr_attendance_list, hr_employee_attendance

urlpatterns = [
   path("me/", my_attendance, name="my_attendance"),
   path("clock-in/", clock_in, name="clock_in"),
   path("clock-out/", clock_out, name="clock_out"),

   path("hr/", hr_attendance_list, name="hr_attendance_list"),
   path("hr/user/<int:user_id>/", hr_employee_attendance, name="hr_employee_attendance"),
]
