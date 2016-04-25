from ..utils import Scraper
from bs4 import BeautifulSoup, NavigableString, Comment
from datetime import datetime, date
from collections import OrderedDict


class Libraries:
    """A scraper for the Libraries at the University of Toronto."""
    host = 'https://onesearch.library.utoronto.ca/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Libraries initialized.')
        Scraper.ensure_location(location)

        for library_link in Libraries.get_library_link():
            doc = Libraries.get_library_doc(library_link)
            if (doc is not None):
                Scraper.save_json(doc, location, library_link.split('/')[-1])
            else:
                # Not a real library page
                Scraper.logger.info('Skipped: ' + library_link.split('/')[-1])
        Scraper.logger.info('Libraries completed.')

    @staticmethod
    def get_library_link():
        vist_libraries_url = Libraries.host + 'visit'
        html = Scraper.get(vist_libraries_url)
        soup = BeautifulSoup(html, 'html.parser')
        list_obj_arr = soup.select('.view-list-of-libraries')[1].select(
            '.view-content')[0].select('.views-row')
        library_links = [l.a['href'] for l in list_obj_arr]
        return library_links

    @staticmethod
    def normalize_text_sections(div):
        paragraph = ''
        for content in div.contents:
            text = ''
            if type(content) == NavigableString:
                text = content
            elif type(content) == Comment:
                pass
            elif content.name == 'li':
                text = content.text
            else:
                text = content.text
            text = text.strip()
            paragraph += text.strip() + ' '
        paragraph = paragraph.strip()
        paragraph = paragraph.replace('\r', '')
        paragraph = paragraph.replace('\n', ', ')
        paragraph = paragraph.strip()
        return paragraph

    @staticmethod
    def get_library_hours(calendar_link):
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        html = Scraper.get(calendar_link, max_attempts=5)
        week = []
        if html is None:
            week = ['Hours are not available, please contact the library.'] * 7
        else:
            soup = BeautifulSoup(html, 'html.parser')
            if soup.select('.calendar-wrapper') != []:
                week = soup.select('.calendar-wrapper')[0].select(
                    '.start-week')[1].select('.start-day')
                week = list(map(Libraries.normalize_text_sections, week))
            else:
                week = ['Hours are not available, login required.'] * 7
        hours = OrderedDict()
        for day in range(len(weekdays)):
            hour = week[day]
            hours[weekdays[day]] = hour
        return hours

    @staticmethod
    def get_library_doc(url_tail):
        library_url = Libraries.host + url_tail
        html = Scraper.get(library_url)
        soup = BeautifulSoup(html, 'html.parser')
        main_content = soup.select('#content-inner')[0].select('.library-info')

        if main_content == []:
            return None
        else:
            main_content = main_content[0]

        library_name = main_content.h1.extract().text

        library_image = ''
        if main_content.img is not None:
            library_image = main_content.img.extract()['src']

        for content in main_content.select('.field-content'):
            content.extract()

        library_website = main_content.a.extract()['href']

        library_hours_link = main_content.a['href']
        library_hours = Libraries.get_library_hours(library_hours_link)
        for day, hour in library_hours.items():
            library_hours[day] = hour[1:].strip()

        library_address = ''
        if main_content.select('.library-address') != []:
            library_address = Libraries.normalize_text_sections(
                main_content.select('.library-address')[0].extract())

        library_phone = ''
        if main_content.select('.phone') != []:
            library_phone = main_content.select(
                '.phone')[0].extract().text.strip()

        library_info = main_content.select('.library-info-text')[0].extract()
        library_info_titles = [s.text for s in library_info.select('h2')]
        library_info_texts = []

        for content in library_info.contents:
            if type(content) != NavigableString:
                if content.name in ['p', 'ul', 'ol']:
                    library_info_texts.append(content)
        library_info_texts = list(
            map(Libraries.normalize_text_sections, library_info_texts))

        library_about = ''
        library_collection_strenghts = ''
        library_how_to_access = ''

        for i in range(len(library_info_titles)):
            if library_info_titles[i] == 'About the library':
                library_about = library_info_texts[i]
            elif library_info_titles[i] == 'Collection strengths':
                library_collection_strenghts = library_info_texts[i].replace(
                    '  ', ', ')
            elif library_info_titles[i] == 'How to access':
                library_how_to_access = library_info_texts[i]

        doc = OrderedDict([
            ('name', library_name),
            ('image', library_image),
            ('website', library_website),
            ('hours', library_hours),
            ('address', library_address),
            ('phone', library_phone),
            ('about', library_about),
            ('collection_strenghts', library_collection_strenghts),
            ('access', library_how_to_access)
        ])
        return doc
