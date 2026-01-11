from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.api_permissions import IsHR, IsTeamLead
from .models import Department, EmployeeProfile
from .serializers import DepartmentSerializer, EmployeeProfileSerializer, EmployeeSelfUpdateSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
   queryset = Department.objects.order_by("name")
   serializer_class = DepartmentSerializer
   permission_classes = [IsAuthenticated, IsHR]

class EmployeeViewSet(viewsets.ModelViewSet):
   serializer_class = EmployeeProfileSerializer
   permission_classes = [IsAuthenticated, IsHR]

   def get_queryset(self):
       qs = EmployeeProfile.objects.select_related("department", "manager", "user").order_by("full_name")
       q = self.request.query_params.get("q", "").strip()
       if q:
           from django.db import models
           qs = qs.filter(
               models.Q(full_name__icontains=q) |
               models.Q(employee_id__icontains=q) |
               models.Q(user__email__icontains=q) |
               models.Q(department__name__icontains=q) |
               models.Q(designation__icontains=q)
           )
       return qs

class MeViewSet(viewsets.GenericViewSet):
   permission_classes = [IsAuthenticated]

   @action(detail=False, methods=["get"])
   def profile(self, request):
       profile = request.user.employee_profile
       return Response(EmployeeProfileSerializer(profile).data)

   @action(detail=False, methods=["patch"])
   def update_profile(self, request):
       profile = request.user.employee_profile
       ser = EmployeeSelfUpdateSerializer(profile, data=request.data, partial=True)
       ser.is_valid(raise_exception=True)
       ser.save()
       return Response(EmployeeProfileSerializer(profile).data)

class TeamViewSet(viewsets.GenericViewSet):
   permission_classes = [IsAuthenticated, IsTeamLead]

   @action(detail=False, methods=["get"])
   def members(self, request):
       qs = EmployeeProfile.objects.filter(manager=request.user).select_related("department", "user").order_by("full_name")
       return Response(EmployeeProfileSerializer(qs, many=True).data)
