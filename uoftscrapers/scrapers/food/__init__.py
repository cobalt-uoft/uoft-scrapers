from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..layers import LayersScraper


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

                if not image == '':
                    image = "%s%s" % (self.host[:-1], image)

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
            """Convert and return time of the form HH:MM a.m./p.m. to
            decimal format."""

            time, period = t[:-4].strip(), t[-4:].strip()

            # for mistyped times, e.g. http://map.utoronto.ca/json/hours/1329
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

        if not soup.find('tbody').text == '':
            hours = OrderedDict()

            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday']

            timings = soup.find('tbody').find_all('td')

            for i in range(len(timings)):
                opening = closing = 0
                day, timing = days[i], timings[i].text

                if 'closed' not in timing:
                    # timing is provided as HH:MM p.d. -HH:MM p.d.
                    timing = timing.split(' -')
                    opening, closing = (conv_time(timing[0]),
                                        conv_time(timing[1]))
                hours.update(
                    {day: OrderedDict([('open', opening), ('close', closing)])})
            return hours
        else:
            return ''  # hours unavailable
