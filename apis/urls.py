from django.conf.urls import patterns, url, include
from apis.views import rules_router


urlpatterns = patterns('apis.views',
    url(r'^validate/$', 'validate', name='validate'),
    url(r'^', include(rules_router.urls)),
)
