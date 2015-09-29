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

# Example: scrape http://map.utoronto.ca/ to ./some/path
m = uoftscrapers.Map("./some/path")
m.run()

# Example: scrape http://coursefinder.utoronto.ca/ to current location
cf = uoftscrapers.CourseFinder()
cf.run()
```

## Class Reference

### Map
```python
# http://map.utoronto.ca/
uoftscrapers.Map
```

#### Output format
```js
{
  id: String,
  code: String,
  name: String,
  short_name: String,
  campus: String,
  lat: Number,
  lng: Number,
  address: {
    street: String,
    city: String,
    province: String,
    country: String,
    postal: String
  }
}
```


### Course Finder
```python
# http://coursefinder.utoronto.ca/
uoftscrapers.CourseFinder
```

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


### UTSG Timetable
```python
# http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm
uoftscrapers.UTSGTimetable
```

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


### UTM Timetable
```python
# https://student.utm.utoronto.ca/timetable/
uoftscrapers.UTMTimetable
```

#### Output format
Not implemented.


### UTSC Timetable
```python
# http://www.utsc.utoronto.ca/~registrar/scheduling/timetable
uoftscrapers.UTSCTimetable
```

#### Output format
Not implemented.


### UTSG Calendar
```python
# http://www.artsandscience.utoronto.ca/ofr/calendar/
uoftscrapers.UTSGCalendar
```

#### Output format
Not implemented.
