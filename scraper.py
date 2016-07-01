from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import getpass
import csv
import os

xpaths = {
    'disabled_next': '//*[@id="ordersContainer"]/div[8]/div/ul/li[@class="a-disabled a-last"]',
    'next_btns': '//*[@id="ordersContainer"]/div[12]/div/ul//li/a',
    'year_picker': '//*[@id="timePeriodForm"]',
    'year_fields': '//*[@id="a-popover-1"]/div/div/ul//li/a',
    'orders_btn': '//*[@id="your-orders-button-announce"]',
    'account_btn': '//*[@id="nav-link-yourAccount"]',
}

class amazonScraper:
    def __init__(self):
        self.url = 'https://www.amazon.com'
        self.invoice_info_paths = {
            'order_date': '/html/body/table/tbody/tr/td/table[1]/tbody/tr[1]/td',
            'order_id': '/html/body/table/tbody/tr/td/table[1]/tbody/tr[2]/td',
            'title': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/i',
            # condition fetches "Condition: <condition>"
            'seller_condition': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/span',
            # seller fetches "Sold by: <seller>"
            'purchase_price_pu': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]',
            # quantity fetches "<quantity> of:"
            'quantity': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]',
        }
        self.scraped_data = []
        self.driver = None

    def close_browser(self):
        self.driver.quit()

    def scrape_invoice_data(self):
        order_id = self.driver.find_element_by_xpath(self.invoice_info_paths['order_id']).text[25:] # cutting off "Amazon.com order number: "
        order_date = self.driver.find_element_by_xpath(self.invoice_info_paths['order_date']).text[14:] # cutting off "Order Placed: "
        title = self.driver.find_element_by_xpath(self.invoice_info_paths['title']).text

        seller_condition = self.driver.find_element_by_xpath(self.invoice_info_paths['seller_condition']).text.splitlines()
        seller = seller_condition[0][9:] # cutting off "Sold by: "
        if '(seller profile)' in seller:
            seller.strip()
            seller = seller[:-17] # cutting off "(seller profile)"
        condition = seller_condition[2][11:] # cutting off "Condition: "

        quantity = self.driver.find_element_by_xpath(self.invoice_info_paths['quantity']).text[:1]
        purchase_price_pu = self.driver.find_element_by_xpath(self.invoice_info_paths['purchase_price_pu']).text

        row = [order_id, order_date, title, quantity, seller, condition, purchase_price_pu]
        self.scraped_data.append(row)
        print self.scraped_data

    def get_invoice_link(self, which):
        try:
            return self.driver.find_element_by_xpath('//*[@id="ordersContainer"]/div[' + str(which + 1) + ']/div[1]/div/div/div/div[2]/div[2]/ul/a[2]')
        except NoSuchElementException:
            return False

    def scrape_invoices(self):
        count = 1
        invoice_link = self.get_invoice_link(count)
        while (invoice_link):
            invoice_link.click()
            time.sleep(3)
            self.scrape_invoice_data()
            self.driver.back()
            count += 1
            invoice_link = self.get_invoice_link(count)

        time.sleep(5)

    def go_next_page(self):
        next_btns = self.driver.find_elements_by_xpath(xpaths['next_btns'])
        last_btn = next_btns[len(next_btns) - 1]
        last_btn.click()

    def next_page(self):
        try:
            next_btns = self.driver.find_elements_by_xpath(xpaths['next_btns'])
            last_btn = next_btns[len(next_btns) - 1]
            if last_btn.text[:4] == 'Next':
                return True
            else:
                return False
        except IndexError:
            return False
        except NoSuchElementException:
            return False

    def navigate_to_current_year(self):
        current_year = datetime.datetime.now().year
        picker = self.driver.find_element_by_xpath(xpaths['year_picker'])
        picker.click()
        current_year_field = self.driver.find_element_by_link_text(str(current_year))
        current_year_field.click()

    def go_to_orders(self):
        account_btn = self.driver.find_element_by_xpath(xpaths['account_btn'])
        account_btn.click()
        time.sleep(4)
        orders_btn = self.driver.find_element_by_xpath(xpaths['orders_btn'])
        orders_btn.click()
        time.sleep(4)

    def sign_in(self, email, pass_word):
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        signInBtn = self.driver.find_element_by_xpath('//*[@id="nav-signin-tooltip"]/a')
        signInBtn.click()

        emailField = self.driver.find_element_by_xpath('//*[@id="ap_email"]')
        passWordField = self.driver.find_element_by_xpath('//*[@id="ap_password"]')
        signInBtn = self.driver.find_element_by_xpath('//*[@id="signInSubmit"]')
        emailField.send_keys(email)
        passWordField.send_keys(pass_word)
        signInBtn.click()

    def save_data_to_csv(self, location):
        csv_file = open(location, 'wb')
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Order ID', 'Date', 'Title', 'Quantity', 'Seller', 'Condition', 'Purchase Price Per Unit'])
        for row in self.scraped_data:
            writer.writerow(row)

    def get_credentials(self):
        try:
            email = os.environ['AMAZON_EMAIL']
        except KeyError:
            email = raw_input('Enter the email address you use to sign into amazon: ')
        try: 
            passwd = os.environ['AMAZON_PASS']
        except KeyError:
            passwd = getpass.getpass('Enter your password: ')

        return email, passwd

scraper = amazonScraper()

email, passwd = scraper.get_credentials()
scraper.sign_in(email, passwd)
scraper.go_to_orders()
scraper.navigate_to_current_year()
scraper.scrape_invoices()

while scraper.next_page():
    scraper.go_next_page()
    time.sleep(3)
    scraper.scrape_invoices()
scraper.save_data_to_csv('orders-new.csv')

scraper.close_browser()
