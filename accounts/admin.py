from django.contrib import admin
from .models import User, Account, Preapproval
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):

    ordering = ('-create_date',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active',
                    'is_staff', 'user_type', 'student_list')

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
        ('Details', {'fields': (
            'phone', 'extension', 'fax_number', 'institution', 'department',
            'room_number', 'address', 'city', 'province', 'country', 'postal_code'
        )}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )

    def student_list(self, obj):
        if obj.students.all():
            # return list(set([obj.students.all().values_list('first_name', flat=True)))
            return list(set([s.display_name() for s in obj.students.all()]))
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
