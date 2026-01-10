from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from accounts.api_permissions import IsTeamLead
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from .services import remaining_leave_days


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "HR_MANAGER":
            return LeaveRequest.objects.select_related(
                "employee",
                "employee__user"
            ).all()

        if user.role == "TEAM_LEAD":
            return LeaveRequest.objects.select_related(
                "employee",
                "employee__user"
            ).filter(employee__manager=user)

        return LeaveRequest.objects.select_related(
            "employee",
            "employee__user"
        ).filter(employee=user.employee_profile)

    def perform_create(self, serializer):
        user = self.request.user

        if user.role in ["EMPLOYEE", "TEAM_LEAD"]:
            profile = user.employee_profile
            lr = serializer.save(employee=profile)

            # Validate balance
            if lr.days_requested > remaining_leave_days(profile):
                lr.delete()
                raise ValueError("Insufficient leave balance.")
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsTeamLead]
    )
    def approve(self, request, pk=None):
        lr = get_object_or_404(
            LeaveRequest,
            pk=pk,
            employee__manager=request.user
        )

        if lr.status != LeaveRequest.STATUS_PENDING:
            return Response(
                {"detail": "Already reviewed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lr.approve(request.user.email)
        return Response(LeaveRequestSerializer(lr).data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsTeamLead]
    )
    def reject(self, request, pk=None):
        lr = get_object_or_404(
            LeaveRequest,
            pk=pk,
            employee__manager=request.user
        )

        if lr.status != LeaveRequest.STATUS_PENDING:
            return Response(
                {"detail": "Already reviewed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lr.reject(request.user.email)
        return Response(LeaveRequestSerializer(lr).data)
