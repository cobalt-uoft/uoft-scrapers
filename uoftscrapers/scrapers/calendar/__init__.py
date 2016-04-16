from ..utils import Scraper
from .utm import UTMCalendar
from .utsc import UTSCCalendar
from .utsg import UTSGCalendar
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests


class Calendar:

    host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Calendar initialized.')
        UTSGCalendar.scrape(location)
        UTMCalendar.scrape(location)
        UTSCCalendar.scrape(location)
        Scraper.logger.info('Calendar completed.')
