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

    @staticmethod
    def scrape(location='.', year=None):
        year = year or now.year

        Scraper.logger.info('UTMCalendar initialized.')

        html = Scraper.get(UTMCalendar.host1.format(year))
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('div', class_='content')
        dates = content.find_all('div', class_='title')
        i = 0
        currentDate = dates[i]
        while(i<len(dates)):
            print(dates[i].text)

            while (currentDate == dates[i]):
                info = dates[i].find_next('div', class_='info')
                print(info.text)
                i+=1
                if(i>=len(dates)):
                    break;
            if(i<len(dates)):
                currentDate = dates[i]



        Scraper.logger.info('UTMCalendar completed.')