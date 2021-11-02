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
from sequences.forms import ReactionEasyOrderForm, ReactionForm, IdRangeForm, DateRangeForm, StatusForm, TextSearch, PriceForm


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


@user_has_accounts
def MethodSelectView(request):
    return render(request, 'sequences/method_select.html')


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

      # Check and make sure the data from the last form are all valid to create new formsets #
        valid_data = True if template_count >= 1 and primer_count >= 0 and reaction_count >= 1 else False
        if not valid_data:
            messages.info(
                request, r'You need to order at least 1 template and 1 reaction.')
            return HttpResponseRedirect(reverse_lazy('sequencing:method_select'))

        # Create formsets to pass to page #
        TemplateFormset = modelformset_factory(Template, fields=(
            'name', 'type', 'template_size', 'insert_size', 'template_concentration', 'template_volume', 'pcr_purify', 'comment'),
            extra=template_count)

        PrimerFormset = modelformset_factory(Primer, fields=(
            'name', 'concentration', 'volume', 'melting_temperature', 'sequence'),
            extra=primer_count)

        ReactionFormset = formset_factory(ReactionForm, extra=reaction_count)

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
        }

        if request.POST.get('template-primer-add'):
            return render(request, 'sequences/add_template.html', context=context)

        adding_reactions = request.POST.get('proceed-reactions')

        if template_formset.is_valid() and primer_formset.is_valid() and adding_reactions:
            templates = template_formset.save(commit=False)
            primers = primer_formset.save(commit=False)
            reaction_formset = ReactionFormset(
                form_kwargs={'templates': templates, 'primers': primers})
            context['reaction_formset'] = reaction_formset
            return render(request, 'sequences/add_reaction.html', context=context)
        elif adding_reactions:
            return render(request, 'sequences/add_template.html', context=context)

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
                id=request.POST.get('account'))

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

    def post(self, request):
        form = ReactionEasyOrderForm(request.POST or None)

        if not form.is_valid():
            return render(request, 'sequences/bulk_add.html', context={'form': form})

        data = form.cleaned_data

        reactions = []
        for reaction in data['reactions']:
            ex = r'^(.+?)[\t;,]\s*(.+?)[\t;,]\s*(.*?)\r$'
            groups = re.match(ex, reaction).groups()
            reactions.append(groups)

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
                return render(request, 'sequences/bulk_add.html', context={'form': form})

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
                account = Account.objects.get(id=request.POST.get('account'))
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

        accounts = request.user.get_financial_accounts()

        context = {
            'form': form,
            'reactions': reactions,
            'previewing': True,
            'reaction_meta': data,
            'accounts': accounts
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

        max_reaction = Reaction.objects.all().order_by('-submission_id').first()
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

        price_data = price_form.cleaned_data
        reaction_range = range_form.cleaned_data
        reactions = Reaction.objects.filter(
            id__gte=reaction_range['low']).filter(id__lte=reaction_range['high']).order_by('account__owner__id', 'account__id')

        class ReportObject:
            def __init__(self):
                self.is_internal = True
                self.order_dates = []
                self.submitter_id = ''
                self.account_id = ''
                self.standard_sequence = 0
                self.plate_sequence = 0
                self.long_sequence = 0
                self.purify_count = 0
                self.hardcopy_coount = 0

        billing_rows = []
        row_counter = 0
        this_row = None

        ## Build up pricing structure ###
        for reaction in reactions:
            # If the user has changed, we'll add an object to the list and switch to it.
            user_has_changed = False
            account_has_changed = False
            if len(billing_rows) != 0:
                user_has_changed = reaction.submitter.id != this_row.submitter_id
                account_has_changed = reaction.account.id != this_row.account_id

            # If the user has changed, add a new row to the table.
            if len(billing_rows) == 0:
                x = ReportObject()
                billing_rows.append(x)
                this_row = billing_rows[row_counter]
                this_row.submitter_id = reaction.submitter.id
                this_row.account_id = reaction.account.id

            elif user_has_changed or account_has_changed:
                x = ReportObject()
                billing_rows.append(x)
                row_counter += 1
                this_row = billing_rows[row_counter]
                this_row.submitter_id = oligo.submitter.id
                this_row.account_id = oligo.account.id

            ## Start processing of actual oligo ###
            this_row.oligo_count += 1

            non_degen_bases = ['A', 'C', 'G', 'T']
            oligo_scale = oligo.scale.split(' ')[0]
            if oligo_scale == '1':
                oligo_scale = '1000'
            for base in oligo.sequence:
                if base in non_degen_bases:
                    this_row.add_count(oligo_scale)
                else:
                    this_row.add_count(oligo_scale, degen=True)
                    if oligo.id not in this_row.degen_oligo_ids:
                        this_row.degen_oligo_ids.append(oligo.id)
                    if oligo.created_at.date() not in this_row.degen_order_dates:
                        this_row.degen_order_dates.append(
                            oligo.created_at.date())

            if oligo.purity == 'desalted':
                this_row.desalt_count += 1
            elif oligo.purity == 'cartridge':
                this_row.cartridge_count += 1

            if oligo.created_at.date() not in this_row.order_dates:
                this_row.order_dates.append(oligo.created_at.date())

        billing_context = []
        for row in billing_rows:
            row_object = {}
            submitter = User.objects.get(id=row.submitter_id)
            account = Account.objects.get(id=row.account_id)
            row_object['order_date'] = row.order_dates
            row_object['supervisor'] = account.owner.display_name
            row_object['client_name'] = submitter.display_name
            row_object['department'] = submitter.department
            row_object['account'] = account.code
            row_object['oligo_count'] = row.oligo_count
            row_object['40nmol'] = row.nmol40_count
            row_object['40price'] = price_data['scale_40_base']
            row_object['200nmol'] = row.nmol200_count
            row_object['200price'] = price_data['scale_200_base']
            row_object['1000nmol'] = row.nmol1000_count
            row_object['1000price'] = price_data['scale_1000_base']

            row_object['degen_order_date'] = row.degen_order_dates
            row_object['degen_oligo_count'] = len(row.degen_oligo_ids)
            row_object['40nmol_degen'] = row.degen40_count
            row_object['40price_degen'] = price_data['degenerate_40_base']
            row_object['200nmol_degen'] = row.degen200_count
            row_object['200price_degen'] = price_data['degenerate_200_base']
            row_object['1000nmol_degen'] = row.degen1000_count
            row_object['1000price_degen'] = price_data['degenerate_1000_base']

            row_object['desalt_count'] = row.desalt_count
            row_object['desalt_price'] = price_data['desalt_fee']
            row_object['cartridge_count'] = row.cartridge_count
            row_object['cartridge_price'] = price_data['cartridge_fee']
            row_object['setup_count'] = len(row.order_dates)
            row_object['setup_price'] = price_data['setup_fee']

            price40 = row.nmol40_count * price_data['scale_40_base']
            price200 = row.nmol200_count * price_data['scale_200_base']
            price1000 = row.nmol1000_count * price_data['scale_1000_base']

            price_desalt = row.desalt_count * price_data['desalt_fee']
            price_cartridge = row.cartridge_count * price_data['cartridge_fee']
            price_setup = len(row.order_dates) * price_data['setup_fee']

            price40_degen = row.degen40_count * \
                price_data['degenerate_40_base']
            price200_degen = row.degen200_count * \
                price_data['degenerate_200_base']
            price1000_degen = row.degen1000_count * \
                price_data['degenerate_1000_base']

            row_object['total'] = price40 + price200 + price1000 + \
                price_desalt + price_cartridge + price_setup
            row_object['total_degen'] = price40_degen + \
                price200_degen + price1000_degen
            billing_context.append(row_object)

        return render(request, 'oligos/billing_output.html', context={'billing': billing_context})
