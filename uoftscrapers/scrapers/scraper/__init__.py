import os
import shutil
import logging

class Scraper:
    """Scraper superclass."""

    def __init__(self, name, location):
        self.name = name
        self.logger = logging.getLogger("uoftscrapers")
        self.location = location

        if not os.path.exists(location):
            os.makedirs(location)

        self.logger.info('%s initialized.' % self.name)
