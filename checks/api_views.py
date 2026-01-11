from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.api_permissions import IsHR
from employees.models import EmployeeProfile

from .services import (
    check_dbs,
    check_bank,
    check_home_office,
    check_credit,
)


class DBSCheckAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHR]

    def post(self, request):
        employee_id = request.data.get("employee_id")
        dbs_number = request.data.get("dbs_number")

        if not employee_id or not dbs_number:
            return Response(
                {"detail": "employee_id and dbs_number required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        emp = EmployeeProfile.objects.filter(employee_id=employee_id).first()

        if not emp:
            return Response(
                {"detail": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        passed, message = check_dbs(emp, dbs_number)

        return Response(
            {"passed": passed, "message": message}
        )


class BankCheckAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHR]

    def post(self, request):
        employee_id = request.data.get("employee_id")
        account_name = request.data.get("account_name")
        sort_code = request.data.get("sort_code")
        account_number = request.data.get("account_number")

        if not all([employee_id, account_name, sort_code, account_number]):
            return Response(
                {
                    "detail": (
                        "employee_id, account_name, "
                        "sort_code, account_number required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        emp = EmployeeProfile.objects.filter(employee_id=employee_id).first()

        if not emp:
            return Response(
                {"detail": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        passed, message = check_bank(
            emp,
            account_name,
            sort_code,
            account_number,
        )

        return Response(
            {"passed": passed, "message": message}
        )


class HomeOfficeCheckAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHR]

    def post(self, request):
        employee_id = request.data.get("employee_id")
        visa_ref = request.data.get("visa_ref")

        if not employee_id or not visa_ref:
            return Response(
                {"detail": "employee_id and visa_ref required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        emp = EmployeeProfile.objects.filter(employee_id=employee_id).first()

        if not emp:
            return Response(
                {"detail": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        passed, message = check_home_office(emp, visa_ref)

        return Response(
            {"passed": passed, "message": message}
        )


class CreditCheckAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, IsHR]

    def post(self, request):
        employee_id = request.data.get("employee_id")
        credit_ref = request.data.get("credit_ref")

        if not employee_id or not credit_ref:
            return Response(
                {"detail": "employee_id and credit_ref required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        emp = EmployeeProfile.objects.filter(employee_id=employee_id).first()

        if not emp:
            return Response(
                {"detail": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        passed, message = check_credit(emp, credit_ref)

        return Response(
            {"passed": passed, "message": message}
        )
