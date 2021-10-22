from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Primer
import re


class ReactionForm(forms.Form):
    def __init__(self, *args, templates, primers, ** kwargs):
        super().__init__(*args, **kwargs)
        template_choices = [(t.name, t.name)
                            for t in templates]
        common_primers = list(Primer.objects.filter(common=True))
        all_primers = primers + common_primers
        primer_choices = [
            (p.name, p.name) for p in all_primers]
        self.fields['template'] = forms.ChoiceField(choices=template_choices)
        self.fields['primer'] = forms.ChoiceField(choices=primer_choices)
        self.fields['hardcopy'] = forms.BooleanField(required=False)
        self.fields['comment'] = forms.CharField(required=False)


class MultiReactionField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        split_values = value.split('\n')
        return [v for v in split_values if v.strip()]

    def validate(self, value):
        super().validate(value)
        regex = r'^(.+?)[\t;,]\s*(.+?)[\t;,]\s*(.*?)\r$'
        for line in value:
            try:
                re.match(regex, line).groups()
            except:
                raise ValidationError(
                    'Check that input is comma, semicolon or tab delimited. One reaction per line.')


class ReactionEasyOrderForm(forms.Form):
    template_type = forms.ChoiceField(choices=(
        ('pl', 'Plasmid'),
        ('pp', 'PCR product'),
        ('co', 'Cosmid'),
        ('ot', 'Other'),
    ))
    template_size = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), validators=[MinValueValidator(500)])
    pcr_purify = forms.BooleanField(required=False, label="PCR Purification?")
    template_comment = forms.ChoiceField(choices=(
        ('no', 'None'),
        ('gc', 'GC rich'),
        ('at', 'AT rich'),
        ('lr', 'Long repeat'),
        ('hp', 'Homopolymer')
    ), required=False)
    insert_size = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), required=False)
    template_concentration = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), label='Template Conc (ng/µL)')
    template_volume = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), label='Template Volume (µL)')

    primer_source = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('cl', 'Client'),
        ('ls', 'Lab Services')
    ), initial='cl')
    hardcopy = forms.BooleanField(label='Hardcopy?', required=False)
    primer_concentration = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), label='Primer Conc (ng/µL)')
    primer_volume = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), label='Primer Volume (µL)')

    reactions = MultiReactionField(
        max_length=5000, widget=forms.Textarea, label='Paste your sequencing information here:')
