from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Div, HTML

from .models import Primer, SeqPrice, Template
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
        self.fields['template'] = forms.ChoiceField(
            choices=template_choices, label='Template Name')
        self.fields['primer'] = forms.ChoiceField(
            choices=primer_choices, label='Primer Name')
        self.fields['comment'] = forms.CharField(required=False)
        self.fields['hardcopy'] = forms.BooleanField(required=False)


class MultiReactionField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        split_values = value.split('\n')
        return [v for v in split_values if v.strip()]

    def validate(self, value):
        super().validate(value)
        regex = r'^(.+?)[\t;,]\s*(.+?).*'
        for line in value:
            try:
                re.match(regex, line).groups()
            except:
                raise ValidationError(
                    'Check that input is comma, semicolon or tab delimited. One reaction per line.')


class TemplateModelForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = (
            'name', 'type', 'template_size', 'insert_size',
            'template_concentration', 'template_volume', 'comment', 'pcr_purify'
        )
        labels = {
            'template_size': 'Size<br>(total bp)',
            'insert_size': 'Insert Size<br>(bp)',
            'template_concentration': 'Conc.<br>(ng/µL)',
            'template_volume': 'Vol.<br>(µL)',
            'pcr_purify': 'Purification Required'
        }


class PrimerModelForm(forms.ModelForm):
    class Meta:
        model = Primer
        fields = (
            'name', 'concentration', 'volume', 'melting_temperature', 'sequence')
        labels = {
            'concentration': 'Conc.<br>(pmol/µL)',
            'volume': 'Vol.<br>(µL)',
            'melting_temperature': 'Temperature',
        }


class ReactionEasyOrderForm(forms.Form):
    template_type = forms.ChoiceField(label='Type', choices=(
        ('pl', 'Plasmid'),
        ('pp', 'PCR product'),
        ('co', 'Cosmid'),
        ('ot', 'Other'),
    ))
    template_size = forms.IntegerField(label='Size (bp)',
                                       widget=forms.TextInput(attrs={'class': 'form-number'}), validators=[MinValueValidator(500)])
    insert_size = forms.IntegerField(label='Insert Size (bp)',
                                     widget=forms.TextInput(attrs={'class': 'form-number'}), required=False)
    template_concentration = forms.IntegerField(label='Conc. (ng/µL)',
                                                widget=forms.TextInput(attrs={'class': 'form-number'}))
    template_volume = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-number'}), label='Volume (µL)')
    template_comment = forms.ChoiceField(choices=(
        ('no', 'None'),
        ('gc', 'GC rich'),
        ('at', 'AT rich'),
        ('lr', 'Long repeat'),
        ('hp', 'Homopolymer')
    ), required=False, label='Comment')
    pcr_purify = forms.BooleanField(required=False, label="PCR Purification?")

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
        max_length=5000, widget=forms.Textarea(attrs={'cols': '80'}), label='Paste your sequencing information here:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                'Template',
                Div(
                    'template_type',
                    'template_size',
                    'insert_size',
                    'template_concentration',
                    'template_volume',
                    'template_comment',
                    'pcr_purify',
                    css_class='row-holder-fieldset'
                ),
            ),
            Fieldset(
                'Primer',
                Div(
                    'primer_source',
                    'primer_concentration',
                    'primer_volume',
                    'hardcopy',
                    css_class='row-holder-fieldset'
                ),
            ),
            Field('reactions')
        )


class IdRangeForm(forms.Form):
    low = forms.IntegerField(
        widget=forms.TextInput, min_value=1, label="From", required=False)
    high = forms.IntegerField(
        widget=forms.TextInput,  min_value=1, label="To",
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
