import requests
import http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint
import tidylib


class Map:

    def __init__(self):
        self.host = 'http://map.utoronto.ca/'
        self.s = requests.Session()
        self.client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
        self.buildings = self.client['cobalt'].buildings
        self.campuses = ['utsg', 'utm', 'utsc']

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists('json'):
            os.makedirs('json')

    def update_files(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        for campus in self.campuses:
            data = self.get_map_json(campus)
            for building in data['buildings']:

                _id = building['id']
                code = building['code']
                name = building['title']
                short_name = self.get_value(building, 'short_name')
                lat = self.get_value(building, 'lat', True)
                lng = self.get_value(building, 'lng', True)

                street = self.get_value(building, 'street')
                city = self.get_value(building, 'city')
                province = self.get_value(building, 'province')
                country = self.get_value(building, 'country')
                postal = self.get_value(building, 'postal')

                doc = OrderedDict([
                    ('id', _id),
                    ('code', code),
                    ('name', name),
                    ('short_name', short_name),
                    ('campus', campus.upper()),
                    ('lat', lat),
                    ('lng', lng),
                    ('address', OrderedDict([
                        ('street', street),
                        ('city', city),
                        ('province', province),
                        ('country', country),
                        ('postal', postal)
                    ]))
                ])

                # TODO: send to a /json!

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

        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus),
                          headers=headers).text

        data = json.loads(html)

        return data
