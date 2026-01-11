from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.roles import is_hr
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name"]


@is_hr
def create_department(request):
    form = DepartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Department created.")
        return redirect("hr_employee_list")
    return render(request, "employees/create_department.html", {"form": form})
