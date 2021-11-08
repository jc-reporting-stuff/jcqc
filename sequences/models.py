from django.db import models


from accounts.models import Account, User


class Primer(models.Model):
    name = models.CharField(max_length=50)
    concentration = models.IntegerField()
    volume = models.IntegerField()
    melting_temperature = models.IntegerField(blank=True, null=True)
    common = models.BooleanField(
        "Is an LSD common primer", blank=True, null=True)
    sequence = models.CharField(
        max_length=150, null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    def dna_sequence(self):
        spaced_sequence = ' '.join(self.sequence[i:i+3]
                                   for i in range(0, len(self.sequence), 3))
        return spaced_sequence

    @property
    def source(self):
        return 'LSD' if self.common else 'Client'


class Template (models.Model):
    COMMENT_CHOICES = [
        ('no', 'None'),
        ('gc', 'GC rich'),
        ('at', 'AT rich'),
        ('lr', 'Long repeat'),
        ('hp', 'Homopolymer')

    ]

    TEMPLATE_TYPES = [
        ('pl', 'Plasmid'),
        ('pp', 'PCR product'),
        ('co', 'Cosmid'),
        ('ot', 'Other'),

    ]

    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    comment = models.CharField(
        max_length=2, choices=COMMENT_CHOICES, blank=True, null=True, default='no')
    type = models.CharField(max_length=2, choices=TEMPLATE_TYPES)
    template_size = models.IntegerField()
    insert_size = models.IntegerField(blank=True, null=True)
    pcr_purify = models.BooleanField("PCR Purify?")
    template_concentration = models.IntegerField()
    template_volume = models.IntegerField()
    primers = models.ManyToManyField(
        Primer, related_name='sequences', through='Reaction')

    def __str__(self):
        return self.name

    def get_pcr_purify(self):
        return 'Yes' if self.pcr_purify else 'No'


class Reaction(models.Model):
    STATUS_CHOICES = [
        ('s', 'Submitted'),
        ('p', 'Preparing'),
        ('r', 'Running'),
        ('c', 'Completed')
    ]

    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    primer = models.ForeignKey(Primer, on_delete=models.CASCADE)
    comment = models.CharField(max_length=150, blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    submission_id = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    plate_name = models.CharField(max_length=20, blank=True, null=True)
    well = models.CharField(max_length=10, blank=True, null=True)
    submit_date = models.DateField(
        auto_now=False, auto_now_add=True)
    complete_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    filename = models.CharField(max_length=150, null=True, blank=True)
    hardcopy = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.template} with {self.primer}'

    @property
    def source(self):
        if self.submitter.user_type == 's' or self.submitter.user_type == 'p':
            return 'LSD'
        else:
            return 'External'

    def get_comment(self):
        return self.comment if self.comment else ' - - '

    def get_hardcopy(self):
        return 'Yes' if self.hardcopy else 'No'


class SeqPrice(models.Model):
    standard_sequencing = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Standard Sequencing')
    ext_standard_sequencing = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Standard sequencing (external)")

    well96_plate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="96-well plate (min 48)")
    ext_well96_plate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="96-well plate (external)")

    large_template = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Large templates (cosmid, etc)")
    ext_large_template = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Large templates (external)")

    pcr_purification = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="PCR Purification")
    ext_pcr_purification = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="PCR Purification (external)")

    printout = models.DecimalField(max_digits=5, decimal_places=2)
    ext_printout = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Printout (external)")

    updated = models.DateTimeField(auto_now=True)

    current = models.BooleanField()

    def __str__(self):
        return f'Price Structure updated {self.updated}'
