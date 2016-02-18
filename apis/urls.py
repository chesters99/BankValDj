from django.conf.urls import url
from apis.views import RuleViewSet, RuleList, Validate

urlpatterns = [
    url(r'^validate/$', Validate.as_view(), name='validate'),
    url(r'^rulelist/$', RuleList.as_view(), name='rulelist'),
    url(r'^rule/(?P<pk>\d+)$', RuleViewSet.as_view({'get':'retrieve', 'put':'update', 'post':'create','delete':'destroy',}), name='rule'),
]
