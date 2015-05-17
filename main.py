from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

from course.course import CourseManager
from building.building import BuildingManager
from food.food import FoodManager


class Scraper:

    def __init__(self):
        with open('config.json') as data_file:
            self.config = json.load(data_file)

        self.db = pymongo.MongoClient(self.config["MONGO_URL"])

    def run(self):
        self.refresh_buildings()
        self.refresh_foods()
        #self.refresh_courses()

    def refresh_courses(self):
        c = CourseManager(self.db.cobalt)
        c.update()
        c.upload()

    def refresh_buildings(self):
        b = BuildingManager(self.db.cobalt)
        b.update()
        b.upload()

    def refresh_foods(self):
        f = FoodManager(self.db.cobalt)
        f.update()
        f.upload()

if __name__ == "__main__":
    s = Scraper()
    s.run()
