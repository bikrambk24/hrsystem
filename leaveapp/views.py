from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.roles import is_team_lead
from .models import LeaveRequest
from .forms import LeaveApplyForm
from .services import remaining_leave_days


@login_required
def leave_dashboard(request):
    profile = request.user.employee_profile
    requests = (
        LeaveRequest.objects
        .filter(employee=profile)
        .order_by("-created_at")[:50]
    )
    balance = remaining_leave_days(profile)

    return render(
        request,
        "leaveapp/leave_dashboard.html",
        {
            "requests": requests,
            "balance": balance,
        }
    )


@login_required
def leave_apply(request):
    profile = request.user.employee_profile
    balance = remaining_leave_days(profile)
    form = LeaveApplyForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        lr: LeaveRequest = form.save(commit=False)
        lr.employee = profile
        requested_days = lr.days_requested

        if requested_days <= 0:
            messages.error(request, "Invalid leave days.")
            return redirect("leave_apply")

        if requested_days > balance:
            messages.error(
                request,
                f"Not enough leave balance. You have {balance} days left."
            )
            return redirect("leave_apply")

        lr.save()
        messages.success(
            request,
            "Leave request submitted (Pending)."
        )
        return redirect("leave_dashboard")

    return render(
        request,
        "leaveapp/leave_apply.html",
        {
            "form": form,
            "balance": balance,
        }
    )


@is_team_lead
def leave_team_requests(request):
    
    pending = (
        LeaveRequest.objects
        .filter(
            employee__manager=request.user,
            status=LeaveRequest.STATUS_PENDING
        )
        .select_related(
            "employee",
            "employee__user",
            "employee__department"
        )
        .order_by("start_date")
    )

    return render(
        request,
        "leaveapp/leave_team_requests.html",
        {
            "pending": pending,
        }
    )


@is_team_lead
def approve_leave(request, pk):
    lr = get_object_or_404(
        LeaveRequest,
        pk=pk,
        employee__manager=request.user
    )

    if request.method == "POST":
        lr.approve(request.user.email)
        messages.success(request, "Leave approved.")
        return redirect("leave_team_requests")


@is_team_lead
def reject_leave(request, pk):
    lr = get_object_or_404(
        LeaveRequest,
        pk=pk,
        employee__manager=request.user
    )

    if request.method == "POST":
        lr.reject(request.user.email)
        messages.success(request, "Leave rejected.")
        return redirect("leave_team_requests")
