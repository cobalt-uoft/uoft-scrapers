from ..utils import Scraper
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime, date
from collections import OrderedDict

class Libraries:
    """A scraper for the Libraries at the University of Toronto."""
    host = 'https://onesearch.library.utoronto.ca/'

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Libraries initialized.')
        Scraper.ensure_location(location)
        # using innis library as example
        return Libraries.get_library_doc(Libraries.get_library_link()[24])
        raise NotImplementedError('This scraper has not been implemented yet.')
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

    # TODO: This should probably a standard scraper function
    @staticmethod
    def normalize_text_sections(div):
        paragraph = ''
        for content in div.contents:
            text = content if type(content) == NavigableString else content.text
            paragraph += text.strip().replace('\r', '').replace('\n', ', ') + ' '
        paragraph = paragraph.strip()
        return paragraph

    @staticmethod
    def get_library_doc(url_tail):
        library_url = Libraries.host + url_tail
        html = Scraper.get(library_url)
        soup = BeautifulSoup(html, 'html.parser')
        main_content = soup.select('#content-inner')[0].select('.library-info')[0]

        library_name = main_content.h1.extract().text
        library_image = main_content.img.extract()['src']
        
        for content in main_content.select('.field-content'):
            content.extract()
        
        library_website = main_content.a.extract()['href']
        library_hours_link = main_content.a['href']

        library_address = Libraries.normalize_text_sections(
            main_content.select('.library-address')[0].extract())

        library_phone = '' 
        if main_content.select('.phone') != []:
            library_phone = main_content.select('.phone')[0].extract().text.strip()

        library_info = main_content.select('.library-info-text')[0].extract()
        library_info_titles = [s.text for s in  library_info.select('h2')]
        library_info_texts = library_info.select('p')

        library_about = ''
        library_collection_strenghts = ''
        library_how_to_access = ''

        for i in range(len(library_info_titles)):
            if library_info_titles[i] == 'About the library':
                library_about = Libraries.normalize_text_sections(
                    library_info_texts[i])
            if library_info_titles[i] == 'Collection strengths':
                library_collection_strenghts = Libraries.normalize_text_sections(
                    library_info_texts[i])
            if library_info_titles[i] == 'How to access':
                library_how_to_access = Libraries.normalize_text_sections(
                    library_info_texts[i])

        doc = OrderedDict([
            ('name', library_name),
            ('image', library_image), 
            ('website', library_website),
            ('hours', library_hours_link),
            ('address', library_address),
            ('phone', library_phone),
            ('about', library_about),
            ('collection_strenghts', library_collection_strenghts),
            ('access', library_how_to_access)
        ])

        return doc
