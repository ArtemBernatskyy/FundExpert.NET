"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'code.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            _('Finance'),
            column=1,
            collapsible=False,
            models=(
                'mutual_funds.finance.models.Fund',
                'mutual_funds.finance.models.FinanceClass',
                'mutual_funds.finance.models.FinanceSector',
                'mutual_funds.company.*',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Newsletter'),
            column=1,
            collapsible=False,
            models=(
                'mutual_funds.landing.models.NewsPost',
                'mutual_funds.landing.models.NewsCategory',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Administration'),
            column=1,
            collapsible=False,
            models=(
                'mutual_funds.accounts.models.Profile',
                'mutual_funds.registration.*'
            ),
        ))

        self.children.append(modules.ModelList(
            _('Advanced'),
            column=2,
            collapsible=False,
            models=(
                'django.contrib.auth.models.User',
                'mutual_funds.accounts.models.LikedFund',
                'mutual_funds.finance.models.NAV',
                'mutual_funds.finance.models.TopFundHolding',
                'django.contrib.auth.models.Group',
                'django.contrib.sites.*',
            ),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Useful websites'),
            column=2,
            collapsible=False,
            children=[
                {
                    'title': _('Bloomberg'),
                    'url': 'http://bloomberg.com/',
                    'external': True,
                },
                {
                    'title': _('Financial times'),
                    'url': 'http://markets.ft.com/',
                    'external': True,
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            column=3,
            limit=6,
            collapsible=False,
        ))
