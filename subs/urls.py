from django.conf.urls import patterns, url
from .views import SubscribeView, SuccessView

urlpatterns = patterns('',
    url(r'^subscribe/$', SubscribeView.as_view(), name='subscribe'),
    url(r'^thank_you/$', SuccessView.as_view(), name='thank_you'),
)
