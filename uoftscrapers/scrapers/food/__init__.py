import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper


class Food(Scraper):
    """A scraper for UofT restaurants.

    UofT Food data is located at http://map.utoronto.ca
    """

    def __init__(self, output_location='.'):
        super().__init__('Food', output_location)

        self.host = 'http://map.utoronto.ca/'
        self.campuses = [('utsg', 2), ('utm', 1), ('utsc', 0)]
        self.s = requests.Session()

    def run(self):
        for campus, food_index in self.campuses:
            data = self.get_map_json(campus)['layers'][food_index]

            for entry in data['markers']:
                id_ = str(entry['id'])
                name = entry['title']

                building_id = self.get_value(entry, 'building_code')
                address = self.get_value(entry, 'address')
                hours = self.get_hours(id_)
                short_name = self.get_value(entry, 'slug')
                desc = self.get_value(entry, 'desc').strip()
                tags = self.get_value(entry, 'tags').split(', ')
                image = self.get_value(entry, 'image')
                lat = self.get_value(entry, 'lat', True)
                lng = self.get_value(entry, 'lng', True)
                url = self.get_value(entry, 'url')

                doc = OrderedDict([
                    ('id', id_),
                    ('building_id', building_id),
                    ('name', name),
                    ('short_name', short_name),
                    ('description', desc),
                    ('url', url),
                    ('tags', tags),
                    ('image', image),
                    ('campus', campus.upper()),
                    ('lat', lat),
                    ('lng', lng),
                    ('address', address),
                    ('hours', hours)
                ])

                with open('%s/%s.json' % (self.location, id_), 'w') as fp:
                    json.dump(doc, fp)

        self.logger.info('%s completed.' % self.name)

    def get_map_json(self, campus):
        """Retrieve the JSON structure from host."""

        self.logger.info('Scraping %s.' % campus)

        headers = {
            'Referer': self.host
        }
        html = self.s.get('%s%s%s' % (self.host, 'data/map/', campus),
                          headers=headers).text
        data = json.loads(html)
        return data

    def get_hours(self, food_id):
        """Parse and return the restaurant's opening and closing times."""

        headers = {
            'Referer': self.host
        }
        html = self.s.get('%s%s%s' % (self.host, 'json/hours/', food_id),
                          headers=headers).text

        soup = BeautifulSoup(html, 'html.parser')

        if not soup.find('tbody').text == '':
            hours = OrderedDict()

            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday']

            timings = soup.find('tbody').find_all('td')

            for i in range(len(timings)):
                closed, opening, closing = False, '', ''
                day, timing = days[i], timings[i].text

                # when closed for the full day, timing will not have a '-'
                if '-' in timing:
                    opening, closing = timing.split(' -')
                else:
                    closed = True

                hours.update({day: OrderedDict([
                    ('closed', closed),
                    ('open', opening),
                    ('close', closing)])})

            return hours
        else:
            return ''  # hours unavailable

    def get_value(self, entry, val, number=False):
        """Retrieve the desired value from the parsed response dictionary."""

        if val in entry.keys():
            return entry[val]
        else:
            return 0 if number else ''
