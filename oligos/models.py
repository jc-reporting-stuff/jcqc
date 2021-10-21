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
    modification = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(
        blank=True, null=True, auto_now_add=False, auto_now=False)
    price = models.DecimalField(
        decimal_places=2, max_digits=7, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    OD_reading = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True)

    def dna_sequence(self):
        spaced_sequence = ' '.join(self.sequence[i:i+3]
                                   for i in range(0, len(self.sequence), 3))
        return spaced_sequence

    def molecular_weight(self):
        a = 312.2
        c = 288.2
        g = 303.2
        t = 303.2
        r = (a + g) / 2
        y = (c + t) / 2
        m = (a + c) / 2
        w = (a + t) / 2
        s = (c + g) / 2
        k = (g + t) / 2
        d = (a + g + t) / 3
        h = (a + c + t) / 3
        b = (c + g + t) / 3
        v = (a + c + g) / 3
        n = (a + c + g + t) / 4

        mw = 0

        for nucleotide in self.sequence:
            letter = nucleotide.lower()
            if letter == 'a':
                mw += a
            elif letter == 'c':
                mw += c
            elif letter == 'g':
                mw += g
            elif letter == 't':
                mw += t
            elif letter == 'r':
                mw += r
            elif letter == 'y':
                mw += y
            elif letter == 'm':
                mw += m
            elif letter == 'w':
                mw += w
            elif letter == 's':
                mw += s
            elif letter == 'k':
                mw += k
            elif letter == 'd':
                mw += d
            elif letter == 'h':
                mw += h
            elif letter == 'b':
                mw += b
            elif letter == 'v':
                mw += v
            elif letter == 'n':
                mw += n

        # Return the calculated molecular weight.
        return round(mw, 2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
