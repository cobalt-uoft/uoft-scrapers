from ..scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime
from collections import OrderedDict
import json
import requests
import pytz

from pprint import pprint


class UTMAthletics:
    """A scraper for the UTM athletics schedule.

    The schedule is located at https://m.utm.utoronto.ca/physed.php.
    """

    host = 'https://m.utm.utoronto.ca/physed.php'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTMAthletics initialized.')
        headers = {
            'Referer': UTMAthletics.host
        }
        html = UTMAthletics.s.get('%s' % UTMAthletics.host,
                                  headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        athletics = OrderedDict()

        date = None

        div = soup.find('div', id='all')
        for child in div.children:

            if child.name == 'br':
                continue

            if child.name == 'h2':
                date = UTMAthletics.parse_date(child.text)

                if date not in athletics:
                    athletics[date] = OrderedDict([
                        ('date', date),
                        ('activities', [])
                    ])

                continue

            if 'title' in child.get('class'):
                title = child.find('b').text
                location_ = child.find('span').text

                athletics[date]['activities'].append(OrderedDict([
                    ('title', title),
                    ('location', location_)
                ]))

            elif 'info' in child.get('class'):
                start, end = UTMAthletics.parse_time(child.text, date)
                athletics[date]['activities'][-1].update([
                    ('start_time', start),
                    ('end_time', end)
                ])

        if athletics:
            Scraper.ensure_location(location)

        for date, doc in athletics.items():
            with open('%s/%s.json' % (location, date), 'w+') as outfile:
                json.dump(doc, outfile)

        Scraper.logger.info('UTMAthletics completed.')

    @staticmethod
    def parse_date(d):
        month, date_, year = [x.strip() for x in d.split(' ')]
        return datetime.strptime('%s %s %s' % (date_.zfill(2), month, year),
                                 '%d %B %Y').date().isoformat()

    @staticmethod
    def parse_time(time_range, d):

        def convert_time(time):
            t, p = time.split(' ')
            h, m = t.split(':')
            date = datetime.strptime('%s %s %s %s' % (d, h, m, p),
                                     '%Y-%m-%d %I %M %p')
            return date.replace(tzinfo=pytz.timezone('US/Eastern')).isoformat()

        start, end = [x.strip() for x in time_range.split(' - ')]
        return convert_time(start), convert_time(end)
