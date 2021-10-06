from django.contrib import admin
from .models import Oligo



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
