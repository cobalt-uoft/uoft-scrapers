from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

import buildings
import courses

class Scraper:

    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get('MONGO_URL'))

    def run(self):
        self.update_courses()
        self.update_buildings()

    def update_courses(self):
        c = CourseManager(self.client)
        c.update()
        c.upload()

    def update_buildings(self):
        b = BuildingManager(self.client)
        b.update()
        b.upload()
