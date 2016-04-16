from ..utils import Scraper
from .utm import UTMAthletics
from .utsc import UTSCAthletics


class Athletics:
    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Athletics initialized.')
        UTMAthletics.scrape(location)
        UTSCAthletics.scrape(location)
        Scraper.logger.info('Athletics completed.')
