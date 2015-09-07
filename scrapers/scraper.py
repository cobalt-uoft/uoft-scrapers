import os

class Scraper:
    """Scraper superclass."""
    
    def __init__(self, name, path):
        self.name = name
        
        os.chdir(path)
        if not os.path.exists('json'):
            os.makedirs('json')

        print('\n%s initialized.' % self.name)