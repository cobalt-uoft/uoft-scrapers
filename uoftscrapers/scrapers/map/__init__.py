import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import os
import re
import json
from ..scraper import Scraper


class Map(Scraper):
    """A scraper for UofT's Map web service.

    UofT Map is located at http://map.utoronto.ca/.
    """

    def __init__(self, output_location='.'):
        super().__init__('Map', output_location)

        self.host = 'http://map.utoronto.ca/'
        self.campuses = ['utsg', 'utm', 'utsc']
        self.s = requests.Session()

    def run(self):
        """Update the local JSON files for this scraper."""

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

                with open('%s/%s.json' % (self.location, _id), 'w') as fp:
                    json.dump(doc, fp)

        self.logger.info('%s completed.' % self.name)

    def get_map_json(self, campus):
        """Retrieve the JSON structure from host."""

        self.logger.info('Scraping %s.' % campus)

        self.s.get(self.host)
        headers = {
            'Referer': self.host
        }
        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus),
                          headers=headers).text
        data = json.loads(html)
        return data

    def get_value(self, building, val, number=False):
        """Retrieve the desired value from the parsed response dictionary."""

        if val in building.keys():
            return building[val]
        else:
            return 0 if number else ''
