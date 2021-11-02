from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

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
        ('40 nmol', '40 nmol'), ('200 nmol', '200 nmol'), ('1 µmol', '1 µmol')),
        initial='40 nmol')
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('standard', 'Standard'), ('desalted', 'Desalted'), ('cartridge', 'Cartridge')),
        initial='standard')
    modification = forms.CharField(required=False, max_length=150)
    sequence = forms.CharField(max_length=150, widget=forms.TextInput(
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
        ('40 nmol', '40 nmol'), ('200 nmol', '200 nmol'), ('1 µmol', '1 µmol')),
        initial='40 nmol')
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('standard', 'Standard'), ('desalted', 'Desalted'), ('cartridge', 'Cartridge')),
        initial='standard')
    modification = forms.CharField(required=False, max_length=150)
    oligos = MultiOligoField(max_length=5000, widget=forms.Textarea)


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
