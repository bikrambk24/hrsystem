from django import forms
from django.utils import timezone
from .models import LeaveRequest


class LeaveApplyForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest
        fields = ["start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        if not start or not end:
            return cleaned

        if end < start:
            raise forms.ValidationError(
                "End date cannot be before start date."
            )

        
        if start < timezone.localdate():
            raise forms.ValidationError(
                "Start date cannot be in the past."
            )

        return cleaned
