from ..utils import Scraper
from .utsg import UTSGExams
from .utm import UTMExams
from .utsc import UTSCExams
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests


class Exams:

    host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Exams initialized.')
        UTSGExams.scrape(location)
        UTMExams.scrape(location)
        UTSCExams.scrape(location)
        Scraper.logger.info('Exams completed.')
