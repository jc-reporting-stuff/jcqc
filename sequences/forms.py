from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

from .models import Primer, SeqPrice
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


class IdRangeForm(forms.Form):
    low = forms.IntegerField(
        widget=forms.TextInput, max_value=1000000, min_value=1, label="From", required=False)
    high = forms.IntegerField(
        widget=forms.TextInput, max_value=1000000, min_value=1, label="To",
        required=False)


class DateRangeForm(forms.Form):
    low = forms.DateField(widget=forms.DateTimeInput(
        attrs={'type': 'date'}), required=False, label="Start Date")
    high = forms.DateField(widget=forms.DateTimeInput(
        attrs={'type': 'date'}), required=False, label="End Date")
    client = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)
        all_clients = get_user_model().objects.all().order_by('last_name')
        client_choices = [
            ('0', f'All Clients (Count: {len(all_clients)})'), ]
        for client in all_clients:
            client_choices.append(
                (client.id, f'{client.display_name()} ({client.id})'),)
        self.fields['client'].choices = client_choices


class TextSearch(forms.Form):
    text = forms.CharField(max_length=150, required=False)


class StatusForm(forms.Form):
    STATUS_CHOICES = [
        ('s', 'Submitted'),
        ('p', 'Preparing'),
        ('r', 'Running'),
    ]
    text = forms.ChoiceField(choices=STATUS_CHOICES)


class PriceForm(forms.ModelForm):
    class Meta:
        model = SeqPrice
        exclude = ['current']
