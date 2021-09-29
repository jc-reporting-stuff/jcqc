from django.contrib import admin
from .models import User, Account
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

class UserAdminConfig(UserAdmin):

    ordering = ('-create_date',)
    list_display = ('username', 'email', 'display_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'display_name')}),
        ('Permissions', {'fields': ('is_student', 'is_supervisor', 'is_active')}),
        ('Personal', {'fields': ('institution',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'display_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

admin.site.register(User, UserAdminConfig)

admin.site.register(Account)
