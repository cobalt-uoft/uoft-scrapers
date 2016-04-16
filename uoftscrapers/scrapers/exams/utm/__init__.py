from ...scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
import json
import requests
import pytz
import re

from pprint import pprint


class UTMExams:
    """A scraper for UTM exams."""

    host = 'https://m.utm.utoronto.ca/'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTMExams initialized.')

        depts = UTMExams.get_page_links('list_dept.php?type=2')
        Scraper.logger.info('Got department links (1/3).')

        courses = []
        for dept in depts:
            courses.extend(UTMExams.get_page_links(dept))
        Scraper.logger.info('Got course links (2/3).')

        exams = OrderedDict()
        count = 1
        for course in courses:
            headers = {
                'Referer': UTMExams.host
            }
            html = UTMExams.s.get('%s%s' % (UTMExams.host, course),
                                  headers=headers).text
            soup = BeautifulSoup(html, 'html.parser')

            course_code = soup.find('div', class_='title').text.strip()

            # some course names include lecture code (e.g. CHI200Y5Y)
            if ' ' in course_code:
                course_code, lecture_code = course_code.split(' ')
            else:
                lecture_code = None

            id_, course_id = UTMExams.parse_course(course_code)

            data = [br.previous_sibling.string.strip()
                    for br in soup.find('div', class_='info').find_all('br')]

            date_ = data[0].split(': ')[1]

            start, end = UTMExams.parse_time(data[1].split(': ')[1],
                                             data[2].split(': ')[1], date_)

            sections = [UTMExams.parse_sections(room.split(': ')[1])
                        for room in [x for x in data[3:] if 'Room:' in x]]

            # add the lecture code to the section range if applicable
            if lecture_code:
                sections[0]['section'] = '%s%s' % (lecture_code,
                                                   sections[0]['section'])

            doc = OrderedDict([
                ('id', id_),
                ('course_id', course_id),
                ('course_code', course_code),
                ('period', 'APR16'),
                ('date', date_),
                ('start_time', start),
                ('end_time', end),
                ('sections', [])
            ])

            if id_ not in exams:
                exams[id_] = doc

            for section in sections:
                exams[id_]['sections'].append({
                    'section': section['section'],
                    'locaton': section['room']
                })

        Scraper.logger.info('Got exam data (3/3).')

        if exams:
            Scraper.ensure_location(location)

        for id_, doc in exams.items():
            with open('%s/%s.json' % (location, id_), 'w+') as outfile:
                json.dump(doc, outfile)

        Scraper.logger.info('UTMExams completed.')

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

        return exam_id, course_id

    @staticmethod
    def parse_sections(room):
        section = ''
        if '(' in room:
            room, section = [x.strip()
                             for x in re.sub('[()]', ' ', room).split('  ')]

        return {
            'section': section,
            'room': room
        }

    @staticmethod
    def get_page_links(endpoint):
        headers = {
            'Referer': UTMExams.host
        }
        html = UTMExams.s.get('%s%s' % (UTMExams.host, endpoint),
                              headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        return [li.find('a')['href']
                for li in soup.find('ul', class_='link').find_all('li')]

    @staticmethod
    def parse_time(start, end, date_):
        def convert_time(t):
            h, m, s = [int(x) for x in t.split(':')]
            d = datetime.strptime('%s %s %s %s' % (date_, h, m, s), '%Y-%m-%d %H %M %S')
            return d.replace(tzinfo=pytz.timezone('US/Eastern')).isoformat()

        return convert_time(start), convert_time(end)

