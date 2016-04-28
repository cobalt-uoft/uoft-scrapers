from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from pytz import timezone


class UTSCExams:
    """A scraper for UTSC exams."""

    host = 'http://www.utsc.utoronto.ca/registrar/examination-schedule'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSCExams initialized.')

        exams = OrderedDict()

        headers = {
            'Referer': UTSCExams.host
        }
        html = Scraper.get('%s' % UTSCExams.host, headers=headers)
        soup = BeautifulSoup(html, 'html.parser')

        for table in soup.find_all('table', class_='views-table'):
            for tr in table.find_all('tr')[1:]:
                data = [x.text.strip() for x in tr.find_all('td')]

                course_code, lecture_code = data[0], None
                if ' ' in course_code:
                    course_code, lecture_code = course_code.split(' ')

                date = data[1]
                start, end = UTSCExams.parse_time(data[2], data[3], date)
                duration = end - start

                location_ = data[4]

                id_, course_id = UTSCExams.get_course_id(course_code, date)

                period = UTSCExams.get_period(date)

                if not id_ or not period:
                    continue

                doc = OrderedDict([
                    ('id', id_),
                    ('course_id', course_id),
                    ('course_code', course_code),
                    ('campus', 'UTSC'),
                    ('period', period),
                    ('date', date),
                    ('start_time', start),
                    ('end_time', end),
                    ('duration', duration),
                    ('sections', [])
                ])

                if id_ not in exams:
                    exams[id_] = doc

                exams[id_]['sections'].append(OrderedDict([
                    ('lecture_code', lecture_code or ''),
                    ('exam_section', ''),
                    ('location', location_)
                ]))

        for id_, doc in exams.items():
            Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTSCExams completed.')

    @staticmethod
    def get_period(d):
        def get_date(month, date, year):
            months = {
                'dec': 12,
                'apr': 4,
                'june': 6,
                'aug': 8
            }
            return datetime.strptime('%s-%d-%d' % (year, months[month], date),
                                     '%Y-%m-%d')

        d = datetime.strptime(d, '%Y-%m-%d')

        year = d.year
        month = None

        for m, ld in (('dec', 31), ('apr', 30), ('june', 30), ('aug', 31)):
            if get_date(m, 1, year) <= d <= get_date(m, ld, year):
                month = m
                break

        if month:
            return '%s%s' % (month.upper(), str(year)[2:])

    @staticmethod
    def get_course_id(course_code, date):
        d = datetime.strptime(date, '%Y-%m-%d')
        month, year, period = d.strftime(
            "%b").lower(), d.year, UTSCExams.get_period(date)
        endings = {
            'dec': {
                'F': '%s9' % str(year),
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

        season = course_code[-1]
        exam_id = course_id = None

        if month in endings and season in endings[month]:
            course_id = '%s%s' % (course_code, endings[month][season])
            exam_id = '%s%s' % (course_id, period)

        return exam_id, course_id

    @staticmethod
    def parse_time(start, end, date):
        def convert_time(t):
            h, m = [int(x) for x in t.split(':')]
            return (h * 60 * 60) + (m * 60)
        return convert_time(start), convert_time(end)
