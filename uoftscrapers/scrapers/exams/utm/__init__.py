from ...scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
import json
import requests
import pytz


class UTMExams:
    """A scraper for UTM exams."""

    host = 'https://m.utm.utoronto.ca/list_dept.php?type=2'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTMExams initialized.')
        Scraper.logger.info('Not implemented.')
        raise NotImplementedError('This scraper has not been implemented yet.')
        Scraper.logger.info('UTMExams completed.')
