from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests


class UTMTimetable:

    host = 'https://student.utm.utoronto.ca/timetable/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('UTMTimetable initialized.')
        Scraper.logger.info('Not implemented.')
        Scraper.logger.info('UTMTimetable completed.')
