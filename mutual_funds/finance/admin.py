from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .tasks import initial_parser
from .models import (
    Fund, FinanceClass, FinanceSector, NAV, TopFundHolding
)


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


make_published.short_description = _('Publish')


def parse_again(modeladmin, request, queryset):
    for fund in queryset:
        initial_parser.apply_async(args=[fund.pk], countdown=2)
        messages.info(request, "{} added to parsing, check back in 4-5 minutes".format(fund.name))


parse_again.short_description = _('Parse again')


def make_parsing(modeladmin, request, queryset):
    queryset.update(is_parcing=True)


make_parsing.short_description = _('Is parsing on')


def make_parsing_and_publish(modeladmin, request, queryset):
    queryset.update(is_parcing=True, is_published=True)


make_parsing_and_publish.short_description = _('Is parsing & Publish')


class TopFundHoldingInline(admin.StackedInline):
    model = TopFundHolding
    extra = 0
    classes = ('grp-collapse',)


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ['name', 'bloombreg_ticker', 'isin_ticker', 'management_company', 'last_updated', 'created_date', 'is_published', 'is_parcing']
    list_editable = ['is_published', 'is_parcing']
    search_fields = ['name', 'bloombreg_ticker', 'isin_ticker']
    list_filter = ['is_parcing', 'is_published', 'management_company', 'finance_sector', 'finance_sector__finance_class']
    list_display_links = ['name']
    fields = ['name', 'last_updated', 'fund_manager', 'is_published', 'is_parcing', 'management_company',
              'finance_sector', 'bloombreg_ticker', 'isin_ticker', 'ms_rating', 'birth_date',
              'country', 'currency', 'total_assets', 'range_52_weeks', 'price_timedelta', 'investment_strategy', 'created_date', 'modified_date']
    readonly_fields = ['last_updated', 'created_date', 'modified_date', 'price_timedelta']
    actions = [make_published, make_parsing, make_parsing_and_publish, parse_again]
    inlines = [TopFundHoldingInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            messages.info(request, "Fund added to parsing, check back in 4-5 minutes")
        super(FundAdmin, self).save_model(request, obj, form, change)


class FinanceSectorInline(admin.StackedInline):
    model = FinanceSector
    extra = 0
    classes = ('grp-collapse',)

    def has_add_permission(self, request):
        return False


@admin.register(FinanceClass)
class FinanceClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name',)
    inlines = [FinanceSectorInline]


class FundInline(admin.StackedInline):
    model = Fund
    extra = 0
    classes = ('grp-collapse',)

    def has_add_permission(self, request):
        return False


@admin.register(FinanceSector)
class FinanceSectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published', 'last_updated', 'cumulative_usd', 'cumulative_eur', 'discrete_usd', 'discrete_eur', 'finance_class']
    search_fields = ('name', 'parsed_name',)
    list_editable = ['is_published']
    list_filter = ['finance_class']
    inlines = [FundInline]
    fields = ['name', 'is_published', 'last_updated', 'finance_class', 'cumulative_usd',
              'cumulative_eur', 'discrete_usd', 'discrete_eur', 'parsed_name', 'slug',
              'created_date', 'modified_date']
    readonly_fields = ['last_updated', 'parsed_name', 'slug', 'created_date', 'modified_date']
    actions = [make_published]

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        # Disable delete
        actions = super(FinanceSectorAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NAV)
class NAVAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = ['price', 'date']
    search_fields = ['fund__name']
    list_filter = ['fund']

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        # Disable delete
        actions = super(NAVAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TopFundHolding)
class TopFundHoldingAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['fund']
