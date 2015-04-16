from collections import OrderedDict
import time
import os
import re
import json
import pymongo
import pprint

from map.map import Map

class BuildingManager:

    def __init__(self, client):
        self.client = client
        self.m = Map()

    def update(self):
        m.update_files()

    def upload(self):
        #Upload the JSON files to database through self.client and the os module
        pass
