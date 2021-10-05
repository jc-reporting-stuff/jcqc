from django.forms.models import formset_factory, modelformset_factory
from django.http.response import HttpResponseGone, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Max

from oligos.forms import OligoInitialForm, OligoOrderForm
from .models import Oligo

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
    fields = ['name', 'sequence']

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
        if previewing:
            context = {
            'formset': formset,
            'previewing': True
            }
            response = render(self.request, 'oligos/order_new.html', context)
            return HttpResponse(response)
        
        print('no option but to save')
        # Override the saving once all the forms have all required fields.
        max_order = Oligo.objects.aggregate(Max('order_id'))
        order_number = max_order['order_id__max'] + 1
        for form in formset:
            new_oligo = form.save(commit=False)
            new_oligo.order_id = order_number
            # add some stuff to the object then .save()
        return HttpResponseRedirect(reverse_lazy('oligos:client_order_list'))

