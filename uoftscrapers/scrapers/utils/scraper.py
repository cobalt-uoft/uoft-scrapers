from time import sleep
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

        with open('%s/%s.json' % (location, filename), 'w+') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def get(url, params=None, cookies=None, headers=None, json=False, max_attempts=10, timeout=5):
        """Fetches an Internet document, automatically retrying if it times out."""

        doc = None
        attempts = 0
        while doc is None and attempts < max_attempts:
            try:
                r = Scraper.s.get(url, params=params, cookies=cookies,
                    headers=headers, timeout=5)
                if r.status_code == 200:
                    doc = r
                else:
                    attempts += 1
                    sleep(0.5)
                    continue
            except (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.InvalidSchema,
                    requests.exceptions.MissingSchema):
                attempts += 1
                continue

        if doc is None:
            return None

        if json:
            return doc.json()
        else:
            return doc.text.encode('utf-8')

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
