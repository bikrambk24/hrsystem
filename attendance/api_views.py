from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.shortcuts import get_object_or_404

from accounts.api_permissions import IsHR
from accounts.models import User
from .models import Attendance
from .serializers import AttendanceSerializer

class MyAttendanceList(APIView):
   permission_classes = [permissions.IsAuthenticated]

   def get(self, request):
       qs = Attendance.objects.filter(user=request.user).order_by("-date")[:30]
       return Response(AttendanceSerializer(qs, many=True).data)

class ClockInAPI(APIView):
   permission_classes = [permissions.IsAuthenticated]

   def post(self, request):
       today = Attendance.today_date()
       att, _ = Attendance.objects.get_or_create(user=request.user, date=today)
       if att.clock_in:
           return Response({"detail": "Already clocked in today."}, status=status.HTTP_400_BAD_REQUEST)
       att.clock_in = timezone.now()
       att.save(update_fields=["clock_in"])
       return Response(AttendanceSerializer(att).data)

class ClockOutAPI(APIView):
   permission_classes = [permissions.IsAuthenticated]

   def post(self, request):
       today = Attendance.today_date()
       att, _ = Attendance.objects.get_or_create(user=request.user, date=today)
       if not att.clock_in:
           return Response({"detail": "Clock in first."}, status=status.HTTP_400_BAD_REQUEST)
       if att.clock_out:
           return Response({"detail": "Already clocked out today."}, status=status.HTTP_400_BAD_REQUEST)
       att.clock_out = timezone.now()
       att.save(update_fields=["clock_out"])
       return Response(AttendanceSerializer(att).data)

class HRUserAttendance(APIView):
   permission_classes = [permissions.IsAuthenticated, IsHR]

   def get(self, request, user_id):
       user = get_object_or_404(User, id=user_id)
       qs = Attendance.objects.filter(user=user).order_by("-date")[:60]
       return Response(AttendanceSerializer(qs, many=True).data)
