from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^detail/(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
    url(r'^create/$', views.Create.as_view(), name='create'),
    url(r'^update/(?P<pk>\d+)/$', views.Update.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.Delete.as_view(), name='delete'),
    url(r'^load/$', views.Load.as_view(), name='load'),
    url(r'^ajax_search', 'rules.views.ajax_search', name='ajax_search'),
    url(r'^rss/$', views.RssFeed()),
)
