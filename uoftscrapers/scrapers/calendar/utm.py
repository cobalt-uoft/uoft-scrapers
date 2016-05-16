from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests


class UTMCalendar:

    host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTMCalendar initialized.')
        Scraper.logger.info('Not implemented.')
        Scraper.logger.info('UTMCalendar completed.')
