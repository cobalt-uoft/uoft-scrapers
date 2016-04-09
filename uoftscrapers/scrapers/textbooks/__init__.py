import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
from ..scraper import Scraper
import os
import time
from pprint import pprint
import re
from queue import Queue
from threading import Thread


class TextbooksWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            download_link(directory, link)
            self.queue.task_done()


class Textbooks(Scraper):
    """A scraper for UofT's book store.

    UofT Book Store is located at http://uoftbookstore.com/.
    """


    def __init__(self, output_location='.'):
        super().__init__('Textbooks', output_location)

        self.host = 'http://uoftbookstore.com'


    def run(self):
        """Update the local JSON files for this scraper."""

        terms = self.retrieve_terms()
        departments = self.retrieve_departments(terms)[:3]
        courses = self.retrieve_courses(departments)
        sections = self.retrieve_sections(courses)
        books = self.retrieve_books(sections)

        queue = Queue()
        for x in range(8):
            worker = TextbooksWorker(queue)
            worker.daemon = True
            worker.start()

        for link in links:
            logger.info('Queueing {}'.format(link))
            queue.put((download_dir, link))
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()


        for book in books:
            with open('%s/%s.json' % (self.location, book['id']), 'w+') as outfile:
                json.dump(book, outfile)


    def retrieve_terms(self):
        r = requests.get('%s/buy_courselisting.asp' % self.host)

        listing = BeautifulSoup(r.text, "html.parser")
        terms = listing.find(id='fTerm').find_all('option')[1:]

        accepted_terms = []
        for term in terms:
            val = term.get_text()
            if val.startswith('ST GEORGE') or val.startswith('MISSISSAUGA') \
                or val.startswith('SCARBOROUGH'):
                accepted_terms.append(term)

        return accepted_terms

    def retrieve_departments(self, terms):
        all_departments = []

        done = 0
        count = len(terms)

        for term in terms:
            term_name = term.get_text()
            m = re.search('(\d{5})', term_name)
            session = m.group(0)

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
            for department in departments:
                all_departments.append({
                    'dept_id': department.get('id'),
                    'dept_name': department.get('name').title(),
                    'term_id': term_id,
                    'session': session
                })

            done += 1
            self.logger.info('(1/4)\t(%s%%)\tRetreived department info from %s.' % (
                str(int((done / count) * 100)),
                term_name
            ))

        return all_departments


    def retrieve_courses(self, departments):
        all_courses = []

        done = 0
        count = len(departments)

        for department in departments:
            payload = {
                'control': 'department',
                'dept': department['dept_id'],
                'term': department['term_id'],
                't': int(round(time.time() * 1000))
            }
            headers = {
                'Referer': '%s/buy_courselisting.asp' % self.host
            }

            r = requests.get('%s/textbooks_xml.asp' % self.host,
                params=payload, headers=headers)

            courses = BeautifulSoup(r.text, "xml").find_all('course')
            for course in courses:
                all_courses.append({
                    'course_id': course.get('id'),
                    'course_name': course.get('name'),
                    'term_id': department['term_id'],
                    'session': department['session']
                })

            done += 1
            self.logger.info('(2/4)\t(%s%%)\tRetreived course info from %s.' % (
                str(int((done / count) * 100)),
                department['dept_name']
            ))

        return all_courses


    def retrieve_sections(self, courses):
        all_sections = []

        done = 0
        count = len(courses)

        for course in courses:
            payload = {
                'control': 'course',
                'course': course['course_id'],
                'term': course['term_id'],
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
                    'course_code': course['course_name'],
                    'session': course['session']
                })

            done += 1
            self.logger.info('(3/4)\t(%s%%)\tRetreived section info from %s.' % (
                str(int((done / count) * 100)),
                course['course_name']
            ))

        return all_sections


    def retrieve_books(self, sections):
        all_books = {}

        count = len(sections)
        done = 0

        for section in sections:
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

                book_id = book.find(class_='product-field-pf_id').get('value')

                url = '%s/buy_book_detail.asp?pf_id=%s' % (self.host, book_id)

                title = self.get_text_from_class(book, 'book-title')

                edition = self.get_text_from_class(book, 'book-edition')
                if len(edition) > 0:
                    edition = ''.join(list(filter(str.isdigit, edition)))
                    try:
                        edition = int(edition)
                    except ValueError:
                        edition = 1
                if edition == '' or 0:
                    edition = 1

                author = self.get_text_from_class(book, 'book-author')
                m = re.search('([\d]+[E]?)', author)
                if m != None:
                    junk = m.group(0)
                    author = author.replace(junk, '').strip()

                isbn = self.get_text_from_class(book, 'isbn')
                requirement = self.get_text_from_class(book, 'book-req')
                requirement = requirement.lower()

                price = self.get_text_from_class(book, 'book-price-list')
                try:
                    price = float(price[1:])
                except ValueError:
                    price = 0

                instructor = section['section_instructor'].split(',')
                if len(instructor) == 2:
                    instructor = '%s %s' % (instructor[0][:1], instructor[1].strip())
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
                    ("requirement", requirement),
                    ("meeting_sections", meeting_sections)
                ])]

                textbook = OrderedDict([
                    ("id", book_id),
                    ("isbn", isbn),
                    ("title", title),
                    ("edition", edition),
                    ("author", author),
                    ("image", image),
                    ("price", price),
                    ("url", url),
                    ("courses", courses)
                ])

                if book_id in all_books:
                    index = -1
                    for i in range(len(all_books[book_id]['courses'])):
                        if courses[i]['id'] == book_id:
                            index = i
                            break
                    if index >= 0:
                        all_books[book_id]['courses'][index]['meeting_sections'] += meeting_sections
                    else:
                        all_books[book_id]['courses'] += courses
                else:
                    all_books[book_id] = textbook

            done += 1
            self.logger.info('(4/4)\t(%s%%)\tScraped %s %s.' % (
                str(int((done / count) * 100)),
                section['course_code'],
                section['section_code']
            ))

        return list(all_books.values())


    def get_text_from_class(self, soup, name):
        obj = soup.find(class_=name)
        if obj != None:
            return obj.get_text().replace('\xa0', ' ').strip()
        else:
            return ''
