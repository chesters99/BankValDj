from django.contrib import admin

# Register your models here.
from rules.models import Rule


class RuleAdmin(admin.ModelAdmin):
    list_display = ('start_sort', 'end_sort', 'mod_rule', 'weight0', 'weight1', 'weight2', 'weight3', 'weight4',
                    'weight5', 'weight6', 'weight7', 'weight8', 'weight9', 'weight10', 'weight11', 'weight12',
                    'weight13', 'mod_exception')


admin.site.register(Rule, RuleAdmin)