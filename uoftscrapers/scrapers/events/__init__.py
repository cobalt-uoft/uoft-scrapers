from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
from ..scraper import Scraper
import requests
import pytz
import json


import urllib.parse as urlparse
from urllib.parse import urlencode

class UTEvents:
    """A scraper for Events at the University of Toronto."""

    host = 'https://www.events.utoronto.ca/'

    campuses = [
    	{"id" : 1, "name" : "St. George", "tag" : "utsg"},
     	{"id" : 2, "name" : "U of T Mississauga", "tag" : "utm"},
     	{"id" : 3, "name" : "U of T Scarborough", "tag" : "utsc"}, 
     	{"id" : 0, "name" : "Off Campus", "tag" : "off"},
     	]

    s = requests.Session()

    @staticmethod
    def scrape(location='.'):

        Scraper.logger.info('UTEvents initialized.')
        return UTEvents.get_events_links()
        Scraper.logger.info('UTEvents completed.')

    @staticmethod
    def get_events_links():
        page_index_url = UTEvents.host + "index.php"
        url_parts = list(urlparse.urlparse(page_index_url))
        events_links = []
        paging_index = 1
        events_count = 10 
        while(events_count == 10):
            params = {
                    'p': paging_index
                }
            url_parts[4] = urlencode(params)
            paging_index += 1
            html = UTEvents.s.get(urlparse.urlunparse(url_parts)).text
            soup = BeautifulSoup(html, 'html.parser')
            events_dom_arr = soup.select('#results')[0].find_all('li')
            events_count = len(events_dom_arr)
            events_links += list(map(lambda e: e.a['href'], events_dom_arr))
        return(events_links)                


