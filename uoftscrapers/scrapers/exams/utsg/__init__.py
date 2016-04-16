from ...scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
import requests
import pytz

class UTSGExams:
    """A scraper for UTSG exams.

    Data is scraped from http://www.artsci.utoronto.ca/current/exams/
    """

    host = 'http://www.artsci.utoronto.ca/current/exams/'
    s = requests.Session()

    @staticmethod
    def scrape(year=None, location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTSGExams initialized.')

        exams = OrderedDict()

        for p in UTSGExams.get_exam_periods(year):
            Scraper.logger.info('Scraping %s exams.' % p.upper())

            headers = {
                'Referer': UTSGExams.host
            }
            html = UTSGExams.s.get('%s%s' % (UTSGExams.host, p),
                                   headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.find('table', class_='vertical listing'):
                # no exam data available
                Scraper.logger.info('No %s exams.' % p.upper())
                continue

            rows = soup.find('table', class_='vertical listing').find_all('tr')
            for row in rows[1:]:
                data = [x.text.strip() for x in row.find_all('td')]

                id_, course_id, course_code = UTSGExams.parse_course_info(p, data[0])

                if id_ is None:
                    continue

                section, location_ = data[1], data[4]
                date_ = UTSGExams.parse_date(data[2], p[-2:]) or ''
                start, end = UTSGExams.parse_time(data[3], date_) or (0, 0)

                doc = OrderedDict([
                    ('id', id_),
                    ('course_id', course_id),
                    ('course_code', course_code),
                    ('period', p.upper()),
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

        if exams:
            Scraper.ensure_location(location)

        for id_, doc in exams.items():
            Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTSGExams completed.')

    @staticmethod
    def parse_course_info(period, course_code):

        month, year, season = period[:-2], period[-2:], course_code[-1]

        endings = {
            'dec': {
                'F': '%s9' % str(int(year)),
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

        exam_id = course_id = None
        if month in endings and season in endings[month]:
            course_id = '%s20%s' % (course_code, endings[month][season])
            exam_id = '%s%s' % (course_id, period.upper())

        return exam_id, course_id, course_code

    @staticmethod
    def parse_date(date_, year):
        """Convert date of form `D DD MMM` to ISO 8601 format."""

        date_ = date_.split(' ')
        if len(date_) == 3:
            day, date_, month = date_

            return datetime.strptime('%s %s %s %s' % (day, date_, month, year),
                                     '%a %d %b %y').date().isoformat()

    @staticmethod
    def parse_time(time, d):
        """Convert time from `pd HH:MM - HH:MM` to start & end datetime."""

        def convert_time(t, is_pm=False):
            """Convert time from `HH:MM` to an ISO 8601 datetime."""
            h, m = [int(x) for x in t.split(':')]
            h += 12 if is_pm else 0

            date_ = datetime.strptime('%s %s %s' % (d, h, m), '%Y-%m-%d %H %M')
            return date_.replace(tzinfo=pytz.timezone('US/Eastern')).isoformat()

        time = list(filter(None, time.replace('-', '').split(' ')))
        if len(time) == 3:
            period, start, end = time
            after_12 = period == 'PM' or period == 'EV'

            return convert_time(start, after_12), convert_time(end, after_12)

    @staticmethod
    def get_exam_periods(year):
        if not year:
            year = date.today().year

        periods = []
        for m in ('dec', 'apr', 'june', 'aug'):
            y = year if not m == 'dec' else int(year) - 1
            periods.append('%s%s' % (m, str(y)[2:]))

        return periods
