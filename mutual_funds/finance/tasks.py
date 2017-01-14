import logging

from django.db import transaction
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

import pycountry
from slugify import slugify
from django_countries.fields import Country
from async_messages import message_users

from mutual_funds.celery import app
from mutual_funds.finance.models import (Fund, NAV, TopFundHolding)

from .parsers.fund_parser import FundParser


@app.task()
def initial_parser(id):
    try:
        staff = User.objects.filter(is_staff=True)
        created_fund = Fund.objects.get(id=id)
        processing_fund = FundParser(created_fund.isin_ticker, created_fund.bloombreg_ticker)
        processing_fund.parse()
        # saving fund data
        created_fund.name = processing_fund.name
        created_fund.fund_manager = processing_fund.fund_manager
        created_fund.birth_date = processing_fund.birth_date
        created_fund.country = Country(code=pycountry.countries.get(name=processing_fund.country).alpha2)
        created_fund.slug = slugify(processing_fund.name, to_lower=True)
        created_fund.currency = processing_fund.currency
        created_fund.total_assets = round(float(processing_fund.total_assets), 3)
        created_fund.range_52_weeks = processing_fund.range_52_weeks
        created_fund.return_1_year = round(float(processing_fund.return_1_year.strip('%')), 2)
        created_fund.investment_strategy = str(processing_fund.investment_strategy)
        created_fund.save()

        with transaction.atomic():
            # cleaning all previous history in case if Reparse method
            NAV.objects.filter(fund=created_fund).delete()

            # saving history data
            for price_item in processing_fund.price_history:
                NAV(
                    fund=created_fund,
                    date=price_item[0],
                    price=round(float(price_item[1]), 2),
                ).save()

            # cleaning all previous TopFundHolding in case if Reparse method
            TopFundHolding.objects.filter(fund=created_fund).delete()

            # saving top_fund_holdings data
            for top_fund_item in processing_fund.top_fund_holdings:
                TopFundHolding(
                    fund=created_fund,
                    portfolio_weight=round(float(top_fund_item[1].strip('%')), 2),
                    name=top_fund_item[0]
                ).save()
            # sending async message
            message_users(staff, "{} successfully downloaded".format(created_fund.name))
    except Exception as error:
        created_fund.name += ' (error during parsing)'
        created_fund.save()
        message_users(staff, "{} error".format(str(error)), constants.WARNING)
        logging.exception('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n', error)
