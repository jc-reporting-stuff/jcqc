from django.contrib import admin
from pages.models import Message


@admin.register(Message)
class PrimerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
        )}),
        ('Details', {'fields': (
            'headline', 'content'
        )}),
        ('Extra', {'fields': (
            'styling', 'is_active'
        )})
    )

    list_display = [
        'name', 'headline', 'content', 'is_active'
    ]
