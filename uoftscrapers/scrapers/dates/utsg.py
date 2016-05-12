from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from pytz import timezone
from pprint import pprint
import re


class UTSGDates:
    """A scraper for UTSG important dates."""

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSGDates initialized.')

        for faculty in ArtSciDates, EngDates:
            docs = faculty.scrape(location, save=False)
            if docs is not None:
                for date, doc in docs.items():
                    Scraper.save_json(doc, location, date)

        Scraper.logger.info('UTSGDates completed.')


class ArtSciDates:
    """A scraper for important dates for UTSG Arts & Science.

    Data is retrieved from
    http://www.artsci.utoronto.ca/current/course/timetable/.
    """

    host = 'http://www.artsci.utoronto.ca/current/course/timetable/'

    @staticmethod
    def scrape(location='.', year=None, save=True):
        """Update the local JSON files for this scraper."""
        Scraper.logger.info('ArtSciDates initialized.')

        for session, endpoint in ArtSciDates.get_sessions(year)[:1]:
            headers = {
                'Referer': ArtSciDates.host
            }
            html = Scraper.get('%s%s' % (ArtSciDates.host, endpoint),
                               headers=headers,
                               max_attempts=3)

            if html is None:
                Scraper.logger.info('No data available for %s.' % session.upper)
                continue

            docs = OrderedDict()

            soup = BeautifulSoup(html, 'html.parser')
            for tr in soup.find(class_='vertical listing').find_all('tr'):
                if tr.find('th'):
                    continue

                event = tr.find_all('td')

                start_date, end_date = ArtSciDates.parse_dates(event[0].text, session)

                events = []
                for t in event[1].text.split(';\n'):
                    events += ArtSciDates.normalize_text(t)

                doc = OrderedDict([
                    ('start_date', start_date),
                    ('end_date', end_date),
                    ('session', session),
                    ('events', events)
                ])

                if start_date not in docs:
                    docs[start_date] = doc
                else:
                    docs[start_date]['events'].extend(doc['events'])

        if save:
            for date, doc in docs.items():
                Scraper.save_json(doc, location, date)

        Scraper.logger.info('ArtSciDates completed.')
        return docs

    @staticmethod
    def normalize_text(text):
        text = re.sub(r'\s\s+', ' ', text).strip()

        if text == '':
            return []

        if '\n' in text and text[-2:] != '\n':
            return text.split('\n')

        return [text]

    @staticmethod
    def get_sessions(year):
        try:
            date = datetime(year=year)
        except:
            year = None

        if year is None:
            year = datetime.now().strftime('%Y')

        shortened_year = str(year)[2:]
        session = '%s%d_fw' % (shortened_year, int(shortened_year) + 1)

        fall = '%s/%s_fall_dates' % (session, str(year))
        winter = '%s/%d_winter_dates' % (session, int(year) + 1)

        summer = '%s5/dates' % year

        return [
            ('FALL%s' % shortened_year, fall),
            ('WINTER%s' % shortened_year, winter),
            ('SUMMER%s' % shortened_year, summer)
        ]

    @staticmethod
    def parse_dates(date, session):
        def get_date(date_string):
            # date_string in the form '%B %d'
            month = date_string.split(' ')[0]
            year = int(session[-2:])
            if 'FALL' in session and int(datetime.strptime(month, '%B').strftime('%m')) < 4:
                year += 1

            return '%s %d' % (date_string, year)

        start = end = None
        if '-' in date:
            # Date range
            if ' - ' in date:
                # e.g. December 21 - January 4
                date = date.split(' - ')

                start, end = get_date(date[0]), get_date(date[1])
            else:
                # e.g. November 7-8
                month, days = date.split(' ')
                days = days.split('-')

                start = get_date('%s %s' % (month, days[0]))
                end = get_date('%s %s' % (month, days[1]))
        else:
            start = end = get_date(date)

        start = datetime.strptime(start, '%B %d %y').date().isoformat()
        end = datetime.strptime(end, '%B %d %y').date().isoformat()

        return start, end


class EngDates:
    """A scraper for important dates for UTSG Engineering.

    Data is retrieved from
    http://www.undergrad.engineering.utoronto.ca/About/Dates_Deadlines.htm.
    """

    @staticmethod
    def scrape(location='.', save=True):
        """Update the local JSON files for this scraper."""
        Scraper.logger.info('EngDates initialized.')

        Scraper.logger.info('EngDates completed.')
