import requests
import http.cookiejar
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import os
import json
import tidylib
import shutil
from ..scraper import Scraper


class UTSGTimetable(Scraper):

    def __init__(self, output_location='.'):
        super().__init__('UTSG Timetable', output_location)

        self.host = 'http://www.artsandscience.utoronto.ca/ofr/timetable/'
        self.day_map = {
            'M': 'MONDAY',
            'T': 'TUESDAY',
            'W': 'WEDNESDAY',
            'R': 'THURSDAY',
            'F': 'FRIDAY',
            'S': 'SATURDAY'
        }
        self.s = requests.Session()
        self.terms = ["summer", "winter"]

    def run(self):
        for term in self.terms:
            year = 0
            data = self.get_sponsors(term)
            sponsors = data["sponsors"]

            if term == "summer":
                # 2015 summer counts as 2014 term
                year = data["year"] - 1
            else:
                year = data["year"]

            for sponsor in sponsors:
                self.logger.info('Scraping %s/%s.' % (term, sponsor.split('.')[0]))
                html = self.s.get('%s/%s/%s' % (self.host, term, sponsor)).text
                self.save('.html/%s/%s' % (str(year), sponsor),
                          html.encode('utf-8'))

                data = self.parse_sponsor(html, year, term, sponsor)

                for course in data:
                    self.save_json('%s/%s/%s' % (self.location, str(year),
                                   course["id"] + ".json"), course)
        shutil.rmtree('.html')
        self.logger.info('%s completed.' % self.name)

    def parse_sponsor(self, html, year, term, sponsor=''):
        document, errors = \
            tidylib.tidy_document(html, options={'numeric-entities': 1})

        soup = BeautifulSoup(document)

        table = soup.table

        trs = table.find_all("tr")[2:] \
            if 'assem' in sponsor else table.find_all("tr")[2:]

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
                    if colspan > 0:
                        for x in range(colspan):
                            tds.insert(i+1, soup.new_tag("td"))
                            i += 1

            if len(tds) >= 9:

                course_code = self.format_data(tds[0].get_text(),
                                               "([A-Z]{3}[0-9]{3}[HY]1)")

                if len(course_code) > 0:
                    course_info.append(current_course)

                    current_course = [
                        None,   # course code
                        None,   # name
                        OrderedDict([]),    # sections
                        []
                    ]

                    semester = tds[1].get_text().strip()
                    current_course[0] = course_code + semester

                    name = tds[2].get_text().split("\n")[0].strip()
                    current_course[1] = name

                section = self.format_data(tds[3].get_text(),
                                           "([LTP][0-9]{4})")

                if len(section) > 0:
                    current_section = section

                time = self.format_data(tds[5].get_text(),
                                        "([MTWRFS]{1,3}[0-9]{1,2}(?::[0-9]" +
                                        "{2})?(?:-[0-9]{1,2}(?::[0-9]{2})?)?)")

                location = self.format_data(tds[6].get_text(),
                                            "([A-Z]{2,4}[ ]?[0-9]{1,8})")

                instructors = tds[7].get_text().strip()

                if instructors.lower() == "tba":
                    instructors = ""

                if len(instructors) > 0:
                    instructors = instructors.split("/")
                    for i in range(len(instructors)):
                        instructors[i] = instructors[i].split(".")
                        instructors[i] = [x.strip() for x in instructors[i]]
                        instructors[i] = ' '.join(instructors[i])
                else:
                    instructors = []

                try:
                    if not isinstance(current_course[2][current_section],
                                      list):
                        current_course[2][current_section] = []
                except KeyError:
                    current_course[2][current_section] = []

                current_course[2][current_section].append({
                    'time': time,
                    'location': location,
                    'instructors': instructors
                })

            elif len(tds) == 6:
                if tds[0].get('colspan') == '6':

                    course_code = \
                        self.format_data(tds[0].get_text(),
                                         "([A-Z]{3}[0-9]{3}[HY]{1}1[YFS]{1})")
                    breadths = [int(x) for x in
                                re.findall("(?:\()([12345])(?:\))",
                                tds[0].get_text().strip())]
                    name = ''.join(tds[0].get_text()
                                   .replace("Categories ", ":")
                                   .replace("Categories:", ":").split(':')[1:]) \
                        .split(', Count')[0].strip()

                    if len(course_code) > 0:
                        course_info.append(current_course)
                        current_course = [
                            course_code,    # course code
                            name,   # name
                            OrderedDict([]),    # sections
                            breadths
                        ]
                else:
                    section = self.format_data(tds[0].get_text(),
                                               "([LTP][0-9]{4})")

                    if len(section) > 0:
                        current_section = section

                    time = self.format_data(tds[3].get_text(),
                                            "([MTWRFS]{1,3}[0-9]{1,2}" +
                                            "(?::[0-9]{2})?(?:-[0-9]{1,2}" +
                                            "(?::[0-9]{2})?)?)")

                    location = self.format_data(tds[4].get_text(),
                                                "([A-Z]{2,4}[ ]?[0-9]{1,8})")

                    instructors = tds[5].get_text().strip()

                    if instructors.lower() == "tba":
                        instructors = ""
                    else:
                        instructors = instructors.replace(".", "")

                    if len(instructors) > 0:
                        instructors = instructors.split("/")
                    else:
                        instructors = []

                    try:
                        if not isinstance(current_course[2][current_section],
                                          list):
                            current_course[2][current_section] = []
                    except KeyError:
                        current_course[2][current_section] = []

                    current_course[2][current_section].append({
                        'time': time,
                        'location': location,
                        'instructors': instructors
                    })

        course_info = course_info[1:] + [current_course]

        courses = []

        for course in course_info:

            if len(course) == 0:
                continue

            course_id = course[0]
            course_term = ""
            if term == "winter":
                if course[0][-1] in "FY":
                    course_id += str(year) + "9"
                    course_term = str(year) + " Fall"
                    if course[0][-1] == "Y":
                        course_term += " +"
                elif course[0][-1] == "S":
                    course_id += str(year + 1) + "1"
                    course_term = str(year + 1) + " Winter"
            elif term == "summer":
                if course[0][-1] == "Y":
                    course_id += str(year + 1) + "5"
                    course_term = str(year + 1) + " Summer Y"
                elif course[0][-1] in "FS":
                    course_id += str(year + 1) + "5" + course[0][-1]
                    if course_id[0][-1] == "F":
                        course_term = str(year + 1) + " Summer F"
                    elif course_id[0][-1] == "S":
                        course_term = str(year + 1) + " Summer S"

            course_code = course[0]

            level = int(course_code[3] + "00")



            sections = []
            for k in course[2]:

                code = k
                instructors = []
                time_data = []
                for x in course[2][k]:

                    if x["time"] != "":

                        instructors += x["instructors"]

                        location = x["location"]

                        # magic

                        days = re.findall("[MTWRFS]", x["time"])

                        time = ""
                        mob = re.search('\d', x["time"])
                        if mob:
                            time = x["time"][mob.start():]

                        hours = []
                        time = time.split('-')
                        for t in time:
                            if ":" in t:
                                t = t.split(':')
                                t = int(t[0]) + (int(t[1]) / 60)
                            else:
                                t = int(t)
                            if t >= 1 and t <= 8:
                                t += 12
                            hours.append(t)

                        if len(hours) == 1:
                            hours.append(hours[0] + 1)

                        for i in range(len(hours)):
                            if 1 <= hours[i] <= 8:
                                hours[i] += 12

                        for day_key in days:
                            day = self.day_map[day_key]

                            time_data.append(OrderedDict([
                                ("day", day),
                                ("start", hours[0]),
                                ("end", hours[1]),
                                ("duration", hours[1] - hours[0]),
                                ("location", location)
                            ]))

                instructors = list(set(instructors))

                course[2][k]
                data = OrderedDict([
                    ("code", code),
                    ("instructors", instructors),
                    ("times", time_data)
                ])

                sections.append(data)

            course = OrderedDict([
                ("id", course_id),
                ("code", course_code),
                ("level", level),
                ("campus", "UTSG"),
                ("term", course_term),
                ("meeting_sections", sections)
            ])

            courses.append(course)

        return courses

    def format_data(self, text, regex):
        text = re.search(regex, text.strip())
        if text is None:
            text = ""
        else:
            text = text.group(1)
        return text

    def save(self, name, data):
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        with open(name, "wb") as file:
            file.write(data)

    def save_json(self, name, data):
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        with open(name, "w+") as file:
            json.dump(data, file)

    def get_sponsors(self, term):
        html = self.s.get('%s/%s/index.html' % (self.host, term)).text

        soup = BeautifulSoup(html)

        title = soup.title.get_text().strip()

        year = -1
        year = int(re.search("([0-9]{4})", title).group(0))

        self.save('.html/%s/sponsors.html' % str(year), html.encode('utf-8'))

        sponsors = []
        for x in soup.find_all('a'):
            url = x.get('href')
            if ".htm" in url and "/" not in url:
                if "intensive" not in url:
                    sponsors.append(url)
        return {
            "year": year,
            "sponsors": sponsors
        }
