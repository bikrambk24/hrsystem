from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
   use_in_migrations = True

   def _create_user(self, email, password, **extra_fields):
       if not email:
           raise ValueError("Email is required")
       email = self.normalize_email(email)
       user = self.model(email=email, username=email, **extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user

   def create_user(self, email, password=None, **extra_fields):
       extra_fields.setdefault("is_staff", False)
       extra_fields.setdefault("is_superuser", False)
       return self._create_user(email, password, **extra_fields)

   def create_superuser(self, email, password, **extra_fields):
       extra_fields.setdefault("is_staff", True)
       extra_fields.setdefault("is_superuser", True)
       extra_fields.setdefault("role", User.ROLE_HR)
       return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
   ROLE_HR = "HR_MANAGER"
   ROLE_TL = "TEAM_LEAD"
   ROLE_EMP = "EMPLOYEE"

   ROLE_CHOICES = [
       (ROLE_HR, "HR Manager"),
       (ROLE_TL, "Team Lead"),
       (ROLE_EMP, "Employee"),
   ]

   username = models.CharField(max_length=150, blank=True)
   email = models.EmailField(unique=True)

   role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EMP)
   must_change_password = models.BooleanField(default=False)

   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = []

   objects = UserManager()

   def __str__(self):
       return f"{self.email} ({self.role})"
