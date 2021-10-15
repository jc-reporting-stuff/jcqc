from django.contrib import admin
from .models import Primer, Template, Reaction


@admin.register(Primer)
class PrimerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name', 'owner'
        )}),
        ('Details', {'fields': (
            'concentration', 'volume', 'melting_temperature', 'sequence', 'common'
        )})
    )

    list_display = [
        'name', 'common', 'concentration', 'volume', 'sequence'
    ]


@admin.register(Template)
class SequenceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'owner',)}),
        ('Details', {'fields': (
            'template_size', 'insert_size', 'pcr_purify', 'template_concentration', 'template_volume',
        )}),
    )

    list_display = ['name', 'owner',
                    'create_date']


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['submission_id', 'template',
                    'primer', 'status', 'sequence_id']
