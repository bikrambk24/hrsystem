from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
   fieldsets = DjangoUserAdmin.fieldsets + (
       ("Role", {"fields": ("role", "must_change_password")}),
   )
   add_fieldsets = DjangoUserAdmin.add_fieldsets + (
       ("Role", {"fields": ("role", "must_change_password")}),
   )
   list_display = ("email", "role", "is_staff", "must_change_password")
   ordering = ("email",)
   search_fields = ("email",)
