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
        self.campuses = ['utsg', 'utm', 'utsc']
        self.s = requests.Session()

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
            return ''
