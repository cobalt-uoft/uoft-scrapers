from ..utils import Scraper
from .athletics_helpers import *
from bs4 import BeautifulSoup
from datetime import datetime
from collections import OrderedDict
import json
import requests


class UTSCAthletics:
    """A scraper for the UTSC athletics schedule.

    The schedule is located at http://www.utsc.utoronto.ca/athletics
    """

    host = 'http://www.utsc.utoronto.ca/athletics/calendar-node-field-date-time/month/'

    @staticmethod
    def scrape(location='.', month=None, save=True):
        """Update the local JSON files for this scraper."""
        month = month or get_current_month()

        Scraper.logger.info('UTSCAthletics initialized.')
        html = Scraper.get('%s%s' % (UTSCAthletics.host, month))
        soup = BeautifulSoup(html, 'html.parser')

        athletics = OrderedDict()

        calendar = soup.find('div', class_='month-view')
        for tr in calendar.find_all('tr', class_='single-day'):
            for td in tr.find_all('td'):
                date = td.get('data-date')
                id_ = get_campus_id(date, 'SC')

                if not is_date_in_month(date, month):
                    continue

                events = []

                for item in td.find(class_='inner').find_all(class_='item'):
                    title = item.find(class_='views-field-title').text.strip()

                    location_ = item.find(class_='views-field-field-location]')

                    if location_.text.strip() == '':
                        location_ = list(location_.next_siblings)[1]

                    location_ = location_.text.strip()

                    start = convert_time(item.find(class_='date-display-start').get('content'))
                    end = convert_time(item.find(class_='date-display-end').get('content'))

                    duration = end - start

                    events.append(OrderedDict([
                        ('title', title.replace('/ ', '/')),
                        ('campus', 'UTSC'),
                        ('location', location_),
                        ('building_id', '208'),
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

        Scraper.logger.info('UTSCAthletics completed.')

        return athletics if not save else None
