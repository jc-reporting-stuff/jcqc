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
        fields = ['name', 'sequence']
