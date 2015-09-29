import logging
import os
import sys

from .scrapers.coursefinder.main import CourseFinder
from .scrapers.utmtimetable.main import UTMTimetable
from .scrapers.utsctimetable.main import UTSCTimetable
from .scrapers.utsgtimetable.main import UTSGTimetable
from .scrapers.utsgcalendar.main import UTSGCalendar
from .scrapers.map.main import Map

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("uoftscrapers").addHandler(NullHandler())
