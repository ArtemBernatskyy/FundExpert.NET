from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, TemplateView, ListView

from .models import Fund, FinanceSector
from .forms import MutualFundsRankingForm


class FundDetailView(DetailView):
    model = Fund
    template_name = 'finance/fund_detail.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Fund.objects.all().select_related('management_company__name').prefetch_related('topfundholdings')
        else:
            return Fund.objects.published().select_related('management_company__name').prefetch_related('topfundholdings')

    def get_context_data(self, **kwargs):
        context = super(FundDetailView, self).get_context_data(**kwargs)
        return context


class MSRatingView(TemplateView):
    template_name = 'finance/ms_rating.html'

    def get_context_data(self, **kwargs):
        context = super(MSRatingView, self).get_context_data(**kwargs)
        context['funds'] = Fund.objects.published().order_by('-ms_rating').select_related('finance_sector__name')
        return context


class MutualFundsRankingView(FormMixin, ListView):
    template_name = 'finance/mutual_funds_ranking.html'
    form_class = MutualFundsRankingForm

    def check_mine(self):
        if 'mine' in self.request.GET and self.request.GET.get('mine') == 'on':
            return True
        else:
            return False

    def get_time_period_date(self):
        if 'time_period_date' in self.request.GET and self.request.GET.get('time_period_date'):
            return int(self.request.GET.get('time_period_date'))
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(MutualFundsRankingView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        context['mine'] = self.check_mine()    # only mine
        context['time_period_date'] = self.get_time_period_date()
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)

        only_mine = self.check_mine()
        if only_mine and self.request.user.is_authenticated():
            qs = self.request.user.profile.liked_funds.published().sort_by_return().select_related('finance_sector__name')
        else:
            qs = Fund.objects.published().sort_by_return().select_related('finance_sector__name')

        if form.is_valid():
            total_assets = form.cleaned_data['total_assets']
            if total_assets is not None:
                qs = qs.filter(total_assets__gte=total_assets)

            finance_sector = form.cleaned_data['finance_sector']
            if finance_sector is not None:
                qs = qs.filter(finance_sector=finance_sector)

            birth_date = form.cleaned_data['birth_date']
            if birth_date:
                qs = qs.filter(birth_date__year__lte=birth_date)

            ms_rating = form.cleaned_data['ms_rating']
            if ms_rating:
                qs = qs.filter(ms_rating=ms_rating)

            t_period_date = form.cleaned_data['time_period_date']
            if t_period_date:
                qs = qs.sort_by_return(days=t_period_date)

            time_period_minimal_return = form.cleaned_data['time_period_minimal_return']
            if time_period_minimal_return:
                qs = qs.filter(growth__gte=time_period_minimal_return)

        return qs


class SectorsRankingView(TemplateView):
    template_name = 'finance/sectors_ranking.html'

    def check_cumulative(self):         # Cumulative View
        if 'cml' in self.request.GET:
            return True
        else:
            return False

    def check_discrete(self):           # Discrete View
        if 'dis' in self.request.GET:
            return True
        else:
            return False

    def check_usd(self):                # USD Currency
        if 'usd' in self.request.GET:
            return True
        else:
            return False

    def check_eur(self):                # EUR Currency
        if 'eur' in self.request.GET:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(SectorsRankingView, self).get_context_data(**kwargs)
        context['sectors'] = FinanceSector.objects.published()
        context['cml'] = self.check_cumulative()    # Cumulative View
        context['dis'] = self.check_discrete()      # Discrete View
        context['usd'] = self.check_usd()           # USD Currency
        context['eur'] = self.check_eur()           # EUR Currency
        return context


class SectorDetailView(SingleObjectMixin, ListView):
    template_name = 'finance/sector_page.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FinanceSector.objects.published())
        return super(SectorDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.object.get_funds()
        return qs
