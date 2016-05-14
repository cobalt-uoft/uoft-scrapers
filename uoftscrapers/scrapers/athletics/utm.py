from ..utils import Scraper
from .athletics_helpers import *
from bs4 import BeautifulSoup
from datetime import datetime
from collections import OrderedDict
import json
import requests


class UTMAthletics:
    """A scraper for the UTM athletics schedule.

    The schedule is located at http://www.utm.utoronto.ca/athletics/schedule
    """

    host = 'http://www.utm.utoronto.ca/athletics/schedule/month/'

    @staticmethod
    def scrape(location='.', month=None, save=True):
        """Update the local JSON files for this scraper."""
        month = month or get_current_month()

        Scraper.logger.info('UTMAthletics initialized.')
        html = Scraper.get('%s%s' % (UTMAthletics.host, month))
        soup = BeautifulSoup(html, 'html.parser')

        athletics = OrderedDict()

        calendar = soup.find('div', class_='month-view')
        for tr in calendar.find_all('tr', class_='single-day'):
            for td in tr.find_all('td'):
                date = td.get('data-date')
                id_ = get_campus_id(date, 'M')

                if not is_date_in_month(date, month):
                    continue

                events = []

                for item in td.find(class_='inner').find_all(class_='item'):

                    # event cancelled or athletic center closed
                    if item.find(class_='cancelled-item'):
                        continue

                    if item.find(class_='athletics-calendar-note'):
                        continue

                    title = item.find(class_='athletics-calendar-title').text
                    location_ = item.find(class_='athletics-calendar-location').text

                    start = convert_time(item.find(class_='date-display-start').get('content'))
                    end = convert_time(item.find(class_='date-display-end').get('content'))

                    duration = end - start

                    events.append(OrderedDict([
                        ('title', title),
                        ('campus', 'UTM'),
                        ('location', location_),
                        ('building_id', '332'),
                        ('start_time', start),
                        ('end_time', end),
                        ('duration', duration)
                    ]))

                athletics[date] = OrderedDict([
                    ('date', date),
                    ('events', events)
                ])

        if save:
            for id_, doc in athletics.items():
                Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTMAthletics completed.')
        return athletics if not save else None
