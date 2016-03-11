""" documentation from views.py for application "**rules**" (for Sphinx) """
from django.contrib.syndication.views import Feed
from django.shortcuts import render_to_response
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from .models import Rule, load_rules
from .forms import RuleForm, LoadRulesForm
from main.decorators import DeleteMessageMixin, ActiveLoginRequiredMixin
from debug_toolbar_line_profiler import profile_additional

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


class Detail(DetailView):
    template_name = 'detail.html'
    queryset = Rule.objects.select_related('created_by').select_related('updated_by').select_related('site')


class Update(ActiveLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Rule
    form_class = RuleForm
    template_name = 'create_update.html'
    success_message = 'Rule Updated Successfully'

    def get_success_url(self):
        return reverse('rules:detail', kwargs={'pk': self.object.pk})


class Delete(ActiveLoginRequiredMixin, DeleteMessageMixin, DeleteView):
    model = Rule
    template_name = 'delete.html'
    delete_message = 'Rule Deleted (Inactivated) Successfully'
    success_url = reverse_lazy('rules:search')


class Create(ActiveLoginRequiredMixin, SuccessMessageMixin, CreateView):  # Using Generic class-based View
    model = Rule
    form_class = RuleForm
    template_name = 'create_update.html'
    success_message = 'Rule Created Successfully'

    def get_success_url(self):
        return reverse('rules:detail', kwargs={'pk': self.object.id})


class Load(ActiveLoginRequiredMixin, FormView):
    form_class = LoadRulesForm
    template_name = 'load.html'
    initial = {'filename': 'valacdos.txt', 'vocalink_filename': 'https://www.vocalink.com/media/1518/valacdos.txt'}

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        filename = form.cleaned_data['filename']
        try:
            records = load_rules(filename)
            messages.success(self.request, 'Rules loaded successfully with {recs} records'.format(recs=records))
        except (IOError, IndexError, RuntimeError):
            messages.error(self.request, 'Cant open file: {file} or file is corrupt'.format(file=filename))
        return self.render_to_response(context)

    @profile_additional(load_rules)
    def dispatch(self, *args, **kwargs): # need dispatch here to collect line profile for Bank Validator
        return super(Load, self).dispatch(*args, **kwargs)

class RssFeed(Feed):
    title = 'UK Bank Validation Rules Feed'
    link = 'https://gchester.com/en/rules/rss/'
    description = 'Pointless Feed for no apparent reason'

    def items(self):
        return Rule.objects.all()[:10]

    def item_title(self, rule):
        return '%s-%s' % (rule.start_sort, rule.end_sort)

    def item_description(self, rule):
        return '%s %s %s %s' % (rule.weight[0], rule.weight[1], rule.weight[2], rule.weight[3])

    def item_link(self, rule):
        return 'https://gchester.com/en/rules/detail/%s/' % rule.id


# method-based equivalent to the above shown as best-practice example
# def RuleCreate(request, template_name = 'templates/rule_form.html'): # using method-based view
#    form = RuleForm(request.POST if request.method == 'POST' else None)
#    if form.is_valid():
#        new_rule = form.save()
#        return redirect(new_rule)
#    return render(request, template_name)
