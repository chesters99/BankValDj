from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from djstripe.models import Customer
from main.decorators import ActiveLoginRequiredMixin
from .forms import StripeForm


@method_decorator(cache_control(private=True), name='dispatch')
class SubscribeView(ActiveLoginRequiredMixin, FormView):
    template_name = 'subscribe.html'
    form_class = StripeForm
    success_url = reverse_lazy('subs:thank_you')

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        profile = self.request.user.profile
        if profile.stripe_customer_id:
            customer = Customer.objects.get(stripe_id=profile.stripe_customer_id)
        else:
            customer = Customer.create(self.request.user)
            profile.stripe_customer_id = customer.stripe_id
            profile.save()
        context['customer'] = customer
        return context

    @transaction.atomic()
    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        customer = context['customer']
        customer.update_card(form.cleaned_data.get('stripe_token', None))
        customer.subscribe('monthly')
        return super(SubscribeView, self).form_valid(form)


class SuccessView(TemplateView):
    template_name = 'thank_you.html'
