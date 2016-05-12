from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests
import datetime
now = datetime.datetime.now()


class UTMCalendar:

    host1 = 'http://m.utm.utoronto.ca/importantDates.php?mode=full&session={0}5&header='
    host2 = 'http://m.utm.utoronto.ca/importantDates.php?mode=full&session={0}9&header='
    sessionLinks = [host1, host2]

    @staticmethod
    def scrape(location='.', year=None):
        year = year or now.year

        calendar = OrderedDict()
        Scraper.logger.info('UTMCalendar initialized.')
        for link in UTMCalendar.sessionLinks:
            html = Scraper.get(link.format(year))
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', class_='content')
            dates = content.find_all('div', class_='title')
            i = 0
            currentDate = dates[i]
            while(i<len(dates)):
                date = dates[i].text
                events = []
                while (currentDate == dates[i]):
                    info = dates[i].find_next('div', class_='info')
                    description = info.text
                    eventStartEnd = date.split('-')
                    eventStart = eventStartEnd[0].strip()
                    if len(eventStartEnd)>1:
                        eventEnd = eventStartEnd[1].strip()
                    else:
                        eventEnd = eventStart

                    events.append(OrderedDict([
                            ('end_date', eventEnd),
                            ('campus', 'UTM'),
                            ('description', description)
                        ]))
                    i+=1
                    if(i>=len(dates)):
                        break;
                calendar[date] = OrderedDict([
                        ('date', eventStart),
                        ('session', "Summer"),
                        ('events', events)
                    ])
                if(i<len(dates)):
                    currentDate = dates[i]


        for date, info in calendar.items():
            Scraper.save_json(info, location, date)

        Scraper.logger.info('UTMCalendar completed.')
        return calendar