from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

from building.map.map import Map

class FoodManager:

    def __init__(self, client):
        self.client = client
        self.m = Map()

    def update(self):
        #The below should already have been called from building.py
        #m.update_files()
        pass

    def upload(self):
        #Upload the JSON files to database through self.client and the os module
        pass
