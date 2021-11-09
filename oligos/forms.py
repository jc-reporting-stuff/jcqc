from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Field, Div
from .models import Oligo, OliPrice

import re


class OligoInitialForm(forms.Form):
    account_id = forms.ChoiceField()
    oligo_count = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        account_choices = kwargs.pop('account_choices')
        initial_oligos = kwargs.pop('initial_oligos')
        super().__init__(*args, **kwargs)
        self.fields['account_id'].choices = account_choices
        self.fields['oligo_count'].initial = initial_oligos


class OligoOrderForm(forms.ModelForm):
    class Meta:
        model = Oligo
        fields = ['name', 'sequence', 'scale', 'purity', 'modification', ]

    scale = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('40 nmole', '40 nmole'), ('200 nmole', '200 nmole'), ('1 µmole', '1 µmole')),
        initial='40 nmole')
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('standard', 'Standard'), ('desalted', 'Desalted'), ('cartridge', 'Cartridge')),
        initial='standard')
    modification = forms.CharField(required=True, max_length=150, initial='No')
    sequence = forms.CharField(max_length=150, label="Sequence 5′ to 3′", widget=forms.TextInput(
        attrs={'pattern': '[ACGTRYMWSKDHBVNIacgtrymwskdhbvni]+'}))


class MultiOligoField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        split_values = value.split('\n')
        return [v for v in split_values if v.strip()]

    def validate(self, value):
        super().validate(value)
        regex = r'^(.+?)[\t;,]\s*([ACGTRYMWSKDHBVNIacgtrymwskdhbvni]+)'
        for line in value:
            try:
                re.match(regex, line).groups()
            except:
                raise ValidationError(
                    'Check that input is comma, semicolon or tab delimited. One oligo per line.')


class EasyOrderForm(forms.Form):
    scale = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('40 nmole', '40 nmole'), ('200 nmole', '200 nmole'), ('1 µmole', '1 µmole')),
        initial='40 nmole')
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('standard', 'Standard'), ('desalted', 'Desalted'), ('cartridge', 'Cartridge')),
        initial='standard')
    modification = forms.CharField(required=True, max_length=150, initial='No')
    oligos = MultiOligoField(max_length=5000, widget=forms.Textarea(attrs={'cols': '80'}),
                             label="Oligos, see below for formatting instructions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'scale',
                'purity',
                'modification',
                css_class='row-holder',
            ),
            Div(
                Field('oligos'),
                css_class='row-holder'
            )
        )


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


class OligoTextSearch(forms.Form):
    text = forms.CharField(max_length=150, required=False)


class MultiODField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        split_values = value.split('\n')
        return [v for v in split_values if v.strip()]

    def validate(self, value):
        super().validate(value)
        regex = r'(\d+)[\t;,\s]+([\d\.]+)'
        for line in value:
            try:
                re.match(regex, line).groups()
            except:
                raise ValidationError(
                    'Check that input is comma, semicolon or tab delimited. One oligo per line.')


class EnterODForm(forms.Form):
    sample_volume = forms.DecimalField(label="Sample volume (mL)",
                                       widget=forms.TextInput(attrs={'class': 'short-input'}), required=True)
    dilution_factor = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'short-input'}), required=True)
    readings = MultiODField(
        max_length=10000, widget=forms.Textarea(), required=True)


class PriceForm(forms.ModelForm):
    class Meta:
        model = OliPrice
        exclude = ['current']
        labels = {
            'scale_40_base': 'Scale 40 nmole ($/base)',
            'scale_200_base': 'Scale 200 nmole ($/base)',
            'scale_1000_base': 'Scale 1 µmole ($/base)',
            'degenerate_40_base': 'Degenerate 40 nmole ($/base)',
            'degenerate_200_base': 'Degenerate 200 nmole ($/base)',
            'degenerate_1000_base': 'Degenerate 1 µmole ($/base)',
            'desalt_fee': 'Desalt fee ($/oligo)',
            'cartridge_fee': 'Cartridge fee ($/oligo)',
            'setup_fee': 'Setup fee ($/order)',
        }
