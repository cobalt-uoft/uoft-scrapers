import requests, http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import os
import re
import json
import pprint
import tidylib

class Map:

    def __init__(self):
        self.host = 'http://map.utoronto.ca/'
        self.s = requests.Session()
        self.campuses = ['utsg', 'utm', 'utsc']

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists('json'):
            os.makedirs('json')

    def update_files(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        for campus in self.campuses:
            data = self.get_map_json(campus)
            #get food data

    def get_map_json(self, campus):
        self.s.get(self.host)

        headers = {
            'Referer': self.host
        }

        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus), headers=headers).text

        data = json.loads(html)

        return data
