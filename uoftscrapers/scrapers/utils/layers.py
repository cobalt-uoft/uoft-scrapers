import requests
import json
from . import Scraper


class LayersScraper:
    """A superclass for scraping Layers of the UofT Map.

    Map is located at http://map.utoronto.ca
    """

    host = 'http://map.utoronto.ca/'

    @staticmethod
    def get_layers_json(campus):
        """Retrieve the JSON structure from host."""

        Scraper.logger.info('Retrieving map layers for %s.' % campus.upper())

        headers = {'Referer': LayersScraper.host}
        data = Scraper.get('%s%s%s' % (
            LayersScraper.host,
            'data/map/',
            campus
        ), headers=headers, json=True)

        return data['layers']

    @staticmethod
    def get_value(entry, val, number=False):
        """Retrieve the desired value from the parsed response dictionary."""

        if val in entry.keys():
            return entry[val]
        else:
            return 0 if number else ''
