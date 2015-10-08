# UofT Scrapers
This is a library of scrapers for various University of Toronto websites. It is built to generate up-to-date databases for [Cobalt](https://cobalt.qas.im/), but is distributed as a stand-alone library for anyone to utilize.

## Requirements
 - [python3](https://www.python.org/download/releases/3.4.3/)
 - [pip](https://pypi.python.org/pypi/pip#downloads)
 - [tidy](http://tidy.sourceforge.net/#binaries)

## Installation
```bash
  pip install uoftscrapers
```

## Usage
```python
import uoftscrapers

# Example: scrape http://map.utoronto.ca to ./some/path
m = uoftscrapers.Map("./some/path")
m.run()

# Example: scrape http://coursefinder.utoronto.ca to current location
cf = uoftscrapers.CourseFinder()
cf.run()
```

## Library Reference

### Map

##### Class name
```python
uoftscrapers.Map
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

------

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
