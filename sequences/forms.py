from django import forms

from .models import Template, Primer


class ReactionForm(forms.Form):
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        templates_available = Template.objects.filter(
            owner=user).order_by('-create_date')
        primers_available = Primer.objects.filter(common=True) | Primer.objects.filter(
            owner=user).order_by('-create_date')
        template_choices = [(t.id, t.name)
                            for t in templates_available]
        primer_choices = [(p.id, p.name) for p in primers_available]
        self.fields['template'] = forms.ChoiceField(choices=template_choices)
        self.fields['primer'] = forms.ChoiceField(choices=primer_choices)
        self.fields['hardcopy'] = forms.BooleanField(required=False)
