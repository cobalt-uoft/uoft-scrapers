from ...scraper import Scraper
from bs4 import BeautifulSoup
from calendar import monthrange
from collections import OrderedDict
import datetime
import json
import logging
import os
import re
import requests
import sys
import time

class UTMShuttle:
    """A scraper for the UTM shuttle bus schedule.

    The schedule is located at https://m.utm.utoronto.ca/shuttle.php.
    """

    host = 'https://m.utm.utoronto.ca/shuttleByDate.php?year=%s&month=%s&day=%s'
    logger = logging.getLogger('uoftscrapers')
    s = requests.Session()

    building_ids = {
        'Instructional Centre Layby': '334',
        'Hart House': '002',
        'Deerfield Hall North Layby': '340'
    }

    @staticmethod
    def scrape(location='.', month=None):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTMShuttle initialized.')
        Scraper.ensure_location(location)

        now = datetime.datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m') if month is None else str(month).zfill(2)
        days = monthrange(int(year), int(month))[1]

        Scraper.logger.info('Fetching schedules for %s-%s.' % (year, month))

        for day in range(1, days + 1):
            html = Scraper.get_html(UTMShuttle.s, UTMShuttle.host % (year, month, day))
            schedule = UTMShuttle.parse_schedule_html(html)

            with open('%s/%s.json' % (
                location,
                '%s-%s-%s' % (year, month, '{0:02d}'.format(day))
            ),'w+') as outfile:
                json.dump(schedule, outfile)

        Scraper.logger.info('UTMShuttle completed.')

    @staticmethod
    def parse_schedule_html(html):
        """Create JSON object from the HTML page."""

        soup = BeautifulSoup(html, 'html.parser')

        # Get date
        date = time.strftime('%Y-%m-%d', time.strptime(soup.find('h2').get_text().strip(), '%b %d %Y'))

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
                    _route_time_clean = re.sub('\*.*\*', '', _route_time_text).strip()

                    time_rush_hour = 'rush hour' in _route_time_text
                    time_no_overload = 'no overload' in _route_time_text

                    times.append(OrderedDict([
                        ('time', '%sT%s:00-04:00' % (
                            date,
                            time.strftime('%H:%M %p', time.strptime(_route_time_clean, '%I:%M %p'))[:-3]
                        )),
                        ('rush_hour', time_rush_hour),
                        ('no_overload', time_no_overload)
                    ]))

                # TODO: fetch this dynamically
                route_building_id = UTMShuttle.building_ids[route_location] if route_location in UTMShuttle.building_ids else ''

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
