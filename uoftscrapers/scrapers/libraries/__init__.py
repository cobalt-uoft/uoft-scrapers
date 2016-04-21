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
    	return Libraries.get_library_link()
    	# ['content_link'] -> 'Teaser Text'
    	# ['info_link'] -> 'Everything Else'
    	library_data_links = Libraries.get_library_link()
    	raise NotImplementedError('This scraper has not been implemented yet.')
    	Scraper.logger.info('Libraries completed.')

    @staticmethod
    def get_library_link():
    	html = Scraper.get(Libraries.host)
    	soup = BeautifulSoup(html, 'html.parser')
    	list_obj_arr = soup.select('.view-list-of-libraries')[1].select(
			'.view-content')[0].select('.views-row')
    	library_links = dict()
    	for l in list_obj_arr:
    		title = l.h2.text
    		library_links[title] = {
    			'content_link': l.select('a')[0]['href'],
    			'info_link': l.select('a')[1]['href']
    		}
    	return library_links