import os
from scrapers.map.main import Map
from scrapers.coursefinder.main import Coursefinder
# from scrapers.utmtimetable.main import UTMTimetable
# from scrapers.utsctimetable.main import UTSCTimetable
# from scrapers.utsgtimetable.main import UTSGTimetable
# from scrapers.utsgcalendar.main import UTSGCalendar


if __name__ == "__main__":
    m = Map()
    m.update_files()

    cf = Coursefinder()
    cf.update_files()

    # utmt = UTMTimetable()
    # utmt.update_files()

    # utsct = UTSCTimetable()
    # utsct.update_files()

    # utsgt = UTSGTimetable()
    # utsgt.update_files()

    # utsgc = UTSCTimetable()
    # utsgc.update_files()
