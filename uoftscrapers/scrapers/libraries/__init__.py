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

    campuses_tags = {
        'St. George': 'UTSG', 
        'U of T Mississauga': 'UTM', 
        'U of T Scarborough': 'UTSC'
        }

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Libraries initialized.')
        Scraper.ensure_location(location)
        library_data_links = Libraries.get_library_link()
        raise NotImplementedError('This scraper has not been implemented yet.')
        Scraper.logger.info('Libraries completed.')

    @staticmethod
    def get_library_link():
        html = Scraper.get(Libraries.host)
        soup = BeautifulSoup(html, 'html.parser')
        list_obj_arr = soup.select('.view-list-of-libraries')[1].select(
            '.view-content')[0].select('.views-row')
        library_links = [l.a['href'] for l in list_obj_arr]
        return library_links

    @staticmethod
    def get_library_doc(url_tail):
        pass
