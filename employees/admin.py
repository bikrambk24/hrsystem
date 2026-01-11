from django.contrib import admin
from .models import Department, EmployeeProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "full_name", "department", "designation")
    search_fields = ("employee_id", "full_name", "user__email")
    list_filter = ("department", "employment_type", "gender")
