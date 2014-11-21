from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^validate/$', views.ValidateAccount.as_view(), name='validate'),
    url(r'^bulktest/$', views.BulkTest.as_view(), name='bulktest'),
)
