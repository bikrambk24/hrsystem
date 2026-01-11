from django import forms
from django.utils.crypto import get_random_string
from django.utils import timezone
from accounts.models import User
from .models import EmployeeProfile, Department


class EmployeeCreateForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    department = forms.ModelChoiceField(queryset=Department.objects.order_by("name"))
    designation = forms.CharField(max_length=100)
    joining_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    employment_type = forms.ChoiceField(choices=EmployeeProfile.EMPLOYMENT_CHOICES)
    gender = forms.ChoiceField(choices=EmployeeProfile.GENDER_CHOICES)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    education = forms.ChoiceField(choices=EmployeeProfile.EDUCATION_CHOICES)
    role = forms.ChoiceField(choices=[(User.ROLE_TL, "Team Lead"), (User.ROLE_EMP, "Employee")])
    manager = forms.ModelChoiceField(queryset=User.objects.none(), required=False)
    annual_leave_entitlement = forms.IntegerField(min_value=0, initial=28)
    profile_picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["manager"].queryset = User.objects.filter(role=User.ROLE_TL, is_active=True).order_by("email")
        self.fields["manager"].empty_label = "No manager"

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get("date_of_birth")
        if dob and dob > timezone.localdate():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob

    def save(self):
        email = self.cleaned_data["email"].lower()
        password = get_random_string(10)

        user = User.objects.create_user(
            email=email,
            password=password,
            role=self.cleaned_data["role"],
        )
        user.must_change_password = True
        user.save(update_fields=["must_change_password"])

        profile = EmployeeProfile.objects.create(
            user=user,
            full_name=self.cleaned_data["full_name"],
            department=self.cleaned_data["department"],
            designation=self.cleaned_data["designation"],
            joining_date=self.cleaned_data["joining_date"],
            employment_type=self.cleaned_data["employment_type"],
            manager=self.cleaned_data.get("manager"),
            annual_leave_entitlement=self.cleaned_data["annual_leave_entitlement"],
            profile_picture=self.cleaned_data.get("profile_picture"),
            gender=self.cleaned_data["gender"],
            date_of_birth=self.cleaned_data.get("date_of_birth"),
            education=self.cleaned_data["education"],
        )

        return user, profile, password


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = [
            "full_name",
            "department",
            "designation",
            "joining_date",
            "employment_type",
            "manager",
            "annual_leave_entitlement",
            "profile_picture",
            "gender",
            "date_of_birth",
            "education",
            "phone",
            "address",
            "emergency_contact",
        ]
        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


class EmployeeSelfUpdateForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["phone", "address", "emergency_contact", "profile_picture"]
