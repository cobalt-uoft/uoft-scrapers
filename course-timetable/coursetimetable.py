import requests, http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import re
import json
import pymongo
import pprint
import tidylib


class CourseTimetable:

    def __init__(self, season):
        self.host = 'http://www.artsandscience.utoronto.ca/ofr/timetable/%s' % season
        self.s = requests.Session()
        self.year = 2014
        self.sponsors = []

    def parse_sponsor(self, sponsor):
        with open('html/%s' % sponsor) as f:
            html = f.read()

        document, errors = tidylib.tidy_document(html,
    options={'numeric-entities':1})

        soup = BeautifulSoup(document)

        table = soup.table

        trs = table.find_all("tr")[2:] if 'assem' in sponsor else table.find_all("tr")[3:]

        course_info = []

        current_course = []

        current_code = ""

        current_breadths = []

        current_section = None

        for tr in trs:

            if "Cancel" in tr.get_text():
                continue

            tds = tr.find_all("td")

            i = 0
            while i < len(tds):
                colspan = tds[i].get('colspan')
                if colspan is None:
                    i += 1
                    continue
                else:
                    colspan = int(colspan) - 1
                    if colspan > 1:
                        for x in range(colspan):
                            tds.insert(i+1, soup.new_tag("td"))
                            i += 1

            if len(tds) in [9, 10]:

                course_code = self.format_data(tds[0].get_text(), "([A-Z]{3}[0-9]{3}[HY]1)")

                if len(course_code) > 0:
                    course_info.append(current_course)

                    current_course = [
                        None, # course code
                        None, # name
                        {}, # sections
                        breadths
                    ]

                    semester = tds[1].get_text().strip()
                    current_course[0] = course_code + semester

                    name = tds[2].get_text().split("\n")[0].strip()
                    current_course[1] = name

                section = self.format_data(tds[3].get_text(),"([LTP][0-9]{4})")

                if len(section) > 0:
                    current_section = section

                time = self.format_data(tds[5].get_text(), "([MTWRFS]{1,3}[0-9]{1,2}(?::[0-9]{2})?(?:-[0-9]{1,2}(?::[0-9]{2})?)?)")

                location = self.format_data(tds[6].get_text(), "([A-Z]{2,4}[ ]?[0-9]{1,8})")

                instructors = tds[7].get_text().strip()

                if instructors.lower() == "tba":
                    instructors = ""
                else:
                    instructors = instructors.replace(".", "")

                if len(instructors) > 0:
                    instructors = instructors.split("/")
                else:
                    instructors = []

                current_course[2][current_section] = {
                    'time': time,
                    'location': location,
                    'instructors': instructors
                }

            elif len(tds) == 6:
                if tds[0].get('colspan') == '6':

                    course_code = self.format_data(tds[0].get_text(), "([A-Z]{3}[0-9]{3}[HY]{1}1[YFS]{1})")
                    breadths = [int(x) for x in re.findall("(?:\()([12345])(?:\))", tds[0].get_text().strip())]
                    name = ''.join(tds[0].get_text().replace("Categories ", ":").replace("Categories:", ":").split(':')[1:]).split(', Count')[0].strip()

                    if len(course_code) > 0:
                        course_info.append(current_course)
                        current_course = [
                            course_code, # course code
                            name, # name
                            {}, # sections
                            breadths
                        ]
                else:
                    section = self.format_data(tds[0].get_text(),"([LTP][0-9]{4})")

                    if len(section) > 0:
                        current_section = section

                    time = self.format_data(tds[3].get_text(), "([MTWRFS]{1,3}[0-9]{1,2}(?::[0-9]{2})?(?:-[0-9]{1,2}(?::[0-9]{2})?)?)")

                    location = self.format_data(tds[4].get_text(), "([A-Z]{2,4}[ ]?[0-9]{1,8})")

                    instructors = tds[5].get_text().strip()

                    if instructors.lower() == "tba":
                        instructors = ""
                    else:
                        instructors = instructors.replace(".", "")

                    if len(instructors) > 0:
                        instructors = instructors.split("/")
                    else:
                        instructors = []

                    current_course[2][current_section] = {
                        'time': time,
                        'location': location,
                        'instructors': instructors
                    }



        course_info = course_info[1:] + [current_course]

        pprint.pprint(course_info)
        print(len(course_info))


    def format_data(self, text, regex):
        text = re.search(regex, text.strip())
        if text is None:
            text = ""
        else:
            text = text.group(1)
        return text

    def save(self, name, data):
        with open(name, "wb") as file:
            file.write(data)

    def save_sponsors(self):
        for x in self.sponsors:
            html = self.s.get('%s/%s' % (self.host, x)).text
            self.save('html/%s' % x, html.encode('utf-8'))

    def get_sponsors(self):
        html = self.s.get('%s/sponsors.htm' % self.host).text
        self.save('html/sponsors.html', html.encode('utf-8'))

        soup = BeautifulSoup(html)

        self.year = int(re.search("([0-9]{4})-[0-9]{4}", soup.title.get_text()).group(1))

        for x in soup.find_all('a'):
            url = x.get('href')
            if ".htm" in url and "/" not in url:
                self.sponsors.append(url)



ct = CourseTimetable("winter")
ct.get_sponsors()
#ct.save_sponsors()
ct.parse_sponsor('assem.html')
