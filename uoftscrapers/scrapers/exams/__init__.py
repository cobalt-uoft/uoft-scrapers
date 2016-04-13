from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import requests
from datetime import date
from ..scraper import Scraper


class Exams:
    """A scraper for UofT exams.

    Exam data is scraped from http://www.artsci.utoronto.ca/current/exams/
    """

    host = 'http://www.artsci.utoronto.ca/current/exams/'
    s = requests.Session()

    @staticmethod
    def scrape(year=None, location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('Exam scraper initialized.')
        Scraper.ensure_location(location)

        for m in Exams.get_exam_months(year):
            Scraper.logger.info('Scraping exams for %s.' % m.upper())

    @staticmethod
    def get_exam_months(year):
        if not year:
            year = date.today().year

        months = []
        for m in ('dec', 'apr', 'june', 'aug'):
            y = year if not m == 'dec' else int(year) - 1
            months.append('%s%s' % (m, str(y)[2:]))

        return months

