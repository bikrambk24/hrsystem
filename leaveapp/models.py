from django.db import models
from django.utils import timezone
from employees.models import EmployeeProfile


class LeaveRequest(models.Model):

    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="leave_requests"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    reviewed_by = models.EmailField(
        blank=True,
        default=""
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def days_requested(self) -> int:
        return max((self.end_date - self.start_date).days + 1, 0)

    def approve(self, reviewer_email: str):
        self.status = self.STATUS_APPROVED
        self.reviewed_by = reviewer_email
        self.reviewed_at = timezone.now()
        self.save(update_fields=["status", "reviewed_by", "reviewed_at"])

    def reject(self, reviewer_email: str):
        self.status = self.STATUS_REJECTED
        self.reviewed_by = reviewer_email
        self.reviewed_at = timezone.now()
        self.save(update_fields=["status", "reviewed_by", "reviewed_at"])

    def __str__(self):
        return f"{self.employee.employee_id} {self.start_date}→{self.end_date} ({self.status})"
