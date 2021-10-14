from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy
from django.db.models import Max
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from sequences.forms import ReactionForm

from sequences.models import Template, Primer, Reaction, Account
import datetime


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


class TemplateDetailView(DetailView):
    model = Primer
    context_object_name = 'primer'
    template_name = 'sequences/primer_detail.html'


def MethodSelectView(request):
    return render(request, 'sequences/method_select.html')


def TemplateAddView(request):
    if request.method == 'GET':

        template_count = int(request.GET.get('template-count'))
        if template_count == 0:
            return HttpResponseRedirect(reverse_lazy('sequencing:add_primers'))

        TemplateFormset = modelformset_factory(Template, fields=(
            'name', 'type', 'template_size', 'insert_size', 'template_concentration', 'template_volume', 'pcr_purify', 'comment'),
            extra=template_count)
        formset = TemplateFormset(
            queryset=Template.objects.none())

        return render(request, 'sequences/add_template.html', context={'formset': formset})

    if request.method == 'POST':
        TemplateFormset = modelformset_factory(Template, fields=(
            'name', 'type', 'template_size', 'insert_size', 'template_concentration', 'template_volume', 'pcr_purify', 'comment'))
        formset = TemplateFormset(request.POST)

        previewing = True if request.POST.get('previewing') else False

        if formset.is_valid() and previewing:
            templates = formset.save(commit=False)
            context = {
                'formset': formset,
                'templates': templates,
                'previewing': previewing
            }
            return render(request, 'sequences/add_template.html', context=context)

        if formset.is_valid():
            templates = formset.save(commit=False)
            for template in templates:
                template.owner = request.user
                template.save()
            return HttpResponseRedirect(reverse_lazy('sequencing:add_primers'))

        return render(request, 'sequences/add_template.html', context={'formset': formset})


def PrimerAddView(request):
    if request.method == 'GET':
        primer_count = request.GET.get('primer-count')

        if not primer_count:
            return render(request, 'sequences/primer_count.html')
        elif int(primer_count) == 0:
            return HttpResponseRedirect(reverse_lazy('sequencing:add_reactions'))

        PrimerFormset = modelformset_factory(Primer, fields=(
            'name', 'concentration', 'volume', 'melting_temperature', 'sequence'),
            extra=int(primer_count))
        formset = PrimerFormset(
            queryset=Primer.objects.none())
        return render(request, 'sequences/add_primer.html', context={'formset': formset})

    if request.method == 'POST':
        PrimerFormset = modelformset_factory(Primer, fields=(
            'name', 'concentration', 'volume', 'melting_temperature', 'sequence'))
        formset = PrimerFormset(request.POST)

        previewing = True if request.POST.get('previewing') else False

        if formset.is_valid() and previewing:
            primers = formset.save(commit=False)
            context = {
                'formset': formset,
                'primers': primers,
                'previewing': previewing
            }
            return render(request, 'sequences/add_primer.html', context=context)

        if formset.is_valid():
            primers = formset.save(commit=False)
            for primer in primers:
                primer.owner = request.user
                primer.common = False
                primer.save()
            return HttpResponseRedirect(reverse_lazy('sequencing:add_reactions'))

        return render(request, 'sequences/add_primer.html', context={'formset': formset})


def ReactionAddView(request):
    if request.method == 'GET':
        reaction_count = request.GET.get('reaction-count')

        if not reaction_count:
            return render(request, 'sequences/reaction_count.html')
        elif int(reaction_count) == 0:
            return HttpResponseRedirect(reverse_lazy('sequencing:add_reactions'))

        ReactionFormset = formset_factory(
            ReactionForm, extra=int(reaction_count))
        formset = ReactionFormset(form_kwargs={'user': request.user})
        return render(request, 'sequences/add_reaction.html', context={'formset': formset})

    if request.method == 'POST':

        ReactionFormset = formset_factory(ReactionForm)
        formset = ReactionFormset(request.POST, form_kwargs={
            'user': request.user})

        previewing = True if request.POST.get('previewing') else False

        if formset.is_valid():
            reactions = []
            for form in formset:
                template_id = form['template'].value()
                template = Template.objects.get(id=template_id)

                primer_id = form['primer'].value()
                primer = Primer.objects.get(id=primer_id)

                hardcopy = form['hardcopy'].value()

                reaction = Reaction(template=template,
                                    primer=primer, hardcopy=hardcopy)
                reactions.append(reaction)

            if previewing:
                context = {
                    'formset': formset,
                    'reactions': reactions,
                    'previewing': previewing
                }
                return render(request, 'sequences/add_reaction.html', context=context)

            else:
                account_id = request.POST.get('account')
                account = Account.objects.get(id=account_id)

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

                for reaction in reactions:
                    reaction.submitter = request.user
                    reaction.account = account
                    reaction.submission_id = submission_id
                    reaction.status = 's'
                    reaction.save()

                messages.success(request, r'Reactions successfully ordered.')
                return HttpResponseRedirect(reverse_lazy('sequencing:list_reactions'))

        return render(request, 'sequences/add_reaction.html', context={'formset': formset})
