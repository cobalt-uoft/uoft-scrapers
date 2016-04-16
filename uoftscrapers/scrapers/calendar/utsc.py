from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests


class UTSCCalendar:

    host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSCCalendar initialized.')
        Scraper.logger.info('Not implemented.')
        Scraper.logger.info('UTSCCalendar completed.')
