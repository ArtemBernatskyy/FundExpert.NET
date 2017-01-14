from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import (FinanceClass, FinanceSector)


class MutualFundsRankingForm(forms.Form):
    finance_class = forms.ModelChoiceField(
        required=False,
        queryset=FinanceClass.objects.all(),
        empty_label=_("(all classes)"),
    )
    finance_sector = forms.ModelChoiceField(
        required=False,
        queryset=FinanceSector.objects.all(),
        empty_label=_("(all sectors)"),
    )
    total_assets = forms.IntegerField(
        required=False,
        max_value=99999,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('total assets'),
                'onfocus': "this.type='number';"
            }
        )
    )
    birth_date = forms.ChoiceField(
        required=False,
        choices=[(None, _('(choose year)'))] + [(year, year) for year in reversed(range(1950, 2017))]
    )
    time_period_minimal_return = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('minimal return')}
        )
    )
    time_period_date = forms.ChoiceField(
        required=False,
        choices=[
            (None, _('(time period)')),
            (30, _('month')),
            (90, _('3 months')),
            (180, _('half year')),
            (1800, _('5 years'))
        ]
    )
    ms_rating = forms.ChoiceField(
        required=False,
        choices=[
            (None, _('(choose rating)')),
            (5, '5 ★ ★ ★ ★ ★ '),
            (4, '4 ★ ★ ★ ★ '),
            (3, '3 ★ ★ ★ '),
            (2, '2 ★ ★ '),
            (1, '1 ★ ')
        ]
    )

    def clean_time_period_minimal_return(self):
        time_period_minimal_return = self.cleaned_data['time_period_minimal_return']
        try:
            return float(time_period_minimal_return.replace(',', '.'))
        except:
            return False
