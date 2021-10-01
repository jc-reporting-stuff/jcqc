from django.contrib.auth import get_user_model
from django.contrib import messages
from allauth.account.views import SignupView
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Account

from .models import Preapproval, User
from .forms import  AccountsFormset, RequestSupervisorForm, ManageStudentsForm

class AccountSignupView(SignupView):
    template_name = 'custom_signup.html'


class EditAccountView(TemplateView):
    template_name = 'edit_account.html'

    def get_context_data(self, **kwargs):
        context = super(EditAccountView, self).get_context_data(**kwargs)
        context['pending_approval'] = Preapproval.objects.filter(supervisor=self.request.user, approved=False)
        return context


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
    

class ApproveStudentsView(FormView):
    template_name = 'approve_students.html'

    def get(self, request, *args, **kwargs):
        ManageStudentsFormset = formset_factory(ManageStudentsForm, extra=0)
        objects_awaiting_approval = Preapproval.objects.filter(supervisor_id=request.user.id, approved=False)
        initial_values = []
        for object in objects_awaiting_approval:
            initial_values.append({'student': str(object.student.id), 'account': '', 'student_id': str(object.student.id) })
        formset = ManageStudentsFormset(initial=initial_values, form_kwargs={'user': request.user})
        return render(request, 'approve_students.html', {'formset': formset})

    def post(self, request, *args, **kwargs):
        ManageStudentsFormset = formset_factory(ManageStudentsForm)
        formset = ManageStudentsFormset(request.POST, form_kwargs={'user': request.user})
        if formset.is_valid():
            for form in formset:
                cd = form.cleaned_data
                student = User.objects.get(id=cd['student_id'])
                supervisor = User.objects.get(id=request.user.id)
                account = Account.objects.get(id=cd['account'])
                try:
                    p = Preapproval.objects.get(supervisor=supervisor, student=student, approved=False)
                    p.approved=True
                    p.save()
                    print(p)
                except:
                    print('oh crap didnt save')
            messages.success(self.request, 'Changes applied successfully.')
            return redirect(reverse('edit_account'))
        return render(request, 'approve_students.html', {'formset': formset})


'''
class ApproveStudentsView(FormView):
    template_name = 'approve_students.html'

    def get(self, request, *args, **kwargs):
        ManageStudentFormset = formset_factory(ManageStudentsForm, can_delete=True)
        initial_students = Preapproval.objects.filter(supervisor=request.user).values_list('student_id', flat=False)
        initial_accounts = Preapproval.objects.filter(supervisor=request.user).values_list('account', flat=False)
        initial_approved = Preapproval.objects.filter(supervisor=request.user).values_list('approved', flat=False)
        initial_list = []
        for i in range(len(initial_students)):
            initial_list.append({'students': initial_students[i], 'account': initial_accounts[i], 'approved': initial_approved[i]})
        formset = ManageStudentFormset(form_kwargs={'user': request.user}, initial=initial_list)
        return render(request, 'approve_students.html', {'formset': formset})

    def post(self, request, *args, **kwargs):
        ManageStudentFormset = formset_factory(ManageStudentsForm)
        formset = ManageStudentFormset(request.POST, form_kwargs={'user': request.user})
        if formset.is_valid():
            for form in formset:
                obj = form.save(commit=False)
                obj.supervisor = request.user
                form.save()
            HttpResponseRedirect(reverse('edit_account'))
        else:
            return render(request, 'approve_students.html', {'formset': formset})
'''
    



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
        return render(request, 'account_list.html', {'user': self.user, 'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('edit_account')
        return self.render(request, 'account_list.html', {'user': self.user, 'formset': formset})


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

            student_supervisor_pair_exists = Preapproval.objects.filter(student=self.request.user, supervisor=supervisor)

            if not student_supervisor_pair_exists:
                # This line creates the preapproval in the model, with no account and not approved.
                Preapproval.add_new(student=self.request.user, supervisor=supervisor, approved=False)


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