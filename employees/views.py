from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from accounts.roles import is_hr, is_team_lead
from .models import EmployeeProfile
from .forms import EmployeeCreateForm, EmployeeUpdateForm, EmployeeSelfUpdateForm
from leaveapp.services import remaining_leave_days
from leaveapp.models import LeaveRequest


@is_hr
def hr_dashboard(request):
    total_employees = EmployeeProfile.objects.count()
    departments = (
        EmployeeProfile.objects.select_related("department")
        .values("department__name")
        .annotate(cnt=models.Count("id"))
        .order_by("-cnt")
    )
    pending_leave = LeaveRequest.objects.filter(status="PENDING").count()
    team_leads = User.objects.filter(role=User.ROLE_TL).count()

    return render(
        request,
        "employees/hr_dashboard.html",
        {
            "total_employees": total_employees,
            "departments": departments,
            "pending_leave": pending_leave,
            "team_leads": team_leads,
        },
    )


@is_team_lead
def teamlead_dashboard(request):
    team_size = EmployeeProfile.objects.filter(manager=request.user).count()
    pending = LeaveRequest.objects.filter(employee__manager=request.user, status="PENDING").count()
    return render(request, "employees/teamlead_dashboard.html", {"team_size": team_size, "pending": pending})


@login_required
def employee_dashboard(request):
    profile = request.user.employee_profile
    bal = remaining_leave_days(profile)
    pending = LeaveRequest.objects.filter(employee=profile, status="PENDING").count()
    return render(
        request,
        "employees/employee_dashboard.html",
        {"leave_balance": bal, "pending": pending},
    )


@is_hr
def hr_employee_list(request):
    q = request.GET.get("q", "").strip()
    qs = EmployeeProfile.objects.select_related("department", "manager", "user")
    if q:
        qs = qs.filter(
            models.Q(full_name__icontains=q)
            | models.Q(employee_id__icontains=q)
            | models.Q(user__email__icontains=q)
            | models.Q(department__name__icontains=q)
            | models.Q(designation__icontains=q)
        )

    employees = qs.order_by("full_name")
    rows = [{"emp": e, "leave_balance": remaining_leave_days(e)} for e in employees]
    return render(request, "employees/hr_employee_list.html", {"rows": rows, "q": q})


@is_hr
def hr_employee_create(request):
    form = EmployeeCreateForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        user, profile, password = form.save()
        request.session["new_employee_creds"] = {
            "email": user.email,
            "password": password,
            "employee_id": profile.employee_id,
            "name": profile.full_name,
        }
        return redirect("hr_employee_credentials")
    return render(request, "employees/hr_employee_form.html", {"form": form, "mode": "create"})


@is_hr
def hr_employee_credentials(request):
    creds = request.session.get("new_employee_creds")
    if not creds:
        messages.error(request, "No credentials to show.")
        return redirect("hr_employee_list")
    del request.session["new_employee_creds"]
    return render(request, "employees/hr_employee_credentials.html", {"creds": creds})


@is_hr
def hr_employee_edit(request, pk):
    emp = get_object_or_404(EmployeeProfile, pk=pk)
    form = EmployeeUpdateForm(request.POST or None, request.FILES or None, instance=emp)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Employee updated.")
        return redirect("hr_employee_list")
    return render(request, "employees/hr_employee_form.html", {"form": form, "mode": "edit", "emp": emp})


@is_hr
def hr_employee_delete(request, pk):
    emp = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == "POST":
        emp.user.delete()  # deletes profile via cascade
        messages.success(request, "Employee deleted.")
        return redirect("hr_employee_list")
    return render(request, "employees/hr_employee_delete.html", {"emp": emp})


@is_team_lead
def team_members(request):
    members = (
        EmployeeProfile.objects.filter(manager=request.user)
        .select_related("department", "user")
        .order_by("full_name")
    )
    return render(request, "employees/team_members.html", {"members": members})


@login_required
def my_profile(request):
    profile = request.user.employee_profile
    form = EmployeeSelfUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("my_profile")
    return render(request, "employees/my_profile.html", {"form": form, "profile": profile})
