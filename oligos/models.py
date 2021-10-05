from django.db.models.fields import CharField
from accounts.models import Account, User
from django.db import models


class Oligo(models.Model):
    order_id = models.IntegerField(unique=False)
    submitter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='oligo_orders')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='oligo_orders')
    name = CharField(max_length=150)
    sequence = models.CharField(max_length=150)
    scale = models.CharField(max_length=20)
    purity = models.CharField(max_length=20)
    modification = models.CharField(max_length=150, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(
        blank=True, null=True, auto_now_add=False, auto_now=False)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    volume = models.IntegerField()
    OD_reading = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
