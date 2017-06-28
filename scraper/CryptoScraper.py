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
        self.base_url = 'https://www.coingecko.com/de/kurs_chart/'

        valid_currencies, errors = DataSchema(many=True).load(currencies_to_scrape)
        if not errors:
            self.currencies_to_scrape = valid_currencies
        else:
            # TODO: Throw in error if the currencies are not valid
            pass

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

    def _transform(self, page_content, exchange_rate, *args, **kwargs):
        """
            Transforms the extraced data into an given format

        :param page_content: extraced page content in html
        :type page_content: str
        :param args:
        :param kwargs:
        :return: Transformed CryptCurrency Details
        """
        return self._get_currency_details(page_content, exchange_rate)

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
                crypt_currency = self._transform(page_content=page_content, exchange_rate=tag)
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

    def clean_currency_amount(self, data):
        m = re.search(r'^\s+(.*\d+)\s+.*', data)
        if m:
            return m.group(1)

    def _get_currency_details(self, page_content, exchange_rate):
        """
            Get all details for an crypt-currency

        :param page_content: The html page content with crypt-currency information
        :type page_content: str
        :return: extracted details for an given crypt-currency
        """
        tree = html.fromstring(page_content)

        # Options for xpath
        opts = {
            'currency': '1',
            'code': '2',
            'exchange_rate': '3',
            'market_capitalisation': '4',
            'trading_volume': '5'
        }

        crypt_currency = dict()

        for key, value in opts.iteritems():
            info = tree.xpath('//div[@class="col-xs-12"]/div/table[@class="table"]/tbody/tr/td[' + value + ']/text()')[0]
            if value in('3', '4', '5'):
                crypt_currency[key] = self.clean_currency_amount(info)
            else:
                crypt_currency[key] = info

        # append actual timestamp
        crypt_currency['date'] = int(time.time())

        # append the exchange_rate
        crypt_currency['exchange_rate'] = exchange_rate.upper()

        return crypt_currency
