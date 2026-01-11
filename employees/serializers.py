from rest_framework import serializers
from .models import Department, EmployeeProfile

class DepartmentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Department
       fields = ["id", "name"]

class EmployeeProfileSerializer(serializers.ModelSerializer):
   email = serializers.CharField(source="user.email", read_only=True)
   role = serializers.CharField(source="user.role", read_only=True)

   department = DepartmentSerializer(read_only=True)
   department_id = serializers.PrimaryKeyRelatedField(
       queryset=Department.objects.all(),
       source="department",
       write_only=True
   )

   manager_email = serializers.SerializerMethodField()

   class Meta:
       model = EmployeeProfile
       fields = [
           "id", "employee_id", "full_name",
           "email", "role",
           "department", "department_id",
           "designation", "joining_date", "employment_type",
           "manager", "manager_email",
           "annual_leave_entitlement",
           "gender", "date_of_birth", "education",
           "phone", "address", "emergency_contact",
           "profile_picture",
       ]

   def get_manager_email(self, obj):
       return obj.manager.email if obj.manager else None

class EmployeeSelfUpdateSerializer(serializers.ModelSerializer):
   class Meta:
       model = EmployeeProfile
       fields = ["phone", "address", "emergency_contact", "profile_picture"]

