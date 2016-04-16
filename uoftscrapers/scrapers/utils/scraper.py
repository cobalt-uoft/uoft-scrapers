import json
import logging
import os
import requests
import shutil
import sys


class Scraper:
    """Scraper class."""

    logger = logging.getLogger('uoftscrapers')
    s = requests.Session()

    @staticmethod
    def ensure_location(location):
        """Ensure that the location given exists."""

        if not os.path.exists(location):
            os.makedirs(location)

    @staticmethod
    def save_json(data, location, filename):
        Scraper.ensure_location(location)

        with open('%s/%s.json' % (location, filename),'w+') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def get_html(url, params=None, cookies=None, headers=None, max_attempts=10):
        """Fetches the HTML page source, automatically retrying if it times out."""

        html = None
        attempts = 0
        while html is None and attempts < max_attempts:
            try:
                r = Scraper.s.get(url, params=params, cookies=cookies, headers=headers)
                if r.status_code == 200:
                    html = r.text
            except (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError):
                attempts += 1
                continue

        return html.encode('utf-8') if html else None

    @staticmethod
    def flush_percentage(decimal):
        """Update the last line in stdout to a percentage formatted value."""

        sys.stdout.write('%.2f%%\r' % (decimal * 100))
        sys.stdout.flush()

    @staticmethod
    def get_text_from_class(soup, name):
        obj = soup.find(class_=name)
        if obj != None:
            return obj.get_text().replace('\xa0', ' ').strip()
        else:
            return ''
