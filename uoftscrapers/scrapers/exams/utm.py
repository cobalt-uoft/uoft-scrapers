from ..utils import Scraper
from .exams_helpers import *
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from pytz import timezone
import re


class UTMExams:
    """A scraper for UTM exams."""

    host = 'https://m.utm.utoronto.ca/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTMExams initialized.')

        depts = UTMExams.get_page_links('list_dept.php?type=2')
        Scraper.logger.info('Got departments (1/3).')

        courses = []
        for dept in depts:
            courses.extend(UTMExams.get_page_links(dept))
        Scraper.logger.info('Got courses (2/3).')

        exams = UTMExams.retrieve_exams(courses)
        Scraper.logger.info('Got exams (3/3).')

        for id_, doc in exams.items():
            Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTMExams completed.')

    @staticmethod
    def retrieve_exams(courses):
        exams = OrderedDict()

        for course in courses:
            headers = {
                'Referer': UTMExams.host
            }
            html = Scraper.get('%s%s' % (UTMExams.host, course),
                               headers=headers)
            soup = BeautifulSoup(html, 'html.parser')

            course_code = soup.find('div', class_='title').text.strip()
            lecture_code = None

            # some course names include lecture code (see CHI200Y5Y)
            if ' ' in course_code:
                course_code, lecture_code = course_code.split(' ')

            data = [br.previous_sibling.string.strip()
                    for br in soup.find('div', class_='info').find_all('br')]

            date = data[0].split(': ')[1]

            exam_id, course_id = get_course_id(course_code, date)

            period = get_period(date)

            if not exam_id or not period:
                continue

            start = convert_time(data[1].split(': ')[1])
            end = convert_time(data[2].split(': ')[1])
            duration = end - start

            sections = [UTMExams.parse_sections(room.split(': ')[1])
                        for room in [x for x in data[3:] if 'Room:' in x]]

            # append lecture code to section range if it exists
            for i in range(len(sections)):
                sections[i]['lecture'] = lecture_code or ''

            doc = OrderedDict([
                ('id', exam_id),
                ('course_id', course_id),
                ('course_code', course_code),
                ('campus', 'UTM'),
                ('period', period),
                ('date', date),
                ('start_time', start),
                ('end_time', end),
                ('duration', duration),
                ('sections', [])
            ])

            if exam_id not in exams:
                exams[exam_id] = doc

            for section in sections:
                exams[exam_id]['sections'].append(OrderedDict([
                    ('lecture_code', section['lecture']),
                    ('exam_section', section['section']),
                    ('location', section['room'])
                ]))
        return exams

    @staticmethod
    def get_page_links(endpoint):
        headers = {
            'Referer': UTMExams.host
        }
        html = Scraper.get('%s%s' % (UTMExams.host, endpoint),
                           headers=headers)
        soup = BeautifulSoup(html, 'html.parser')
        return [li.find('a')['href']
                for li in soup.find('ul', class_='link').find_all('li')]

    @staticmethod
    def parse_sections(room):
        section = ''
        if '(' in room:
            room, section = [x.strip()
                             for x in re.sub('[()]', ' ', room).split('  ')]
        return {'section': section, 'room': room}
