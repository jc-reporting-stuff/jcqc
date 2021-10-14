from django import forms
from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator
from .models import Oligo

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
        fields = ['scale', 'purity', 'modification', 'name', 'sequence', ]

    scale = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('4 nmol', '4 nmol'), ('200 nmol', '200 nmol'), ('1 µmol', '1 µmol')))
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('standard', 'Standard'), ('desalted', 'Desalted'), ('cartridge', 'Cartridge')))
    modification = forms.CharField(required=False, max_length=150)
    sequence = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'pattern': '[ACGTRYMWSKDHBVNIacgtrymwskdhbvni]+'}))


class MultiOligoField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        split_values = value.split('\n')
        return [v for v in split_values if v]

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
        ('4 nmol', '4 nmol'), ('200 nmol', '200 nmol'), ('1 µmol', '1 µmol')))
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(
        ('standard', 'Standard'), ('desalted', 'Desalted'), ('cartridge', 'Cartridge')))
    modification = forms.CharField(required=False, max_length=150)
    oligos = MultiOligoField(max_length=5000, widget=forms.Textarea)
