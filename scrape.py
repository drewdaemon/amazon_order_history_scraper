import datetime
import getpass
import os
from amazonscraper import AmazonScraper

def get_credentials():
    try:
        email = os.environ['AMAZON_EMAIL']
    except KeyError:
        email = raw_input('Enter the email address you use to sign into amazon: ')
    try:
        passwd = os.environ['AMAZON_PASS']
    except KeyError:
        passwd = getpass.getpass('Enter your password: ')

    return email, passwd

def get_dates():
    print('You can leave the start date blank if you want the scraper to begin from today.')
    while(True):
        try:
            start_date_str = str(raw_input('Start date (YYYY.MM.DD): '))
            if start_date_str == '':
                start_date = datetime.datetime.now()
            else:
                start_date = datetime.datetime.strptime(start_date_str, '%Y.%m.%d')
            break
        except ValueError:
            print('Incorrect format!')

    print('You can leave the end date blank if you want the scraper to scrape the entire history from the start date.')
    while(True):
        try:
            end_date_str = str(raw_input('End date (YYYY.MM.DD): '))
            if end_date_str == '':
                end_date = None
            else:
                end_date = datetime.datetime.strptime(end_date_str, '%Y.%m.%d')
            break
        except ValueError:
            print('Incorrect format!')

    return start_date, end_date

email, pass_word = get_credentials()
start_date, end_date = get_dates()

print('Starting browser...')

scraper = AmazonScraper(email, pass_word, start_date, end_date, 'invoices/', 'csvs/')

scraper.open_browser()

print('Navigating to invoices...')
scraper.go_to_sign_in()
scraper.sign_in()
scraper.go_to_orders()

print('Beginning scrape...')
scraper.scrape()

scraper.close()

print('Scrape completed!')
