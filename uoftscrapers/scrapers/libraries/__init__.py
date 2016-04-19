from ..utils import Scraper
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime, date
from collections import OrderedDict
import urllib.parse as urlparse
from urllib.parse import urlencode
import re

class Libraries:
    """A scraper for the Libraries at the University of Toronto."""
    host = 'https://onesearch.library.utoronto.ca/visit'

    campuses_tags = {'St. George': 'UTSG', 'U of T Mississauga': 'UTM', 'U of T Scarborough': 'UTSC'}

    @staticmethod
    def scrape(location='.'):
    	Scraper.logger.info('Libraries initialized.')
    	Scraper.ensure_location(location)
    	raise NotImplementedError('This scraper has not been implemented yet.')
    	Scraper.logger.info('Libraries completed.')