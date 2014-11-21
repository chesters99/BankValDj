from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class StaticViewSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['index', 'accounts:validate', 'accounts:bulktest', 'rules:search', 'rules:load',
                # 'templates:detail', 'templates:create', 'templates:update', 'templates:delete', # problem with pk
                'main:about', 'main:contact', 'main:showdoc', 'main:createuser', 'main:loginuser', 'main:logoutuser']

    def location(self, item):
        return reverse(item)
