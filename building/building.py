from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

from building.map.map import Map

class BuildingManager:

    def __init__(self, client):
        self.client = client
        self.m = Map()

    def update(self):
        self.m.update_files()

    def upload(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        #Upload the JSON files to database through self.client and the os module
