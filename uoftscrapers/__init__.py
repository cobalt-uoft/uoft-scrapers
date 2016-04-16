import logging
import os
import sys


from .scrapers.coursefinder import CourseFinder

from .scrapers.buildings import Buildings

from .scrapers.textbooks import Textbooks

from .scrapers.food import Food

from .scrapers.calendar import Calendar
from .scrapers.calendar.utsg import UTSGCalendar
from .scrapers.calendar.utm import UTMCalendar
from .scrapers.calendar.utsc import UTSCCalendar

from .scrapers.timetable.utm import UTMTimetable
from .scrapers.timetable.utsc import UTSCTimetable
from .scrapers.timetable.utsg import UTSGTimetable

from .scrapers.exams import Exams
from .scrapers.exams.utsg import UTSGExams
from .scrapers.exams.utm import UTMExams
from .scrapers.exams.utsc import UTSCExams

from .scrapers.parking import Parking

from .scrapers.utmshuttle import UTMShuttle


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("uoftscrapers").addHandler(NullHandler())
