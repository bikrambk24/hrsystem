from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "start_date",
        "end_date",
        "days_requested",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "employee__employee_id",
        "employee__full_name",
        "employee__user__email",
    )
