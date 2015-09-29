import os
import shutil
import logging

class Scraper:
    """Scraper superclass."""

    def __init__(self, name, location):
        self.name = name
        self.logger = logging.getLogger("uoftscrapers")

        if not os.path.exists(location):
            os.makedirs(location)
        os.chdir(location)

        self.logger.info('%s initialized.' % self.name)
