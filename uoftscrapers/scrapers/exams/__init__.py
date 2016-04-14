from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import requests
from datetime import datetime, date
from ..scraper import Scraper
import pytz


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

        exams = OrderedDict()

        for p in Exams.get_exam_periods(year):

            Scraper.logger.info('Scraping %s exams.' % p.upper())

            headers = {
                'Referer': Exams.host
            }
            html = Exams.s.get('%s%s' % (Exams.host, p), headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.find('table', class_='vertical listing'):
                # no exam data available
                Scraper.logger.info('No exams for %s.' % p.upper())
                continue

            rows = soup.find('table', class_='vertical listing').find_all('tr')
            for row in rows[1:]:
                data = [x.text.strip() for x in row.find_all('td')]

                id_, course_id, course_code = Exams.parse_course_info(p, data[0])

                if id_ is None:
                    continue

                section, location_ = data[1], data[4]
                date_ = Exams.parse_date(data[2], p[-2:]) or ''
                start, end = Exams.parse_time(data[3], date_) or (0, 0)

                doc = OrderedDict([
                    ('id', id_),
                    ('course_id', course_id),
                    ('course_code', course_code),
                    ('period', p),
                    ('date', date_),
                    ('start_time', start),
                    ('end_time', end),
                    ('sections', [])
                ])

                if id_ not in exams:
                    exams[id_] = doc

                exams[id_]['sections'].append(OrderedDict([
                    ('section', section),
                    ('location', location_)
                ]))

        for id_, doc in exams.items():
            with open('%s/%s.json' % (location, id_), 'w+') as outfile:
                json.dump(doc, outfile)

        Scraper.logger.info('Exams completed.')

    @staticmethod
    def parse_course_info(period, course_code):

        month, year, season = period[:-2], period[-2:], course_code[-1]

        endings = {
            'dec': {
                'F': '%s9' % str(int(year) - 1),
                'Y': '%s9' % str(int(year) - 1)
            },
            'apr': {
                'S': '%s1' % str(year),
                'Y': '%s9' % str(int(year) - 1)
            },
            'june': {
                'F': '%s5F' % str(year),
                'Y': '%s5' % str(year)
            },
            'aug': {
                'S': '%s5S' % str(year),
                'Y': '%s5' % str(year)
            }
        }

        try:
            course_id = '%s20%s' % (course_code, endings[month][season])
        except KeyError:
            return None, None, None

        exam_id = '%s%s' % (course_id, period.upper())
        return exam_id, course_id, course_code

    @staticmethod
    def parse_date(date_, year):
        """Convert date of form `D DD MMM` to ISO 8601 format."""

        date_ = date_.split(' ')
        if len(date_) == 3:
            day, date_, month = date_

            # TODO add EST offset
            return datetime.strptime('%s %s %s %s' % (day, date_, month, year),
                                     '%a %d %b %y').date().isoformat()

    @staticmethod
    def parse_time(time, date_):
        """Convert time range of form `pd hh:mm - hh:mm` to start and end
        decimal hours."""

        def convert_time_to_iso(t, is_pm=False):
            h, m = [int(x) for x in t.split(':')]
            h += 12 if is_pm else 0
            m //= 60

            return datetime.strptime('%s %s %s' % (date_, h, m),
                                     '%Y-%m-%d %H %M').replace(
                tzinfo=pytz.timezone('US/Eastern')).isoformat()

        time = list(filter(None, time.replace('-', '').split(' ')))
        if len(time) == 3:
            period, start, end = time
            after_12 = period == 'PM' or period == 'EV'

            return convert_time_to_iso(start, after_12), \
                   convert_time_to_iso(end, after_12)

    @staticmethod
    def get_exam_periods(year):
        if not year:
            year = date.today().year

        months = []
        for m in ('dec', 'apr', 'june', 'aug'):
            y = year if not m == 'dec' else int(year) - 1
            months.append('%s%s' % (m, str(y)[2:]))

        return months
