from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginForm, ForceChangePasswordForm
from .models import User

def login_view(request):
   if request.user.is_authenticated:
       return redirect("dashboard")

   form = LoginForm(request.POST or None)
   if request.method == "POST" and form.is_valid():
       email = form.cleaned_data["email"].lower()
       password = form.cleaned_data["password"]
       user = authenticate(request, email=email, password=password)
       if user:
           dj_login(request, user)
           if user.must_change_password:
               return redirect("force_change_password")
           return redirect("dashboard")
       messages.error(request, "Invalid credentials.")
   return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
   dj_logout(request)
   return redirect("login")

@login_required
def force_change_password(request):
   if not request.user.must_change_password:
       return redirect("dashboard")

   form = ForceChangePasswordForm(request.POST or None)
   if request.method == "POST" and form.is_valid():
       request.user.set_password(form.cleaned_data["new_password"])
       request.user.must_change_password = False
       request.user.save(update_fields=["must_change_password"])
       messages.success(request, "Password updated. Please log in again.")
       dj_logout(request)
       return redirect("login")

   return render(request, "accounts/force_change_password.html", {"form": form})

@login_required
def dashboard(request):
   if request.user.role == User.ROLE_HR:
       return redirect("hr_dashboard")
   if request.user.role == User.ROLE_TL:
       return redirect("teamlead_dashboard")
   return redirect("employee_dashboard")
