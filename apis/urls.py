from django.conf.urls import url
from apis.views import RuleView, RuleChange, validate

urlpatterns = [
    url(r'^validate/$', validate, name='validate'),
    url(r'^rules/$', RuleView.as_view(), name='ruleview'),
    url(r'^rulechg/(?P<pk>\d+)/$', RuleChange.as_view(), name='rulechg'),
]
