from django import forms

from .models import Template, Primer


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
