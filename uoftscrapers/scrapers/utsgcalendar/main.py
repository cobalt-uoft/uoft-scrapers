import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os

class UTSGCalendar(Scraper):

    def __init__(self):
        super().__init__('UTSG Calendar', os.path.dirname(os.path.abspath(__file__)))
        self.host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'

    def update_files(self):
        print('Not implemented', flush=True)
        print('%s completed.' % self.name, flush=True)
