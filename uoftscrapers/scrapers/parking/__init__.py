from ..utils import Scraper, LayersScraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
import json


class Parking:
    """A scraper for parking lots / bicycle racks.

    Parking data is located at http://map.utoronto.ca
    """

    host = 'http://map.utoronto.ca/'
    indices = {
        'utsg': [4, 1],
        'utm': 6,
        'utsc': 5
    }

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('Parking initialized.')

        data = LayersScraper.get_layers_json('utsg')

        # UTSG car parking
        for entry in data[Parking.indices['utsg'][0]]['markers']:
            _id = str(entry['id']).zfill(4)
            title = LayersScraper.get_value(entry, 'title')
            building_id = LayersScraper.get_value(entry, 'building_code')
            _type = 'car'
            access = LayersScraper.get_value(entry, 'access')
            description = BeautifulSoup(
                LayersScraper.get_value(entry, 'desc').strip(),
                'html.parser').text
            lat = LayersScraper.get_value(entry, 'lat', True)
            lng = LayersScraper.get_value(entry, 'lng', True)
            address = LayersScraper.get_value(entry, 'address')

            doc = OrderedDict([
                ('id', _id),
                ('title', title),
                ('building_id', building_id),
                ('campus', 'UTSG'),
                ('type', _type),
                ('description', description),
                ('lat', lat),
                ('lng', lng),
                ('address', address)
            ])

            Scraper.save_json(doc, location, _id)

        # UTSG bicycle parking
        for entry in data[Parking.indices['utsg'][1]]['markers']:
            if 64 in entry['attribs']:
                # Ignore Bikeshare (third party)
                continue

            _id = str(entry['id']).zfill(4)
            title = LayersScraper.get_value(entry, 'title')
            building_id = LayersScraper.get_value(entry, 'building_code')
            _type = 'bicycle'
            access = LayersScraper.get_value(entry, 'access')
            description = BeautifulSoup(
                LayersScraper.get_value(entry, 'desc').strip(),
                'html.parser').text
            if len(description) > 0 and description[-1] == '.':
                description = description[:-1]

            lat = LayersScraper.get_value(entry, 'lat', True)
            lng = LayersScraper.get_value(entry, 'lng', True)
            address = LayersScraper.get_value(entry, 'address')

            doc = OrderedDict([
                ('id', _id),
                ('title', title),
                ('building_id', building_id),
                ('campus', 'UTSG'),
                ('type', _type),
                ('description', description),
                ('lat', lat),
                ('lng', lng),
                ('address', address)
            ])

            Scraper.save_json(doc, location, _id)

        # UTM / UTSC car parking
        for campus in ('utm', 'utsc'):
            data = LayersScraper.get_layers_json(campus)

            for entry in data[Parking.indices[campus]]['markers']:
                if 'parking' not in LayersScraper.get_value(entry, 'slug'):
                    continue

                _id = str(entry['id']).zfill(4)
                title = LayersScraper.get_value(entry, 'title')
                building_id = LayersScraper.get_value(entry, 'building_code')
                _type = 'car'
                description = BeautifulSoup(
                    LayersScraper.get_value(entry, 'desc').strip(),
                    'html.parser').text
                lat = LayersScraper.get_value(entry, 'lat', True)
                lng = LayersScraper.get_value(entry, 'lng', True)
                address = LayersScraper.get_value(entry, 'address')

                doc = OrderedDict([
                    ('id', _id),
                    ('title', title),
                    ('building_id', building_id),
                    ('campus', campus.upper()),
                    ('type', _type),
                    ('description', description),
                    ('lat', lat),
                    ('lng', lng),
                    ('address', address)
                ])

                with open('%s/%s.json' % (location, _id), 'w') as fp:
                    json.dump(doc, fp)

        Scraper.logger.info('Parking completed.')
