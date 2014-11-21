from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class CreateUserForm(forms.Form):  # could/should have user ModelForm based on user
    username = forms.CharField(max_length=User._meta.get_field('username').max_length, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'more than 5 characters'}))
    password = forms.CharField(max_length=User._meta.get_field('password').max_length, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'more than 5 characters', 'type': 'password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not len(username) > 5:
            raise forms.ValidationError(_('Username must be more than 5 characters'), code='invalid')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not len(password) > 5:
            raise forms.ValidationError(_('Password must be more than 5 characters'), code='invalid')
        return password

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        if cleaned_data.get('username') == cleaned_data.get('password') and \
                cleaned_data.get('username') is not None:
            message = _('Username cannot be the same as password')
            self.add_error('username', message)
            self.add_error('password', message)
