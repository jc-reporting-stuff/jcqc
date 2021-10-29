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
    volume = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True)
    OD_reading = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True)
    OD_reading_dilution_factor = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True)

    @property
    def OD(self):
        if self.OD_reading_reading:
            return float(self.OD_reading_reading) * float(self.OD_reading_reading_dilution_factor)
        else:
            return None

    @property
    def dna_sequence(self):
        spaced_sequence = ' '.join(self.sequence[i:i+3]
                                   for i in range(0, len(self.sequence), 3))
        return spaced_sequence

    @property
    def micrograms(self):
        if self.OD_reading:
            return round(float(self.micromoles) * float(self.molecular_weight), 1)
        else:
            return -1

    @property
    def micrograms_per_ml(self):
        if self.OD_reading:
            return round(float(self.micrograms) / float(self.volume), 2)
        else:
            return -1

    @property
    def micrograms_per_microliter(self):
        if self.OD_reading:
            return round(float(self.micrograms_per_ml) / 1000, 1)
        else:
            return -1

    @property
    def micromoles(self):
        if not self.OD_reading:
            return -1

        a = 15.4
        c = 7.3
        g = 11.7
        t = 8.8
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

        bases_sum = 0

        for nucleotide in self.sequence:
            letter = nucleotide.lower()
            if letter == 'a':
                bases_sum += a
            elif letter == 'c':
                bases_sum += c
            elif letter == 'g':
                bases_sum += g
            elif letter == 't':
                bases_sum += t
            elif letter == 'r':
                bases_sum += r
            elif letter == 'y':
                bases_sum += y
            elif letter == 'm':
                bases_sum += m
            elif letter == 'w':
                bases_sum += w
            elif letter == 's':
                bases_sum += s
            elif letter == 'k':
                bases_sum += k
            elif letter == 'd':
                bases_sum += d
            elif letter == 'h':
                bases_sum += h
            elif letter == 'b':
                bases_sum += b
            elif letter == 'v':
                bases_sum += v
            elif letter == 'n':
                bases_sum += n

        micromoles_made = float(self.OD_reading) / float(bases_sum)
        return round(micromoles_made, 3)

    @property
    def nanomoles(self):
        if self.OD_reading:
            return self.micromoles * 1000
        else:
            return -1

    @property
    def nanomoles_per_ml(self):
        if self.OD_reading:
            return round(float(self.nanomoles) / float(self.volume), 2)
        else:
            return -1

    @property
    def pmol_per_microliter(self):
        if self.OD_reading:
            return round(float(self.nanomoles_per_ml) / 1000, 1)
        else:
            return -1

    @property
    def molecular_weight(self):
        a = 312.2
        c = 288.2
        g = 323.2
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
        i = 754.8

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
            elif letter == 'i':
                mw += i

        # Return the calculated molecular weight.
        return round(mw, 2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Price(models.Model):
    scale_40_base = models.DecimalField(max_digits=5, decimal_places=2)
    scale_200_base = models.DecimalField(max_digits=5, decimal_places=2)
    scale_1000_base = models.DecimalField(max_digits=5, decimal_places=2)

    degenerate_40_base = models.DecimalField(max_digits=5, decimal_places=2)
    degenerate_200_base = models.DecimalField(max_digits=5, decimal_places=2)
    degenerate_1000_base = models.DecimalField(max_digits=5, decimal_places=2)

    desalt_fee = models.DecimalField(max_digits=5, decimal_places=2)
    cartridge_fee = models.DecimalField(max_digits=5, decimal_places=2)
    setup_fee = models.DecimalField(max_digits=5, decimal_places=2)

    updated = models.DateTimeField(auto_now=True)

    current = models.BooleanField()

    def __str__(self):
        return f'Price Structure updated {self.updated}'
