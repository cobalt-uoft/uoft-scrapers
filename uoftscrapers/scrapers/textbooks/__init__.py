import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os

class Textbooks(Scraper):
    """A scraper for UofT's book store.

    UofT Book Store is located at http://uoftbookstore.com/.
    """

    def __init__(self, output_location='.'):
        super().__init__('Textbooks', output_location)

        self.host = \
            'http://uoftbookstore.com/buy_courselisting.asp'

    def run(self):
        self.logger.info('Not implemented')
        raise NotImplementedError('This scraper has not been implemented yet.')
        self.logger.info('%s completed.' % self.name)
