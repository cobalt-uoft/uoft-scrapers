# UofT Scrapers
This is a library of scrapers for various University of Toronto websites. It is built to generate up-to-date databases for [Cobalt](https://github.com/cobalt-io), but can be used as a stand-alone script for anyone to utilize.

## Requirements
 - [python3](https://www.python.org/download/releases/3.4.3/)
 - [pip](https://pypi.python.org/pypi/pip#downloads)
 - [tidy](http://www.w3.org/People/Raggett/tidy/)

## Installation
Clone the repository:
```bash
  git clone https://github.com/cobalt-io/uoft-scrapers.git && cd uoft-scrapers
```

Install the required python module dependencies:
```bash
  pip install -r requirements.txt
  ```

## Update
```bash
  git pull
```

## Usage
Execute the scraper by passing which scrapers to run. For example, in order to scrape [map.utoronto.ca](http://map.utoronto.ca):
```bash
  python3 main.py map
```
Scrape multiple sources at once by specifying more than one scraper:
```bash
  python3 main.py map utsgtimetable
```
All scraped data is outputted in JSON files located in the scraper's respective directory at `json/`.
A complete list of accepted arguments:
 - all
 - [coursefinder](http://coursefinder.utoronto.ca/)
 - [utmtimetable](https://student.utm.utoronto.ca/timetable/)
 - [utsctimetable](http://www.utsc.utoronto.ca/~registrar/scheduling/timetable)
 - [utsgtimetable](http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm)
 - [utsgcalendar](http://www.artsandscience.utoronto.ca/ofr/calendar/)
 - [map](http://map.utoronto.ca/)
