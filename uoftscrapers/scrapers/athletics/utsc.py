from ..utils import Scraper
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
    s = requests.Session()

    @staticmethod
    def scrape(location='.', month=None):
        """Update the local JSON files for this scraper."""
        month = month or UTSCAthletics.get_month(month)

        Scraper.logger.info('UTSCAthletics initialized.')
        headers = {
            'Referer': UTSCAthletics.host
        }
        html = UTSCAthletics.s.get('%s%s' % (UTSCAthletics.host, month),
                                   headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        athletics = OrderedDict()

        for tr in soup.find('div', class_='month-view').find_all('tr', class_='single-day'):
            for td in tr.find_all('td'):
                date = td.get('data-date')

                if not UTSCAthletics.date_in_month(date, month):
                    continue

                events = []
                for item in td.find(class_='inner').find_all(class_='item'):
                    title = item.find(class_='views-field-title').text.strip()

                    location_ = item.find(class_='views-field-field-location]')

                    if location_.text.strip() == '':
                        location_ = list(location_.next_siblings)[1]

                    location_ = location_.text.strip()

                    start = item.find(class_='date-display-start').get('content')
                    end = item.find(class_='date-display-end').get('content')

                    events.append(OrderedDict([
                        ('title', title),
                        ('location', location_),
                        ('building_id', '208'),
                        ('start_time', start),
                        ('end_time', end)
                    ]))

                athletics[date] = OrderedDict([
                    ('date', date),
                    ('events', events)
                ])

        for date, doc in athletics.items():
            Scraper.save_json(doc, location, date)

        Scraper.logger.info('UTSCAthletics completed.')

    @staticmethod
    def get_month(m):
        now = datetime.now()
        return '%s-%s' % (now.year, now.month)

    @staticmethod
    def date_in_month(d, m):
        d = datetime.strptime(d, '%Y-%m-%d')
        m = datetime.strptime(m, '%Y-%m')

        return d.month == m.month
