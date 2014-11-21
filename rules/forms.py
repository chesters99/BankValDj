from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Rule


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['start_sort', 'end_sort', 'mod_rule', 'mod_exception', 'weight0', 'weight1', 'weight2', 'weight3',
                  'weight4', 'weight5', 'weight6', 'weight7', 'weight8', 'weight9', 'weight10', 'weight11', 'weight12',
                  'weight13', 'active']
        labels = {
            'start_sort': _('Start Sort'),
            'end_sort': _('End Sort'),
            'mod_exception': _('Mod Exception'),
            'weight0': _('Weight 0'),
            'weight1': _('Weight 1'),
            'weight2': _('Weight 2'),
            'weight3': _('Weight 3'),
            'weight4': _('Weight 4'),
            'weight5': _('Weight 5'),
            'weight6': _('Weight 6'),
            'weight7': _('Weight 7'),
            'weight8': _('Weight 8'),
            'weight9': _('Weight 9'),
            'weight10': _('Weight 10'),
            'weight11': _('Weight 11'),
            'weight12': _('Weight 12'),
            'weight13': _('Weight 13'),
            'active': _('Active'),
        }

    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)
        for field in self.fields:  # flag with correct CSS class (short than declaring in 'class Meta'
            self.fields[field].widget.attrs['class'] = 'form-control'
            # self.fields[field].widget.attrs['readonly'] = True  ## flag fields as read only (&override clean methods)
            # def clean_field_1(self):  ## override of clean methon to make field read only
            #     if self.instance.is_disabled:
            #     return self.instance.field_1
            # else:
            #     return self.cleaned_data.get('field_1')


class LoadRulesForm(forms.Form):
    filename = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'local or http file'}))


#class RuleSearchForm(forms.Form):
#     sort_code = forms.CharField(required=False, max_length=6, widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'wildcard is %'}))
#
#     def clean_sort_code(self):
#         sort_code = self.cleaned_data.get('sort_code')
#         if sort_code in (None, ''):
#             raise forms.ValidationError(_('Sort code must be digit or %'))
#         if not all(c in '1234567890%' for c in sort_code):
#             raise forms.ValidationError(_('Sort code must be digit or %'))
#         return sort_code
#
#     def clean(self):
#         if any(self.errors):
#             # Don't bother validating the formset unless each field is valid
#             return self.cleaned_data
#         sort_code = self.cleaned_data.get('sort_code')
#         if sort_code is None:
#             raise forms.ValidationError(_('Sort Code must be entered'))
#         return self.cleaned_data