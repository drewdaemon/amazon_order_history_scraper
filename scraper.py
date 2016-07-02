from selenium import webdriver
from locators import InvoiceLocators as IL, AmazonLocators as AL, SignInLocators as SI
from selenium.common.exceptions import NoSuchElementException
import time
import getpass
import csv
import os

class amazonScraper:
    def __init__(self):
        self.url = 'https://www.amazon.com'
        self.csv_headers = [
                        'Order ID',
                        'Date',
                        'Title',
                        'Quantity',
                        'Seller',
                        'Condition',
                        'Purchase Price Per Unit',
                        'Subtotal',
                        'Shipping',
                        'Sales Tax',
                        'Total',
                        'Payment Method',
                        'Date Shipped'
                        ]
        self.scraped_data = []
        self.driver = None

    def close_browser(self):
        self.driver.quit()

    def scrape_invoice_data(self):
        order_id = self.driver.find_element(*IL.ORDER_ID).text[25:] # cutting off "Amazon.com order number: "
        order_date = self.driver.find_element(*IL.ORDER_DATE).text[14:] # cutting off "Order Placed: "
        title = self.driver.find_element(*IL.TITLE).text

        seller_condition = self.driver.find_element(*IL.SELLER_CONDITION).text.splitlines()
        seller = seller_condition[0][9:] # cutting off "Sold by: "
        if '(seller profile)' in seller:
            seller.strip()
            seller = seller[:-17] # cutting off "(seller profile)"
        condition = seller_condition[2][11:] # cutting off "Condition: "

        quantity = self.driver.find_element(*IL.QUANTITY).text[:1]
        purchase_price_pu = self.driver.find_element(*IL.PURCHASE_PRICE_PU).text
        subtotal = self.driver.find_element(*IL.SUBTOTAL).text
        shipping = self.driver.find_element(*IL.SHIPPING).text
        sales_tax = self.driver.find_element(*IL.SALES_TAX).text
        total = self.driver.find_element(*IL.TOTAL).text
        method = self.driver.find_element(*IL.PAYMENT_METHOD).text
        shipped = self.driver.find_element(*IL.DATE_SHIPPED).text[11:] # cutting off "Shipped on: "

        # the order of these variables should correspond to self.csv_headers
        row = [order_id, order_date, title, quantity, seller, condition, purchase_price_pu, subtotal, shipping, sales_tax, total, method, shipped]
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
        next_btns = self.driver.find_elements_by_xpath(*AL.NAV_BTNS)
        last_btn = next_btns[len(next_btns) - 1]
        last_btn.click()

    def next_page(self):
        try:
            next_btns = self.driver.find_elements_by_xpath(*AL.NAV_BTNS)
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
        picker = self.driver.find_element(*AL.YEAR_PICKER)
        picker.click()
        current_year_field = self.driver.find_element(*AL.CURRENT_YEAR_LINK)
        current_year_field.click()

    def go_to_orders(self):
        account_btn = self.driver.find_element(*AL.ACCOUNT_BTN)
        account_btn.click()
        time.sleep(4)
        orders_btn = self.driver.find_element(*AL.ORDERS_BTN)
        orders_btn.click()
        time.sleep(4)

    def sign_in(self, email, pass_word):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(self.url)
        sign_in_btn = self.driver.find_element(*AL.SIGN_IN_BTN)
        sign_in_btn.click()

        email_field = self.driver.find_element(*SI.EMAIL_FIELD)
        pass_word_field = self.driver.find_element(*SI.PASS_FIELD)
        submit_btn = self.driver.find_element(*SI.SUBMIT_BTN)
        email_field.send_keys(email)
        pass_word_field.send_keys(pass_word)
        submit_btn.click()

    def save_data_to_csv(self, location):
        csv_file = open(location, 'wb')
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(self.csv_headers)
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
