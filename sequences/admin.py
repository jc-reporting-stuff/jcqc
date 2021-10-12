from django.contrib import admin
from .models import Primer, Template


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
        (None, {'fields': ('submission_id', 'submitter', 'account')}),
        ('Details', {'fields': (
            'name', 'template_size', 'plate_name', 'well', 'status', 'completed_date', 'insert_size', 'pcr_purify', 'template_concentration', 'template_volume', 'primer',
        )}),
        ('Analysis', {'fields': ('filename',)}),
    )

    list_display = ['name', 'owner',
                    'create_date']
