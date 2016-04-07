from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper.layers import LayersScraper


class Food(LayersScraper):
    """A scraper for UofT restaurants.

    UofT Food data is located at http://map.utoronto.ca
    """

    def __init__(self, output_location='.'):
        super().__init__('Food', output_location)

        self.campuses = [('utsg', 2), ('utm', 1), ('utsc', 0)]

    def run(self):
        for campus, food_index in self.campuses:
            data = self.get_layers_json(campus)[food_index]

            for entry in data['markers']:
                id_ = str(entry['id']).zfill(4)
                name = entry['title']

                building_id = self.get_value(entry, 'building_code')

                address = ' '.join(
                    filter(None, self.get_value(entry, 'address').split()))

                hours = self.get_hours(id_)
                short_name = self.get_value(entry, 'slug')

                desc = BeautifulSoup(self.get_value(entry, 'desc').strip(),
                                     'html.parser').text

                tags = list(filter(
                    None, self.get_value(entry, 'tags').lower().split(', ')))
                image = self.get_value(entry, 'image')
                lat = self.get_value(entry, 'lat', True)
                lng = self.get_value(entry, 'lng', True)
                url = self.get_value(entry, 'url')

                if not image == '':
                    image = '%s%s' % (self.host[:-1], image)

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

    def get_hours(self, food_id):
        """Parse and return the restaurant's opening and closing times."""

        def conv_time(t):
            """Convert time of form "HH:MM p.d." to decimal (p.d. is one
            of a.m./p.m.)"""

            time, period = t[:-4].strip(), t[-4:].strip()

            # for mistyped times (i.e. http://map.utoronto.ca/json/hours/1329)
            if t[0] == ':':
                time = time[1:len(time)-2] + ':' + time[-2:]

            m = 0
            if ':' in time:
                h, m = [int(x) for x in time.split(':')]
            else:
                h = int(time)

            h += 12 if period == 'p.m.' else 0
            return h + (m / 60)

        headers = {
            'Referer': self.host
        }
        html = self.s.get('%s%s%s' % (self.host, 'json/hours/', food_id),
                          headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        hours = OrderedDict()

        if not soup.find('tbody').text == '':
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday']

            timings = soup.find('tbody').find_all('td')

            for i in range(len(timings)):
                is_closed = True
                open_ = close = 0
                day, timing = days[i], timings[i].text

                if 'closed' not in timing:
                    is_closed = False
                    # timing is of form "HH:MM p.d. -HH:MM p.d."
                    open_, close = [conv_time(t) for t in timing.split(' -')]

                hours.update({day: OrderedDict([('closed', is_closed),
                                                ('open', open_),
                                                ('close', close)])})
        return hours
