from django.contrib import admin
from .models import User, Account, Preapproval
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):

    ordering = ('-create_date',)
    list_display = ('username', 'email', 'display_name', 'is_active', 'is_staff', 'is_student', 'is_supervisor', 'student_list')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'display_name')}),
        ('Details', {'fields': (
            'phone', 'extension', 'fax_number', 'institution', 'department',
            'room_number', 'address', 'city', 'province', 'country', 'postal_code'
            )}),
        ('Permissions', {'fields': ('is_student', 'is_supervisor', 'is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'display_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    def student_list(self, obj):
        if obj.students.all():
            return list(obj.students.all().values_list('display_name', flat=True))
        else:
            return []

admin.site.register(User, UserAdminConfig)

class AccountAdminConfig(admin.ModelAdmin):
    list_display = ('owner', 'code', 'comment', 'is_active')

    fieldsets = (
        (None, {'fields': ('owner',)}),
        ('Details', {'fields': ('code', 'comment',)}),
        ('Status', {'fields': ('is_active',)}),
    )

admin.site.register(Account, AccountAdminConfig)
