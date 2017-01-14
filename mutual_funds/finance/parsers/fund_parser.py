import time
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup


logging.getLogger("requests").setLevel(logging.WARNING)


class FundParser:

    """
    Class for parsing funds data with bs4 and urllib
    """

    def __init__(self, isin_ticker, bloombreg_ticker):
        # 'financial times' parsed data
        self.name = str()
        self.finance_sector = str()
        self.bloombreg_ticker = bloombreg_ticker
        self.isin_ticker = isin_ticker
        self.birth_date = str()
        self.country = str()
        self.top_fund_holdings = list()
        self.price_history = list()
        # bloomberg parsed data
        self.fund_manager = str()
        self.currency = str()
        self.total_assets = str()
        self.range_52_weeks = str()
        self.return_1_year = str()
        self.investment_strategy = str()

    def __download_url(self, url):
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        result = requests.get(url, headers=headers)
        webContent = result.text
        self.soup = BeautifulSoup(webContent, "html5lib")

    def __routes(self, goto):
        if goto == "bloomberg":
            url = "https://www.bloomberg.com/quote/{}".format(self.bloombreg_ticker)
            self.__download_url(url)
        elif goto == "markets":
            url = "http://markets.ft.com/data/funds/tearsheet/summary?s={}".format(self.isin_ticker)
            self.__download_url(url)
        elif goto == "holdings":
            url = "http://markets.ft.com/data/funds/tearsheet/holdings?s={}".format(self.isin_ticker)
            self.__download_url(url)
        elif goto == "history":
            url = "http://markets.ft.com/data/funds/tearsheet/historical?s={}".format(self.isin_ticker)
            self.__download_url(url)

    def __get_name(self):
        self.name = self.soup('h1', limit=1)[0].text

    def __get_birth_date(self):
        table = self.soup('table')[0]
        try:
            for i in range(100):
                if 'Launch date' in table('tr')[i].th:
                    parsed_date = table('tr')[i].td.text
                    self.birth_date = datetime.strptime(parsed_date, '%d %b %Y')
                    break
        except IndexError:
            pass

    def __get_country(self):
        table = self.soup('table')[0]
        try:
            for i in range(100):
                if 'Domicile' in table('tr')[i].th:
                    self.country = table('tr')[i].td.text
                    break
        except IndexError:
            pass

    def __get_top_fund_holdings(self):
        for t_id in range(1,6):
            try:
                t = self.soup('table')[t_id]
                if "1 year change" in self.soup('table')[t_id].thead.text:
                    try:
                        for row in t('tr')[1:11]:
                            try:
                                data1 = row.td.a.text
                            except AttributeError:
                                data1 = row.td.text
                            self.top_fund_holdings.append((data1, row('td')[2].text))
                    except IndexError:
                        pass
            except IndexError:
                break

    def __get_history(self):
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

        # getting last row before starting parsing from ajax requests
        last_row = int(self.soup.find("button", text="Show more")['data-mod-results-startdate'])
        while True:
            url = 'http://markets.ft.com/data/equities/ajax/getmorehistoricalprices?resultsStartDate={0!s}&symbol={1!s}&isLastRowStriped=false'.format(last_row, self.isin_ticker)
            while True:
                try:
                    r = requests.get(url=url, timeout=6)
                    data = r.json()
                    break
                except Exception:
                    time.sleep(1)
                    print('retrying in 1s ----------------------')
            if data["data"]["html"] == '':
                break
            html = data["data"]["html"]
            soup = BeautifulSoup(html, "lxml")
            all_data = soup.findAll('tr')
            all_data_len = len(all_data)
            for m in range(all_data_len):
                str_date = all_data[m].td.span.string
                str_float = all_data[m].find_all('td')[4].string
                real_date = datetime.strptime(str_date, "%A, %B %d, %Y")
                real_float = float(str_float)
                if real_date.date() not in unique_history_dates:
                    self.price_history.append((real_date, real_float))
                    unique_history_dates.add(real_date.date())
            last_row -= all_data_len

    def __get_fund_manager(self):
        divs = self.soup("div", class_="cell")
        try:
            for i in range(100):
                if 'Fund Managers' in divs[i].div.text:
                    self.fund_manager = divs[i]("div")[1].text.strip()
                    break
        except IndexError:
            pass

    def __get_currency(self):
        self.currency = self.soup.find("div", class_="currency").text

    def __get_total_assets(self):
        divs = self.soup("div", class_="cell")
        try:
            for i in range(100):
                if 'Total Assets' in divs[i].div.text:
                    self.total_assets = divs[i]("div")[1].text.strip()
                    break
        except IndexError:
            pass

    def __get_range_52_weeks(self):
        divs = self.soup("div", class_="cell cell__mobile-basic")
        try:
            for i in range(100):
                if '52Wk Range' in divs[i].div.text:
                    self.range_52_weeks = divs[i]("div")[1].text.strip()
                    break
        except IndexError:
            pass

    def __get_return_1_year(self):
        divs = self.soup("div", class_="cell cell__mobile-basic")
        try:
            for i in range(100):
                if '1 Yr Return' in divs[i].div.text:
                    self.return_1_year = divs[i]("div")[1].text.strip()
                    break
        except IndexError:
            pass

    def __get_investment_strategy(self):
        self.investment_strategy = self.soup.find("div", class_="profile__description").text.strip()

    def parse(self):
        '''
        method which combines all parsing
        '''
        self.__routes('markets')    # read page markets
        self.__get_name()
        self.__get_country()
        self.__get_birth_date()

        self.__routes('holdings')
        self.__get_top_fund_holdings()

        self.__routes('history')
        self.__get_history()

        self.__routes('bloomberg')
        self.__get_fund_manager()
        self.__get_currency()
        self.__get_total_assets()
        self.__get_range_52_weeks()
        self.__get_return_1_year()
        self.__get_investment_strategy()

    def to_dict(self):
        '''
        method which saves all necessary data to dict for further serialising
        '''
        return {
            'name': self.name,
            'finance_sector': self.finance_sector,
            'bloombreg_ticker': self.bloombreg_ticker,
            'isin_ticker': self.isin_ticker,
            'birth_date': self.birth_date,
            'country': self.country,
            'top_fund_holdings': self.top_fund_holdings,
            'price_history': self.price_history,
            'fund_manager': self.fund_manager,
            'currency': self.currency,
            'total_assets': self.total_assets,
            'range_52_weeks': self.range_52_weeks,
            'return_1_year': self.return_1_year,
            'investment_strategy': self.investment_strategy
        }
