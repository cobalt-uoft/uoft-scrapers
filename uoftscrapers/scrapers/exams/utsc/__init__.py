from ...scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, date
from collections import OrderedDict
import json
import requests
import pytz


class UTSCExams:
    """A scraper for UTSC exams."""

    host = 'http://www.utsc.utoronto.ca/registrar/examination-schedule'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTSCExams initialized.')
        Scraper.logger.info('Not implemented.')
        raise NotImplementedError('This scraper has not been implemented yet.')
        Scraper.logger.info('UTSCExams completed.')
