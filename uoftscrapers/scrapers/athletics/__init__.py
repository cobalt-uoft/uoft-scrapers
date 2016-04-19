from ..utils import Scraper
from .utsg import UTSGAthletics
from .utm import UTMAthletics
from .utsc import UTSCAthletics


class Athletics:

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Athletics initialized.')
        UTSGAthletics.scrape(location)
        UTMAthletics.scrape(location)
        UTSCAthletics.scrape(location)
        Scraper.logger.info('Athletics completed.')
