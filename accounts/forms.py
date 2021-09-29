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
        form_fields = [
            'display_name', 'phone', 'extension', 'fax_number', 'institution', 'department', 'room_number',
            'address', 'city', 'province', 'country', 'postal_code',
            ]
        user.display_name = self.cleaned_data['display_name']
        user.phone = self.cleaned_data['phone']
        user.extension = self.cleaned_data['extension']
        user.fax_number = self.cleaned_data['fax_number']
        user.institution = self.cleaned_data['institution']
        user.department = self.cleaned_data['department']
        user.room_number = self.cleaned_data['room_number']
        user.address = self.cleaned_data['address']
        user.city = self.cleaned_data['city']
        user.province = self.cleaned_data['province']
        user.country = self.cleaned_data['country']
        user.postal_code = self.cleaned_data['postal_code']
        user.is_student = self.cleaned_data['is_student']
        user.is_supervisor = self.cleaned_data['is_supervisor']
        user.save()
        return user

    def get_success_url(self):
        return reverse('edit_account')