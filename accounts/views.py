import os
from django.contrib import messages
from django.views.generic import FormView
from .forms import ValidateAccountForm, BulkTestForm
from .utils import Validator, BulkTestModel
from django.conf import settings
from .tasks import test_task


class ValidateAccount(FormView):
    """ Validate UK Bank Account """
    form_class = ValidateAccountForm
    template_name = 'validate.html'

    def form_valid(self, form, **kwargs):
        sort_code = form.cleaned_data['sort_code']
        account_number = form.cleaned_data['account_number']
        bv = Validator()
        result = bv.validate(sort_code, account_number)
        if result:
            messages.success(self.request, sort_code + "-" + account_number + " is a valid bank account")
        else:
            messages.error(self.request, sort_code + "-" + account_number + " " + bv.message)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class BulkTest(FormView):
    """ Test a bunch of UK Bank Accounts  """
    form_class = BulkTestForm
    template_name = 'bulktest.html'
    initial = {'filename': 'vocalinkTests.txt'}

    def form_valid(self, form, **kwargs):
        test_task.delay(5)  # test for batch process- runs an X seconds delay
        filename = form.cleaned_data['filename']
        tests = BulkTestModel(os.path.join(settings.MEDIA_ROOT, filename).replace('..', ''))
        if tests.message is None:
            bv = Validator()
            for sort_code, account_number in tests.test:
                valid = bv.validate(sort_code, account_number)
                if bv.message is not None:
                    messages.error(self.request,
                                   sort_code + '-' + account_number + ' Valid=' + str(valid) + ' ' + bv.message)
                else:
                    messages.success(self.request, sort_code + '-' + account_number + ' Valid=' + str(valid))
        else:
            messages.error(self.request, "Error Opening:" + filename + '. ' + tests.message)
        context = self.get_context_data(**kwargs)
        context['form'] = form  # use this pattern as it allows easy addition of other variables to pass to template
        return self.render_to_response(context)

#
# method-based equivalents to the above shown as best-practice examples
#
#def ValidateFormView(request, template_name = 'templates/validate_form_view.html'):
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
#def bulktest(request, template_name = 'templates/bulktest.html'):
#    filename = './static/static/vocalinkTests.txt' # set default for display on form
#    form = ValidateAccountForm(request.POST if request.method == 'POST' else None)
#    if form.is_valid():
#        filename = form.cleaned_data['filename']
#        tests = BulkTestModel(filename)
#        if tests.message is None:
#            bv = Validator()
#            for sort_code, account_number in tests.test:
#                if bv.templates(sort_code, account_number):
#                    messages.success(request, sort_code+' '+account_number+' is Valid)
#                else:
#                    messages.error(request, sort_code+' '+account_number+' is not Valid: '+bv.message)
#        else:
#            messages.error(request, "Error Opening:" + filename + '. ' + tests.message)
#    return render(request, template_name, {'form': form)
