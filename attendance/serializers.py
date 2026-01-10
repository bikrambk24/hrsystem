from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
   total_time = serializers.CharField(read_only=True)

   class Meta:
       model = Attendance
       fields = ["id", "date", "clock_in", "clock_out", "total_time"]
