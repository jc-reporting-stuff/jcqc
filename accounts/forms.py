from allauth.account.forms import SignupForm
from django.urls import reverse
from django import forms


class UserSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field.label})

    username = forms.CharField(label='Username', max_length=150, required=False)
    display_name = forms.CharField(max_length=150, label='Full name')
    phone = forms.CharField(max_length=30, required=True)
    extension = forms.CharField(max_length=40, label='Phone Extension', required=False)
    fax_number = forms.CharField(max_length=30, required=False, label='Fax number')
    institution = forms.CharField(max_length=150, required=False, label='Company or Institution')
    department = forms.CharField(max_length=150, required=False, label='Department')
    room_number = forms.CharField(max_length=150, required=False, label='Room number')
    address = forms.CharField(max_length=250, required=True, label='Address')
    city = forms.CharField(max_length=150, required=True, label='City')
    province = forms.CharField(max_length=100, required=True, label='Province/State')
    country = forms.CharField(max_length=150, required=True, label='Country')
    postal_code = forms.CharField(max_length=150, required=True, label='Postal or zip code')
    is_student = forms.BooleanField(label='Are you a student?', required=False)
    is_supervisor = forms.BooleanField(label='Are you UofG faculty or staff?', required=False)

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.display_name = self.cleaned_data['display_name']
        user.institution = self.cleaned_data['institution']
        user.save()
        return user

    def get_success_url(self):
        return reverse('edit_account')