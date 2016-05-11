from ..utils import Scraper
from .utsg import UTSGDates


class Dates:

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Dates initialized.')
        UTSGDates.scrape(location)
        Scraper.logger.info('Dates completed.')
