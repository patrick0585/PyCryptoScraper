# coding: utf-8

from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod


class CryptScraperBase(object):
    """
        Base class for the crypto-scraper
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def _extract(self, *args, **kwargs):
        """ extracting data"""

    @abstractmethod
    def _transform(self, *args, **kwargs):
        """ transform data"""
