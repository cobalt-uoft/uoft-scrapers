from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

from course.cal.calendar import Calendar
from course.coursefinder.coursefinder import Coursefinder
from course.timetable.timetable import Timetable

class CourseManager:

    def __init__(self, client):
        self.courses = client
        self.c = Calendar()
        self.cf = Coursefinder()
        self.t = Timetable()

    def update(self):
        self.c.update_files()
        self.cf.update_files()
        self.t.update_files()

    def upload(self):
        #upload the best possible schema by getting the most up to date
        #information from each scraper directory's JSON files
        pass
