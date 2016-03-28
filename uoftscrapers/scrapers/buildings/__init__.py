import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import os
import re
import json
from decimal import *
from ..scraper import Scraper


class Buildings(Scraper):
    """A scraper for UofT's buildings.

    UofT Map is located at http://map.utoronto.ca/.
    """

    def __init__(self, output_location='.'):
        super().__init__('Buildings', output_location)

        self.host = 'http://map.utoronto.ca/'
        self.campuses = ['utsg', 'utm', 'utsc']
        self.s = requests.Session()

    def run(self):
        """Update the local JSON files for this scraper."""

        for campus in self.campuses:
            data = self.get_map_json(campus)
            regions = self.get_regions_json(campus)['buildings']

            for building in data['buildings']:
                _id = building['id']
                code = building['code']
                name = building['title']
                short_name = self.get_value(building, 'short_name')
                lat = self.get_value(building, 'lat', True)
                lng = self.get_value(building, 'lng', True)

                street = ' '.join(filter(
                    None, self.get_value(building, 'street').split(' ')))
                city = self.get_value(building, 'city')
                province = self.get_value(building, 'province')
                country = self.get_value(building, 'country')
                postal = self.get_value(building, 'postal')

                polygon = []
                for region in regions:
                    if region['id'] == _id:
                        lat_lng = region['center_point']
                        if lat_lng:
                            lat_lng = lat_lng[1:-2].split(', ')
                            if len(lat_lng) == 2:
                                lat = float(lat_lng[0])
                                lng = float(lat_lng[1])
                            polygon = region['points']

                doc = OrderedDict([
                    ('id', _id),
                    ('code', code),
                    ('name', name),
                    ('short_name', short_name),
                    ('campus', campus.upper()),
                    ('address', OrderedDict([
                        ('street', street),
                        ('city', city),
                        ('province', province),
                        ('country', country),
                        ('postal', postal)
                    ])),
                    ('lat', lat),
                    ('lng', lng),
                    ('polygon', polygon)
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

    def get_regions_json(self, campus):
        """Retrieve the JSON structure from host."""

        self.s.get(self.host)
        headers = {
            'Referer': self.host
        }
        html = self.s.get('%s%s%s' % (self.host, 'data/regions/', campus),
                          headers=headers).text
        data = json.loads(html)
        return data

    def get_value(self, building, val, number=False):
        """Retrieve the desired value from the parsed response dictionary."""

        if val in building.keys():
            return building[val]
        else:
            return 0 if number else ''
