from django.contrib.auth import get_user_model
from django.contrib import messages
from allauth.account.views import SignupView
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from .models import Account, User
from .forms import  AccountsFormset

class AccountSignupView(SignupView):
    template_name = 'custom_signup.html'

class EditAccountView(TemplateView):
    template_name = 'edit_account.html'

class UpdateProfileView(UpdateView):
    model = get_user_model()
    fields = [
        'username', 'email', 'display_name', 'phone', 'extension', 'fax_number',
        'institution', 'department', 'room_number', 'address', 'city', 'province',
        'country', 'postal_code', 'is_student', 'is_supervisor',
    ]
    template_name = 'update_profile.html'

    def get_success_url(self):
        messages.success(self.request, 'Profile update successful!')
        return reverse('edit_account')


class UserAccountsView(TemplateResponseMixin, View):
    template_name = 'account_list.html'
    user = None

    def get_formset(self, data=None):
        return AccountsFormset(instance=self.request.user, data=data)

    def dispatch(self, request):
        self.user = get_object_or_404(User, id=request.user.id)
        return super().dispatch(request)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'user': self.user, 'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('edit_account')
        return self.render_to_response({'user': self.user, 'formset': formset})
    