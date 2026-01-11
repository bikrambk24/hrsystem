from django.db import models
from django.conf import settings
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    EMPLOYMENT_CHOICES = [
        ("FULL_TIME", "Full-time"),
        ("PART_TIME", "Part-time"),
        ("INTERN", "Intern"),
        ("CONTRACT", "Contract"),
    ]

    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
        ("PREFER_NOT", "Prefer not to say"),
    ]

    EDUCATION_CHOICES = [
        ("NONE", "None"),
        ("SCHOOL", "School"),
        ("COLLEGE", "College"),
        ("BACHELOR", "Bachelor"),
        ("MASTER", "Master"),
        ("PHD", "PhD"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )

    full_name = models.CharField(max_length=150)
    employee_id = models.CharField(max_length=50, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default="FULL_TIME")

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_employees"
    )

    annual_leave_entitlement = models.PositiveIntegerField(default=28)
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="PREFER_NOT")
    date_of_birth = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default="NONE")

    
    phone = models.CharField(max_length=30, blank=True, default="")
    address = models.TextField(blank=True, default="")
    emergency_contact = models.CharField(max_length=100, blank=True, default="")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.employee_id:
            self.employee_id = f"EMP{self.pk:05d}"
            super().save(update_fields=["employee_id"])

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"
