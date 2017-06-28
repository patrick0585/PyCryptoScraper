# coding: utf-8

from __future__ import absolute_import, unicode_literals
import unittest
from scraper.CryptoScraper import CryptoScraper


class CryptoScraperTest(unittest.TestCase):

    def setUp(self):
        self.cryptoscraper = CryptoScraper(currencies_to_scrape=[dict(name='bitcoin', tags=['usd', 'eur']),
                                                                 dict(name='ethereum', tags=['usd', 'eur'])])

    def test_instance(self):
        self.assertIsNotNone(self.cryptoscraper)

    def test_scrape_results(self):
        results = self.cryptoscraper.scrape()
        self.assertIsNot(0, len(results))

    def tearDown(self):
        del self.cryptoscraper
