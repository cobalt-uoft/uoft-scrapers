from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from pytz import timezone


class UTSGDates:
    """A scraper for UTSG important dates.

    Data is retrieved from http://www.artsci.utoronto.ca/current/course/timetable/.
    """

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSGDates initialized.')

        for faculty in ArtSciDates, EngDates:
            dates = faculty.scrape(location)
            if dates is not None:
                # save json file
                pass

        Scraper.logger.info('UTSGDates completed.')


class ArtSciDates:
    """A scraper for important dates for the Faculty of Arts & Science.

    Data is retrieved from http://www.artsci.utoronto.ca/current/course/timetable/.
    """

    @staticmethod
    def scrape(location='.', year=None):
        """Update the local JSON files for this scraper."""
        Scraper.logger.info('ArtSciDates initialized.')

        year = year[2:] or datetime.now().strftime('%y')

        Scraper.logger.info('ArtSciDates completed.')


class EngDates:
    """A scraper for important dates for UTSG Engineering.

    Data is retrieved from http://www.undergrad.engineering.utoronto.ca/About/Dates_Deadlines.htm.
    """

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""
        Scraper.logger.info('EngDates initialized.')

        Scraper.logger.info('EngDates completed.')

