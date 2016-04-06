import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os
import time
from pprint import pprint
import re

class Textbooks(Scraper):
    """A scraper for UofT's book store.

    UofT Book Store is located at http://uoftbookstore.com/.
    """

    def __init__(self, output_location='.'):
        super().__init__('Textbooks', output_location)

        self.host = 'http://uoftbookstore.com'

    def run(self):
        """Update the local JSON files for this scraper."""

        all_sections = []

        r = requests.get('%s/buy_courselisting.asp' % self.host)

        listing = BeautifulSoup(r.text, "html.parser")
        terms = listing.find(id='fTerm').find_all('option')[1:]

        for term in terms:
            if 'MICHENER' or 'CONTINUING STUDIES' or 'MEDICAL' in term.get_text():
                terms.remove(term)

        for term in terms[:1]:
            campus, term_id = term.get('value').split('|')
            payload = {
                'control': 'campus',
                'campus': campus,
                'term': term_id,
                't': int(round(time.time() * 1000))
            }
            headers = {
                'Referer': '%s/buy_courselisting.asp' % self.host
            }

            r = requests.get('%s/textbooks_xml.asp' % self.host,
                params=payload, headers=headers)

            departments = BeautifulSoup(r.text, "xml").find_all('department')

            for department in departments[:1]:
                dept_id = department.get('id')
                dept_name = department.get('name').title()
                self.logger.info('Retrieving section info from %s.' % dept_name)
                payload = {
                    'control': 'department',
                    'dept': dept_id,
                    'term': term_id,
                    't': int(round(time.time() * 1000))
                }
                headers = {
                    'Referer': '%s/buy_courselisting.asp' % self.host
                }

                r = requests.get('%s/textbooks_xml.asp' % self.host,
                    params=payload, headers=headers)

                courses = BeautifulSoup(r.text, "xml").find_all('course')

                for course in courses[:1]:
                    course_id = course.get('id')
                    course_name = course.get('name')
                    payload = {
                        'control': 'course',
                        'course': course_id,
                        'term': term_id,
                        't': int(round(time.time() * 1000))
                    }
                    headers = {
                        'Referer': '%s/buy_courselisting.asp' % self.host
                    }

                    r = requests.get('%s/textbooks_xml.asp' % self.host,
                        params=payload, headers=headers)

                    sections = BeautifulSoup(r.text, "xml").find_all('section')

                    for section in sections[:1]:
                        term_name = term.get_text()
                        m = re.search('(\d{5})', term_name)
                        session = m.group(0)

                        all_sections.append({
                            'section_id': section.get('id'),
                            'section_code': section.get('name'),
                            'section_instructor': section.get('instructor'),
                            'course_code': course_name,
                            'session': session
                        })

        all_books = []

        count = len(all_sections)
        done = 0

        for section in all_sections:
            payload = {
                'control': 'section',
                'section': section['section_id'],
                't': int(round(time.time() * 1000))
            }
            headers = {
                'Referer': '%s/buy_courselisting.asp' % self.host
            }

            r = requests.get('%s/textbooks_xml.asp' % self.host,
                params=payload, headers=headers)

            soup = BeautifulSoup(r.text, "html.parser")
            books = soup.find_all('tr', { 'class': 'book' })

            if books == None:
                done += 1
                continue

            for book in books:
                if len(book.get_text().strip()) == 0:
                    continue

                image = book.find(class_='book-cover').img.get('src')
                image = 'http://uoftbookstore.com/%s' % image
                image = image.replace('Size=M', 'Size=L')

                # This doesn't mean "avoid textbooks with no image"
                # This is a case when the textbook is called "No required text"
                if 'not_available_' in image:
                    continue

                title = self.get_text_from_class(book, 'book-title')
                edition = self.get_text_from_class(book, 'book-edition')
                author = self.get_text_from_class(book, 'book-author')
                isbn = self.get_text_from_class(book, 'isbn')
                required = self.get_text_from_class(book, 'book-req')
                required = required == 'Required'
                price = self.get_text_from_class(book, 'book-price-list')
                price = float(price[1:])

                instructor = section['section_instructor'].split(',')
                if len(instructor) == 2:
                    instructor = '%s %s' % (instructor[0][0], instructor[1].strip())
                else:
                    instructor = None

                meeting_sections = [OrderedDict([
                    ("code", section['section_code']),
                    ("instructors", [instructor])
                ])]

                course_id = '%s%s' % (section['course_code'], section['session'])

                courses = [OrderedDict([
                    ("id", course_id),
                    ("code", section['course_code']),
                    ("required", required),
                    ("meeting_sections", meeting_sections)
                ])]

                textbook = OrderedDict([
                    ("id", isbn),
                    ("title", title),
                    ("edition", edition),
                    ("author", author),
                    ("image", image),
                    ("price", price),
                    ("courses", courses)
                ])

                print(json.dumps(textbook))

            done += 1
            self.logger.info('Scraped %s %s. (%s%%)' % (
                section['course_code'],
                section['section_code'],
                str(int((done / count) * 100))
            ))

    def get_text_from_class(self, soup, name):
        obj = soup.find(class_=name)
        if obj != None:
            return obj.get_text().replace('\xa0', ' ')
        else:
            return ''
