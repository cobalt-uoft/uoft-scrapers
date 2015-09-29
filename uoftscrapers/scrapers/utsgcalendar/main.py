import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os

class UTSGCalendar(Scraper):

    def __init__(self, output_location='.'):
        super().__init__('UTSG Calendar', output_location)

        self.host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'

    def run(self):
        self.logger.info('Not implemented')
        raise NotImplementedError('This scraper has not been implemented yet.')
        self.logger.info('%s completed.' % self.name)
