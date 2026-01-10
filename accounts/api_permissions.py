from rest_framework.permissions import BasePermission
from .models import User

class IsHR(BasePermission):
   def has_permission(self, request, view):
       return request.user.is_authenticated and request.user.role == User.ROLE_HR

class IsTeamLead(BasePermission):
   def has_permission(self, request, view):
       return request.user.is_authenticated and request.user.role == User.ROLE_TL

class IsEmployee(BasePermission):
   def has_permission(self, request, view):
       return request.user.is_authenticated and request.user.role == User.ROLE_EMP
