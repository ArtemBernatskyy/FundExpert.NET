import requests
from collections import defaultdict

from bs4 import BeautifulSoup
from django.conf import settings


class SectorsParser:
    def __init__(self, username=settings.TRUSTNET_USERNAME, password=settings.TRUSTNET_PASSWORD):
        self.username = username
        self.password = password
        self.parsed_data = defaultdict(list)     # {'name': [[cum_usd],[cum_eur],[dis_usd], [dis_eur]]}
        self.s = requests.session()

    def login(self):
        '''Login method'''
        data = {
            'EmailAddress': self.username,
            'userPwd': self.password,
            'remember': 'on',
            'Url': '/Investments/SectorPerf.aspx?univ=DC',
        }
        self.s = requests.session()
        self.s.post('http://trustnetoffshore.com/Tools/Portfolio/PortfolioLogin.aspx?url=%2fInvestments%2fSectorPerf.aspx%3funiv%3dDC',
                    data=data
                    )

    def change_currency(self, currency):
        '''Change currency to specified'''
        self.s.cookies.set("TN_Currency", None)
        self.s.cookies.set("TN_Currency", currency)

    def parse_cum(self, currency):
        '''Parse cumulative data to defauldict'''
        self.change_currency(currency)
        result = self.s.get("http://trustnetoffshore.com/Investments/SectorPerf.aspx?univ=DC")
        soup = BeautifulSoup(result.text, "html5lib")
        table = soup.find("table", id="fundslist")
        for pos in range(1, 200):
            try:
                data_list = []
                tr = table("tr")[pos]
                name = tr("td")[2].text
                for i in range(3, 10):
                    data_list.append(tr("td")[i].text)
                self.parsed_data[name].append(data_list)
            except IndexError:
                break

    def parse_dis(self, currency):
        '''Parse discrete data to defauldict'''
        self.change_currency(currency)
        data = {
            'CurrTab': 'discPerf',
        }
        result = self.s.post("http://trustnetoffshore.com/Investments/SectorPerf.aspx?univ=DC", data=data)
        soup = BeautifulSoup(result.text, "html5lib")
        table = soup.find("table", id="fundslist")
        for pos in range(1, 200):
            try:
                data_list = []
                tr = table("tr")[pos]
                name = tr("td")[2].text
                for i in range(3, 8):
                    data_list.append(tr("td")[i].text)
                self.parsed_data[name].append(data_list)
            except IndexError:
                break

    def parse(self):
        '''Method for parsing in order'''
        self.login()            # login and grab auth cookies
        self.parse_cum("USD")   # cumulative USD
        self.parse_cum("EUR")   # cumulative EUR
        self.parse_dis("USD")   # cumulative USD
        self.parse_dis("EUR")   # cumulative EUR
