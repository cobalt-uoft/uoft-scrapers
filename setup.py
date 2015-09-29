from distutils.core import setup
from codecs import open

setup(
    name = 'uoftscrapers',
    packages = [
        'uoftscrapers',
        'uoftscrapers.scrapers.coursefinder',
        'uoftscrapers.scrapers.map',
        'uoftscrapers.scrapers.utmtimetable',
        'uoftscrapers.scrapers.utsctimetable',
        'uoftscrapers.scrapers.utsgcalendar',
        'uoftscrapers.scrapers.utsgtimetable',
        'uoftscrapers.scrapers.scraper'
    ],
    version = '0.1.6',
    description = 'University of Toronto public web scraping scripts.',
    author = 'Qasim Iqbal',
    author_email = 'me@qas.im',
    url = 'https://github.com/cobalt-io/uoft-scrapers',
    download_url = 'https://github.com/cobalt-io/uoft-scrapers/tarball/0.1.6',
    package_data={'': ['LICENSE.md']},
    package_dir={'uoftscrapers': 'uoftscrapers'},
    include_package_data=True,
    keywords = ['uoft', 'scraper', 'toronto'],
    install_requires = ['requests>=2.6.2', 'beautifulsoup4>=4.3.2', 'pytidylib>=0.2.4'],
    classifiers = [],
)
