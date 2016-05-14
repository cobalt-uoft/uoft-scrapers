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

        docs = OrderedDict()

        for endpoint in ArtSciDates.get_endpoints(year):
            headers = {'Referer': ArtSciDates.host}
            html = Scraper.get('%s%s' % (ArtSciDates.host, endpoint),
                               headers=headers,
                               max_attempts=3)

            if html is None:
                Scraper.logger.info('No data available for %s.' % endpoint.upper)
                continue

            soup = BeautifulSoup(html, 'html.parser')

            session = ArtSciDates.parse_session(soup)

            for tr in soup.find(class_='vertical listing').find_all('tr'):
                if tr.find('th'):
                    continue

                data = tr.find_all('td')

                start, end = ArtSciDates.parse_dates(data[0].text, session)

                descriptions = []
                for t in data[1].text.split(';\n'):
                    descriptions += ArtSciDates.normalize_text(t)

                events = []
                for description in descriptions:
                    events.append(OrderedDict([
                        ('end', end),
                        ('session', session.upper()),
                        ('campus', 'UTSG'),
                        ('description', description)
                    ]))

                doc = OrderedDict([
                    ('date', start),
                    ('events', events),
                ])

                if start not in docs:
                    docs[start] = doc
                else:
                    docs[start]['events'].extend(doc['events'])

        if save:
            for date, doc in docs.items():
                Scraper.save_json(doc, location, date)

        Scraper.logger.info('ArtSciDates completed.')
        return docs if not save else None

    @staticmethod
    def get_endpoints(year):
        try:
            date = datetime(year=year)
        except:
            year = None

        if year is None:
            year = datetime.now().strftime('%y')

        session = '%s%d_fw' % (year, int(year) + 1)

        endpoints = []

        headers = {'Referer': ArtSciDates.host}
        html = Scraper.get('%s%s' % (ArtSciDates.host, session),
                           headers=headers,
                           max_attempts=3)

        if html is None:
            return endpoints

        soup = BeautifulSoup(html, 'html.parser')

        for a in soup.find(id='portal-column-one').find_all('a'):
            if a.has_attr('title') and 'important dates' in a['title'].lower():
                endpoints.append(a['href'])

        return ['%s/%s' % (session, a.split('/')[-1]) for a in endpoints] +\
            ['20%s5/dates' % year]

    @staticmethod
    def parse_session(soup):
        session = ''
        if soup.find(id='parent-fieldname-title'):
            session = soup.find(id='parent-fieldname-title').text
            session = session.replace('Important Dates', '').replace(':', '')
        else:
            # TODO parse page title
            pass
        return session.strip()

    @staticmethod
    def parse_dates(date, session):

        def get_full_date(partial_date):
            """Convert a partial date of the form `B d` (e.g. November 8)
            to the form `B d Y` (e.g. November 8 2016)."""
            month, day = partial_date.split(' ')
            year = session[:4]
            return '%s %s %s' % (month, day, year)

        date = date.replace(' to ', '-').replace('(tentative)', '').strip()
        if '-' in date:
            # Date range (e.g. December 21 - January 4 or November 7-8)
            if ' - ' in date:
                date = date.split(' - ')
                start, end = get_full_date(date[0]), get_full_date(date[1])
            else:
                month, days = date.split(' ')
                days = days.split('-')

                start, end = get_full_date('%s %s' % (month, days[0])),\
                    get_full_date('%s %s' % (month, days[1]))
        else:
            start = end = get_full_date(date)

        return ArtSciDates.convert_date(start), ArtSciDates.convert_date(end)

    @staticmethod
    def convert_date(date):
        """Convert a date of form `B d Y` (eg. May 13 2016) to ISO-8601."""
        return datetime.strptime(date, '%B %d %Y').date().isoformat()

    @staticmethod
    def normalize_text(text):
        text = re.sub(r'\s\s+', ' ', text).strip()

        if text == '':
            return []

        if '\n' in text and text[-2:] != '\n':
            return text.split('\n')

        return [text]


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
