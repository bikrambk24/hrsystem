from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from accounts.roles import is_hr
from accounts.models import User
from .models import Attendance

@login_required
def my_attendance(request):
   today = Attendance.today_date()
   att, _ = Attendance.objects.get_or_create(user=request.user, date=today)
   history = Attendance.objects.filter(user=request.user).order_by("-date")[:30]
   return render(request, "attendance/my_attendance.html", {"today_att": att, "history": history, "today": today})

@login_required
def clock_in(request):
   if request.method != "POST":
       return redirect("my_attendance")
   today = Attendance.today_date()
   att, _ = Attendance.objects.get_or_create(user=request.user, date=today)
   if att.clock_in:
       messages.error(request, "You have already clocked in today.")
       return redirect("my_attendance")
   att.clock_in = timezone.now()
   att.save(update_fields=["clock_in"])
   messages.success(request, "✅ Clock-in successful.")
   return redirect("my_attendance")

@login_required
def clock_out(request):
   if request.method != "POST":
       return redirect("my_attendance")
   today = Attendance.today_date()
   att, _ = Attendance.objects.get_or_create(user=request.user, date=today)
   if not att.clock_in:
       messages.error(request, "You must clock in before clocking out.")
       return redirect("my_attendance")
   if att.clock_out:
       messages.error(request, "You have already clocked out today.")
       return redirect("my_attendance")
   att.clock_out = timezone.now()
   att.save(update_fields=["clock_out"])
   messages.success(request, "✅ Clock-out successful.")
   return redirect("my_attendance")

@is_hr
def hr_attendance_list(request):
   user_id = request.GET.get("user_id") or ""
   date_str = request.GET.get("date") or ""

   qs = Attendance.objects.select_related("user").all()
   if user_id:
       qs = qs.filter(user_id=user_id)
   if date_str:
       qs = qs.filter(date=date_str)

   qs = qs.order_by("-date")[:200]
   users = User.objects.filter(role__in=[User.ROLE_EMP, User.ROLE_TL]).order_by("email")

   return render(request, "attendance/hr_attendance_list.html", {
       "rows": qs,
       "users": users,
       "selected_user_id": user_id,
       "selected_date": date_str,
   })

@is_hr
def hr_employee_attendance(request, user_id):
   user = get_object_or_404(User, id=user_id)
   rows = Attendance.objects.filter(user=user).order_by("-date")[:60]
   return render(request, "attendance/hr_employee_attendance.html", {"emp": user, "rows": rows})
