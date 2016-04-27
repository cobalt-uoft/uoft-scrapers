from ..utils import Scraper
from .utsg import UTSGAthletics
from .utm import UTMAthletics
from .utsc import UTSCAthletics

from collections import OrderedDict


class Athletics:
    @staticmethod
    def scrape(location='.', month=None):
        Scraper.logger.info('Athletics initialized.')

        docs = OrderedDict()

        for campus in UTSGAthletics, UTMAthletics, UTSCAthletics:
            athletics = campus.scrape(location, month=month, save=False)

            if athletics is None:
                continue

            for date, data in athletics.items():
                if date not in docs:
                    docs[date] = OrderedDict([
                        ('date', date),
                        ('events', [])
                    ])
                docs[date]['events'].extend(data['events'])

        for date, doc in docs.items():
            Scraper.save_json(doc, location, date)

        Scraper.logger.info('Athletics completed.')
