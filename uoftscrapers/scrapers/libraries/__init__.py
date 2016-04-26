from ..utils import Scraper
from bs4 import BeautifulSoup, NavigableString, Comment
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
                Scraper.save_json(
                    doc, location, library_link.split('/')[-1].upper())
                Scraper.logger.info(
                    'Scraped ' + library_link.split('/')[-1].upper() + '.')
            else:
                # Not a real library page
                Scraper.logger.info(
                    'Skipped ' + library_link.split('/')[-1].upper() + '.')

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
    def convert_time(time_str):
        end = len(time_str)
        if 'am' in time_str:
            end = time_str.index('am') + 2
        elif 'pm' in time_str:
            end = time_str.index('pm') + 2
        time_str = time_str[:end]
        hour_tks = time_str[:-2].split(':')
        meridiem = time_str[-2:]
        hours = int(hour_tks[0])
        minutes = 0
        if len(hour_tks) > 1:
            minutes = int(hour_tks[1])
        if (meridiem == 'pm'):
            if (int(hours) != 12):
                hours = int(hours) + 12
        posix_from_midnight = hours*60*60 + minutes*60
        return posix_from_midnight

    @staticmethod
    def get_library_hours(calendar_link):
        weekdays = ['sunday', 'monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday']
        html = Scraper.get(calendar_link, max_attempts=1)
        week = ['Closed'] * 7
        if html is not None:
            soup = BeautifulSoup(html, 'html.parser')
            if soup.select('.calendar-wrapper') != []:
                week = soup.select('.calendar-wrapper')[0].select(
                    '.start-week')[1].select('.start-day')
                week = list(map(Libraries.normalize_text_sections, week))
        hours = OrderedDict()
        week = [day[1:].strip() for day in week]
        for day in range(len(weekdays)):
            hour = week[day]
            closed = not hour.startswith('Open')
            opening_hour = 0
            closing_hour = 0
            if not closed:
                hour_tks = hour.replace('Open:', '').split('-')
                opening_hour = Libraries.convert_time(hour_tks[0])
                closing_hour = Libraries.convert_time(hour_tks[1])
            hours[weekdays[day]] = OrderedDict([
                ('closed', closed),
                ('open', opening_hour),
                ('close', closing_hour)
            ])
        return hours

    @staticmethod
    def get_library_doc(url_tail):
        _id = url_tail.split('/')[-1].upper()

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
        library_collection_strengths = ''
        library_how_to_access = ''

        for i in range(len(library_info_titles)):
            if library_info_titles[i] == 'About the library':
                library_about = library_info_texts[i]
            elif library_info_titles[i] == 'Collection strengths':
                library_collection_strengths = library_info_texts[i].replace(
                    '  ', ', ')
            elif library_info_titles[i] == 'How to access':
                library_how_to_access = library_info_texts[i]

        doc = OrderedDict([
            ('id', _id),
            ('name', library_name),
            ('image', library_image),
            ('website', library_website),
            ('address', library_address),
            ('phone', library_phone),
            ('about', library_about),
            ('collection_strengths', library_collection_strengths),
            ('access', library_how_to_access),
            ('hours', library_hours)
        ])
        return doc
