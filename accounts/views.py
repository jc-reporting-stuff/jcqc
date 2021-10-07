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
from .forms import  AccountsFormset, RequestSupervisorForm, ManageStudentsForm, ApproveStudentsForm

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
        'email', 'display_name', 'phone', 'extension', 'fax_number',
        'institution', 'department', 'room_number', 'address', 'city', 'province',
        'country', 'postal_code', 'is_student', 'is_supervisor',
    ]
    template_name = 'update_profile.html'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

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


class ApproveStudentsView(FormView):
    template_name = 'approve_students.html'

    def get(self, request, *args, **kwargs):
        ManageStudentsFormset = formset_factory(ApproveStudentsForm, extra=0, can_delete=True)
        objects_awaiting_approval = Preapproval.objects.filter(supervisor_id=request.user.id, approved=False)
        initial_values = []
        for object in objects_awaiting_approval:
            initial_values.append({'student': str(object.student.id), 'account': '', 'student_id': str(object.student.id) })
        formset = ManageStudentsFormset(initial=initial_values, form_kwargs={'user': request.user})
        return render(request, 'approve_students.html', {'formset': formset})

    def post(self, request, *args, **kwargs):
        ApproveStudentsFormset = formset_factory(ApproveStudentsForm, can_delete=True)
        formset = ApproveStudentsFormset(request.POST, form_kwargs={'user': request.user})
        if formset.is_valid():

            # If the form needs to be deleted, delete it.
            for form in formset.deleted_forms:
                cd = form.cleaned_data
                student = User.objects.get(id=cd['student_id'])
                supervisor = User.objects.get(id=request.user.id)
                account = Account.objects.get(id=cd['account'])
                try:
                    p = Preapproval.objects.get(supervisor=supervisor, student=student, approved=False)
                    p.delete()
                except:
                    print('Do better errorchecking please')

            # if the forms needs saved, save it.
            for form in formset:
                if form in formset.deleted_forms:
                    continue

                cd = form.cleaned_data
                student = User.objects.get(id=cd['student_id'])
                supervisor = User.objects.get(id=request.user.id)
                account = Account.objects.get(id=cd['account'])
                try:
                    p = Preapproval.objects.get(supervisor=supervisor, student=student, approved=False)
                    p.approved = True
                    p.account = account
                    p.save()
                except:
                    #### Do better error-cjecling?!!!! ###
                    print('Saving failed')
            messages.success(self.request, 'Changes applied successfully.')
            return redirect(reverse('edit_account'))
        return render(request, 'approve_students.html', {'formset': formset})


class ManageStudentsView(TemplateView):
    template_name = 'manage_students.html'

    def get(self, request, *args, **kwargs):
        ManageStudentsFormset = formset_factory(ManageStudentsForm, extra=1, can_delete=True)
        objects = Preapproval.objects.filter(supervisor_id=request.user.id, approved=True)
        initial_values = []
        for object in objects:
            initial_values.append({'student': str(object.student.id), 'account': object.account.id, 'preapproval_id': object.id or '' })
        formset = ManageStudentsFormset(initial=initial_values, form_kwargs={'user': request.user})
        return render(request, 'manage_students.html', {'formset': formset})
    
    def post(self, request, *args, **kwargs):
        ManageStudentsFormset = formset_factory(ManageStudentsForm, can_delete=True)
        formset = ManageStudentsFormset(request.POST, form_kwargs={'user': request.user})
        if formset.is_valid():

            # If the form needs to be deleted, delete it.
            for form in formset.deleted_forms:
                cd = form.cleaned_data
                print(cd['preapproval_id'] or 'none')
                student = User.objects.get(id=cd['student'])
                account = Account.objects.get(id=cd['account'])
                try:
                     p = Preapproval.objects.get(id=cd['preapproval_id'])
                     p.delete()
                except:
                     print('Do better errorchecking please')

            # if the forms needs saved, save it.
            for form in formset:
                if form in formset.deleted_forms:
                    continue
                
                cd = form.cleaned_data
                if not cd:
                    continue
                student = User.objects.get(id=cd['student'])
                supervisor = User.objects.get(id=request.user.id)
                account = Account.objects.get(id=cd['account'])                

                try:
                    p = Preapproval.objects.get(id=cd['preapproval_id'])
                    p.student = student
                    p.account = account
                    p.approved = True
                    p.save()
                except:
                    p = Preapproval.objects.create(student=student, supervisor=supervisor, account=account, approved=True)
                    # if there is an addition to the form - add a student.
                    print('Created new preapproval.')
            messages.success(self.request, 'Changes applied successfully.')
            return redirect(reverse('edit_account'))
        return render(request, 'approve_students.html', {'formset': formset})