from django.contrib import admin
from .models import Primer, Template, Reaction, SeqPrice


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
                    'primer', 'status', ]


@admin.register(SeqPrice)
class PriceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Prices for standard sequencing',
         {'fields': (
             'standard_sequencing', 'ext_standard_sequencing',
         )}),
        ('96 well plate prices',
         {'fields': (
             'well96_plate', 'ext_well96_plate',
         )}),
        ('Large template (cosmids, etc) prices',
         {'fields': ('large_template', 'ext_large_template'
                     )}),
        ('PCR purification prices',
         {'fields': ('pcr_purification', 'ext_pcr_purification'
                     )}),
        ('Printout prices',
         {'fields': ('printout', 'ext_printout'
                     )}),
        ('Make current - only one at a time can be current!',
         {'fields': ('current',)})
    )
