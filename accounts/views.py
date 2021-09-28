# from django.urls import reverse_lazy
# from django.views import generic
#from .forms import CustomUserCreationForm

# class SignUpPageView(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('account_email_verification_sent')
#     template_name = 'account/signup.html'

from django.contrib.auth import get_user_model
from django.contrib import messages
from allauth.account.views import SignupView
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse

class AccountSignupView(SignupView):
    template_name = 'custom_signup.html'

class EditAccountView(TemplateView):
    template_name = 'edit_account.html'

class UpdateProfileView(UpdateView):
    model = get_user_model()
    fields = [
        'username', 'email', 'display_name', 'phone', 'extension', 'fax_number',
        'institution', 'department', 'room_number', 'address', 'city', 'province',
        'country', 'postal_code', 'is_supervisor', 'is_student'
    ]
    template_name = 'update_profile.html'

    def get_success_url(self):
        messages.success(self.request, 'Profile update successful!')
        return reverse('edit_account')