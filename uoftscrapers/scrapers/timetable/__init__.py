from ..utils import Scraper, LayersScraper
from .utm import UTMTimetable
from .utsc import UTSCTimetable
from .utsg import UTSGTimetable
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests


class Timetable:

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Timetable initialized.')
        UTSGTimetable.scrape(location)
        UTMTimetable.scrape(location)
        UTSCTimetable.scrape(location)
        Scraper.logger.info('Timetable completed.')
