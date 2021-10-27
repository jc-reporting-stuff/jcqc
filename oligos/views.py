from django.forms.models import formset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, FormView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.db.models import Max
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.utils.timezone import localtime, now, make_aware
from django.core.paginator import Paginator

from oligos.forms import EasyOrderForm, OligoInitialForm, OligoOrderForm, IdRangeForm, DateRangeForm, OligoTextSearch
from .models import Oligo
from accounts.models import Account, User
from core.decorators import user_has_accounts

import pytz
import datetime
import re


class ClientOrderListView(ListView):
    template_name = 'oligos/client_view_all.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = Oligo.objects.filter(submitter=self.request.user) | Oligo.objects.filter(
            account__owner__username=self.request.user)
        return qs


class OligoDetailView(DetailView):
    model = Oligo
    context_object_name = 'oligo'

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(submitter__id=user.id) | qs.filter(account__owner__id=user.id)


@method_decorator(user_has_accounts, name='dispatch')
class OligoNewTypeView(FormView):
    form_class = OligoInitialForm
    template_name = 'oligos/order_method.html'
    success_url = reverse_lazy('oligos:order_create')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        user = self.request.user
        approved_accounts = user.get_financial_accounts()
        approved_choices = [((account.id), (': '.join(
            [account.code, account.comment]))) for account in approved_accounts]
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

            NewOligoFormset = formset_factory(
                OligoOrderForm, extra=int(oligo_count))
            formset = NewOligoFormset()

            response = render(request, 'oligos/order_new.html',
                              context={'formset': formset, 'account_id': account_id})
            return HttpResponse(response)
        return HttpResponseRedirect(reverse_lazy('oligos:order_quantity'))

    def post(self, request, *args, **kwargs):
        OligoFormset = formset_factory(OligoOrderForm)
        formset = OligoFormset(request.POST)

        # Make sure that all required fields are filled out.
        num_forms = 0
        for form in formset:
            if form.has_changed():
                num_forms += 1
            if not form.is_valid():
                return HttpResponse(render(request, 'oligos/order_new.html', context={'formset': formset}))

        # If nothing was changed in any form, send user back to choose number to order.
        if num_forms == 0:
            return HttpResponseRedirect(reverse_lazy('oligos:order_quantity'))

        # If the 'preview' button has been pressed, re-open the template in preview mode
        previewing = request.POST.get('previewing')

        account_id = request.POST.get('account_id')

        if previewing:
            account = Account.objects.get(id=account_id)
            sequences = []

            for form in formset:
                spaced_sequence = ' '.join(form['sequence'].value()[i:i+3]
                                           for i in range(0, len(form['sequence'].value()), 3))
                sequences.append(spaced_sequence)

            context = {
                'formset': formset,
                'previewing': True,
                'account_id': account_id,
                'sequences': sequences,
                'account': account
            }
            response = render(self.request, 'oligos/order_new.html', context)
            return HttpResponse(response)

        return self.form_valid(formset)

    def form_valid(self, formset):
        cd = []
        for form in formset:
            cleaned_data = form.clean()
            if cleaned_data:
                cd.append(cleaned_data)

        max_order = Oligo.objects.aggregate(Max('order_id'))
        order_number = max_order['order_id__max'] + 1

        submitter = User.objects.get(id=self.request.user.id)
        account = Account.objects.get(id=self.request.POST.get('account_id'))

        for oligo in cd:
            Oligo.objects.create(
                name=oligo['name'], sequence=oligo['sequence'].upper(), order_id=order_number,
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

            response = render(request, 'oligos/easy_order.html',
                              context={'form': EasyOrderForm, 'account_id': account_id})
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
            'data': cd,
            'oligos': oligo_groups,
            'previewing': True
        }

        # Pass everything along to the preview view.
        response = render(
            self.request, 'oligos/easy_preview.html', context=context)
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
            form_oligo_name = 'oligo-' + str(i) + '-name'
            form_sequence_name = 'oligo-' + str(i) + '-sequence'
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
                messages.add_message(
                    request, r'Saving oligo {oligo.name} failed! Check your values and try again.')

        return HttpResponseRedirect(reverse_lazy('oligos:client_order_list'))


class OligoAdminHomeView(View):
    def get(self, request):
        return render(request, 'oligos/admin-home.html')


class OligoTodayListView(ListView):
    model = Oligo
    context_object_name = 'oligos'
    template_name = 'oligos/todays_oligos.html'

    def get_queryset(self, *args, **kwargs):
        today = localtime(now()).date()
        return Oligo.objects.filter(created_at__gte=today).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(OligoTodayListView, self).get_context_data(**kwargs)
        context['title'] = "Today's Oligos"
        return context


def get_redirect_url(search, low=None, high=None, text='', client=''):
    base_url = reverse_lazy('oligos:search_results')
    low_str = f'&low={low}' if low else ''
    high_str = f'&high={high}' if high else ''
    text_str = f'&text={text}' if text else ''
    client_str = f'&client={client}' if client else ''
    return f'{base_url}?query={search}{low_str}{high_str}{text_str}{client_str}'


def get_search_queries(search_type):
    if search_type == 'range':
        return ['oligo', 'date', 'order']
    elif search_type == 'text':
        return ['name', 'sequence']
    else:
        return []


class OligoSearchView(View):
    def get(self, request):
        if request.GET.get('search'):
            args = request.GET
            search = args.get('search')
            range_searches = get_search_queries('range')
            text_searches = get_search_queries('text')
            if search in range_searches:
                low = args.get(f'{search}-low')
                high = args.get(f'{search}-high')
                client = args.get(f'{search}-client')
                return redirect(get_redirect_url(search=search, low=low, high=high, client=client))
            elif search in text_searches:
                text = args.get(f'{search}-text')
                return redirect(get_redirect_url(search=search, text=text))

        max_oligo = Oligo.objects.all().order_by('-id').first()
        id_range_form = IdRangeForm(
            prefix="oligo", initial={'high': max_oligo.id})
        date_range_form = DateRangeForm(prefix="date")
        order_range_form = IdRangeForm(
            prefix="order", initial={'high': max_oligo.order_id})
        oligo_name_form = OligoTextSearch(prefix="name")
        oligo_sequence_form = OligoTextSearch(prefix="sequence")

        context = {
            'id_range_form': id_range_form,
            'date_range_form': date_range_form,
            'order_range_form': order_range_form,
            'oligo_name_form': oligo_name_form,
            'oligo_sequence_form': oligo_sequence_form
        }
        return render(request, 'oligos/searches.html', context=context)


def create_aware_date(form_date_string):
    time_zone = pytz.timezone('Canada/Eastern')
    split_date = form_date_string.split('-')
    naive_date = datetime.datetime(
        int(split_date[0]), int(split_date[1]), int(split_date[2]))
    return make_aware(naive_date, time_zone)


class OligoListView(View):
    def get(self, request):
        args = request.GET

        ### Error-checking -- make sure all necessary search params exist and are valid ###
        params = ['query', 'low', 'high', 'text', 'client', 'page']
        data = {}
        for param in params:
            data[param] = args.get(param) if args.get(param) else None
        if not (data['query'] and ((data['low'] and data['high']) or data['text'])) and not data['page']:
            messages.warning(
                request, 'Missing search parameter(s), try again please.')
            return redirect(reverse('oligos:search'))

        if data['low'] and data['high']:
            if data['low'] > data['high']:
                temp = data['low']
                data['low'] = data['high']
                data['high'] = temp
                messages.info(
                    request, 'Low value greater than high value: Values were swapped.')

        queryset = None

        if data['query'] == 'oligo':
            queryset = Oligo.objects.filter(
                id__gte=data['low'], id__lte=data['high'])

        elif data['query'] == 'date':
            start_date = create_aware_date(data['low'])
            end_date = create_aware_date(data['high'])

            client = data['client'] or False
            queryset = Oligo.objects.filter(
                created_at__gte=start_date, created_at__lte=end_date)
            if client != '0':
                queryset = queryset.filter(submitter__id=int(data['client']))

        elif data['query'] == 'order':
            queryset = Oligo.objects.filter(
                order_id__gte=data['low'], order_id__lte=data['high'])

        elif data['query'] == 'name':
            queryset = Oligo.objects.filter(name__icontains=data['text'])

        elif data['query'] == 'sequence':
            stripped_sequence = data['text'].strip().replace(' ', '')
            queryset = Oligo.objects.filter(
                sequence__icontains=stripped_sequence)

        queryset = queryset.order_by("id")

        PAGINATE_NUMBER = 5
        paginator = Paginator(queryset, PAGINATE_NUMBER)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        current_path = request.get_full_path()

        context = {
            'page_obj': page_obj,
            'data': data,
            'current_path': current_path,
        }

        return render(request, 'oligos/admin_list.html', context=context)


class OligoListActionsView(View):
    def post(self, request):
        action = request.POST.get('button')
        print(action)

        post_data = dict(request.POST.lists())

        if action == 'update-delivery':
            oligos_to_update = []
            for key, value in post_data.items():
                try:
                    checkbox = re.match('^(\d+)-checkbox$', key).groups()[0]
                    oligos_to_update.append(checkbox)
                except:
                    pass
            for oligo_to_update in oligos_to_update:
                if request.POST.get(f'{oligo_to_update}-delivery-date'):
                    date = request.POST.get(f'{oligo_to_update}-delivery-date')
                    aware_date = create_aware_date(date)
                    oligo = Oligo.objects.get(id=oligo_to_update)
                    oligo.delivery_date = aware_date
                    oligo.save()
            messages.success(request, f'Delivery dates saved.')

        if action == 'update-all-delivery':
            delivery_date = request.POST.get('all-delivery-date')
            if delivery_date:
                aware_delivery_date = create_aware_date(delivery_date)
            else:
                aware_delivery_date = None
            for key, value in post_data.items():
                try:
                    oligo_id = re.match(
                        '^(\d+)-delivery-date$', key).groups()[0]
                except:
                    continue
                oligo = Oligo.objects.get(id=oligo_id)
                oligo.delivery_date = aware_delivery_date
                oligo.save()
            messages.success(request, f'Delivery dates saved successfully.')

        redirect_url = request.POST.get('return-url')
        return HttpResponseRedirect(redirect_url)


class BillingView(View):
    def get(self, request):
        render(request, 'oligos/billing.html')
