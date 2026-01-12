from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect

from .forms import LoginForm, ForceChangePasswordForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        # authenticate using email as username (works if your USERNAME_FIELD is email)
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, "accounts/login.html", {"form": form})

        auth_login(request, user)

        # first-login password change
        if getattr(user, "must_change_password", False):
            return redirect("force_change_password")

        return redirect("dashboard")

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    """
    Central router: sends user to correct dashboard based on role.
    """
    if request.user.role == User.ROLE_HR:
        return redirect("hr_dashboard")
    if request.user.role == User.ROLE_TL:
        return redirect("teamlead_dashboard")
    return redirect("employee_dashboard")


@login_required
def force_change_password(request):
    if not getattr(request.user, "must_change_password", False):
        return redirect("dashboard")

    form = ForceChangePasswordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        new_password = form.cleaned_data["new_password"]

        user = request.user
        user.set_password(new_password)          # ✅ correct hashing
        user.must_change_password = False        # ✅ stop forcing
        user.save()

        # keep session valid after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.")
        return redirect("dashboard")

    return render(request, "accounts/force_change_password.html", {"form": form})
