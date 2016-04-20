from ..utils import Scraper, LayersScraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from decimal import *
import os
import re


class Buildings:
    """A scraper for UofT's buildings.

    UofT Map is located at http://map.utoronto.ca/.
    """

    host = 'http://map.utoronto.ca/'
    campuses = ['utsg', 'utm', 'utsc']

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('Buildings initialized.')

        for campus in Buildings.campuses:
            data = Buildings.get_map_json(campus)
            regions = Buildings.get_regions_json(campus)['buildings']

            for building in data['buildings']:
                _id = building['id']
                code = building['code']
                name = building['title']
                short_name = LayersScraper.get_value(building, 'short_name')
                lat = LayersScraper.get_value(building, 'lat', True)
                lng = LayersScraper.get_value(building, 'lng', True)

                street = ' '.join(filter(None,
                                         LayersScraper.get_value(building, 'street').split(' ')))
                city = LayersScraper.get_value(building, 'city')
                province = LayersScraper.get_value(building, 'province')
                country = LayersScraper.get_value(building, 'country')
                postal = LayersScraper.get_value(building, 'postal')

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

                Scraper.save_json(doc, location, _id)

        Scraper.logger.info('Buildings completed.')

    @staticmethod
    def get_map_json(campus):
        """Retrieve the JSON structure from host."""

        Scraper.logger.info('Scraping %s.' % campus.upper())

        Scraper.get(Buildings.host)

        headers = {'Referer': Buildings.host}
        data = Scraper.get('%s%s%s' % (
            Buildings.host,
            'data/map/',
            campus
        ), headers=headers, json=True)

        return data

    @staticmethod
    def get_regions_json(campus):
        """Retrieve the JSON structure from host."""

        Scraper.get(Buildings.host)

        headers = {'Referer': Buildings.host}
        data = Scraper.get('%s%s%s' % (
            Buildings.host,
            'data/regions/',
            campus
        ), headers=headers, json=True)

        return data
