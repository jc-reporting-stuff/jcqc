from django.contrib import admin
from .models import Oligo, OliPrice


@admin.register(Oligo)
class OligoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('order_id', 'submitter', 'account')}),
        ('Details', {'fields': (
            'name', 'sequence', 'scale', 'purity', 'modification',
            'delivery_date', 'price', 'volume',
        )}),
        ('Analysis', {'fields': ('OD_reading',)}),
    )

    list_display = ['name', 'submitter', 'account',
                    'created_at', 'delivery_date']


@admin.register(OliPrice)
class PriceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Prices per base pair',
         {'fields': (
             'scale_40_base', 'scale_200_base', 'scale_1000_base',
         )}),
        ('Prices per degenerate base pair',
         {'fields': (
             'degenerate_40_base', 'degenerate_200_base', 'degenerate_1000_base',
         )}),
        ('Other fees',
         {'fields': ('desalt_fee', 'cartridge_fee', 'setup_fee',)
          }),
        ('Make current - only one at a time can be current!',
         {'fields': ('current',)})
    )
