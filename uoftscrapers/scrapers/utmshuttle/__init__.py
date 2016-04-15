from ..scraper import Scraper
from bs4 import BeautifulSoup
import datetime
import json
import logging
import os
import re
import requests
import sys
import time

class UTMShuttle:
    """A scraper for the UTM shuttle bus schedule.

    The schedule is located at https://m.utm.utoronto.ca/shuttle.php.
    """

    host = "https://m.utm.utoronto.ca/shuttleByDate.php?year=%s&month=%s&day=%s"
    logger = logging.getLogger("uoftscrapers")
    s = requests.Session()

    @staticmethod
    def scrape(location=".", month=None):
        """Update the local JSON files for this scraper."""

        Scraper.logger.info("UTMShuttle initialized.")
        Scraper.ensure_location(location)

        if month is None:
            month = "04"  # TODO: get current month

        # TODO: pad month if needed and get year

        # TODO: do for all days in month
        html = UTMShuttle.get_schedule_html(UTMShuttle.host % ("2016", "04", "22"))
        json = UTMShuttle.parse_schedule_html(html)

        # TODO: output to files
        print(json)

        Scraper.logger.info("UTMShuttle completed.")

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

        return html.encode("utf-8")

    @staticmethod
    def parse_schedule_html(html):
        """Create JSON files from the HTML pages downloaded."""

        soup = BeautifulSoup(html, "html.parser")

        # Get date
        html_date = time.strptime(soup.find("h2").get_text().strip(), '%b %d %Y')
        date = time.strftime('%Y-%m-%d', html_date)

        # Get route data
        routes = {}
        for html_route_opt in soup.find(id="chooseRoute").find_all("option"):
            html_route_id = html_route_opt.get("value")
            html_route_times = soup.find(id=html_route_id).find_all("li")

            route_name = html_route_opt.get_text().strip().split(" @ ")

            times = []
            for html_time in html_route_times:
                html_time_text = html_time.get_text().strip().lower()

                time_rush_hour = "rush hour" in html_time_text
                time_no_overload = "no overload" in html_time_text

                html_time_clean = re.sub(' \*.*\*| (a|p)m', '', html_time_text).strip()

                times.append({
                    "time": "%sT%s" % (
                        date,
                        time.strftime("%H:%M:00-04:00", time.strptime(html_time_clean, "%I:%M"))
                    ),
                    "rush_hour": time_rush_hour,
                    "no_overload": time_no_overload
                })

            route_id = re.sub('\.|ROUTE| ', '', route_name[0].upper())
            route_stops = {
                "location": route_name[1],
                "building_id": "123",  # TODO: get building_id
                "times": times
            }

            if route_id in routes.keys():
                routes[route_id]["stops"].append(route_stops)
            else:
                routes[route_id] = {
                    "id": route_id,
                    "name": route_name[0],
                    "stops": [route_stops]
                }

        return {
            "date": date,
            "routes": [v for k, v in routes.items()]
        }
