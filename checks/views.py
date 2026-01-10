from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from accounts.roles import is_hr
from employees.models import EmployeeProfile

from .forms import (
    DBSCheckForm,
    BankCheckForm,
    HomeOfficeCheckForm,
    CreditCheckForm,
)
from .services import (
    check_dbs,
    check_bank,
    check_home_office,
    check_credit,
)

CHECK_TYPES = ["dbs", "bank", "home_office", "credit"]


@is_hr
def check_page(request, employee_pk: int, check_type: str):
    if check_type not in CHECK_TYPES:
        messages.error(request, "Invalid check type.")
        return redirect("hr_employee_list")

    emp = get_object_or_404(EmployeeProfile, pk=employee_pk)

    form_map = {
        "dbs": DBSCheckForm,
        "bank": BankCheckForm,
        "home_office": HomeOfficeCheckForm,
        "credit": CreditCheckForm,
    }

    runner_map = {
        "dbs": lambda data: check_dbs(
            emp,
            data["dbs_number"],
        ),
        "bank": lambda data: check_bank(
            emp,
            data["account_name"],
            data["sort_code"],
            data["account_number"],
        ),
        "home_office": lambda data: check_home_office(
            emp,
            data["visa_ref"],
        ),
        "credit": lambda data: check_credit(
            emp,
            data["credit_ref"],
        ),
    }

    FormCls = form_map[check_type]
    form = FormCls(request.POST or None)

    result = None
    message = None
    passed = None

    if request.method == "POST" and form.is_valid():
        passed, message = runner_map[check_type](form.cleaned_data)
        result = True

        if passed:
            messages.success(request, message)
        else:
            messages.error(request, message)

    tabs = [
        {"key": "dbs", "label": "DBS"},
        {"key": "bank", "label": "Bank"},
        {"key": "home_office", "label": "Home Office"},
        {"key": "credit", "label": "Credit Agency"},
    ]

    return render(
        request,
        "checks/check_page.html",
        {
            "emp": emp,
            "check_type": check_type,
            "tabs": tabs,
            "form": form,
            "result": result,
            "passed": passed,
            "message": message,
        },
    )
