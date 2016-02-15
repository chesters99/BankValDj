""" documentation from views.py for application "**main**" (for sphinx) """
from time import sleep
from django.contrib import auth
from django.contrib.auth import user_login_failed, get_user_model
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, FormView, RedirectView
from django.db import IntegrityError, transaction
from django.contrib import messages
from eventlog.models import Log
from .forms import CreateUserForm
from main.decorators import ActiveLoginRequiredMixin
from django.utils.decorators import method_decorator

@receiver(user_login_failed)
def delay_next_login(*args, **kwargs):
    sleep(2)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['logs'] = Log.objects.order_by('-timestamp')[:10]
        return context


class Graph(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)
        x_labels = []
        y_values = []
        for i in range(1, 101):
            if i % 10 == 0:
                x_labels.append(i)
                y_values.append(i * i / 10)
        context['x_labels'] = x_labels
        context['y_values'] = y_values
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class CreateUser(ActiveLoginRequiredMixin, FormView):
    form_class = CreateUserForm
    template_name = 'create_user.html'

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        if self.request.user.is_superuser:
            context['users'] = get_user_model().objects.all()
            try:
                with transaction.atomic():  # needed to ensure User and UserProfile are in sync
                    get_user_model().objects.create_user(form.cleaned_data['username'], None,
                                                         form.cleaned_data['password'], **kwargs)
                    messages.success(self.request, "User Created Successfully")
            except IntegrityError:
                messages.error(self.request, "Cant create user %s. User already exists" % form.cleaned_data['username'])
        else:
            messages.error(self.request, "Must be superuser to view/maintain users")
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        context = self.get_context_data(**kwargs)
        context['form'] = form
        if self.request.user.is_superuser:
            context['users'] = get_user_model().objects.all()
        return self.render_to_response(context)


class LogoutUser(ActiveLoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        messages.success(self.request, "User '{0}' Logged Out Successfully".format(self.request.user.username))
        auth.logout(self.request)
        return reverse('main:loginuser')

@csrf_exempt
def text_email(request):
    subject = 'Rubbish Text Email'
    to_email = ['chesters99@yahoo.com']
    context = {'user': 'graham', 'content': 'rubbish content to annoy you1'}
    message = render_to_string('email.txt', context)
    EmailMessage(subject, message, to=to_email).send()
    return HttpResponse('text email sent')

@csrf_exempt
def html_email(request):
    subject = 'Rubbish HTML Email'
    to_email = ['chesters99@yahoo.com']
    context = {'user': 'graham', 'content': 'rubbish content to annoy you2'}
    contents = get_template('email.html').render(Context(context))
    message = EmailMessage(subject, contents, to=to_email)
    message.content_subtype = 'html'
    message.send()
    print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])
    return HttpResponse('html email sent')


# method based equivalents shown here as a best-practice pattern 
#
# @login_required
# def adduser(request, template_name='templates/adduser.html'):
#    """ add new use and display current users in table """
#    title = 'Add New User'
#    form = AddUserForm(request.POST if request.method == 'POST' or None)
#    if form.is_valid():
#        if request.user.is_superuser:
#            try:
#                user = User.objects.create(username=request.POST['username'], password=request.POST['password'])
#                user.save()
# messages.success(request, "User Created Successfully")
#            except:
#                messages.error(request, "User Creation Failed")
#            users = User.objects.all()
#        else:
#            messages.error(request, "Must be superuser to view/maintain users")
#    return render(request, template_name, {'form': form)
#
#
# def loginuser(request): # Use standard Django admin instead
#     form = AuthenticationForm(request.POST if request.method == 'POST' else None)
#     if form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 auth_login(request, user)
#                 messages.success(request,"Login Successful")
#             else:
#                 messages.error(request,"User Account is Disabled")
#                 time.sleep(1)
#         else:
#             messages.error(request,"User or Password not valid")
#             time.sleep(1)
#     else:
#         if not request.user.is_authenticated():
#             messages.warning(request,"Please login to access system")
#     return render(request, 'templates/loginuser.html' ,{'form': form)
# @login_required
# def logoutuser(request):
#     """ use this method instead of standard django logout so can show logout message"""
#     messages.success(request, request.user.username + " Logged Out Successfully")
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('main:loginuser'))
