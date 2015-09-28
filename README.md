# UofT Scrapers
This is a library of scrapers for various University of Toronto websites. It is built to generate up-to-date databases for [Cobalt](https://github.com/cobalt-io), but is distributed as a stand-alone library for anyone to utilize.

## Requirements
 - [python3](https://www.python.org/download/releases/3.4.3/)
 - [pip](https://pypi.python.org/pypi/pip#downloads)
 - [tidy](http://www.w3.org/People/Raggett/tidy/)

## Installation
```bash
  pip install uoftscrapers
```

## Usage
```python
import uoftscrapers

# Example: scrape http://map.utoronto.ca/
uoftscrapers.scrape_map()
```

## API Reference

### Map
```python
# http://map.utoronto.ca/
uoftscrapers.scrape_map()
```

### Course Finder
```python
# http://coursefinder.utoronto.ca/
uoftscrapers.scrape_cf()
```

### UTSG Timetable
```python
# http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm
uoftscrapers.scrape_utsgt()
```

### UTM Timetable
```python
# https://student.utm.utoronto.ca/timetable/
uoftscrapers.scrape_utmt()
```

### UTSC Timetable
```python
# http://www.utsc.utoronto.ca/~registrar/scheduling/timetable
uoftscrapers.scrape_utmt()
```

### UTSG Calendar
```python
# http://www.artsandscience.utoronto.ca/ofr/calendar/
uoftscrapers.scrape_utsgc()
```
