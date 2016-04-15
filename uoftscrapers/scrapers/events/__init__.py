from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
from ..scraper import Scraper
import requests
import pytz
import json

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
        Scraper.logger.info('Not implemented.')
        raise NotImplementedError('This scraper has not been implemented yet.')
        Scraper.logger.info('UTEvents completed.')
