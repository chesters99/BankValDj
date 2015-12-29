from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^validate/$', views.ValidateAccount.as_view(), name='validate'),
    url(r'^bulktest/$', views.BulkTest.as_view(), name='bulktest'),
]
