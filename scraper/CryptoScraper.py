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
        self.base_url = 'https://www.coingecko.com/en/'
        self.price_charts_url = self.base_url+'price_charts/'

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
        content = self.get_page_content(name, tag)
        return content

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
        response = requests.get(self.price_charts_url+name+'/'+tag)
        response.raise_for_status()
        return response.content

    def _get_currency_details(self, page_content, price_symbol):
        """
            Get all details for a crypto-currency

        :param page_content: The html page content with crypto-currency information
        :type page_content: str
        :return: extracted details for an given crypto-currency
        """
        tree = html.fromstring(page_content)
    
        # Options for xpath
        limb = tree.xpath('//div[@class="card-footer bg-transparent"]/div[@class="table-responsive"]/table[@class="table mt-2"]/tbody/tr')[0]
        opts = {
            'currency':   'td[1]/text()',
            'symbol':     'td[2]/text()',
            'price':      'td[3]/span/text()',
            'market_cap': 'td[4]/span/text()',
            'volume':     'td[5]/span/text()'
        }

        crypt_currency = dict()

        for key, path in opts.iteritems():
            if key is 'currency':
                info = limb.xpath(path)[1]
                crypt_currency[key] = str(info).replace("\n",'')
            elif key in('price', 'market_cap', 'volume'):
                info = limb.xpath(path)[0]
                crypt_currency[key] = clean_currency_amount(info)
            else:
                info = limb.xpath(path)[0]
                crypt_currency[key] = info

        # append current timestamp
        crypt_currency['date'] = int(time.time())

        # append the exchange_symbol
        crypt_currency['price_symbol'] = price_symbol.upper()
        return crypt_currency

def clean_currency_amount(data):
    m = re.search(r'^\S([,\d.]+)', data)
    if m:
        return m.group(1).replace(',','')
    else:
        return data
