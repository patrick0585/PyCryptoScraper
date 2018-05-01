#!/usr/bin/python
# coding: utf-8
from __future__ import absolute_import, unicode_literals

from scraper.CryptoScraper import CryptoScraper
from schema.DataSchema import DataSchema
import optparse
import ast
import json

def scrape():
    crypto_scraper = CryptoScraper(currencies_to_scrape=valid_currencies)

    results = crypto_scraper.scrape()

    print json.dumps(results)

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog [options] arg1")
    parser.add_option("-c", "--currencies", dest="currencies", type = "str", help = "specify currencies to scrape")
    parser.add_option("-o", "--output", dest="output", type="str", default="json", help="specify output format")

    (options, args) = parser.parse_args()

    if len(args) != 0:
        parser.error("incorrect number of arguments")

    currencies_to_scrape = ast.literal_eval(options.currencies)
    output = options.output

    # validate currency data
    valid_currencies = DataSchema(many=True).load(currencies_to_scrape)

    # scraping the currencies
    scrape()
