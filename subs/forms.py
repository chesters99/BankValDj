from django.forms import TextInput, Select, Form, CharField, ChoiceField
from django.utils import timezone


class StripeForm(Form):
    def __init__(self, *args, **kwargs):
        super(StripeForm, self).__init__(*args, **kwargs)
        for field in self.fields:  # flag with correct CSS class (short than declaring on each field
            self.fields[field].widget.attrs['class'] = 'form-control'

    YEAR_CHOICES = [(i, i) for i in range(timezone.now().year, timezone.now().year + 12)]
    MONTH_CHOICES = [(i, i) for i in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')]

    card_number = CharField(required=False, max_length=20, widget=TextInput(attrs={'data-stripe': 'number'}))
    expiry_month = ChoiceField(required=False, choices=MONTH_CHOICES, initial=timezone.now().month,
                               widget=Select(attrs={'data-stripe': 'exp-month', 'placeholder': 'MM'}))
    expiry_year = ChoiceField(required=False, choices=YEAR_CHOICES, initial=YEAR_CHOICES[0][0],
                              widget=Select(attrs={'data-stripe': 'exp-year', 'placeholder': 'YYYY'}))
    cvc = CharField(required=False, max_length=4, widget=TextInput(attrs={'data-stripe': 'cvc'}))
    stripe_token = CharField()
