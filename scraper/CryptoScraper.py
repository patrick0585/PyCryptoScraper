# coding: utf-8

from __future__ import absolute_import, unicode_literals
from scraper.Base import CryptScraperBase
from schema.DataSchema import DataSchema

from lxml import html
import re
import time
import requests


class CryptoScraper(CryptScraperBase):

    def __init__(self, currencies_to_scrape):
        """
            Initializes the crypto-scraper

        :param currencies_to_scrape: Currencies to scrape
                                    format:  [{ name => "bitcoin", tags => ["usd", "eur"] }, ...]
        :type currencies_to_scrape: list
        """
        self.base_url = 'https://www.coingecko.com/en/price_charts/'

        valid_currencies = DataSchema(many=True).load(currencies_to_scrape)
        self.currencies_to_scrape = valid_currencies

    def _extract(self, name, tag, *args, **kwargs):
        """
            Extract data from the given url

        :param name: CryptCurrency name
        :type name: str
        :param tag: Tag for the CryptCurrency
        :type tag: str
        :param args:
        :param kwargs:
        :return:
        """
        status_code, content = self.get_page_content(name, tag)
        if status_code == 200:
            return content
        else:
            raise ('page is not available')

    def _transform(self, page_content, exchange_symbol, *args, **kwargs):
        """
            Transforms the extracted data into an given format

        :param page_content: extracted page content in html
        :type page_content: str
        :param args:
        :param kwargs:
        :return: Transformed CryptCurrency Details
        """
        return self._get_currency_details(page_content, exchange_symbol)

    def scrape(self):
        """
            Scrape Crypt-Currencies from the given page

        :return: Scraped Crypt-Currencies
        """
        results = []

        for currency in self.currencies_to_scrape:
            name = currency.get('name')
            tags = currency.get('tags')

            for tag in tags:
                page_content = self._extract(name=name, tag=tag)
                crypt_currency = self._transform(page_content=page_content, exchange_symbol=tag)
                results.append(crypt_currency)

        return results

    def get_page_content(self, name, tag):
        """
            Returns content from the page crypto-currencies are listed

        :param name: Crypto-Currency name
        :type name: str
        :param tag: The Tag for the crypto-currency (usd, eur, ..)
        :type tag: str
        :return: The page content and statuscode
        """
        response = requests.get(self.base_url+name+'/'+tag)
        return response.status_code, response.content

    def _get_currency_details(self, page_content, exchange_symbol):
        """
            Get all details for a crypto-currency

        :param page_content: The html page content with crypto-currency information
        :type page_content: str
        :return: extracted details for an given crypto-currency
        """
        tree = html.fromstring(page_content)
    
        # Options for xpath
        opts = {
            'currency': '//div[@class="card-footer bg-transparent"]/div[@class="table-responsive"]/table[@class="table mt-2"]/tbody/tr/td[1]/',
            'symbol': '//div[@class="card-footer bg-transparent"]/div[@class="table-responsive"]/table[@class="table mt-2"]/tbody/tr/td[2]/',
            'exchange_rate': '//div[@class="card-footer bg-transparent"]/div[@class="table-responsive"]/table[@class="table mt-2"]/tbody/tr/td[3]/',
            'market_cap': '//div[@class="card-footer bg-transparent"]/div[@class="table-responsive"]/table[@class="table mt-2"]/tbody/tr/td[4]/',
            'volume': '//div[@class="card-footer bg-transparent"]/div[@class="table-responsive"]/table[@class="table mt-2"]/tbody/tr/td[5]/'
        }

        crypt_currency = dict()

        for key, path in opts.iteritems():
            if key is 'currency':
                info = tree.xpath(path+'text()')[1]
                crypt_currency[key] = str(info).replace("\n",'')
            elif key in('exchange_rate', 'market_cap', 'volume'):
                info = tree.xpath(path+'span/text()')[0]
                crypt_currency[key] = clean_currency_amount(info)
            else:
                info = tree.xpath(path+'text()')[0]
                crypt_currency[key] = info

        # append current timestamp
        crypt_currency['date'] = int(time.time())

        # append the exchange_symbol
        crypt_currency['exchange_symbol'] = exchange_symbol.upper()
        return crypt_currency

def clean_currency_amount(data):
    m = re.search(r'^\S([,\d.]+)', data)
    if m:
        return m.group(1).replace(',','')
    else:
        return data

