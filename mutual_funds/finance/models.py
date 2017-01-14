from datetime import timedelta

from django.db import models
from django.db.models import Max
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import RawSQL
from django.utils.translation import ugettext_lazy as _

from model_utils.fields import StatusField
from model_utils import Choices
from autoslug import AutoSlugField
from django_countries.fields import CountryField


class FinanceClass(models.Model):
    name = models.CharField(max_length=320)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Finance classes'


class FinanceSectorQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class FinanceSector(models.Model):
    name = models.CharField(max_length=320)
    parsed_name = models.CharField(max_length=320, help_text=_('same as at trustnetoffshore'))
    is_published = models.BooleanField(default=True, help_text=_(
        "Tick to make this entry live "
    ))
    slug = AutoSlugField(populate_from='parsed_name', unique=True, null=True, blank=True)
    finance_class = models.ForeignKey('FinanceClass', related_name='sectors', on_delete=models.SET_NULL, blank=True, null=True)
    cumulative_usd = models.CharField(max_length=300, verbose_name=_("Cumulative in USD"), blank=True, null=True)
    cumulative_eur = models.CharField(max_length=300, verbose_name=_("Cumulative in EUR"), blank=True, null=True)
    discrete_usd = models.CharField(max_length=300, verbose_name=_("Discrete in USD"), blank=True, null=True)
    discrete_eur = models.CharField(max_length=300, verbose_name=_("Discrete in EUR"), blank=True, null=True)

    last_parsed = models.DateTimeField(default=now)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = FinanceSectorQuerySet.as_manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('finance:sector_detail', kwargs={'slug': self.slug})

    def last_updated(self):
        last_update = self.last_parsed.date()
        days_ago = (now().date() - last_update).days
        if days_ago <= 1:
            color = 'green'
        elif 1 < days_ago <= 2:
            color = 'orange'
        else:
            color = 'red'
        text = 'Last Data: {} ({} days ago)'.format(last_update.strftime("%d-%m-%Y"), days_ago)
        return '<span style="color:{0};">{1}</span>'.format(color, text)
    last_updated.allow_tags = True

    def get_funds(self):
        return self.funds.published()


class FundQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def parsing(self):
        return self.filter(is_parcing=True)

    def sort_by_return(self, days=365):
        # safely converting days to string with fallback
        try:
            days = int(days)
        except ValueError:
            days = 365
        # checking if date exists in all Funds if no then trying date minus -1
        safe_belt = 5
        while safe_belt > 0:
            t_date = str(now().date() - timedelta(days=days))
            if not Fund.objects.count() == NAV.objects.filter(date=t_date).count():
                days += 1
                safe_belt -= 1
            else:
                break
        # filtering
        timedelta_date = str(now().date() - timedelta(days=days))
        now_date = str(Fund.objects.annotate(max_date=Max('navs__date')).order_by('max_date')[0].max_date)
        qs = self.annotate(growth=RawSQL("""
            (select price from finance_nav where finance_fund.id=fund_id and date=%s)
            / (select price from finance_nav where finance_fund.id=fund_id and date=%s)""",
                           (now_date, timedelta_date))).order_by('-growth')
        return qs


class Fund(models.Model):
    MS_CHOICES = Choices('0', '1', '2', '3', '4', '5')
    CURRENCY_CHOICES = Choices('USD', 'EUR')

    name = models.CharField(max_length=320, verbose_name=_('fund name'), unique=True)
    fund_manager = models.CharField(max_length=320, null=True, blank=True)
    is_published = models.BooleanField(default=False, help_text=_(
        "Tick to make this entry live "
        "Note that administrators (like yourself) are allowed to preview "
        "inactive entries whereas the general public aren't."
    ))
    is_parcing = models.BooleanField(default=True, help_text=_('using for parsing'))
    management_company = models.ForeignKey('company.ManagementCompany', related_name='funds', blank=True, null=True, on_delete=models.SET_NULL)
    finance_sector = models.ForeignKey('FinanceSector', related_name='funds', blank=True, null=True, on_delete=models.SET_NULL)
    bloombreg_ticker = models.CharField(
        max_length=320,
        verbose_name=_("Bloomberg ticker"),
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\w*:[A-Z]{2}$',
                message=_("example: ROBAGED:LX")
            )
        ]
    )
    isin_ticker = models.CharField(
        max_length=320,
        verbose_name=_("ISIN ticker"),
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\w*:(USD|EUR)$',
                message=_("example: LU1274831590:EUR")
            )
        ]
    )
    ms_rating = StatusField(choices_name='MS_CHOICES', blank=True, null=True)
    birth_date = models.DateField(verbose_name=_("launch date"), blank=True, null=True)
    country = CountryField(blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    currency = StatusField(choices_name='CURRENCY_CHOICES', blank=True, null=True)
    total_assets = models.DecimalField(max_digits=19, decimal_places=3, verbose_name=_('total assets'), blank=True, null=True)
    range_52_weeks = models.CharField(max_length=320, verbose_name=_('52Wk Range '), blank=True, null=True)
    return_1_year = models.DecimalField(max_digits=19, decimal_places=2, verbose_name=_('1 Yr Return'), blank=True, null=True)
    investment_strategy = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = FundQuerySet.as_manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('finance:fund_detail', kwargs={'slug': self.slug})

    def get_total_assets(self):
        return "{} <small>{}</small>".format(self.total_assets, self.currency)

    def last_updated(self):
        last_price_date = self.navs.latest().date
        days_ago = (now().date() - last_price_date).days
        if days_ago <= 2:
            color = 'green'
        elif 2 < days_ago <= 4:
            color = 'orange'
        else:
            color = 'red'
        text = 'Last Data: {} ({} days ago)'.format(last_price_date.strftime("%d-%m-%Y"), days_ago)
        return '<span style="color:{0};">{1}</span>'.format(color, text)
    last_updated.allow_tags = True

    def get_newest_price(self):
        return "{} <small>{}</small>".format(self.navs.latest('date').price, self.currency)

    def price_timedelta(self, days=30):
        fresh_price = self.navs.latest().price
        try:
            days = int(days)
        except (ValueError, TypeError):
            days = 30
        old_price = None
        safe_belt = 5
        while safe_belt > 0:
            try:
                old_price = self.navs.get(date=now().date() - timedelta(days=days)).price
                break
            except ObjectDoesNotExist:
                safe_belt -= 1
                days += 1
        if not old_price:
            return float("-inf")
        return str(round((fresh_price / old_price) - 1, 3))
    price_timedelta.allow_tags = True
    price_timedelta.short_description = 'return 1 year'

    def topfundholdings_data(self):
        labels = [holding.name for holding in self.topfundholdings.all()]
        series = [float(holding.portfolio_weight) for holding in self.topfundholdings.all()]
        labels.append('others')             # adding the whats left of 100% pie
        series.append(float(100 - sum(series)))    # adding the whats left of 100% pie
        return [labels, series]


@receiver(post_save, sender=Fund)
def run_initial_parser(sender, instance, created, **kwargs):
    if created:
        from .tasks import initial_parser
        initial_parser.apply_async(args=[instance.pk], countdown=2)    # waiting for transaction to complete


class NAV(models.Model):
    """
    Table for NAVs of Fund and afterwards sorting by date
    """
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('NAV'))
    date = models.DateField(verbose_name=_('date'))
    fund = models.ForeignKey('Fund', related_name='navs', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now)

    class Meta:
        ordering = ('date',)
        unique_together = ('date', 'fund')
        get_latest_by = 'date'

    def __str__(self):
        return "fund_id: {}, price: {}".format(self.fund_id, self.price)


class TopFundHolding(models.Model):
    """
    Table for Top Fund Holdings of Fund
    """
    fund = models.ForeignKey('Fund', related_name='topfundholdings', on_delete=models.CASCADE)
    portfolio_weight = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    name = models.CharField(max_length=320)
    created_date = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
