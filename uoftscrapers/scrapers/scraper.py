import os
import shutil

class Scraper:
    """Scraper superclass."""

    def __init__(self, name, path):
        self.name = name

        os.chdir(path)
        if os.path.exists('json'):
            shutil.rmtree('json')
        os.makedirs('json')

        print('%s initialized.' % self.name, flush=True)
