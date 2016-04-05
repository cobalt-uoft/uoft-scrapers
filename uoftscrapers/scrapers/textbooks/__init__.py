import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os
import time
from pprint import pprint

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
            if 'MICHENER'  or 'CONTINUING STUDIES' in term.get_text():
                terms.remove(term)

        for term in terms[:1]:
            campus, term = term.get('value').split('|')
            payload = {
                'control': 'campus',
                'campus': campus,
                'term': term,
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
                    'term': term,
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
                        'term': term,
                        't': int(round(time.time() * 1000))
                    }
                    headers = {
                        'Referer': '%s/buy_courselisting.asp' % self.host
                    }

                    r = requests.get('%s/textbooks_xml.asp' % self.host,
                        params=payload, headers=headers)

                    sections = BeautifulSoup(r.text, "xml").find_all('section')

                    for section in sections:
                        all_sections.append({
                            'section_id': section.get('id'),
                            'section_code': section.get('name'),
                            'section_instructor': section.get('instructor'),
                            'course_code': course_name
                        })

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
            books = soup.find('tr', class_='book')

            for book in books:
                # TODO: scrape the books! :D
                pass

            done += 1
            self.logger.info('Scraped %s %s. (%s%%)' % (
                section['course_code'],
                section['section_code'],
                str(int((done / count) * 100))
            ))
