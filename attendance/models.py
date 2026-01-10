from django.conf import settings
from django.db import models
from django.utils import timezone

class Attendance(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendances")
   date = models.DateField()
   clock_in = models.DateTimeField(null=True, blank=True)
   clock_out = models.DateTimeField(null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
       constraints = [
           models.UniqueConstraint(fields=["user", "date"], name="unique_attendance_per_user_per_day")
       ]
       ordering = ["-date", "-created_at"]

   @staticmethod
   def today_date():
       return timezone.localdate()

   @property
   def total_time(self) -> str:
       if self.clock_in and self.clock_out:
           secs = int((self.clock_out - self.clock_in).total_seconds())
           secs = max(secs, 0)
           h = secs // 3600
           m = (secs % 3600) // 60
           s = secs % 60
           return f"{h:02d}:{m:02d}:{s:02d}"
       if self.clock_in and not self.clock_out:
           return "In progress"
       return "-"
