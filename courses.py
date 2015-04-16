from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

class CourseManager:

    def __init__(self, client):
        self.courses = client

    def update(self):
        #Init all the course scraper classes, and update_files()

        #Calendar
        #Timetable
        #CourseFinder

        pass

    def upload(self):
        #upload the best possible schema by getting the most up to date
        #information from each scraper file

        year = 2015

        for (dirpath, dirnames, filenames) in os.walk('course-timetable/json/%s' % str(year)):
            for filename in filenames[2:500]:
                file1 = open('course-timetable/json/%s/%s' % (str(year), filename), 'r')
                timetable_data = json.loads(file1.read())
                file2 = open('calendar/json/%s.json' % filename[:8], 'r')
                calendar_data = json.loads(file2.read())
                print(calendar_data)
                #print('%s.json' % filename[:8])
