from django.contrib.auth import get_user_model
from django.contrib import messages
from allauth.account.views import SignupView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import Preapproval, User
from .forms import  AccountsFormset, RequestSupervisorForm

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


def add_sent_message(request):
    return messages.info(request, r"Pre-approval requested. If your supervisor can't see you on their page in a few minutes, verify their email address, make sure their profile lists them as a supervisor, and try again.")

class RequestSupervisorView(FormView):
    form_class = RequestSupervisorForm
    template_name = 'request-supervisor.html'
    success_url = reverse_lazy('edit_account')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                supervisor = User.objects.get(email=email, is_supervisor=True)
            except:
                add_sent_message(request)
                return HttpResponseRedirect(reverse('edit_account'))

            # This line creates the preapproval in the model, with no account and not approved.
            Preapproval.objects.create(student=self.request.user, supervisor=supervisor, approved=False)


            subject = render_to_string('request_supervisor_email_subject.txt')
            body = render_to_string('request_supervisor_email_body.txt', {'user': self.request.user.display_name, 'site_domain': request.get_host })
            send_mail(
                subject,
                body,
                'DNAtest@uoguelph.ca',
                [email],
                fail_silently=False
            )
            add_sent_message(request)
            return self.form_valid(form)
        else:
             return self.form_invalid(form)