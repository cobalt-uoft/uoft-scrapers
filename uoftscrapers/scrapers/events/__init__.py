from ..scraper import Scraper
from bs4 import BeautifulSoup, NavigableString
from datetime import datetime, date
from collections import OrderedDict
import urllib.parse as urlparse
from urllib.parse import urlencode
import requests
import pytz
import json
import re

class Events:
    """A scraper for Events at the University of Toronto."""
    host = 'https://www.events.utoronto.ca/'
    s = requests.Session()

    @staticmethod
    def scrape(location='.'):
        Scraper.logger.info('Events initialized.')
        Scraper.ensure_location(location)

        def scrape_event(doc):
            Scraper.logger.info('Scraped event: %s ' % (
                doc['id'],
            ))
            with open('%s/%s.json' % (location, doc['id']), 'w') as fp: 
                json.dump(doc, fp)
       
        for event_link in Events.get_events_links():
            doc = Events.get_event_doc(event_link)
            scrape_event(doc)

        Scraper.logger.info('Events completed.')

    @staticmethod
    def get_events_links():
        page_index_url = Events.host + 'index.php'
        url_parts = list(urlparse.urlparse(page_index_url))
        events_links = []
        paging_index = 1
        events_count = 10 
        while(events_count == 10):
            params = {
                    'p': paging_index
                }
            url_parts[4] = urlencode(params)
            paging_index += 1
            html = Events.s.get(urlparse.urlunparse(url_parts)).text
            soup = BeautifulSoup(html, 'html.parser')
            events_dom_arr = soup.select('#results')[0].find_all('li')
            events_count = len(events_dom_arr)
            events_links += list(map(lambda e: e.a['href'], events_dom_arr))
        return(events_links)                

    @staticmethod
    def get_event_doc(url_tail):
        event_url = Events.host + url_tail
        html = Events.s.get(event_url).text
        url_parts = list(urlparse.urlparse(event_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        soup = BeautifulSoup(html, 'html.parser')

        event_id = query['eventid']
        event_title = soup.select('.eventTitle')[0].text.strip()
        raw_time = soup.select('.date')[0].text.split(',')
        
        date_arr = raw_time[0].split(' - ')
        time_arr = re.split(' - | ', raw_time[1].strip())
        
        # Some of the strings are misformed and gives an extra empty space
        time_arr = list(filter(None, time_arr))
        event_start_date = datetime.strptime(date_arr[0],
            '%b %d').replace(year=date.today().year).date().isoformat()
        event_end_date = datetime.strptime(date_arr[-1], 
            '%b %d').replace(year=date.today().year).date().isoformat()

        # Note: Some events span across several days e.g. 8350, thus specifying dates makes no sense
        event_meridiem = time_arr[2]
        event_start_time = time_arr[0] + ' ' + event_meridiem
        event_end_time = time_arr[1] + ' ' + event_meridiem
        
        evt_bar = soup.select('#evt_bar')[0]
        event_url = evt_bar.select('dd')[1].a['href']
        event_price = evt_bar.select('dl')[1].dd.text

        event_campus = 'Off Campus'
        if evt_bar.select('dd')[0].b != None:
            event_campus = evt_bar.select('dd')[0].b.text

        event_address = ''
        address_block = evt_bar.select('dd')[0]
        if address_block.a != None:
            address_block = address_block.a
        for content in address_block.contents:
            text = content if type(content) == NavigableString else content.text
            event_address += text.strip().replace('\r', '') + ' '
        event_address = event_address.strip()

        event_audiences = list(map(lambda a: a.text, 
            evt_bar.select('dl')[1].select('dd')[1].select('a')))

        soup.select('.eventTitle')[0].extract()
        soup.select('.date')[0].extract()
        evt_bar.extract()
        soup.select('#cal_bar')[0].extract()
        event_description = ''
        for content in soup.select('#content')[0].contents:
            text = content if type(content) == NavigableString else content.text
            event_description += text.strip().replace('\r', '') + ' '
        event_description = event_description.strip()

        doc = OrderedDict([
            ('id', event_id),
            ('title', event_title),
            ('start_date', event_start_date),
            ('end_date', event_end_date),
            ('start_time', event_start_time),
            ('end_time', event_end_time),
            ('url', event_url),
            ('description', event_description),
            ('admission_price', event_price),
            ('campus', event_campus),
            ('address', event_address),
            ('audiences', event_audiences),
        ])
        return doc