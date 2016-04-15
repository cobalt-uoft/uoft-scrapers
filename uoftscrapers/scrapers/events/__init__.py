from ...scraper import Scraper
from datetime import datetime, date
from collections import OrderedDict
from bs4 import BeautifulSoup
import pytz

import json
import requests

class UTEvents:
    """A scraper for Events at the University of Toronto."""

    host = 'https://www.events.utoronto.ca/'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTEvents initialized.')
        Scraper.logger.info('Not implemented.')
        raise NotImplementedError('This scraper has not been implemented yet.')
        Scraper.logger.info('UTEvents completed.')
