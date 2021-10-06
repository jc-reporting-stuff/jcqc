from django.forms.forms import Form
from django.forms.models import formset_factory, modelformset_factory
from django.http.response import HttpResponseGone, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Max
from django.contrib import messages

from oligos.forms import EasyOrderForm, OligoInitialForm, OligoOrderForm
from .models import Oligo
from accounts.models import Account, User

import re

class ClientOrderListView(ListView):
    template_name = 'oligos/client_view_all.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = Oligo.objects.filter(submitter=self.request.user) | Oligo.objects.filter(account__owner__username=self.request.user)
        return qs


class OligoNewTypeView(FormView):
    form_class = OligoInitialForm
    template_name = 'oligos/order_method.html'
    success_url = reverse_lazy('oligos:order_create')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        user = self.request.user
        approved_accounts = user.get_financial_accounts()
        approved_choices = [((account.id), (': '.join([account.code, account.comment]))) for account in approved_accounts]
        kwargs['account_choices'] = approved_choices
        kwargs['initial_oligos'] = 1
        return kwargs




class OligoCreateView(CreateView):
    template_name = 'oligos/order_new.html'
    model = Oligo
    fields = ['name', 'sequence', 'order_id']

    def get(self, request, *args, **kwargs):
        # If coming from the "how many oligos page", this will be carried out.
        if request.GET.get('account_id'):
            account_id = request.GET.get('account_id')
            oligo_count = request.GET.get('oligo_count')

            NewOligoFormset = formset_factory(OligoOrderForm, extra=int(oligo_count))
            formset = NewOligoFormset()

            response = render(request, 'oligos/order_new.html', context={'formset': formset, 'account_id': account_id})
            return HttpResponse(response)
        return HttpResponseRedirect(reverse_lazy('oligos:order_quantity'))

    def post(self, request, *args, **kwargs):
        OligoFormset = formset_factory(OligoOrderForm)
        formset = OligoFormset(request.POST)

        # Make sure that all required fields are filled out.
        num_forms = 0
        for form in formset:
            if form.has_changed(): num_forms += 1
            if not form.is_valid():
                return HttpResponse(render(request, 'oligos/order_new.html', context={'formset': formset}))

        # If nothing was changed in any form, send user back to choose number to order.
        if num_forms == 0:
            return HttpResponseRedirect(reverse_lazy('oligos:order_quantity'))

        # If the 'preview' button has been pressed, re-open the template in preview mode
        previewing = request.POST.get('previewing')

        account_id = request.POST.get('account_id')
        if previewing:
            context = {
            'formset': formset,
            'previewing': True,
            'account_id': account_id,
            }
            response = render(self.request, 'oligos/order_new.html', context)
            return HttpResponse(response)

        return self.form_valid(formset)

    def form_valid(self, formset):
        cd = []
        for form in formset:
            cleaned_data = form.clean()
            if cleaned_data: cd.append(cleaned_data)

        max_order = Oligo.objects.aggregate(Max('order_id'))
        order_number = max_order['order_id__max'] + 1

        submitter = User.objects.get(id=self.request.user.id)
        account = Account.objects.get(id=self.request.POST.get('account_id'))

        for oligo in cd:
            Oligo.objects.create(
                    name=oligo['name'], sequence=oligo['sequence'], order_id=order_number, 
                    account=account, submitter=submitter, modification=oligo['modification'],
                    scale=oligo['scale'], purity=oligo['purity']
                    )
        
        request = self.request
        messages.success(request, r'Ordered Successfully.')

        return HttpResponseRedirect(reverse_lazy('oligos:client_order_list'))




class OligoEasyOrder(FormView):
    form_class = EasyOrderForm
    template_name = 'oligos/easy_order.html'
    success_url = reverse_lazy('oligos:easy_order')
    context_object_name = 'context'

    def get(self, request):
        # If coming from the "how many oligos page", this will be carried out.
        if request.GET.get('account_id'):
            account_id = request.GET.get('account_id')

            response = render(request, 'oligos/easy_order.html', context={'form': EasyOrderForm, 'account_id': account_id})
            return HttpResponse(response)
        return HttpResponseRedirect(reverse_lazy('oligos:order_quantity'))

    def form_valid(self, form):
        cd = form.cleaned_data
        account_id = self.request.POST.get('account_id')

        # Process the oligos from the textarea field.
        # Split them by line, then use regular expressions to split into name, sequence groups.

        # TODO: Validate textarea form input to error on invalid values or improper formatting.

        oligo_text = form['oligos'].value()
        oligos_text_split = oligo_text.split('\n')
        ex = r'(.+?)[\t;,] *([ACGTRYMWSKDHBVN]+)'
        oligo_groups = []
        for line in oligos_text_split:
            if line and line != '\r':
                groups = re.match(ex, line).groups()
                current_oligo = {'name': groups[0], 'sequence': groups[1]}
                oligo_groups.append(current_oligo)

        account = Account.objects.get(id=account_id)

        context = {
            'account': account,
            'data' : cd,
            'oligos': oligo_groups,
            'previewing': True
        }

        # Pass everything along to the preview view.
        response = render(self.request, 'oligos/easy_preview.html', context=context)
        return HttpResponse(response)




class OligoEasySubmitView(TemplateView):
    template_name = 'oligos/easy_preview.html'

    def post(self, request):

        data = request.POST
        submitter = User.objects.get(id=self.request.user.id)
        account = Account.objects.get(id=data['account_id'])

        # Build a list of oligos from the form data.
        oligos = []
        for i in range(int(data['oligo_count'])):
            object = {}
            form_oligo_name = 'oligo-' + str(i) +'-name'
            form_sequence_name = 'oligo-' + str(i) +'-sequence'
            object['name'] = data[form_oligo_name]
            object['sequence'] = data[form_sequence_name]
            oligos.append(object)
            

        # Cycle through list of oligos, add necessary fields and save.
        max_order = Oligo.objects.aggregate(Max('order_id'))
        order_number = max_order['order_id__max'] + 1

        for oligo in oligos:
            try:
                object = Oligo.objects.create(
                    name=oligo['name'], sequence=oligo['sequence'], order_id=order_number, 
                    account=account, submitter=submitter, modification=data['modification'],
                    scale=data['scale'], purity=data['purity']
                    )
            except:
                messages.add_message(request, r'Saving oligo {oligo.name} failed! Check your values and try again.')

        return HttpResponseRedirect(reverse_lazy('oligos:client_order_list'))
