from rest_framework import serializers
from .models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):
    days_requested = serializers.IntegerField(
        read_only=True
    )
    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True
    )
    employee_name = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",  
            "employee_id",
            "employee_name",
            "start_date",
            "end_date",
            "reason",
            "status",
            "days_requested",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]
        read_only_fields = [
            "status",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]
