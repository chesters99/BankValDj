from django.contrib import admin

# Register your models here.
from rules.models import Rule


class RuleAdmin(admin.ModelAdmin):
    list_display = ('start_sort', 'end_sort', 'mod_rule', 'weight', 'mod_exception')


admin.site.register(Rule, RuleAdmin)
