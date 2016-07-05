import datetime
from amazonscraper import AmazonScraper

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

start_date, end_date = get_dates()
year = start_date.year

scraper = AmazonScraper('orders-new4.csv', year, 'invoices/')

scraper.get_credentials()
scraper.open_browser()
scraper.go_to_sign_in()
scraper.sign_in()
scraper.go_to_orders()
scraper.scrape()

scraper.close()
