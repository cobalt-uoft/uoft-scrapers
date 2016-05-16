from ..utils import Scraper
from .utsg import UTSGDates
from .utm import UTMDates

from collections import OrderedDict


class Dates:

    @staticmethod
    def scrape(location='.', year=None):
        Scraper.logger.info('Dates initialized.')

        docs = OrderedDict()

        for campus in UTSGDates, UTMDates:
            dates = campus.scrape(location, year=year, save=False)

            if dates is None:
                continue

            for date, doc in dates.items():
                if date not in docs:
                    docs[date] = OrderedDict([
                        ('date', date),
                        ('events', [])
                    ])
                docs[date]['events'].extend(doc['events'])

        for date, doc in docs.items():
            Scraper.save_json(doc, location, date)

        Scraper.logger.info('Dates completed.')
