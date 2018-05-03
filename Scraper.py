#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, unicode_literals
from __future__ import print_function

from scraper.CryptoScraper import CryptoScraper
from schema.DataSchema import DataSchema
import optparse
import ast
import json
import requests
import re
import sys

def scrape():
    crypto_scraper = CryptoScraper(currencies_to_scrape=valid_currencies)

    results = crypto_scraper.scrape()

    print(json.dumps(results))

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog [options] arg1")
    parser.add_option("-c", "--currencies", dest="currencies", type = "str", help = "specify currencies to scrape")
    parser.add_option("-o", "--output", dest="output", type="str", default="json", help="specify output format")

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.error("incorrect number of arguments")

    if options.currencies is None or options.currencies == '':
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
        results = []
        response = requests.get('https://www.coingecko.com/en/coins/all')
        response.raise_for_status()
        matches = re.findall(r"<span class='coin-content-name'>([^<]+)</span>\s*<span\s+class='coin-content-symbol'>([^<]+)</span>", response.content)
        print("[")
        for mtch in matches:
            coinPath = mtch[0].lower().replace(' ','-').replace('.','-').replace('-[futures]','')

            if coinPath in coinPathMap:
                coinPath = coinPathMap[coinPath]

            keep_trying = True
            while keep_trying:
                keep_trying = False
                currencies_to_scrape = ast.literal_eval("[{'name':'"+coinPath+"','tags':['usd']}]")
                output = options.output
                valid_currencies = DataSchema(many=True).load(currencies_to_scrape)
                crypto_scraper = CryptoScraper(currencies_to_scrape=valid_currencies)
                try:
                    results = crypto_scraper.scrape()
                except requests.exceptions.HTTPError as ex:
                    if '-' in coinPath: # Sometimes CoinGecko just deletes a ' ' or a '-'.
                        coinPath = coinPath.replace('-','')
                        keep_trying = True
                    else:
                        print(str(ex), file=sys.stderr)

            print(json.dumps(results) + ",")

        print("]")
    else:
        currencies_to_scrape = ast.literal_eval(options.currencies)
        output = options.output
        # validate currency data
        valid_currencies = DataSchema(many=True).load(currencies_to_scrape)
        # scraping the currencies
        scrape()
