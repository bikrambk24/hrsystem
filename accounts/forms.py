from django import forms
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):
   email = forms.EmailField()
   password = forms.CharField(widget=forms.PasswordInput)

class ForceChangePasswordForm(forms.Form):
   new_password = forms.CharField(widget=forms.PasswordInput)
   confirm_password = forms.CharField(widget=forms.PasswordInput)

   def clean(self):
       cleaned = super().clean()
       p1 = cleaned.get("new_password")
       p2 = cleaned.get("confirm_password")
       if p1 and p2 and p1 != p2:
           raise forms.ValidationError("Passwords do not match.")
       if p1:
           validate_password(p1)
       return cleaned
