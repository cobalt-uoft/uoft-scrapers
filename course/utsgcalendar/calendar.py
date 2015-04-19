import requests, http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import re
import json
import os
import pymongo

class UTSGCalendar:

    def __init__(self):
        self.host = 'http://www.artsandscience.utoronto.ca/ofr/calendar/'
        
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists('json'):
            os.makedirs('json')

    def update_files(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
