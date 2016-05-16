from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests
import datetime


class UTMDates:
    '''Scraper for Important dates from UTM calendar found at https://www.utm.utoronto.ca/registrar/important-dates
        '''

    link = 'http://m.utm.utoronto.ca/importantDates.php?mode=full&session={0}{1}&header='
    sessionNumber = [5, 9]
    @staticmethod
    def scrape(location='.', year=None, save=True):  # scrapes most current sessions by default

        year = year or datetime.datetime.now().year

        currentSession = "{0} SUMMER"
        calendar = OrderedDict()
        Scraper.logger.info('UTMDates initialized.')
        for session in UTMDates.sessionNumber:
            html = Scraper.get(UTMDates.link.format(year, session))
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', class_='content')
            dates = content.find_all('div', class_='title')
            i = 0
            currentDate = dates[i]
            while(i < len(dates)):
                date = dates[i].text
                events = []
                while (currentDate == dates[i]):
                    info = dates[i].find_next('div', class_='info')
                    description = info.text
                    eventStartEnd = date.split('-')  # splits event dates over a period
                    eventStart = UTMDates.convert_date(eventStartEnd[0].strip())
                    if len(eventStartEnd) > 1:
                        eventEnd = UTMDates.convert_date(eventStartEnd[1].strip())
                    else:
                        eventEnd = eventStart

                    events.append(OrderedDict([
                            ('end_date', eventEnd),
                            ('session', currentSession.format(UTMDates.get_year_from(eventStart))),
                            ('campus', 'UTM'),
                            ('description', description)
                        ]))
                    i += 1
                    if(i >= len(dates)):
                        break
                calendar[eventStart] = OrderedDict([
                    ('date', eventStart),
                    ('events', events)
                ])
                if(i < len(dates)):
                    currentDate = dates[i]
            currentSession = "{0} FALL/WINTER"

        if save:
            for date, info in calendar.items():
                Scraper.save_json(info, location, UTMDates.convert_date(date))

        Scraper.logger.info('UTMDates completed.')
        return calendar if not save else None

    @staticmethod
    def convert_date(date):
        splitDate = date.split(' ')
        year = splitDate[2]
        day = splitDate[1].strip(',')
        month = datetime.datetime.strptime(splitDate[0], '%B').strftime('%m')
        return("{0}-{1}-{2}".format(year, month, day.zfill(2)))

    @staticmethod
    def get_year_from(date):
        splitDate = date.split('-')
        return splitDate[0]
