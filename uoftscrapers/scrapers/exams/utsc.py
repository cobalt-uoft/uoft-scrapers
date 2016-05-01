from ..utils import Scraper
from .exams_helpers import *
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

                exam_id, course_id = get_course_id(course_code, date)

                period = get_period(date)

                if not exam_id or not period:
                    continue

                start = convert_time(data[2])
                end = convert_time(data[3])
                duration = end - start

                location_ = data[4]

                doc = OrderedDict([
                    ('id', exam_id),
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

                if exam_id not in exams:
                    exams[exam_id] = doc

                exams[exam_id]['sections'].append(OrderedDict([
                    ('lecture_code', lecture_code or ''),
                    ('exam_section', ''),
                    ('location', location_)
                ]))

        for id_, doc in exams.items():
            Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTSCExams completed.')
