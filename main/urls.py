from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'^about/$',   views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^showdoc/$', views.DocumentView.as_view(), name='showdoc'),
    url(r'^createuser/$', views.CreateUser.as_view(), name='createuser'),
    url(r'^graph/$',      views.Graph.as_view(), name='graph'),
    url(r'^loginuser/$',  login, {'template_name': 'login.html'}, name='loginuser'),
    url(r'^logoutuser/$', views.LogoutUser.as_view(), name='logoutuser'),
    url(r'^text_email/$', views.text_email, name='text_email'),
    url(r'^html_email/$', views.html_email, name='html_email'),
]
