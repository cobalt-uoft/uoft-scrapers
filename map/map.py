import requests, http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import re
import json
import pymongo
import pprint
import tidylib

class Map:

    def __init__(self):
        self.host = 'http://map.utoronto.ca/'
        self.s = requests.Session()

    def update_buildings(self, campus):
        # have to send info to database, after formatting it
        pass

    def get_map_json(self, campus):
        self.s.get(self.host)

        headers = {
            'Referer': self.host
        }

        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus), headers=headers).text

        data = json.loads(html)

        return data

map = Map()
