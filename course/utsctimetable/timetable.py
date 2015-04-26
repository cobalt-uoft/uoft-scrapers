import requests
import http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import re
import os
import json
import pprint
import tidylib


class UTSCTimetable:

    def __init__(self):
        self.host = \
            'http://www.utsc.utoronto.ca/~registrar/scheduling/timetable'

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists('json'):
            os.makedirs('json')

    def update_files(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
