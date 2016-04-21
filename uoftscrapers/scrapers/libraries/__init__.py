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
    	# ['content'] -> 'Teaser text', ['data]
    	library_data_links = Libraries.get_library_link()
    	raise NotImplementedError('This scraper has not been implemented yet.')
    	Scraper.logger.info('Libraries completed.')

    @staticmethod
    def get_library_link():
    	html = Scraper.get(Libraries.host)
    	soup = BeautifulSoup(html, 'html.parser')
    	content_links = []
    	library_info_links = []
    	list_obj_arr = soup.select('.view-list-of-libraries')[1].select(
			'.view-content')[0].select('.views-row')
    	content_links[:] = [l.select('a')[0]['href'] for l in list_obj_arr]
    	library_info_links = [l.select('a')[1]['href'] for l in list_obj_arr]
    	return {'content' : content_links , 'info': library_info_links}