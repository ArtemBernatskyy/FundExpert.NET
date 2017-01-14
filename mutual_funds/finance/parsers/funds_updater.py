from datetime import datetime
from urllib.request import urlopen, Request

from django.db import transaction
from bs4 import BeautifulSoup

from mutual_funds.finance.models import NAV


class FundParser:

    """
    Class for updating history data with bs4 and urllib
    """

    def __init__(self, fund):
        self.fund = fund
        self.isin_ticker = self.fund.isin_ticker
        self.price_history = list()

    def __download_url(self, url):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        with urlopen(Request(url, headers=headers)) as webContent:
            webContent = webContent.read()
            self.soup = BeautifulSoup(webContent, "html5lib")

    def __routes(self, goto):
        if goto == "bloomberg":
            url = "https://www.bloomberg.com/quote/{}".format(self.bloombreg_ticker)
            self.__download_url(url)
        elif goto == "markets":
            url = "http://markets.ft.com/data/funds/tearsheet/summary?s={}".format(self.isin_ticker)
            self.__download_url(url)
        elif goto == "history":
            url = "http://markets.ft.com/data/funds/tearsheet/historical?s={}".format(self.isin_ticker)
            self.__download_url(url)

    def update(self):
        self.__routes("history")
        unique_history_dates = set()
        # parsing main page
        for i in range(1, 100):
            try:
                str_date = self.soup("table")[0]('tr')[i].td.span.text
                str_float = self.soup("table")[0]('tr')[i]('td')[4].text
            except IndexError:
                break

            real_date = datetime.strptime(str_date, "%A, %B %d, %Y")
            real_float = float(str_float)
            if real_date.date() not in unique_history_dates:
                self.price_history.append((real_date, real_float))
                unique_history_dates.add(real_date.date())

        # adding new NAVS to database
        last_nav = self.fund.navs.latest()

        new_navs = []

        for item in self.price_history:
            if last_nav.date < item[0].date():
                new_navs.append(item)
            else:
                break

        with transaction.atomic():
            # saving history data
            for price_item in new_navs:
                NAV(
                    fund=self.fund,
                    date=price_item[0],
                    price=round(float(price_item[1]), 2),
                ).save()
