from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import requests
from datetime import datetime, date
from ..scraper import Scraper


class Exams:
    """A scraper for UofT exams.

    Exam data is scraped from http://www.artsci.utoronto.ca/current/exams/
    """

    host = 'http://www.artsci.utoronto.ca/current/exams/'
    s = requests.Session()

    @staticmethod
    def scrape(year=None, location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('Exams initialized.')
        Scraper.ensure_location(location)

        all_exams = OrderedDict()

        for m in Exams.get_exam_months(year):

            exams = OrderedDict()

            Scraper.logger.info('Scraping %s exams.' % m.upper())

            headers = {
                'Referer': Exams.host
            }
            html = Exams.s.get('%s%s' % (Exams.host, m), headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.find('table', class_='vertical listing'):
                # no exam data available
                continue

            rows = soup.find('table', class_='vertical listing').find_all('tr')
            for row in rows[1:]:
                data = [x.text.strip() for x in row.find_all('td')]

                course, section, location_ = data[0], data[1], data[4]
                date_ = Exams.parse_date(data[2], m[-2:])
                start, end = Exams.parse_time(data[3])

                if course not in exams:
                    exams[course] = OrderedDict([
                        ('date', date_),
                        ('start_time', start),
                        ('end_time', end),
                        ('sections', [])
                    ])

                exams[course]['sections'].append(OrderedDict([
                    ('section', section),
                    ('location', location_)
                ]))

            all_exams[m] = exams

        for m in all_exams:
            with open('%s/%s.json' % (location, m.upper()), 'w+') as outfile:
                json.dump(all_exams[m], outfile)

        Scraper.logger.info('Exams completed.')

    @staticmethod
    def parse_date(date_, year):
        day, date_, month = date_.split(' ')
        return datetime.strptime('%s %s %s %s' % (day, date_, month, year),
                                 '%a %d %b %y').isoformat()

    @staticmethod
    def parse_time(time):

        def convert_time(t, is_pm=False):
            h, m = [int(x) for x in t.split(':')]
            h += 12 if is_pm else 0
            return h + (m / 60)

        period, start, _, end = time.split(' ')

        after_12 = period == 'PM' or period == 'EV'
        return convert_time(start, after_12), convert_time(end, after_12)

    @staticmethod
    def get_exam_months(year):
        if not year:
            year = date.today().year

        months = []
        for m in ('dec', 'apr', 'june', 'aug'):
            y = year if not m == 'dec' else int(year) - 1
            months.append('%s%s' % (m, str(y)[2:]))

        return months
