from ..scraper import Scraper
from bs4 import BeautifulSoup
import http.cookiejar
import json
import logging
import os
import re
import requests
import sys

class UTMShuttle:
    """A scraper for the UTM shuttle bus schedule.

    The schedule is located at https://m.utm.utoronto.ca/shuttle.php.
    """

    host = 'https://m.utm.utoronto.ca/shuttleByDate.php?year=%s&month=%s&day=%s'
    logger = logging.getLogger("uoftscrapers")
    cookies = http.cookiejar.CookieJar()
    s = requests.Session()
    threads = 32

    @staticmethod
    def scrape(location='.'):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info('UTMShuttle initialized.')
        Scraper.ensure_location(location)

        html = UTMShuttle.get_schedule_html(UTMShuttle.host % ('2016', '04', '22'))

        UTMShuttle.parse_course_html(html)

    @staticmethod
    def get_schedule_html(url):
        """Update the locally stored schedule pages."""

        html = None
        while html is None:
            try:
                r = UTMShuttle.s.get(url)
                if r.status_code == 200:
                    html = r.text
            except (requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError):
                continue

        return html.encode('utf-8')

    @staticmethod
    def parse_course_html(html):
        """Create JSON files from the HTML pages downloaded."""

        soup = BeautifulSoup(html, "html.parser")

        # get options (routes): names and corresponding ul ids
        routes = {}
        for route in soup.find(id="chooseRoute").find_all("option"):
            route_id = route.get('value')

            route_times = soup.find(id=route_id).find_all("li")

            routes[route_id] = {
                'name': route.get_text().strip(),
                'times': [time.get_text().strip() for time in route_times]
            }


        print(routes)

