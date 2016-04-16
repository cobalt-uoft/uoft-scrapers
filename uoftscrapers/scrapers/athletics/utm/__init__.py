from ...scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime
from collections import OrderedDict
import json
import requests

from pprint import pprint


class UTMAthletics:
    """A scraper for the UTM athletics schedule.

    The schedule is located at http://www.utm.utoronto.ca/athletics/schedule
    """

    host = 'http://www.utm.utoronto.ca/athletics/schedule/month/'
    s = requests.Session()

    @staticmethod
    def scrape(location='.', month=None):
        """Update the local JSON files for this scraper."""
        month = month or UTMAthletics.get_month(month)

        Scraper.logger.info('UTMAthletics initialized.')
        headers = {
            'Referer': UTMAthletics.host
        }
        html = UTMAthletics.s.get('%s%s' % (UTMAthletics.host, month),
                                  headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        athletics = OrderedDict()

        for tr in soup.find('div', class_='month-view').find_all('tr', class_='single-day'):
            for td in tr.find_all('td'):
                date = td.get('data-date')

                if not UTMAthletics.date_in_month(date, month):
                    continue

                events = []
                for item in td.find(class_='inner').find_all(class_='item'):

                    # event cancelled or athletic center closed
                    if item.find(class_='cancelled-item') or item.find(class_='athletics-calendar-note'):
                        continue

                    title = item.find(class_='athletics-calendar-title').text
                    location_ = item.find(class_='athletics-calendar-location').text
                    start = item.find(class_='date-display-start').get('content')
                    end = item.find(class_='date-display-end').get('content')

                    events.append(OrderedDict([
                        ('title', title),
                        ('location', location_),
                        ('start_time', start),
                        ('end_time', end)
                    ]))

                athletics[date] = OrderedDict([
                    ('date', date),
                    ('events', events)
                ])

        if athletics:
            Scraper.ensure_location(location)

        for date, doc in athletics.items():
            with open('%s/%s.json' % (location, date), 'w+') as outfile:
                json.dump(doc, outfile)

        Scraper.logger.info('UTMAthletics completed.')

    @staticmethod
    def get_month(m):
        now = datetime.now()
        return '%s-%s' % (now.year, now.month)

    @staticmethod
    def date_in_month(d, m):
        d = datetime.strptime(d, '%Y-%m-%d')
        m = datetime.strptime(m, '%Y-%m')

        return d.month == m.month
