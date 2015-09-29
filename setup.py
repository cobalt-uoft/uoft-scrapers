from distutils.core import setup

setup(
  name = 'uoftscrapers',
  packages = ['uoftscrapers'],
  version = '0.1',
  description = 'University of Toronto public web scraping scripts.',
  author = 'Qasim Iqbal',
  author_email = 'me@qas.im',
  url = 'https://github.com/cobalt-io/uoft-scrapers',
  download_url = 'https://github.com/cobalt-io/uoft-scrapers/tarball/0.1',
  keywords = ['uoft', 'scraper', 'toronto'],
  install_requires = ['docutils>=2.6.2', 'beautifulsoup4>=4.3.2', 'pytidylib>=0.2.4'],
  classifiers = [],
)
