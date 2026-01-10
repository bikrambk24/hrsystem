from .models import LeaveRequest
from employees.models import EmployeeProfile


def approved_leave_days(employee: EmployeeProfile) -> int:
    
    total = 0
    qs = LeaveRequest.objects.filter(
        employee=employee,
        status=LeaveRequest.STATUS_APPROVED
    )

    for lr in qs:
        total += lr.days_requested

    return total


def remaining_leave_days(employee: EmployeeProfile) -> int:
    used = approved_leave_days(employee)
    remaining = int(employee.annual_leave_entitlement) - int(used)

    return max(remaining, 0)
