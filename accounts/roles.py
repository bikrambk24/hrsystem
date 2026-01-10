from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import User

def role_required(*allowed_roles):
   def decorator(view_func):
       @wraps(view_func)
       def _wrapped(request, *args, **kwargs):
           if not request.user.is_authenticated:
               return redirect("login")
           if request.user.role not in allowed_roles:
               return HttpResponseForbidden("Forbidden")
           return view_func(request, *args, **kwargs)
       return _wrapped
   return decorator

is_hr = role_required(User.ROLE_HR)
is_team_lead = role_required(User.ROLE_TL)
is_employee = role_required(User.ROLE_EMP)
