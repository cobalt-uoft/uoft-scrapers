from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import requests
from ...scraper.layers import LayersScraper
from ...scraper import Scraper
from pprint import pprint

class UTSGParking:
    """A scraper for UTSG parking lots / bicycle racks.

    UTSG parking data is located at http://map.utoronto.ca
    """

    host = 'http://map.utoronto.ca/'
    lot_index = 4
    rack_index = 1
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTSGParking initialized.')
        Scraper.ensure_location(location)

        data = LayersScraper.get_layers_json('utsg')

        for entry in data['markers'][UTSGParking.lot_index]:
            _id = str(entry['id'])
            building_id = LayersScraper.get_value(entry, 'building_code')
            _type = 'vehicle'
            access = LayersScraper.get_value(entry, 'access')
            description = BeautifulSoup(
                LayersScraper.get_value(entry, 'desc').strip(),
                'html.parser').text
            lat = LayersScraper.get_value(entry, 'lat', True)
            lng = LayersScraper.get_value(entry, 'lng', True)
            address = LayersScraper.get_value(entry, 'address')

            doc = OrderedDict([
                ('id', _id),
                ('building_id', building_id),
                ('type', _type),
                ('description', description),
                ('lat', lat),
                ('lng', lng),
                ('address', address)
            ])

        Scraper.logger.info('UTSGParking completed.')
