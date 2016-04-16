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

        for day in range(days):
            html = UTMShuttle.get_schedule_html(UTMShuttle.host % (year, month, day + 1))
            schedule = UTMShuttle.parse_schedule_html(html)

            with open('%s/%s.json' % (
                location,
                '%s-%s-%s' % (year, month, '{0:02d}'.format(day + 1))
            ),'w+') as outfile:
                json.dump(schedule, outfile)

        Scraper.logger.info('UTMShuttle completed.')

    @staticmethod
    def get_schedule_html(url):
        """Update the locally stored schedule pages."""

        html = None
        while html is None:
            try:
                r = UTMShuttle.s.get(url)
                if r.status_code == 200:
                    html = r.text
            except (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError):
                continue

        return html.encode('utf-8')

    @staticmethod
    def parse_schedule_html(html):
        """Create JSON object from the HTML page download."""

        soup = BeautifulSoup(html, 'html.parser')

        # Get date
        html_date = time.strptime(soup.find('h2').get_text().strip(), '%b %d %Y')
        date = time.strftime('%Y-%m-%d', html_date)

        # Get route data
        routes = {}
        html_route_opts = soup.find(id='chooseRoute')
        if html_route_opts:
            for html_route_opt in html_route_opts.find_all('option'):
                html_route_id = html_route_opt.get('value')
                html_route_times = soup.find(id=html_route_id).find_all('li')

                route_name = html_route_opt.get_text().strip().split(' @ ')

                times = []
                for html_time in html_route_times:
                    html_time_text = html_time.get_text().strip().lower()

                    time_rush_hour = 'rush hour' in html_time_text
                    time_no_overload = 'no overload' in html_time_text

                    html_time_clean = re.sub('\*.*\*', '', html_time_text).strip()

                    times.append(OrderedDict([
                        ('time', '%sT%s:00-04:00' % (
                            date,
                            time.strftime('%H:%M %p', time.strptime(html_time_clean, '%I:%M %p'))[:-3]
                        )),
                        ('rush_hour', time_rush_hour),
                        ('no_overload', time_no_overload)
                    ]))

                route_id = re.sub('\.|ROUTE| ', '', route_name[0].upper())

                # TODO: fetch this dynamically
                route_building_id = UTMShuttle.building_ids[route_name[1]] if route_name[1] in UTMShuttle.building_ids else ''

                route_stops = OrderedDict([
                    ('location', route_name[1]),
                    ('building_id', route_building_id),
                    ('times', times)
                ])

                if route_id in routes.keys():
                    routes[route_id]['stops'].append(route_stops)
                else:
                    routes[route_id] = OrderedDict([
                        ('id', route_id),
                        ('name', route_name[0]),
                        ('stops', [route_stops])
                    ])

        return OrderedDict([
            ('date', date),
            ('routes', [v for k, v in routes.items()])
        ])
