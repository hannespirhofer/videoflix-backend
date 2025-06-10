from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Media', {"fields": ["avatar"]}),
    )

admin.site.register(CustomUser, CustomUserAdmin)