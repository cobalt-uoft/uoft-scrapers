from ..utils import Scraper
from bs4 import BeautifulSoup
from calendar import monthrange
from collections import OrderedDict
import datetime
import re
import time


class Shuttles:
    """A scraper for UofT's shuttle bus schedule.

    The schedule is located at https://m.utm.utoronto.ca/Shuttles.php.
    """

    host = 'https://m.utm.utoronto.ca/shuttleByDate.php?year=%s&month=%s&day=%s'

    building_ids = {
        'Instructional Centre Layby': '334',
        'Hart House': '002',
        'Deerfield Hall North Layby': '340'
    }

    @staticmethod
    def scrape(location='.', month=None):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('Shuttle initialized.')

        now = datetime.datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m') if month is None else str(month).zfill(2)
        days = monthrange(int(year), int(month))[1]

        Scraper.logger.info(
            'Fetching schedules for {0}-{1}-01 to {0}-{1}-{2}.'.format(year, month, days))

        for day in range(1, days + 1):
            html = Scraper.get(Shuttles.host % (year, month, day))
            schedule = Shuttles.parse_schedule_html(html)

            Scraper.save_json(schedule, location, schedule['date'])

        Scraper.logger.info('Shuttle completed.')

    @staticmethod
    def parse_schedule_html(html):
        """Create JSON object from the HTML page."""

        soup = BeautifulSoup(html, 'html.parser')

        # Get date
        date = time.strftime(
            '%Y-%m-%d', time.strptime(soup.find('h2').get_text().strip(), '%b %d %Y'))

        # Get route data
        routes = {}
        _routes = soup.find(id='chooseRoute')
        if _routes:
            for _route in _routes.find_all('option'):
                _route_id = _route.get('value')
                _route_times = soup.find(id=_route_id).find_all('li')

                route_name, route_location = _route.get_text().strip().split(' @ ')
                route_id = re.sub('\.|ROUTE| ', '', route_name.upper())

                times = []
                for _route_time in _route_times:
                    _route_time_text = _route_time.get_text().strip().lower()
                    _route_time_clean = re.sub(
                        '\*.*\*', '', _route_time_text).strip()

                    time_rush_hour = 'rush hour' in _route_time_text
                    time_no_overload = 'no overload' in _route_time_text

                    military_time = time.strftime('%H:%M %p',
                        time.strptime(_route_time_clean, '%I:%M %p'))[:-3]
                    military_time = [int(x) for x in military_time.split(':')]

                    seconds = military_time[0] * 3600 + military_time[1] * 60

                    times.append(OrderedDict([
                        ('time', seconds),
                        ('rush_hour', time_rush_hour),
                        ('no_overload', time_no_overload)
                    ]))

                # TODO: fetch this dynamically
                route_building_id = Shuttles.building_ids[route_location] if route_location in Shuttles.building_ids else ''

                route_stops = OrderedDict([
                    ('location', route_location),
                    ('building_id', route_building_id),
                    ('times', times)
                ])

                if route_id in routes.keys():
                    routes[route_id]['stops'].append(route_stops)
                else:
                    routes[route_id] = OrderedDict([
                        ('id', route_id),
                        ('name', route_name),
                        ('stops', [route_stops])
                    ])

        return OrderedDict([
            ('date', date),
            ('routes', [v for k, v in routes.items()])
        ])
