import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os

class UTMTimetable(Scraper):

    def __init__(self):
        super().__init__('UTM Timetable', os.path.dirname(os.path.abspath(__file__)))
        self.host = 'https://student.utm.utoronto.ca/timetable/'

    def update_files(self):
        print('Not implemented')
        print('%s completed.' % self.name)
