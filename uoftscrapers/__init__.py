import logging
import os
import sys

from .scrapers.coursefinder.main import Coursefinder
from .scrapers.utmtimetable.main import UTMTimetable
from .scrapers.utsctimetable.main import UTSCTimetable
from .scrapers.utsgtimetable.main import UTSGTimetable
from .scrapers.utsgcalendar.main import UTSGCalendar
from .scrapers.map.main import Map

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

def scrape_map():
    m = Map()
    m.update_files()

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())
