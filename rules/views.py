from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.syndication.views import Feed
from django.shortcuts import render_to_response
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.views.decorators.http import last_modified

from .models import Rule, load_rules, get_rules
from .forms import RuleForm, LoadRulesForm
from main.decorators import DeleteMessageMixin, class_decorator


@csrf_exempt
def ajax_search(request):
    if request.method == "POST":
        rules = Rule.objects.filter(start_sort__startswith=request.POST['search_text'])
    else:
        rules = Rule.objects.all()
    return render_to_response('ajax_results.html', {'rules': rules})


def latest_update(self, *args, **kwargs):
    return Rule.objects.all().latest("updated").updated


class Search(ListView):
    model = Rule
    paginate_by = 11
    template_name = 'search.html'

    def get_queryset(self):
        queryset = super(Search, self).get_queryset()
        q = self.request.GET.get('q')
        if q:
            return queryset.filter(start_sort__startswith=q).order_by('id')
        return queryset


@class_decorator(last_modified(latest_update))
class Detail(DetailView):
    template_name = 'detail.html'
    model = Rule


@class_decorator(login_required)
class Update(SuccessMessageMixin, UpdateView):
    model = Rule
    form_class = RuleForm
    template_name = 'create_update.html'
    success_message = 'Rule Updated Successfully'

    def get_success_url(self):
        return reverse('rules:detail', kwargs={'pk': self.object.pk})


@class_decorator(login_required)
class Delete(DeleteMessageMixin, DeleteView):
    model = Rule
    template_name = 'delete.html'
    delete_message = 'Rule Deleted (Inactivated) Successfully'
    success_url = reverse_lazy('rules:search')


@class_decorator(login_required)
class Create(SuccessMessageMixin, CreateView):  # Using Generic class-based View
    model = Rule
    form_class = RuleForm
    template_name = 'create_update.html'
    success_message = 'Rule Created Successfully'

    def get_success_url(self):
        return reverse('rules:detail', kwargs={'pk': self.object.id})


@class_decorator(login_required)
class Load(FormView):
    form_class = LoadRulesForm
    template_name = 'load.html'
    initial = {'filename': 'valacdos.txt', 'vocalink_filename': 'http://www.vocalink.com/media/307043/valacdos.txt'}

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        filename = form.cleaned_data['filename']
        if not 'http' in filename:
            filename = os.path.join(settings.MEDIA_ROOT, filename).replace('..', '')
        rows = get_rules(filename)
        if not rows:
            messages.error(self.request, 'Cant open file: ' + filename)
        else:
            try:
                with transaction.atomic():  # create a 'sub-transaction' that can rollback on exception
                    records = load_rules(rows)
                    if not records:
                        raise RuntimeError
            except RuntimeError:
                messages.error(self.request, 'File load Failed. Invalid record(s) found - check file format and re-run')
            else:
                messages.success(self.request, 'Rules loaded successfully with %s records' % records)
        return self.render_to_response(context)


class RssFeed(Feed):
    title = 'UK Bank Validation Rules Feed'
    link = 'https://gchester.com/en/rules/rss/'
    description = 'Pointless Feed for no apparent reason'

    def items(self):
        return Rule.objects.all()[:10]

    def item_title(self, rule):
        return '%s-%s' % (rule.start_sort, rule.end_sort)

    def item_description(self, rule):
        return '%s %s %s %s' % (rule.weight0, rule.weight1, rule.weight2, rule.weight3)

    def item_link(self, rule):
        return 'https://gchester.com/en/rules/detail/%s/' % rule.id


# method-based equivalent to the above shown as best-practice example
#def RuleCreate(request, template_name = 'templates/rule_form.html'): # using method-based view
#    form = RuleForm(request.POST if request.method == 'POST' else None)
#    if form.is_valid():
#        new_rule = form.save()
#        return redirect(new_rule)
#    return render(request, template_name)
