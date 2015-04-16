from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

class CourseScraper:

    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
        self.courses = {
            '2014': self.client['cobalt'].courses_2014,
            '2015': self.client['cobalt'].courses_2015
        }
        pass

    def upload(self):
        year = 2015

        for (dirpath, dirnames, filenames) in os.walk('course-timetable/json/%s' % str(year)):
            for filename in filenames[2:500]:
                file1 = open('course-timetable/json/%s/%s' % (str(year), filename), 'r')
                timetable_data = json.loads(file1.read())
                file2 = open('calendar/json/%s.json' % filename[:8], 'r')
                calendar_data = json.loads(file2.read())
                print(calendar_data)
                #print('%s.json' % filename[:8])
