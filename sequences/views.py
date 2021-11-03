from typing import Sequence
from django.forms.formsets import formset_factory
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy
from django.db.models import Max
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.timezone import make_aware
from django.core.paginator import Paginator

from sequences.models import Reaction, SeqPrice
from sequences.forms import PrimerModelForm, ReactionEasyOrderForm, ReactionForm, IdRangeForm, DateRangeForm, StatusForm, TemplateModelForm, TextSearch, PriceForm


from sequences.models import Template, Primer, Reaction, Account
from core.decorators import user_has_accounts
import datetime
import pytz
import re


class ReactionListView(ListView):
    model = Reaction
    context_object_name = 'reactions'

    def get_queryset(self):
        user = self.request.user
        qs1 = Reaction.objects.filter(
            account__owner=user).order_by('-submission_id', 'template', 'primer')
        qs2 = Reaction.objects.filter(
            submitter=user).order_by('-submission_id', 'template', 'primer')
        qs = qs1 | qs2
        return qs


class TemplateDetailView(DetailView):
    model = Template
    context_object_name = 'template'
    template_name = 'sequences/template_detail.html'


class SubmissionDetailView(ListView):
    model = Reaction

    def get(self, request, submission_id):
        qs = Reaction.objects.filter(submission_id=submission_id)
        templates = list(set([x.template for x in qs]))
        primers = list(set([x.primer for x in qs]))
        client_primers_exist = True if len(
            [x for x in primers if x.common == False]) >= 1 else False
        context = {
            'templates': templates,
            'primers': primers,
            'reactions': qs,
            'submission_id': submission_id,
            'submitter': qs.first().submitter,
            'client_primers_exist': client_primers_exist
        }
        return render(request, 'sequences/submission_detail.html', context=context)


class PrimerDetailView(DetailView):
    model = Primer
    context_object_name = 'primer'
    template_name = 'sequences/primer_detail.html'


class CommonPrimerView(ListView):
    model = Primer
    context_object_name = 'primer'
    template_name = 'sequences/common.html'

    def get_queryset(self):
        return Primer.objects.filter(common=True).order_by('id')


@user_has_accounts
def MethodSelectView(request):
    accounts = request.user.get_financial_accounts()
    return render(request, 'sequences/method_select.html', context={'accounts': accounts})


def get_submission_id():
    submission_id = 0
    latest_submission = Reaction.objects.aggregate(
        Max('submit_date'), Max('submission_id'))
    latest_submission_date = latest_submission['submit_date__max']
    max_submission_id = latest_submission['submission_id__max']

    if latest_submission_date == datetime.date.today():
        submission_id = int(max_submission_id) + 1
    else:
        d = datetime.date.today()
        submission_id = int(d.strftime('%Y%m%d') + '01')

    return submission_id


def ReactionAddView(request):
    if request.method == 'POST':
        template_count = int(request.POST.get('template-count'))
        primer_count = int(request.POST.get('primer-count'))
        reaction_count = int(request.POST.get('reaction-count'))
        account_id = int(request.POST.get('account-id'))

      # Check and make sure the data from the last form are all valid to create new formsets #
        valid_data = True if template_count >= 1 and primer_count >= 0 and reaction_count >= 1 and account_id >= 1 else False
        if not valid_data:
            messages.info(
                request, r'You need to order at least 1 template and 1 reaction.')
            return HttpResponseRedirect(reverse_lazy('sequencing:method_select'))

        # Create formsets to pass to page #
        TemplateFormset = modelformset_factory(Template, form=TemplateModelForm,
                                               extra=template_count)

        PrimerFormset = modelformset_factory(Primer, form=PrimerModelForm,
                                             extra=primer_count)

        ReactionFormset = formset_factory(ReactionForm, extra=reaction_count)

        # This indicates coming from the method-select/choose number of things page
        if request.POST.get('template-primer-add'):
            template_formset = TemplateFormset(
                queryset=Template.objects.none(), prefix="template")
            primer_formset = PrimerFormset(
                queryset=Primer.objects.none(), prefix="primer")
        else:
            template_formset = TemplateFormset(
                request.POST, prefix="template")
            primer_formset = PrimerFormset(
                request.POST, prefix="primer")

        context = {
            'template_count': template_count,
            'primer_count': primer_count,
            'reaction_count': reaction_count,
            'template_formset': template_formset,
            'primer_formset': primer_formset,
            'account_id': account_id
        }

        # If the user hasn't had a chance to add templates and primers yet, serve them the blank forms
        if request.POST.get('template-primer-add'):
            return render(request, 'sequences/add_template.html', context=context)

        # This is the button on the template/primer-add page to move onto defining reactions
        adding_reactions = request.POST.get('proceed-reactions')

        # If the templates/primers look good, we can define the reactions formset and serve
        if template_formset.is_valid() and primer_formset.is_valid() and adding_reactions:
            templates = template_formset.save(commit=False)
            primers = primer_formset.save(commit=False)
            reaction_formset = ReactionFormset(
                form_kwargs={'templates': templates, 'primers': primers})
            context['reaction_formset'] = reaction_formset
            return render(request, 'sequences/add_reaction.html', context=context)
        # if forms aren't valid, send them back to the template/primer template
        elif adding_reactions:
            return render(request, 'sequences/add_template.html', context=context)

        # This comes from the reactions page, indicating moving onto preview.
        previewing_reactions = request.POST.get('previewing-reactions')

        if previewing_reactions:
            templates = template_formset.save(commit=False)
            primers = primer_formset.save(commit=False)
            reaction_formset = ReactionFormset(request.POST,
                                               form_kwargs={'templates': templates, 'primers': primers})

            reactions = []
            for form in reaction_formset:
                reaction = {
                    'template': form['template'].value(),
                    'primer': form['primer'].value(),
                    'hardcopy': form['hardcopy'].value(),
                    'comment': form['comment'].value(),
                }
                reactions.append(reaction)

            context['common_primers'] = list(Primer.objects.filter(
                common=True).values_list('name', flat=True))
            context['reaction_formset'] = reaction_formset
            context['previewing'] = True
            context['reactions'] = reactions
            context['account'] = Account.objects.get(id=account_id)
            return HttpResponse(render(request, 'sequences/preview.html', context=context))

        finalize_order = request.POST.get('finalize-order')
        if finalize_order:
            # Set the Reaction submission number
            submission_id = get_submission_id()

            # Get the templates and primers
            template_formset = TemplateFormset(request.POST, prefix="template")
            templates = template_formset.save(commit=False)
            for template in templates:
                template.owner = request.user
                template.save()

            primer_formset = PrimerFormset(request.POST, prefix="primer")
            primers = primer_formset.save(commit=False)
            for primer in primers:
                primer.owner = request.user
                primer.save()

            reaction_formset = ReactionFormset(request.POST, form_kwargs={
                'templates': templates, 'primers': primers})

            account_to_save = Account.objects.get(
                id=request.POST.get('account-id'))

            for form in reaction_formset:
                ## Filter out the template and primer that we want from the saved instances ##
                template_name = form['template'].value()
                template_to_save = next(
                    (template for template in templates if template.name == template_name))

                primer_name = form['primer'].value()
                primer_to_save = None
                try:
                    primer_to_save = next(
                        (primer for primer in primers if primer.name == primer_name))
                except:
                    primer_to_save = Primer.objects.get(
                        name=primer_name, common=True)

                hardcopy = form['hardcopy'].value()
                comment = form['comment'].value()

                reaction = Reaction(
                    submitter=request.user,
                    template=template_to_save,
                    primer=primer_to_save,
                    account=account_to_save,
                    submission_id=submission_id,
                    status='s',
                    hardcopy=hardcopy,
                    comment=comment
                )
                reaction.save()

            messages.success(
                request, r'Reactions successfully ordered! Be sure to follow instructions on this page.')

            return HttpResponseRedirect(reverse_lazy('sequencing:submission_detail', kwargs={'submission_id': submission_id}))


class BulkReactionAddView(FormView):
    template_name = 'sequences/bulk_add.html'
    form_class = ReactionEasyOrderForm

    def get(self, request):
        form = ReactionEasyOrderForm()
        account_id = request.GET.get('account_id')
        if not account_id:
            messages.info(
                request, 'Please select an account before proceeding')
            return redirect(reverse('sequencing:method_select'))
        return render(request, 'sequences/bulk_add.html', context={'form': form, 'account_id': account_id})

    def post(self, request):
        form = ReactionEasyOrderForm(request.POST or None)

        if not form.is_valid():
            return render(request, 'sequences/bulk_add.html', context={'form': form})

        data = form.cleaned_data
        account_id = request.POST.get('account-id')

        reactions = []
        for reaction in data['reactions']:
            try:
                ex = r'^([^\t;,]+)[\t;,]\s*([^\t\r;,]+)[\t;,]?\s*?([^\r]*)\r?$'
                groups = re.match(ex, reaction).groups()
                reactions.append(groups)
                print(groups)
            except AttributeError:
                messages.info(
                    request, f'Could not match the line {reaction}. Check formatting and try again.')
                return render(request, 'sequences/bulk_add.html', context={'form': form, 'account_id': account_id})

        primer_names = []
        for reaction in reactions:
            primer = reaction[1]
            if primer in primer_names:
                continue
            primer_names.append(primer)

        primers = []
        if data['primer_source'] == 'ls':
            common_primers = Primer.objects.filter(
                common=True).values_list('name', flat=True)
            all_primers_are_common = True
            for primer_name in primer_names:
                if not primer_name in common_primers:
                    all_primers_are_common = False
                    messages.warning(
                        request, f'Primer {primer_name} not found as common primer. Check spelling and try again.')

            if not all_primers_are_common:
                return render(request, 'sequences/bulk_add.html', context={'form': form, 'account_id': account_id})

        if request.POST.get('finalize'):
            template_names = []
            for reaction in reactions:
                template = reaction[0]
                if template in template_names:
                    continue
                template_names.append(template)

            templates = []
            for template_name in template_names:
                t = Template(
                    name=template_name,
                    owner=request.user,
                    comment=data['template_comment'],
                    type=data['template_type'],
                    template_size=data['template_size'],
                    insert_size=data['insert_size'],
                    pcr_purify=data['pcr_purify'],
                    template_concentration=data['template_concentration'],
                    template_volume=data['template_volume'],
                )
                templates.append(t)
                t.save()

            primers = []
            if data['primer_source'] == 'cl':
                for primer_name in primer_names:
                    p = Primer(
                        name=primer_name,
                        concentration=data['primer_concentration'],
                        volume=data['primer_volume'],
                        common=False,
                        owner=request.user
                    )
                    primers.append(p)
                    p.save()
            else:
                primers = list(Primer.objects.filter(common=True))

            submission_id = get_submission_id()

            for reaction in reactions:
                reaction_template = next(
                    (t for t in templates if t.name == reaction[0]))
                reaction_primer = next(
                    p for p in primers if p.name == reaction[1])
                account = Account.objects.get(id=account_id)
                r = Reaction(
                    submitter=request.user,
                    template=reaction_template,
                    primer=reaction_primer,
                    account=account,
                    submission_id=submission_id,
                    status='s',
                    hardcopy=data['hardcopy']
                )
                r.save()
            order_count = len(reactions)
            messages.success(
                request, f'Successfully ordered {order_count} sequencing reactions. Be sure to follow instructions on this page.')
            return HttpResponseRedirect(reverse_lazy('sequencing:submission_detail', kwargs={'submission_id': submission_id}))

        data['template_type_display'] = dict(
            form.fields['template_type'].choices)[data['template_type']]

        data['primer_source_display'] = dict(
            form.fields['primer_source'].choices)[data['primer_source']]

        account = Account.objects.get(id=account_id)

        context = {
            'form': form,
            'reactions': reactions,
            'previewing': True,
            'reaction_meta': data,
            'account': account,
            'account_id': account_id,
        }

        return render(request, 'sequences/bulk_add.html', context=context)


class SequencingAdminHomeView(View):
    def get(self, request):
        return render(request, 'sequences/admin_home.html')


def create_aware_date(date_string):
    time_zone = pytz.timezone('Canada/Eastern')
    split_date = date_string.split('-')
    naive_date = datetime.datetime(
        int(split_date[0]), int(split_date[1]), int(split_date[2]))
    return make_aware(naive_date, time_zone)


class SequencesTodayListView(ListView):
    model = Sequence
    context_object_name = 'reactions'
    template_name = 'sequences/todays_sequences.html'

    def get_queryset(self, *args, **kwargs):
        today = create_aware_date(
            datetime.datetime.today().strftime('%Y-%m-%d'))
        return Reaction.objects.filter(submit_date__gte=today).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(SequencesTodayListView,
                        self).get_context_data(**kwargs)
        context['title'] = "Today's Sequences"
        return context


def get_search_queries(search_type):
    if search_type == 'range':
        return ['submission', 'date', 'sequence']
    elif search_type == 'text':
        return ['template', 'primer', 'status']
    else:
        return []


def get_redirect_url(search, low=None, high=None, text='', client=''):
    base_url = reverse_lazy('sequencing:search_results')
    low_str = f'&low={low}' if low else ''
    high_str = f'&high={high}' if high else ''
    text_str = f'&text={text}' if text else ''
    client_str = f'&client={client}' if client else ''
    return f'{base_url}?query={search}{low_str}{high_str}{text_str}{client_str}'


class SequenceSearchView(View):
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

        max_reaction = Reaction.objects.all().order_by('-id').first()
        id_range_form = IdRangeForm(
            prefix="submission", initial={'high': max_reaction.submission_id})
        date_range_form = DateRangeForm(prefix="date")
        sequence_range_form = IdRangeForm(
            prefix="sequence", initial={'high': max_reaction.id})
        template_name_form = TextSearch(prefix="template")
        primer_name_form = TextSearch(prefix="primer")
        status_form = StatusForm(prefix='status')

        context = {
            'id_range_form': id_range_form,
            'date_range_form': date_range_form,
            'sequence_range_form': sequence_range_form,
            'template_name_form': template_name_form,
            'primer_name_form': primer_name_form,
            'status_form': status_form
        }
        return render(request, 'sequences/searches.html', context=context)


class SequenceListView(View):
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

        if data['query'] == 'submission':
            queryset = Reaction.objects.filter(
                submission_id__gte=data['low'], submission_id__lte=data['high'])

        elif data['query'] == 'date':
            start_date = create_aware_date(data['low'])
            end_date = create_aware_date(data['high'])

            client = data['client'] or False
            queryset = Reaction.objects.filter(
                submit_date__gte=start_date, submit_date__lte=end_date)
            if client != '0':
                queryset = queryset.filter(submitter__id=int(data['client']))

        elif data['query'] == 'sequence':
            queryset = Reaction.objects.filter(
                id__gte=data['low'], id__lte=data['high'])

        elif data['query'] == 'template':
            queryset = Reaction.objects.filter(
                template__name__icontains=data['text'])

        elif data['query'] == 'primer':
            queryset = Reaction.objects.filter(
                primer__name__icontains=data['text'])

        elif data['query'] == 'status':
            queryset = Reaction.objects.filter(
                status=data['text'])

        queryset = queryset.order_by("id")

        PAGINATE_NUMBER = 10
        paginator = Paginator(queryset, PAGINATE_NUMBER)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        current_path = request.get_full_path()

        context = {
            'page_obj': page_obj,
            'data': data,
            'current_path': current_path,
        }

        return render(request, 'sequences/admin_list.html', context=context)


class BillingView(View):
    def get(self, request):
        max_reaction = Reaction.objects.all().order_by('-id').first()
        range_form = IdRangeForm(initial={'high': max_reaction.id})

        prices = SeqPrice.objects.filter(current=True).last()
        price_form = PriceForm(instance=prices, prefix="price")

        context = {
            'range_form': range_form,
            'price_form': price_form
        }
        return render(request, 'sequences/billing.html', context=context)

    def post(self, request):
        range_form = IdRangeForm(request.POST)
        price_form = PriceForm(request.POST, prefix="price")
        if not range_form.is_valid() or not price_form.is_valid():
            context = {
                'range_form': range_form,
                'price_form': price_form
            }
            return render(request, 'sequences/billing.html', context=context)

        reaction_range = range_form.cleaned_data
        reactions = Reaction.objects.filter(
            id__gte=reaction_range['low']).filter(id__lte=reaction_range['high']).order_by('submitter__id', 'account__id', 'id')

        billing_objects = []

        class SubmissionObject:
            def __init__(self):
                self.sequences = 0
                self.long_sequences = 0
                self.total_count = 0
                self.date = None

            def __repr__(self):
                return f'submission: {self.total_count} sequences'

        for reaction in reactions:
            user_account_id = f'{reaction.submitter.id}-{reaction.account.id}'

            if len(billing_objects) > 0:
                order = list(
                    filter(lambda x: x['name'] == user_account_id, billing_objects))
                obj = order[0] if order else None
            if len(billing_objects) == 0 or not obj:
                obj = {
                    'name': user_account_id,
                    'meta': {
                        'submitter': reaction.submitter,
                        'account': reaction.account,
                        'hardcopies': 0,
                        'purify_count': 0,
                    }
                }
                billing_objects.append(obj)

            try:
                submission = obj[f'sub-{reaction.submission_id}']
            except KeyError:
                obj.update(
                    {f'sub-{reaction.submission_id}': SubmissionObject()})
                submission = obj[f'sub-{reaction.submission_id}']

            meta = obj['meta']

            submission.date = reaction.submit_date

            if reaction.template.type in ['co', 'ot']:
                submission.long_sequences += 1
            else:
                submission.sequences += 1

            submission.total_count += 1

            if reaction.template.pcr_purify:
                meta['purify_count'] += 1

            if reaction.hardcopy:
                meta['hardcopies'] += 1

        price_data = price_form.cleaned_data
        billing_context = []

        class Row():
            def __init__(self, submitter, account):
                self.submitter = submitter
                self.account = account
                self.sequences = 0
                self.plate_sequences = 0
                self.long_sequences = 0
                self.purify_count = 0
                self.hardcopies = 0
                self.order_dates = []

            def __repr__(self):
                return f'{self.submitter}-{self.account.code}'

        for obj in billing_objects:
            row = Row(obj['meta']['submitter'], obj['meta']['account'])
            for k, v in obj.items():
                if (k[:4] == 'sub-'):
                    if v.total_count >= 48:
                        row.plate_sequences += v.sequences
                    else:
                        row.sequences += v.sequences
                    row.long_sequences += v.long_sequences

                    if not v.date in row.order_dates:
                        row.order_dates.append(v.date)

            if obj['meta']['submitter'].is_external:
                row.reg_price = price_data['ext_standard_sequencing']
                row.plate_price = price_data['ext_well96_plate']
                row.long_price = price_data['ext_large_template']
                row.purify_price = price_data['ext_pcr_purification']
                row.hardcopy_price = price_data['ext_printout']

            else:
                row.reg_price = price_data['standard_sequencing']
                row.plate_price = price_data['well96_plate']
                row.long_price = price_data['large_template']
                row.purify_price = price_data['pcr_purification']
                row.hardcopy_price = price_data['printout']

            standard_cost = row.sequences * row.reg_price
            plate_cost = row.plate_sequences * row.plate_price
            long_cost = row.long_sequences * row.long_price
            purify_cost = row.purify_count * row.purify_price
            hardcopy_cost = row.hardcopies * row.hardcopy_price

            row.total_price = standard_cost + plate_cost + \
                long_cost + purify_cost + hardcopy_cost

            billing_context.append(row)

        return render(request, 'sequences/billing_output.html', context={'billing': billing_context})
