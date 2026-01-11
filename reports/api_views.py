from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count

from accounts.api_permissions import IsHR
from accounts.models import User
from employees.models import EmployeeProfile
from leaveapp.models import LeaveRequest


class HRSummaryReportAPI(APIView):
    """
    HR-only summary report for dashboards and analytics.
    Endpoint: GET /api/reports/hr-summary/
    """

    permission_classes = [permissions.IsAuthenticated, IsHR]

    def get(self, request):
        total_employees = EmployeeProfile.objects.count()

        total_team_leads = User.objects.filter(
            role=User.ROLE_TL
        ).count()

        pending_leave = LeaveRequest.objects.filter(
            status=LeaveRequest.STATUS_PENDING
        ).count()

        dept_breakdown = (
            EmployeeProfile.objects
            .select_related("department")
            .values(
                "department__id",
                "department__name"
            )
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        gender_breakdown = (
            EmployeeProfile.objects
            .values("gender")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        employment_breakdown = (
            EmployeeProfile.objects
            .values("employment_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return Response({
            "total_employees": total_employees,
            "total_team_leads": total_team_leads,
            "pending_leave_requests": pending_leave,
            "department_breakdown": list(dept_breakdown),
            "gender_breakdown": list(gender_breakdown),
            "employment_breakdown": list(employment_breakdown),
        })