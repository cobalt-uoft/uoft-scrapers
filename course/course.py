from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint


from course.coursefinder.coursefinder import Coursefinder

from course.utsgcalendar.calendar import UTSGCalendar
from course.utsgtimetable.timetable import UTSGTimetable

from course.utmtimetable.timetable import UTMTimetable

from course.utsctimetable.timetable import UTSCTimetable

class CourseManager:

    def __init__(self, client):
        self.courses = client
        self.cf = Coursefinder()
        self.utsg = {
            "calendar": UTSGCalendar(),
            "timetable": UTSGTimetable()
        }
        self.utm = {
            "timetable": UTMTimetable()
        }
        self.utsc = {
            "timetable": UTSCTimetable()
        }

    def update(self):
        self.cf.update_files()

        self.utsg["calendar"].update_files()
        self.utsg["timetable"].update_files()

        self.utm["timetable"].update_files()

        self.utsc["timetable"].update_files()

    def upload(self):
        #upload the best possible schema by getting the most up to date
        #information from each scraper directory's JSON files
        pass
