from ..utils import Scraper
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import requests
import datetime
now = datetime.datetime.now()


class UTMCalendar:
    '''Scraper for Important dates from UTM calendar found at https://www.utm.utoronto.ca/registrar/important-dates
        '''

    summerLink = 'http://m.utm.utoronto.ca/importantDates.php?mode=full&session={0}5&header='
    fallLink = 'http://m.utm.utoronto.ca/importantDates.php?mode=full&session={0}9&header='
    sessionLinks = [summerLink, fallLink]
    currentSession = "Summer"
    @staticmethod
    def scrape(location='.', year=None): #scrapes most current sessions by default
        
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
                    eventStartEnd = date.split('-') #splits event dates over a period
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
                        ('session', UTMCalendar.currentSession),
                        ('events', events)
                    ])
                if(i<len(dates)):
                    currentDate = dates[i]
            UTMCalendar.currentSession = "Fall/Winter"


        for date, info in calendar.items():
            Scraper.save_json(info, location, UTMCalendar.convert_date(date))

        Scraper.logger.info('UTMCalendar completed.')
        return calendar

    @staticmethod
    def convert_date(date):
        date_dict = {'January':'1', 'February':'2', 'March':'3', 'April':'4', 'May':'5', 'June':'6', 'July':'7',
                     'August':'8', 'September':'9', 'October':'10', 'November':'11', 'December':'12'}
        splitDate = date.split(' ')
        year = splitDate[2]
        day = splitDate[1].strip(',')
        month = date_dict[splitDate[0]]
        return("{0}-{1}-{2}".format(year, month, day))