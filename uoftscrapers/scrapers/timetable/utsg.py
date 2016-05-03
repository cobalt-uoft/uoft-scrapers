from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import tidylib
from math import floor
import json


class UTSGTimetable:

    host = 'https://timetable.iit.artsci.utoronto.ca/api'
    day_map = {
        'MO': 'MONDAY',
        'TU': 'TUESDAY',
        'WE': 'WEDNESDAY',
        'TH': 'THURSDAY',
        'FR': 'FRIDAY',
        'SA': 'SATURDAY',
        'SU': 'SUNDAY'
    }

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSGTimetable initialized.')

        orgs = UTSGTimetable.get_orgs()
        for org in orgs:
            Scraper.logger.info('Scraping %s.' % org)

            data = UTSGTimetable.search(org)

            if not data:
                continue

            for c in data.keys():
                x = data[c]

                course_id = '%s%s%s' % (x['code'], x['section'], x['session'])
                course_code = '%s%s' % (x['code'], x['section'])
                course_name = x['courseTitle']
                description = BeautifulSoup(x['courseDescription'], 'html.parser').text
                division = 'Faculty of Arts and Science'
                department = x['orgName']
                prerequisites = x['prerequisite']
                exclusions = x['exclusion']

                m = re.search('(?:[^\d]*)(\d+)', x['code'])
                level = int(floor(int(m.group(1)) / 100.0)) * 100

                campus = 'UTSG'

                year = x['session'][:4]
                month = x['session'][4:]
                term = ''
                if month == '9':
                    term = '%s Fall' % year
                elif month == '1':
                    term = '%s Winter' % year
                elif month == '5':
                    term = '%s Summer Y' % year
                elif month == '5F':
                    term = '%s Summer F' % year
                elif month == '5S':
                    term = '%s Summer S' % year

                breadths = []
                for ch in x['breadthCategories']:
                    if ch in '12345':
                        breadths.append(int(ch))
                breadths = sorted(breadths)

                sections = []

                meetings = x['meetings']
                if meetings:
                    for meeting in meetings.keys():
                        y = meetings[meeting]

                        code = '%s%s' % (y['teachingMethod'][:1], y['sectionNumber'])

                        instructors = []
                        if y['instructors']:
                            for instructor_id in y['instructors'].keys():
                                instructor = y['instructors'][instructor_id]
                                formatted = '%s %s' % (
                                    instructor['firstName'][:1],
                                    instructor['lastName']
                                )
                                formatted = formatted.strip()
                                if len(formatted) == 0:
                                    continue
                                instructors.append(formatted)


                        size = 0
                        if 'enrollmentCapacity' in y.keys():
                            size = y['enrollmentCapacity']
                            if size:
                                if len(size) > 0:
                                    size = int(size)
                                else:
                                    size = 0
                            else:
                                size = 0

                        # TODO: they haven't added this yet
                        enrolment = 0

                        times = []
                        if y['schedule']:
                            for time_id in y['schedule'].keys():
                                z = y['schedule'][time_id]

                                if z['meetingStartTime'] == None:
                                    continue

                                day = ''
                                if z['meetingDay'] in UTSGTimetable.day_map.keys():
                                    day = UTSGTimetable.day_map[z['meetingDay']]

                                startTime = z['meetingStartTime'].split(':')
                                start = (60 * 60 * int(startTime[0])) + (int(startTime[1]) * 60)

                                endTime = z['meetingEndTime'].split(':')
                                end = (60 * 60 * int(endTime[0])) + (int(endTime[1]) * 60)

                                times.append(OrderedDict([
                                    ("day", day),
                                    ("start", start),
                                    ("end", end),
                                    ("duration", end - start),
                                    ("location", '')
                                ]))

                        sections.append(OrderedDict([
                            ("code", code),
                            ("instructors", instructors),
                            ("times", times),
                            ("size", size),
                            ("enrolment", enrolment)
                        ]))

                course = OrderedDict([
                    ("id", course_id),
                    ("code", course_code),
                    ("name", course_name),
                    ("description", description),
                    ("division", division),
                    ("department", department),
                    ("prerequisites", prerequisites),
                    ("exclusions", exclusions),
                    ("level", level),
                    ("campus", campus),
                    ("term", term),
                    ("breadths", breadths),
                    ("meeting_sections", sections)
                ])

                Scraper.save_json(course, location, course_id)

        Scraper.logger.info('UTSGTimetable completed.')

    @staticmethod
    def get_orgs():
        data = Scraper.get('%s/orgs' % UTSGTimetable.host, json=True)
        if 'orgs' in data.keys():
            return list(data['orgs'].keys())
    @staticmethod
    def search(org):
        data = Scraper.get('%s/courses?org=%s' % (UTSGTimetable.host, org),
            json=True, timeout=60)
        if data:
            return data
