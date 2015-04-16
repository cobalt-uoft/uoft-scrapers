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
        pass

    def update_files(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
