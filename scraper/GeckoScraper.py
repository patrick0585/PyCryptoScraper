# coding: utf-8

from __future__ import absolute_import, unicode_literals
from __future__ import print_function

#from scraper.Base import CryptScraperBase
from scraper.CryptoScraper import CryptoScraper
from schema.DataSchema import DataSchema

import sys
import re
import requests
import ast
import json

class GeckoScraper():

    def __init__(self):
        """
            Initializes the gecko-scraper
        """
        self.base_url = 'https://www.coingecko.com/en/'

        #currencies_to_scrape = ast.literal_eval("[{'name':'ALL','tags':['usd']}]")
        #valid_currencies = DataSchema(many=True).load(currencies_to_scrape)
        #self.currencies_to_scrape = valid_currencies

    def scrape(self):
        """
            Scrape All Currencies from CoinGecko

        :return: Scraped Crypt-Currencies
        """
        coinPathMap = { # Some of CoinGecko's coinName to coinPath mappings are just random
            'bitblocks':'bitblocks-project',
            'bitfinex-bitcoin-future': 'bt1', 'bitcoin-segwit2x': 'bt2',
            'bancor-network-token':'bancor',
            'byteball-bytes':'byteball',
            'coimatic-2-0': 'coimatic-2', 'coimatic-3-0': 'coimatic-3',
            'decentralized-machine-learning-protocol': 'decentralized-machine-learning',
            #'bitcoinultra': 'bitcoin-ultra',
            'esports-com': 'esports',
            'gamebet': 'gamebetcoin',
            'globalboost-y': 'globalboost',
            'hempcoin':'hempcoin-thc',
            'ico-openledger': 'openledger',
            'i/o-coin':'iocoin',
            'jibrel-network':'jibrel',
            "miners&#39;-reward-token": 'miners-reward-token',
            'ohmcoin': 'ohm-coin', 'cryptoinsight': 'crypto-insight',
            'omni-(mastercoin)':'omni',
            'spectreai-dividend-token':'spectre-dividend-token',
            'starcoin': 'starcointv',
            'tattoocoin-(standard-edition)': 'tattoocoin',
            'tattoocoin-(limited-edition)': 'tattoocoin-limited',
        }
        response = requests.get('https://www.coingecko.com/en/coins/all')
        response.raise_for_status()
        matches = re.findall(r"<span class='coin-content-name'>([^<]+)</span>\s*<span\s+class='coin-content-symbol'>([^<]+)</span>", response.content)
        results = []
        for mtch in matches:
            one_result = []
            coinPath = mtch[0].lower().replace(' ','-').replace('.','-').replace('-[futures]','')

            if coinPath in coinPathMap:
                coinPath = coinPathMap[coinPath]

            keep_trying = True
            while keep_trying:
                keep_trying = False
                currencies_to_scrape = ast.literal_eval("[{'name':'"+coinPath+"','tags':['usd']}]")
                #output = options.output
                valid_currencies = DataSchema(many=True).load(currencies_to_scrape)
                gecko_scraper = CryptoScraper(currencies_to_scrape=valid_currencies)
                try:
                    one_result = gecko_scraper.scrape()
                except requests.exceptions.HTTPError as ex:
                    if '-' in coinPath: # Sometimes CoinGecko just deletes a ' ' or a '-'.
                        coinPath = coinPath.replace('-','')
                        keep_trying = True
                    else:
                        print(str(ex), file=sys.stderr)

            #results.append(one_result)
            print(json.dumps(one_result))

        return results

