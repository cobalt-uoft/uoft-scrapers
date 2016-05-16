from ..utils import Scraper
from .exams_helpers import *
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from pytz import timezone


class UTSGExams:
    """A scraper for UTSG exams."""

    @staticmethod
    def scrape(location='.', year=None):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTSGExams initialized.')

        for faculty in ArtSciExams, EngExams:
            exams = faculty.scrape(location=location, year=year, save=False)
            if exams is None:
                continue
            for id_, doc in exams.items():
                Scraper.save_json(doc, location, id_)

        Scraper.logger.info('UTSGExams completed.')


class ArtSciExams:
    """A scraper for Arts & Science exams.

    Data is scraped from http://www.artsci.utoronto.ca/current/exams/
    """

    host = 'http://www.artsci.utoronto.ca/current/exams/'

    @staticmethod
    def scrape(location='.', year=None, save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('ArtSciExams initialized.')

        exams = OrderedDict()

        for p in ArtSciExams.get_exam_periods(year):
            Scraper.logger.info('Scraping %s exams.' % p.upper())

            headers = {
                'Referer': ArtSciExams.host
            }
            html = Scraper.get('%s%s' % (ArtSciExams.host, p),
                               headers=headers,
                               max_attempts=3)

            try:
                soup = BeautifulSoup(html, 'html.parser')
            except TypeError:
                soup = None

            if not (html and soup and soup.find(class_='vertical listing')):
                # no exam data available
                Scraper.logger.info('No %s exams.' % p.upper())
                continue

            rows = soup.find('table', class_='vertical listing').find_all('tr')
            for row in rows[1:]:
                data = [x.text.strip() for x in row.find_all('td')]

                exam_id, course_id, course_code = \
                    ArtSciExams.parse_course_info(p, data[0])

                if exam_id is None:
                    continue

                section = data[1]

                lecture_section = exam_section = None

                if '  ' in section:
                    lecture_section, exam_section = section.split('  ')
                elif '-' in section:
                    exam_section = section
                else:
                    lecture_section = section

                location_ = data[4]

                date = ArtSciExams.parse_date(data[2], p[-2:]) or ''
                start, end = ArtSciExams.parse_time(data[3], date) or (0, 0)
                duration = end - start

                doc = OrderedDict([
                    ('id', exam_id),
                    ('course_id', course_id),
                    ('course_code', course_code),
                    ('campus', 'UTSG'),
                    ('period', p.upper()),
                    ('date', date),
                    ('start_time', start),
                    ('end_time', end),
                    ('duration', duration),
                    ('sections', [])
                ])

                if exam_id not in exams:
                    exams[exam_id] = doc

                exams[exam_id]['sections'].append(OrderedDict([
                    ('lecture_code', lecture_section or ''),
                    ('exam_section', exam_section or ''),
                    ('location', location_)
                ]))

        if save:
            for id_, doc in exams.items():
                Scraper.save_json(doc, location, id_)

        Scraper.logger.info('ArtSciExams completed.')
        return exams if not save else None

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
    def parse_date(date, year):
        """Convert date of form `D DD MMM` to ISO 8601 format."""
        if date.count(' ') == 2:
            return datetime.strptime('%s %s' % (date, year),
                                     '%a %d %b %y').date().isoformat()

    @staticmethod
    def parse_time(time, d):
        """Convert time from `pd HH:MM - HH:MM` to start & end datetime."""

        def convert_time(t, is_pm=False):
            """Convert time from `HH:MM` to an ISO 8601 datetime."""
            h, m = [int(x) for x in t.split(':')]
            h += 12 if is_pm and h != 12 else 0
            return (h * 60 * 60) + (m * 60)

        time = list(filter(None, time.replace('-', '').split(' ')))
        if len(time) == 3:
            period, start, end = time
            after_12 = period == 'PM' or period == 'EV'

            return convert_time(start, after_12), convert_time(end, after_12)

    @staticmethod
    def get_exam_periods(year):
        if not year:
            year = datetime.today().year

        periods = []
        for m in ('dec', 'apr', 'june', 'aug'):
            y = year if not m == 'dec' else int(year) - 1
            periods.append('%s%s' % (m, str(y)[2:]))

        return periods


class EngExams:
    """A scraper for Engineering exams.

    Data is scraped from http://www.apsc.utoronto.ca/timetable/fes.aspx
    """

    host = 'http://www.apsc.utoronto.ca/timetable/fes.aspx'

    @staticmethod
    def scrape(location='.', year=None, save=True):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('EngExams initialized.')

        exams = OrderedDict()

        headers = {
            'Referer': EngExams.host
        }
        html = Scraper.get(EngExams.host, headers=headers, max_attempts=3)
        soup = BeautifulSoup(html, 'html.parser')

        if soup is None:
            return

        for tr in soup.find('table', id='DataList1').find_all('tr'):
            for td in tr.find_all('td'):
                entry = td.find('div', id='logo')

                if entry is None:
                    continue

                info = entry.find('div')

                date, time = [br.next_sibling.strip()
                              for br in info.find_all('br')[:2]]

                date = datetime.strptime(date.split(':')[-1].strip(),
                                         '%b %d, %Y').date().isoformat()

                time = time.strip().split(':')
                hour = int(time[1])
                minute, meridiem = time[2].split(' ')

                hour += 12 if meridiem == 'PM' and hour != 12 else 0

                # No end times, using 2.5h for duration per
                # http://www.undergrad.engineering.utoronto.ca/Office_of_the_Registrar/Examinations/Schedules_Locations.htm
                start = hour * 60 * 60 + int(minute) * 60
                duration = 2 * 60 * 60 + 30 * 60
                end = start + duration

                period = get_period(date)

                exam_id, course_id, course_code = \
                    EngExams.get_course_info(info.find('strong').text.strip(), period)

                locations = entry.find('table', class_='xx')

                exam_sections = []
                for tr in locations.find_all('tr')[1:]:
                    location, range = [td.text.strip() for td in tr.find_all('td')[:2]]

                    exam_sections.append(OrderedDict([
                        ('lecture_code', ''),
                        ('exam_section', range),
                        ('location', location.replace('-', ' '))
                    ]))

                exams[exam_id] = OrderedDict([
                    ('id', exam_id),
                    ('course_id', course_id),
                    ('course_code', course_code),
                    ('campus', 'UTSG'),
                    ('period', period),
                    ('date', date),
                    ('start_time', start),
                    ('end_time', end),
                    ('duration', duration),
                    ('sections', exam_sections)
                ])

        if save:
            for id_, doc in exams.items():
                Scraper.save_json(doc, location, id_)

        Scraper.logger.info('EngExams completed.')
        return exams if not save else None

    @staticmethod
    def get_course_info(course, period):
        endings = {
            'dec': {'season': 'F', 'month': '9'},
            'apr': {'season': 'S', 'month': '1'},
            'june': {'season': 'F', 'month': '5F'},
            'aug': {'season': 'S', 'month': '5S'}
        }

        month, year = period[:-2].lower(), period[-2:]
        exam_id = course_id = course_code = None
        if month in endings:
            course_code = '%s%s' % (course, endings[month]['season'])
            course_id = '%s20%s%s' % (course_code, year, endings[month]['month'])
            exam_id = '%s%s' % (course_id, period)
        return exam_id, course_id, course_code
