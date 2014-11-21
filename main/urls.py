from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = patterns('',
    url(r'^about/$', cache_page(60*15)(TemplateView.as_view(template_name='about.html')), name='about'),
    url(r'^contact/$', cache_page(60*15)(TemplateView.as_view(template_name='contact.html')), name='contact'),
    url(r'^showdoc/$', cache_page(60*15)(TemplateView.as_view(template_name='show_document.html')), name='showdoc'),
    url(r'^createuser/$', views.CreateUser.as_view(), name='createuser'),
    url(r'^graph/$', views.Graph.as_view(), name='graph'),
    url(r'^loginuser/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='loginuser'),
    url(r'^logoutuser/$', views.LogoutUser.as_view(), name='logoutuser'),
    url(r'^text_email/$', 'main.views.text_email', name='text_email'),
    url(r'^html_email/$', 'main.views.html_email', name='html_email'),
)
