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

    def update_files(self):
        #remove mongo(self) and add this method that just makes the dict and
        #saves it as JSON
        pass

    def mongo(self):
        # have to send info to database, after formatting it
        for campus in self.campuses:
            data = self.get_map_json(campus)
            #get food places from data object

    def get_value(self, building, val, number=False):
        if val in building.keys():
            return building[val]
        else:
            return 0 if number else ''

    def get_map_json(self, campus):
        self.s.get(self.host)

        headers = {
            'Referer': self.host
        }

        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus), headers=headers).text

        data = json.loads(html)

        return data
