from ...scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
import json
import requests
import pytz


class UTSCExams:
    """A scraper for UTSC exams."""

    host = 'http://www.utsc.utoronto.ca/registrar/examination-schedule'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSCExams initialized.')

        exams = OrderedDict()

        headers = {
            'Referer': UTSCExams.host
        }
        html = UTSCExams.s.get('%s' % UTSCExams.host, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')

        for table in soup.find_all('table', class_='views-table'):
            for tr in table.find_all('tr')[1:]:
                data = [x.text.strip() for x in tr.find_all('td')]

                id_, course_id, course_code = UTSCExams.parse_course(data[0])

                if not id_:
                    continue

                # TODO dynamic period value
                period = 'APR16'
                date_ = data[1]
                start, end = UTSCExams.parse_time(data[2], data[3], date_)
                location_ = data[4]

                doc = OrderedDict([
                    ('id', id_),
                    ('course_id', course_id),
                    ('course_code', course_code),
                    ('period', period),
                    ('date', date_),
                    ('start_time', start),
                    ('end_time', end),
                    ('sections', [])
                ])

                if id_ not in exams:
                    exams[id_] = doc

                exams[id_]['sections'].append(OrderedDict([
                    ('section', ''),
                    ('location', location_)
                ]))

        if exams:
            Scraper.ensure_location(location)

        for id_, doc in exams.items():
            with open('%s/%s.json' % (location, id_), 'w+') as outfile:
                json.dump(doc, outfile)

        Scraper.logger.info('UTSCExams completed.')

    @staticmethod
    def parse_course(course_code):
        # TODO dynamic month/year values
        month, year, period = 'apr', 2016, 'apr16'
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
            exam_id = '%s%s' % (course_id, period.upper())

        return exam_id, course_id, course_code

    @staticmethod
    def parse_time(start, end, date):
        def convert_time(t):
            h, m = [int(x) for x in t.split(':')]
            d = datetime.strptime('%s %s %s' % (date, h, m), '%Y-%m-%d %H %M')
            return d.replace(tzinfo=pytz.timezone('US/Eastern')).isoformat()
        return convert_time(start), convert_time(end)
