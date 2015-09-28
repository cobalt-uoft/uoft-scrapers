import os
import sys

from scrapers.coursefinder.main import Coursefinder
from scrapers.utmtimetable.main import UTMTimetable
from scrapers.utsctimetable.main import UTSCTimetable
from scrapers.utsgtimetable.main import UTSGTimetable
from scrapers.utsgcalendar.main import UTSGCalendar
from scrapers.map.main import Map


class UofTScrapers:
    """Static class wrapping all the scrapers."""

    def scrape_all():
        scrape_cf()
        scrape_utmt()
        scrape_utsct()
        scrape_utsgt()
        scrape_utsgc()
        scrape_m()

    def scrape_cf():
        cf = Coursefinder()
        cf.update_files()

    def scrape_utmt():
        utmt = UTMTimetable()
        utmt.update_files()

    def scrape_utsct():
        utsct = UTSCTimetable()
        utsct.update_files()

    def scrape_utsgt():
        utsgt = UTSGTimetable()
        utsgt.update_files()

    def scrape_utsgc():
        utsgc = UTSGCalendar()
        utsgc.update_files()

    def scrape_m():
        m = Map()
        m.update_files()


if __name__ == "__main__":
    args = [x.lower() for x in sys.argv]

    if 'all' in args:
        UofTScrapers.scrape_all()
    else:
        for x in args:
            if x == 'coursefinder':
                UofTScrapers.scrape_cf()
            elif x == 'utmtimetable':
                UofTScrapers.scrape_utmt()
            elif x == 'utsctimetable':
                UofTScrapers.scrape_utsct()
            elif x == 'utsgtimetable':
                UofTScrapers.scrape_utsgt()
            elif x == 'utsgcalendar':
                UofTScrapers.scrape_utsgc()
            elif x == 'map':
                UofTScrapers.scrape_m()

    print("Finished.", flush=True)
