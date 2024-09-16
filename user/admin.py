from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = 'username', 'fullname', 'role', 'is_superuser',
    filter_horizontal = 'user_permissions',
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'branch', 'fullname', 'role', 'birthday', 'start_time', 'end_time', 'phone', 'address')}),
    )


admin.site.unregister(Group)
