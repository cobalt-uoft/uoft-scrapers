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
from threading import Thread, Lock
import logging
from operator import itemgetter

class Textbooks(Scraper):
    """A scraper for UofT's book store.

    UofT Book Store is located at http://uoftbookstore.com/.
    """

    host = 'http://uoftbookstore.com'
    logger = logging.getLogger("uoftscrapers")
    threads = 32

    def __init__(self, output_location='.'):
        super().__init__('Textbooks', output_location)

    def run(self):
        """Update the local JSON files for this scraper."""

        terms = self.retrieve_terms()
        departments = self.retrieve_departments(terms)

        # Get course info
        ts = time.time()
        queue = Queue()

        for x in range(Textbooks.threads):
            worker = CoursesWorker(queue)
            worker.daemon = True
            worker.start()

        Textbooks.logger.info('Queued %d departments.' % len(departments))
        for department in departments:
            queue.put(department)

        queue.join()
        Textbooks.logger.info('Took %.2fs to retreive course info.' % (time.time() - ts))

        # Get section info
        ts = time.time()
        queue = Queue()

        for x in range(Textbooks.threads):
            worker = SectionsWorker(queue)
            worker.daemon = True
            worker.start()

        Textbooks.logger.info('Queued %d courses.' % len(CoursesWorker.all_courses))
        for course in CoursesWorker.all_courses:
            queue.put(course)

        queue.join()
        Textbooks.logger.info('Took %.2fs to retreive section info.' % (time.time() - ts))

        # Get book info
        ts = time.time()
        queue = Queue()

        for x in range(Textbooks.threads):
            worker = BooksWorker(queue)
            worker.daemon = True
            worker.start()

        Textbooks.logger.info('Queued %d sections.' % len(SectionsWorker.all_sections))
        for section in SectionsWorker.all_sections:
            queue.put(section)

        queue.join()
        Textbooks.logger.info('Took %.2fs to retreive book info.' % (time.time() - ts))

        books = list(BooksWorker.all_books.values())

        for book in books:
            book['courses'] = sorted(book['courses'], key=itemgetter('id'))
            for i in range(len(book['courses'])):
                book['courses'][i]['meeting_sections'] = sorted(book['courses'][i]['meeting_sections'], key=itemgetter('code'))
            with open('%s/%s.json' % (self.location, book['id']), 'w+') as outfile:
                json.dump(book, outfile)

        self.logger.info('%s completed.' % self.name)

    @staticmethod
    def retrieve_terms():
        r = requests.get('%s/buy_courselisting.asp' % Textbooks.host)

        listing = BeautifulSoup(r.text, "html.parser")
        terms = listing.find(id='fTerm').find_all('option')[1:]

        accepted_terms = []
        for term in terms:
            val = term.get_text()
            if val.startswith('ST GEORGE') or val.startswith('MISSISSAUGA') \
                or val.startswith('SCARBOROUGH'):
                accepted_terms.append(term)

        return accepted_terms

    @staticmethod
    def retrieve_departments(terms):
        all_departments = []

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
                'Referer': '%s/buy_courselisting.asp' % Textbooks.host
            }

            r = requests.get('%s/textbooks_xml.asp' % Textbooks.host,
                params=payload, headers=headers)

            departments = BeautifulSoup(r.text, "xml").find_all('department')
            for department in departments:
                all_departments.append({
                    'dept_id': department.get('id'),
                    'dept_name': department.get('name').title(),
                    'term_id': term_id,
                    'session': session
                })

            Textbooks.logger.info('Retreived department info from %s.' % term_name)

        return all_departments

    @staticmethod
    def retrieve_courses(department):
        all_courses = []

        payload = {
            'control': 'department',
            'dept': department['dept_id'],
            'term': department['term_id'],
            't': int(round(time.time() * 1000))
        }
        headers = {
            'Referer': '%s/buy_courselisting.asp' % Textbooks.host
        }

        r = requests.get('%s/textbooks_xml.asp' % Textbooks.host,
            params=payload, headers=headers)

        courses = BeautifulSoup(r.text, "xml").find_all('course')
        for course in courses:
            all_courses.append({
                'course_id': course.get('id'),
                'course_name': course.get('name'),
                'term_id': department['term_id'],
                'session': department['session']
            })

        return all_courses

    @staticmethod
    def retrieve_sections(course):
        all_sections = []

        payload = {
            'control': 'course',
            'course': course['course_id'],
            'term': course['term_id'],
            't': int(round(time.time() * 1000))
        }
        headers = {
            'Referer': '%s/buy_courselisting.asp' % Textbooks.host
        }

        r = requests.get('%s/textbooks_xml.asp' % Textbooks.host,
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

        return all_sections

    @staticmethod
    def retrieve_books(section):
        all_books = []

        payload = {
            'control': 'section',
            'section': section['section_id'],
            't': int(round(time.time() * 1000))
        }
        headers = {
            'Referer': '%s/buy_courselisting.asp' % Textbooks.host
        }

        r = requests.get('%s/textbooks_xml.asp' % Textbooks.host,
            params=payload, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")
        books = soup.find_all('tr', { 'class': 'book' })

        if books == None:
            done += 1
            return []

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

            url = '%s/buy_book_detail.asp?pf_id=%s' % (Textbooks.host, book_id)

            title = Textbooks.get_text_from_class(book, 'book-title')

            edition = Textbooks.get_text_from_class(book, 'book-edition')
            if len(edition) > 0:
                edition = ''.join(list(filter(str.isdigit, edition)))
                try:
                    edition = int(edition)
                except ValueError:
                    edition = 1
            if edition == '' or 0:
                edition = 1

            author = Textbooks.get_text_from_class(book, 'book-author')
            m = re.search('([\d]+[E]?)', author)
            if m != None:
                junk = m.group(0)
                author = author.replace(junk, '').strip()

            isbn = Textbooks.get_text_from_class(book, 'isbn')
            requirement = Textbooks.get_text_from_class(book, 'book-req')
            requirement = requirement.lower()

            price = Textbooks.get_text_from_class(book, 'book-price-list')
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

            all_books.append(textbook)

        return all_books

    @staticmethod
    def get_text_from_class(soup, name):
        obj = soup.find(class_=name)
        if obj != None:
            return obj.get_text().replace('\xa0', ' ').strip()
        else:
            return ''


class CoursesWorker(Thread):

    all_courses = []
    lock = Lock()

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            department = self.queue.get()
            courses = Textbooks.retrieve_courses(department)

            CoursesWorker.lock.acquire()
            CoursesWorker.all_courses += courses
            CoursesWorker.lock.release()

            self.queue.task_done()


class SectionsWorker(Thread):

    all_sections = []
    lock = Lock()

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            course = self.queue.get()
            sections = Textbooks.retrieve_sections(course)

            SectionsWorker.lock.acquire()
            SectionsWorker.all_sections += sections
            SectionsWorker.lock.release()

            self.queue.task_done()


class BooksWorker(Thread):

    all_books = {}
    lock = Lock()

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            section = self.queue.get()
            books = Textbooks.retrieve_books(section)

            BooksWorker.lock.acquire()
            for book in books:
                if book['id'] in BooksWorker.all_books:
                    index = -1
                    for i in range(len(BooksWorker.all_books[book['id']]['courses'])):
                        if BooksWorker.all_books[book['id']]['courses'][i]['id'] == book['courses'][0]['id']:
                            index = i
                            break
                    if index >= 0:
                        BooksWorker.all_books[book['id']]['courses'][index]['meeting_sections'] += book['courses'][0]['meeting_sections']
                    else:
                        BooksWorker.all_books[book['id']]['courses'] += book['courses']
                else:
                    BooksWorker.all_books[book['id']] = book
            BooksWorker.lock.release()

            self.queue.task_done()
