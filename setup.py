from distutils.core import setup
from codecs import open

setup(
    name = 'uoftscrapers',
    packages = [
        'uoftscrapers',
        'uoftscrapers.scrapers.buildings',
        'uoftscrapers.scrapers.calendar.utsg',
        'uoftscrapers.scrapers.coursefinder',
        'uoftscrapers.scrapers.exams.utm',
        'uoftscrapers.scrapers.exams.utsc',
        'uoftscrapers.scrapers.exams.utsg',
        'uoftscrapers.scrapers.food',
        'uoftscrapers.scrapers.textbooks',
        'uoftscrapers.scrapers.timetable.utm',
        'uoftscrapers.scrapers.timetable.utsc',
        'uoftscrapers.scrapers.timetable.utsg',
        'uoftscrapers.scrapers.utmshuttle',
        'uoftscrapers.scrapers.parking.utsg',
        'uoftscrapers.scrapers.scraper',
        'uoftscrapers.scrapers.scraper.layers'
    ],
    version = '0.3.2',
    description = 'University of Toronto public web scraping scripts.',
    author = 'Qasim Iqbal',
    author_email = 'me@qas.im',
    url = 'https://github.com/cobalt-io/uoft-scrapers',
    download_url = 'https://github.com/cobalt-io/uoft-scrapers/tarball/0.3.2',
    package_data={'': ['LICENSE.md']},
    package_dir={'uoftscrapers': 'uoftscrapers'},
    include_package_data=True,
    keywords = ['uoft', 'scraper', 'toronto', 'university of toronto', 'cobalt'],
    install_requires = ['requests>=2.6.2', 'beautifulsoup4>=4.3.2', 'pytidylib>=0.2.4', 'lxml>=3.6.0', 'pytz>=2016.3'],
    classifiers = [],
)
