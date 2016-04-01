import requests
import json
from ..scraper import Scraper


class LayersScraper(Scraper):
    """A superclass for scraping Layers of the UofT Map.

    Map is located at http://map.utoronto.ca
    """

    def __init__(self, name, output_location='.'):
        super().__init__(name, output_location)

        self.host = 'http://map.utoronto.ca/'
        self.s = requests.Session()

    def get_layers_json(self, campus):
        """Retrieve the JSON structure from host."""

        self.logger.info('Scraping map layers %s.' % campus)

        headers = {
            'Referer': self.host
        }
        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus),
                          headers=headers).text
        data = json.loads(html)
        return data['layers']

    @staticmethod
    def get_value(entry, val, number=False):
        """Retrieve the desired value from the parsed response dictionary."""

        if val in entry.keys():
            return entry[val]
        else:
            return 0 if number else ''
