from django.forms.formsets import formset_factory
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy
from django.db.models import Max
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from accounts.models import Preapproval
from sequences.forms import ReactionEasyOrderForm, ReactionForm

from sequences.models import Template, Primer, Reaction, Account
from core.decorators import user_has_accounts
import datetime
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
        d = datetime.datetime.now()
        submission_id = int(
            str(d.year) + str(d.month) + str(d.day) + '01')

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

                reaction = Reaction(
                    submitter=request.user,
                    template=template_to_save,
                    primer=primer_to_save,
                    account=account_to_save,
                    submission_id=submission_id,
                    status='s',
                    hardcopy=hardcopy
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
