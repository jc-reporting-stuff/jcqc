from django import forms
from .models import Oligo

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
        fields = ['scale', 'purity', 'modification', 'name', 'sequence',]
        
    scale = forms.ChoiceField(widget=forms.RadioSelect, choices=(('4 nmol','4 nmol'),('200 nmol', '200 nmol'),('1 µmol','1 µmol')))
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(('standard','Standard'),('desalted', 'Desalted'),('cartridge','Cartridge')))
    modification = forms.CharField(required=False, max_length=150)


class EasyOrderForm(forms.Form):
    scale = forms.ChoiceField(widget=forms.RadioSelect, choices=(('4 nmol','4 nmol'),('200 nmol', '200 nmol'),('1 µmol','1 µmol')))
    purity = forms.ChoiceField(widget=forms.RadioSelect, choices=(('standard','standard'),('desalted', 'desalted'),('cartridge','cartridge')))
    modification = forms.CharField(required=False, max_length=150)
    oligos = forms.CharField(max_length=5000, widget=forms.Textarea)

