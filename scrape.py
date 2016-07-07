import datetime

from bs4 import BeautifulSoup
from amazonscraper import AmazonScraper

with open('scrapespecs.xml') as specfile:
    soup = BeautifulSoup(specfile.read(), 'html.parser')

attrs = soup.find('spec')

spec = {
        'username': attrs.find('username').text,
        'password': attrs.find('password').text,
        'business': True if attrs.find('business').text == 'true' else False,
        'start_date': datetime.datetime.strptime(attrs.find('start').text, '%Y.%m.%d'),
        'end_date': datetime.datetime.strptime(attrs.find('end').text, '%Y.%m.%d')
    }

scraper = AmazonScraper(spec['username'], spec['password'], spec['business'], spec['start_date'], spec['end_date'])

print('Starting browser...')
scraper.open_browser()

print('Navigating to invoices...')
scraper.go_to_sign_in()
scraper.sign_in()
scraper.go_to_orders()

print('Beginning scrape...')
scraper.scrape()

scraper.close()

print('Scrape completed!')
