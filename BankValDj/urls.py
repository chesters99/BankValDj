from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

from main.views import IndexView, TemplateView
from .sitemaps import StaticViewSiteMap


admin.autodiscover()

sitemaps = {'static': StaticViewSiteMap}

urlpatterns = i18n_patterns(
    url(r'^admin/doc/', include(admindocs_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^payments/', include('djstripe.urls', namespace='djstripe'), name='payments'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

for app in settings.LOCAL_APPS:
    urlpatterns += [
        url(r'^%s/' % app, include(app + '.urls', namespace=app)),
    ]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', TemplateView.as_view(template_name="404.html")),     # enable local preview of error pages
        url(r'^500/$', TemplateView.as_view(template_name="500.html")), ]
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),]

#    urlpatterns += [url(r'^silk', include('silk.urls', namespace='silk'))]
