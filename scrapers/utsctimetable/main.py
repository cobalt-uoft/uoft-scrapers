import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os

class UTSCTimetable(Scraper):

    def __init__(self):
        super().__init__('UTSC Timetable', os.path.dirname(os.path.abspath(__file__)))
        self.host = \
            'http://www.utsc.utoronto.ca/~registrar/scheduling/timetable'

    def update_files(self):
        print('Not implemented')
        print('%s completed.' % self.name)
