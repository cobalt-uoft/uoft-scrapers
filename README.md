# UofT Scrapers [![PyPI version](https://badge.fury.io/py/uoftscrapers.svg)](https://badge.fury.io/py/uoftscrapers)

This is a library of scrapers for various University of Toronto websites. It is built to generate up-to-date databases for [Cobalt](https://cobalt.qas.im/), but is distributed as a stand-alone library for anyone to utilize.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Library Reference](#library-reference)
  - [Courses](#courses)
  - [Buildings](#buildings)
  - [Textbooks](#textbooks)
  - [Food](#food)
  - [Calendar](#calendar)
    - [UTSG Calendar](#utsg-calendar)
    - [UTM Calendar](#utm-calendar)
    - [UTSC Calendar](#utsc-calendar)
  - [Timetable](#timetable)
    - [UTSG Timetable](#utsg-timetable)
    - [UTM Timetable](#utm-timetable)
    - [UTSC Timetable](#utsc-timetable)
  - [Exams](#exams)
    - [UTSG Exams](#utsg-exams)
    - [UTM Exams](#utm-exams)
    - [UTSC Exams](#utsc-exams)
  - [Athletics](#athletics)
    - [UTSG Athletics](#utsg-athletics)
    - [UTM Athletics](#utm-exams)
    - [UTSC Athletics](#utsc-athletics)
  - [Parking](#parking)
  - [Shuttle Bus Schedule](#shuttle)
  - [Events](#events)
  - [Libraries](#libraries)

## Requirements
 - [python3](https://www.python.org/download/releases/3.5.1)
 - [pip](https://pypi.python.org/pypi/pip#downloads)
 - [tidy](http://binaries.html-tidy.org/)
 - [lxml](http://lxml.de/installation.html)

## Installation
```bash
pip install uoftscrapers
```

## Usage
```python
import uoftscrapers

# Example: scrape http://map.utoronto.ca building data to ./some/path
uoftscrapers.Buildings.scrape('./some/path')

# Example: scrape http://coursefinder.utoronto.ca to current working directory
uoftscrapers.Courses.scrape()
```

## Library Reference

### Courses

##### Class name
```python
uoftscrapers.Courses
```

##### Scraper source
http://coursefinder.utoronto.ca

#### Output format
```js
{
  "id": String,
  "code": String,
  "name": String,
  "description": String,
  "division": String,
  "department": String,
  "prerequisites": String,
  "exclusions": String,
  "level": Number,
  "campus": String,
  "term": String,
  "breadths": [Number],
  "meeting_sections": [{
    "code": String,
    "instructors": [String],
    "times": [{
      "day": String,
      "start": Number,
      "end": Number,
      "duration": Number,
      "location": String
    }],
    "size": Number,
    "enrolment": Number
  }]
}
```

--------------------------------------------------------------------------------

### Buildings

##### Class name
```python
uoftscrapers.Buildings
```

##### Scraper source
http://map.utoronto.ca

##### Output format
```js
{
  "id": String,
  "code": String,
  "name": String,
  "short_name": String,
  "campus": String,
  "address": {
    "street": String,
    "city": String,
    "province": String,
    "country": String,
    "postal": String
  },
  "lat": Number,
  "lng": Number,
  "polygon": [
    [Number, Number]
  ]
}
```

--------------------------------------------------------------------------------

### Textbooks

##### Class name
```python
uoftscrapers.Textbooks
```

##### Scraper source
http://uoftbookstore.com

##### Output format
```js
{
  "id": String,
  "isbn": String,
  "title": String,
  "edition": Number,
  "author": String,
  "image": String,
  "price": Number,
  "url": String,
  "courses":[{
    "id": String,
    "code": String,
    "requirement": String,
    "meeting_sections":[{
      "code": String,
      "instructors": [String]
    }]
  }]
}
```

--------------------------------------------------------------------------------

### Food

##### Class name
```python
uoftscrapers.Food
```

##### Scraper source
http://map.utoronto.ca

##### Output format
```js
{
  "id": String,
  "building_id": String,
  "name": String,
  "short_name": String,
  "description": String,
  "url": String,
  "tags": [String],
  "image": String,
  "campus": String,
  "lat": Number,
  "lng": Number,
  "address": String,
  "hours": {
    "sunday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    },
    "monday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    }
    "tuesday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    },
    "wednesday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    },
    "thursday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    },
    "friday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    },
    "saturday": {
      "closed": Boolean,
      "open": Number,
      "close": Number
    }
  }
}
```

--------------------------------------------------------------------------------

### Calendar

##### Class name
```python
uoftscrapers.Calendar
```

##### Scraper source
 - [UTSG Calendar](#utsg-calendar)
 - [UTM Calendar](#utm-calendar)
 - [UTSC Calendar](#utsc-calendar)

##### Output format
Not implemented.

----------------------------------------

### UTSG Calendar

##### Class name
```python
uoftscrapers.UTSGCalendar
```

##### Scraper source
http://www.artsandscience.utoronto.ca/ofr/calendar/

##### Output format
Refer to [Calendar](#calendar)

--------------------

### UTM Calendar

##### Class name
```python
uoftscrapers.UTMCalendar
```

##### Scraper source
https://student.utm.utoronto.ca/calendar/calendar.pl

##### Output format
Refer to [Calendar](#calendar)

--------------------

### UTSC Calendar

##### Class name
```python
uoftscrapers.UTSCCalendar
```

##### Scraper source
http://www.utsc.utoronto.ca/~registrar/calendars/calendar/index.html

##### Output format
Refer to [Calendar](#calendar)

--------------------------------------------------------------------------------

### Timetable

##### Class name
```python
uoftscrapers.Timetable
```

##### Scraper source
 - [UTSG Timetable](#utsg-timetable)
 - [UTM Timetable](#utm-timetable)
 - [UTSC Timetable](#utsc-timetable)

##### Output format
```js
{
  "id": String,
  "code": String,
  "name": String,
  "level": Number,
  "campus": String,
  "term": String,
  "breadths": [Number],
  "meeting_sections": [{
    "code": String,
    "instructors": [String],
    "times": [{
      "day": String,
      "start": Number,
      "end": Number,
      "duration": Number,
      "location": String
    }],
    "size": Number,
    "enrolment": Number
  }]
}
```

----------------------------------------

### UTSG Timetable

##### Class name
```python
uoftscrapers.UTSGTimetable
```

##### Scraper source
http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm

##### Output format
Refer to [Timetable](#timetable)

--------------------

### UTM Timetable

##### Class name
```python
uoftscrapers.UTMTimetable
```

##### Scraper source
https://student.utm.utoronto.ca/timetable

##### Output format
Refer to [Timetable](#timetable)

--------------------

### UTSC Timetable

##### Class name
```python
uoftscrapers.UTSCTimetable
```

##### Scraper source
http://www.utsc.utoronto.ca/~registrar/scheduling/timetable

##### Output format
Refer to [Timetable](#timetable)

--------------------------------------------------------------------------------

### Exams

##### Class name
```python
uoftscrapers.Exams
```

##### Scraper source
 - [UTSG Exams](#utsg-exams)
 - [UTM Exams](#utm-exams)
 - [UTSC Exams](#utsc-exams)

##### Output format
```js
{
  "id": String,
  "course_id": String,
  "course_code": String
  "period": String,
  "date": String,
  "start_time": String,
  "end_time": String,
  "sections": [{
    "section": String,
    "location": String
  }]
}
```

----------------------------------------

### UTSG Exams

##### Class name
```python
uoftscrapers.UTSGExams
```

##### Scraper source
http://www.artsci.utoronto.ca/current/exams

##### Output format
Refer to [Exams](#exams)

--------------------

### UTM Exams

##### Class name
```python
uoftscrapers.UTMExams
```

##### Scraper source
https://student.utm.utoronto.ca/examschedule/finalexams.php

##### Output format
Refer to [Exams](#exams)

--------------------

### UTSC Exams

##### Class name
```python
uoftscrapers.UTSCExams
```

##### Scraper source
http://www.utsc.utoronto.ca/registrar/examination-schedule

##### Output format
Refer to [Exams](#exams)

--------------------------------------------------------------------------------

### Athletics

##### Class name
```python
uoftscrapers.Athletics
```

##### Scraper source
 - [UTSG Athletics](#utsg-athletics)
 - [UTM Athletics](#utm-athletics)
 - [UTSC Athletics](#utsc-athletics)

##### Output format
```js
{
  "id": String,
  "date": String,
  "campus": String,
  "events":[{
    "title": String,
    "location": String,
    "building_id": String,
    "start_time": String,
    "end_time": String
  }]
}
```

----------------------------------------

### UTSG Athletics

##### Class name
```python
uoftscrapers.UTSGAthletics
```

##### Scraper source
_Not yet implemented_

##### Output format
Refer to [Athletics](#athletics)

--------------------

### UTM Athletics

##### Class name
```python
uoftscrapers.UTMAthletics
```

##### Scraper source
http://www.utm.utoronto.ca/athletics/schedule/month/

##### Output format
Refer to [Athletics](#athletics)

--------------------

### UTSC Athletics

##### Class name
```python
uoftscrapers.UTSCAthletics
```

##### Scraper source
http://www.utsc.utoronto.ca/athletics/calendar-node-field-date-time/month/

##### Output format
Refer to [Athletics](#athletics)

--------------------------------------------------------------------------------

### Parking

##### Class name
```python
uoftscrapers.Parking
```

##### Scraper source
http://map.utoronto.ca

##### Output format
```js
{
  "id": String,
  "title": String,
  "building_id": String,
  "campus": String,
  "type": String,
  "description": String,
  "lat": Number,
  "lng": Number,
  "address": String
}
```

--------------------------------------------------------------------------------

### Shuttle

##### Class name
```python
uoftscrapers.Shuttle
```

##### Scraper source
https://m.utm.utoronto.ca/shuttle.php

##### Output format
```js
{
  "date": String,
  "routes": [{
    "id": String,
    "name": String,
    "stops": [{
      "location": String,
      "building_id": String,
      "times": [{
        "time": String,
        "rush_hour": Boolean,
        "no_overload": Boolean
      }]
    }]
  }]
}
```

------

### Events

##### Class name
```python
uoftscrapers.Events
```

##### Scraper source
https://www.events.utoronto.ca/

##### Output format
```js
{
  id: String,
  title: String,
  start_date: String
  end_date: String,
  start_time: String,
  end_time: String,
  url: String,
  description: String,
  admission_price: String,
  campus: String,
  location: String,
  audiences: [String],
}
```

------

### Libraries

##### Class name
```python
uoftscrapers.Libraries
```

##### Scraper source
https://onesearch.library.utoronto.ca/

##### Output format
```js
{
  name: String,
  image: String,
  website: String,
  hours: {
    Sun: String,
    Mon: String,
    Tue: String,
    Wed: String,
    Thu: String,
    Fri: String,
    Sat: String
  },
  address: String,
  phone: String,
  about: String,
  collection_strenghts: String,
  access: String
}
```