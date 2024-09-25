from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = 'phone', 'fullname', 'role', 'is_superuser',
    filter_horizontal = 'user_permissions',
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': (
            'branch', 'fullname', 'role', 'birthday', 'start_time', 'end_time', 'address')}),
    )


admin.site.unregister(Group)
