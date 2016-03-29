from django import forms
from django.utils.translation import ugettext_lazy as _


class ValidateAccountForm(forms.Form):
    sort_code = forms.CharField(max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '6 digits'}))
    account_number = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '6-10 digits'}))

    def clean_sort_code(self):
        sort_code = self.cleaned_data.get('sort_code')
        # if not sort_code.isdigit():
        #     raise forms.ValidationError(_('Sort Code must be numeric'), code='invalid')
        if len(sort_code) != 6:
            raise forms.ValidationError(_('Sort code must be 6 digits'), code='invalid')
        return sort_code

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if not account_number.isdigit():
            raise forms.ValidationError(_('Account Number must be numeric'), code='invalid')
        if not (6 <= len(str(account_number)) <= 11):
            raise forms.ValidationError(_('Account Number must be between 6 and 11 digits'), code='invalid')
        return account_number

    def clean(self):
        cleaned_data = super(ValidateAccountForm, self).clean()
        if cleaned_data.get('sort_code') == cleaned_data.get('account_number') and \
                cleaned_data.get('sort_code') is not None:
            msg = _('Sort Code = Account Number. Is that right?!?')
            self.add_error('sort_code', msg)
            self.add_error('account_number', msg)


class BulkTestForm(forms.Form):
    filename = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'class': 'form-control'}))
