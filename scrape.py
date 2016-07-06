import datetime
import getpass
import os

from xml.etree import ElementTree
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

try:
    tree = ElementTree.parse('users.xml')
    nodes = tree.getroot()
    users = []
    for node in nodes:
        users.append(
            {
                'username': node[0].text,
                'password': node[1].text,
                'business': True if node[2].text == 'true' else False
            }
        )

    if len(users) >= 1:
        print('Here are the available usernames: ')
        for i in range(len(users)):
            print(str(i + 1) + ' - ' + users[i]['username'])
        while(1):
            which = input('Which one should I scrape? ')
            if which > 0 and which <= len(users):
                start_date, end_date = get_dates()
                scraper = AmazonScraper(users[which - 1]['username'], users[which - 1]['password'], users[which - 1]['business'], start_date, end_date)
                break
            else:
                print('Invalid input!')

except:
    email, pass_word = get_credentials()
    business = raw_input('And is this an amazon business account? (y/n) ')

    if business == 'y':
        scraper = AmazonScraper(email, pass_word, True, start_date, end_date)
    else:
        scraper = AmazonScraper(email, pass_word, False, start_date, end_date)

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
