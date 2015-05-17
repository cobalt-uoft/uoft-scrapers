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
        # Upload the JSON files to database through self.client
        # and the os module
        print('Emptying building collection...')
        self.client.buildings.remove({})

        print('Pushing building data...')
        for root, dirs, files in os.walk("map/json"):
            for file in files:
                with open('map/json/%s' % file, 'r') as fp:
                    data = json.load(fp)
                    print(data['name'])
                    self.client.buildings.insert(data, True)
        print('Buildings updated!')