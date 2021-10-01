from allauth.account.forms import SignupForm
from django.db.models.fields import BooleanField
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.forms.models import ModelForm, inlineformset_factory
from django.urls import reverse
from django import forms
from .models import Account, User, Preapproval


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


AccountsFormset = inlineformset_factory(User, Account, fields=['code','comment','is_active'], extra=1, can_delete=False)

class RequestSupervisorForm(forms.Form):
    email = forms.EmailField(max_length=130, required=True, label='Supervisor email')


class ManageStudentsForm(forms.Form):
    def __init__(self, *args, user, **kwargs):
        super(ManageStudentsForm, self).__init__(*args, **kwargs)
        student_choices = ((approval_request.student.id, str(approval_request.student.display_name)) for approval_request in Preapproval.objects.filter(supervisor_id=user.id, approved=False))
        account_choices = ((account.id, str(account.code)) for account in user.accounts.all())
        self.fields['student'] = forms.ChoiceField(choices=student_choices, widget=forms.Select(attrs={'disabled':'disabled'}), required=False)
        self.fields['student_id'] = forms.CharField(max_length=10, widget=forms.widgets.HiddenInput())
        self.fields['account'] = forms.ChoiceField(choices=account_choices)


'''
class ManageStudentsForm(forms.ModelForm):
    class Meta:
        model = Preapproval
        fields = ['student','account','approved', 'supervisor']

    def __init__(self, *args, user, **kwargs):
        super(ManageStudentsForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.ModelChoiceField(queryset=user.students.all())
        self.fields['account'] = forms.ModelChoiceField(queryset=user.accounts.all())
        self.fields['approved'] = forms.BooleanField(required=False)
    '''