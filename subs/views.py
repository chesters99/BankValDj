from django.db import transaction
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from djstripe.models import Customer
from main.countries import COUNTRIES
from main.decorators import class_decorator, ActiveLoginRequiredMixin
from main.models import UserProfile
from .forms import StripeForm


@class_decorator(cache_control(private=True))
class SubscribeView(ActiveLoginRequiredMixin, FormView):
    template_name = 'subscribe.html'
    form_class = StripeForm
    success_url = reverse_lazy('subs:thank_you')

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        context['customer'] = self.request.user.customer or None

        profile = UserProfile.objects.get(user_id=self.request.user.id)
        context['profile'] = profile
        context['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        context['stripe_customer_id'] = profile.stripe_customer_id
        context['email'] = self.request.user.email
        context['address_line1'] = profile.address_line1
        context['address_line2'] = profile.address_line2
        context['city'] = profile.city
        context['post_code'] = profile.post_code
        context['state'] = profile.state
        context['country'] = dict(COUNTRIES)[profile.country or 'GB']
        return context

    # def form_valid(self, form, **kwargs):
    #     stripe.api_key = settings.STRIPE_SECRET_KEY
    #     context = self.get_context_data(**kwargs)
    #     if context['stripe_customer_id']:
    #         customer = stripe.Customer.retrieve(context['stripe_customer_id'])
    #     else:
    #         customer_data = {
    #             'description': context['name'],
    #             'card': form.cleaned_data['stripe_token'],
    #             'email': context['email'],
    #         }
    #         customer = stripe.Customer.create(**customer_data)
    #         context['profile'].stripe_customer_id = customer['id']
    #         context['profile'].save()
    #     customer.subscriptions.create(plan="monthly_plan")
    #     # charge = stripe.Charge.create(amount=400, currency="gbp", card=form.cleaned_data['stripe_token'],
    #     # description="Charge for test@gchester.com" )
    #     return super(SubscribeView, self).form_valid(form)

    @transaction.atomic()
    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        customer = context['customer']
        if not customer:
            customer = Customer.create(self.request.user)
        customer.update_card(form.cleaned_data.get('stripe_token', None))
        customer.subscribe('monthly')
        return super(SubscribeView, self).form_valid(form)


class SuccessView(TemplateView):
    template_name = 'thank_you.html'
