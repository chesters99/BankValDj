from os import path
from django.contrib import messages
from django.views.generic import FormView
from django.conf import settings
from .forms import ValidateAccountForm, BulkTestForm
from .utils import Validator
from .tasks import test_task
# from debug_toolbar_line_profiler import profile_additional


class ValidateAccount(FormView):
    """ Validate UK Bank Account """
    form_class = ValidateAccountForm
    template_name = 'validate.html'

    def form_valid(self, form, **kwargs):
        sort_code = form.cleaned_data['sort_code']
        account_number = form.cleaned_data['account_number']
        bv = Validator()
        if bv.validate(sort_code, account_number):
            messages.success(self.request, '%s-%s is a valid bank account' % (sort_code, account_number ))
        else:
            messages.error(self.request, '%s-%s %s' % (sort_code, account_number, bv.message))
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class BulkTest(FormView):
    """ Test a bunch of UK Bank Accounts  """
    form_class = BulkTestForm
    template_name = 'bulktest.html'
    initial = {'filename': 'vocalinkTests.txt'}

    def form_valid(self, form, **kwargs):
        test_task.delay(4)  # test for batch process- runs an X seconds delay
        filename = form.cleaned_data['filename']
        try:
            tests = [(line[0:6], line[7:15]) for line in open(path.join(settings.MEDIA_ROOT, filename), 'r')];
            bv=Validator()
            for sort_code, account_number in tests:
                if bv.validate(sort_code, account_number):
                    messages.success(self.request, '%s-%s Valid=True' % (sort_code, account_number))
                else:
                    messages.error(self.request, '%s-%s Valid=False %s' % (sort_code, account_number, bv.message))
        except IOError as err:
            messages.error(self.request, "Error Opening: %s. %s" % (filename, str(err.strerror)))
        context = self.get_context_data(**kwargs)
        context['form'] = form  # use this pattern as it allows easy addition of other variables to pass to template
        return self.render_to_response(context)

    # @profile_additional(Validator._get_rules)
    def dispatch(self, *args, **kwargs): # need dispatch here to collect line profile for Bank Validator
        return super(BulkTest, self).dispatch(*args, **kwargs)


# method-based equivalents to the above shown as best-practice examples
#
# def ValidateFormView(request, template_name = 'templates/validate_form_view.html'):
#    form = ValidateAccountForm(request.POST if request.method == 'POST' else None)
#    if form.is_valid(): == None:
#        sort_code = form.cleaned_data['sort_code']
#        account_number = form.cleaned_data['account_number']
#        bv = Validator()
#        if bv.templates(sort_code, account_number):
#            messages.success(request, sort_code+' '+account_number+' is Valid')
#        else:
#            messages.error(request, sort_code+' '+account_number+' is not Valid: ' + bv.message)
#    return render(request, template_name, {'form': form)
#
#
# @profile_additional(Validator.validate)
# def bulktest(request, template_name = 'bulktest.html'):
#    filename = 'vocalinkTests.txt' # set default for display on form
#    form = BulkTestForm(request.POST if request.method == 'POST' else None)
#    if form.is_valid():
#        filename = form.cleaned_data['filename']
#        tests = BulkTestModel(path.join(settings.MEDIA_ROOT, filename).replace('..', ''))
#        if tests.message is None:
#            bv = Validator()
#            for sort_code, account_number in tests.test:
#                if bv.validate(sort_code, account_number):
#                    messages.success(request, sort_code+' '+account_number+' is Valid')
#                else:
#                    messages.error(request, sort_code+' '+account_number+' is not Valid: '+bv.message)
#        else:
#            messages.error(request, "Error Opening:" + filename + '. ' + tests.message)
#    return render(request, template_name, {'form': form} )
