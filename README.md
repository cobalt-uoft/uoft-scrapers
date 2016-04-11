# UofT Scrapers [![PyPI version](https://badge.fury.io/py/uoftscrapers.svg)](https://badge.fury.io/py/uoftscrapers)

This is a library of scrapers for various University of Toronto websites. It is built to generate up-to-date databases for [Cobalt](https://cobalt.qas.im/), but is distributed as a stand-alone library for anyone to utilize.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Library Reference](#library-reference)
  - [Course Finder](#course-finder)
  - [Buildings](#buildings)
  - [Textbooks](#textbooks)
  - [Food](#food)
  - [UTSG Timetable](#utsg-timetable)
  - [UTM Timetable](#utm-timetable)
  - [UTSC Timetable](#utsc-timetable)
  - [UTSG Calendar](#utsg-calendar)

## Requirements
 - [python3](https://www.python.org/download/releases/3.4.3/)
 - [pip](https://pypi.python.org/pypi/pip#downloads)
 - [tidy](http://tidy.sourceforge.net/#binaries)
 - [lxml](http://lxml.de/installation.html)

## Installation
```bash
pip install uoftscrapers
```

## Usage
```python
import uoftscrapers

# Example: scrape http://map.utoronto.ca building data to ./some/path
b = uoftscrapers.Buildings("./some/path")
b.run()

# Example: scrape http://coursefinder.utoronto.ca to current location
cf = uoftscrapers.CourseFinder()
cf.run()
```

## Library Reference

### Course Finder

##### Class name
```python
uoftscrapers.CourseFinder
```

##### Scraper source
http://coursefinder.utoronto.ca/

#### Output format
```js
{
  id: String,
  code: String,
  name: String,
  description: String,
  division: String,
  department: String,
  prerequisites: String,
  exclusions: String,
  level: Number,
  campus: String,
  term: String,
  breadths: [Number],
  meeting_sections: [{
    code: String,
    instructors: [String],
    times: [{
      day: String,
      start: Number,
      end: Number,
      duration: Number,
      location: String
    }],
    size: Number,
    enrolment: Number
  }]
}
```

------

### Buildings

##### Class name
```python
uoftscrapers.Buildings
```

##### Scraper source
http://map.utoronto.ca/

##### Output format
```js
{
  id: String,
  code: String,
  name: String,
  short_name: String,
  campus: String,
  address: {
    street: String,
    city: String,
    province: String,
    country: String,
    postal: String
  },
  lat: Number,
  lng: Number,
  polygon: [
    [Number, Number]
  ]
}
```

------

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

------

### Food

##### Class name
```python
uoftscrapers.Food
```

##### Scraper source
http://map.utoronto.ca/

##### Output format
```js
{
  id: String,
  building_id: String,
  name: String,
  short_name: String,
  description: String,
  url: String,
  tags: [String],
  image: String,
  campus: String,
  lat: Number,
  lng: Number,
  address: String,
  hours: {
    sunday: {
      closed: Boolean,
      open: Number,
      close: Number
    },
    monday: {
      closed: Boolean,
      open: Number,
      close: Number
    }
    tuesday: {
      closed: Boolean,
      open: Number,
      close: Number
    },
    wednesday: {
      closed: Boolean,
      open: Number,
      close: Number
    },
    thursday: {
      closed: Boolean,
      open: Number,
      close: Number
    },
    friday: {
      closed: Boolean,
      open: Number,
      close: Number
    },
    saturday: {
      closed: Boolean,
      open: Number,
      close: Number
    }
  }
}
```

------

### UTSG Timetable

##### Class name
```python
uoftscrapers.UTSGTimetable
```

##### Scraper source
http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm

##### Output format
```js
{
  id: String,
  code: String,
  name: String,
  level: Number,
  campus: String,
  term: String,
  breadths: [Number],
  meeting_sections: [{
    code: String,
    instructors: [String],
    times: [{
      day: String,
      start: Number,
      end: Number,
      duration: Number,
      location: String
    }],
    size: Number,
    enrolment: Number
  }]
}
```

------

### UTM Timetable

##### Class name
```python
uoftscrapers.UTMTimetable
```

##### Scraper source
https://student.utm.utoronto.ca/timetable/

##### Output format
Not implemented.

------

### UTSC Timetable

##### Class name
```python
uoftscrapers.UTSCTimetable
```

##### Scraper source
http://www.utsc.utoronto.ca/~registrar/scheduling/timetable

##### Output format
Not implemented.

------

### UTSG Calendar

##### Class name
```python
uoftscrapers.UTSGCalendar
```

##### Scraper source
http://www.artsandscience.utoronto.ca/ofr/calendar/

##### Output format
Not implemented.
