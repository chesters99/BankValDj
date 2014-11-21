from django.dispatch import receiver
from djstripe.signals import WEBHOOK_SIGNALS


@receiver(WEBHOOK_SIGNALS['customer.subscription.deleted'])
def subscription_deleted(sender, ** kwargs):
    print('subscription cancelled')

