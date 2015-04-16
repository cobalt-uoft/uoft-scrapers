from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

from course.course import CourseManager

from building.building import BuildingManager
from building.food import FoodManager

class Scraper:

    def __init__(self):
        self.client = pymongo.MongoClient(os.environ.get('MONGO_URL'))

    def run(self):
        self.refresh_courses()
        self.refresh_buildings()

    def refresh_courses(self):
        c = CourseManager(self.client)
        c.update()
        c.upload()

    def refresh_buildings(self):
        b = BuildingManager(self.client)
        b.update()
        b.upload()

        f = FoodManager(self.client)
        f.upload()

if __name__ == "__main__":
    s = Scraper()
    s.run()
