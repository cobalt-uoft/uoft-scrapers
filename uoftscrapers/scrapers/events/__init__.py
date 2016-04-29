from ..utils import Scraper
from bs4 import BeautifulSoup, NavigableString, Comment
from collections import OrderedDict
from datetime import datetime, date
from urllib.parse import urlencode
import re
import urllib.parse as urlparse


class Events:
    """A scraper for Events at the University of Toronto."""
    host = 'https://www.events.utoronto.ca/'

    campuses_tags = {'St. George': 'UTSG', 'U of T Mississauga': 'UTM',
                     'U of T Scarborough': 'UTSC'}

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Events initialized.')
        Scraper.ensure_location(location)

        for event in Events.get_events_list():
            doc = Events.get_event_doc(event[0], event[1])
            Scraper.save_json(doc, location, doc['id'])

        Scraper.logger.info('Events completed.')

    @staticmethod
    def get_events_list():
        page_index_url = Events.host + 'index.php'
        url_parts = list(urlparse.urlparse(page_index_url))
        events_links, events_dates = [], []
        paging_index = 1
        events_count = 10

        while events_count == 10:
            params = {
                'p': paging_index
            }
            url_parts[4] = urlencode(params)
            paging_index += 1
            html = Scraper.get(urlparse.urlunparse(url_parts))
            soup = BeautifulSoup(html, 'html.parser')
            events_dom_arr = soup.select('#results')[0].find_all('li')
            events_count = len(events_dom_arr)
            events_links += list(map(lambda e: e.a['href'], events_dom_arr))
            events_dates += list(map(lambda e: e.find('p').text.split(' : ')[1].split(', ')[0], events_dom_arr))

        return zip(events_links, events_dates)

    @staticmethod
    def convert_time(time_str):
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
        paragraph = paragraph.replace('  ', ' ')
        paragraph = paragraph.strip()
        return paragraph

    @staticmethod
    def get_event_doc(url_tail, event_date):
        event_url = Events.host + url_tail
        html = Scraper.get(event_url)
        url_parts = list(urlparse.urlparse(event_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        soup = BeautifulSoup(html, 'html.parser')

        event_id = query['eventid']
        event_title = soup.select('.eventTitle')[0].text.strip()

        date_arr = event_date.split(' - ')

        start_date = date_arr[0].strip()
        end_date = start_date if len(date_arr) == 1 else date_arr[1].strip()

        if start_date.count(' ') == 1:
            # year not in start date
            start_date = '%s %s' % (start_date, end_date[-4:])

        start_date = datetime.strptime(start_date, '%b %d %Y')
        end_date = datetime.strptime(end_date, '%b %d %Y')

        event_start_date = start_date.date().isoformat()
        event_end_date = end_date.date().isoformat()

        raw_time = soup.select('.date')[0].text.split(',')

        time_arr = re.split(' - | ', raw_time[1].strip())

        # Some of the strings are misformed and gives an extra empty space
        time_arr = list(filter(None, time_arr))

        event_start_str = time_arr[0]
        event_end_str = time_arr[-2] + time_arr[-1]
        if (len(time_arr) == 3):
            event_start_str += time_arr[-1]
        else:
            event_start_str += time_arr[1]

        event_start_time = Events.convert_time(event_start_str)
        event_end_time = Events.convert_time(event_end_str)

        event_duration = event_end_time - event_start_time

        evt_bar = soup.select('#evt_bar')[0]
        event_url = evt_bar.select('dd')[1].a['href']
        event_price = evt_bar.select('dl')[1].dd.text

        event_campus = ''
        if evt_bar.select('dd')[0].b is not None:
            campus_full_name = evt_bar.select('dd')[0].b.text
            event_campus = Events.campuses_tags[campus_full_name]

        event_address = ''
        address_block = evt_bar.select('dd')[0]
        if address_block.a is not None:
            address_block = address_block.a
        event_address = Events.normalize_text_sections(address_block)

        event_audiences = list(
            map(lambda a: a.text, evt_bar.select(
                'dl')[1].select('dd')[1].select('a')))

        soup.select('.eventTitle')[0].extract()
        soup.select('.date')[0].extract()
        evt_bar.extract()
        soup.select('#cal_bar')[0].extract()
        event_description = Events.normalize_text_sections(
            soup.select('#content')[0])

        doc = OrderedDict([
            ('id', event_id),
            ('title', event_title),
            ('start_date', event_start_date),
            ('end_date', event_end_date),
            ('start_time', event_start_time),
            ('end_time', event_end_time),
            ('duration', event_duration),
            ('url', event_url),
            ('description', event_description),
            ('admission_price', event_price),
            ('campus', event_campus),
            ('location', event_address),
            ('audiences', event_audiences)
        ])
        return doc
