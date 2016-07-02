from selenium import webdriver
from locators import InvoiceLocators as IL, AmazonLocators as AL, SignInLocators as SI
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import getpass
import csv
import os

class amazonScraper:
    def __init__(self, csv_name):
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
        self.csv_file = open(csv_name, 'wb')
        self.writer = csv.writer(self.csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        self.write_row(self.csv_headers)
        self.scraped_data = []
        self.driver = None
        self.wait = None
        self.current_page = 1
        self.current_year = None

    def open_browser(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10)

    def close_browser(self):
        self.driver.quit()

    def scrape_invoice_data(self):
        order_id = self.driver.find_element(*IL.ORDER_ID).text[25:] # cutting off "Amazon.com order number: "
        order_date = self.driver.find_element(*IL.ORDER_DATE).text[14:] # cutting off "Order Placed: "
        subtotal = self.driver.find_element(*IL.SUBTOTAL).text
        shipping = self.driver.find_element(*IL.SHIPPING).text
        sales_tax = self.driver.find_element(*IL.SALES_TAX).text
        total = self.driver.find_element(*IL.TOTAL).text
        method = self.driver.find_element(*IL.PAYMENT_METHOD).text.splitlines()[8]
        shipped = self.driver.find_element(*IL.DATE_SHIPPED).text[11:] # cutting off "Shipped on: "

        items = self.driver.find_elements(*IL.ITEMS)
        items.pop(0) # the first row only contains "Items Ordered"
        for item in items:
            title = item.find_element(*IL.TITLE).text
            seller_condition = item.find_element(*IL.SELLER_CONDITION).text.splitlines()
            seller = seller_condition[0][9:] # cutting off "Sold by: "
            if '(seller profile)' in seller:
                seller.strip()
                seller = seller[:-17] # cutting off "(seller profile)"
            condition = seller_condition[2][11:] # cutting off "Condition: "

            quantity = item.find_element(*IL.QUANTITY).text.split(' ')[0]
            purchase_price_pu = item.find_element(*IL.PURCHASE_PRICE_PU).text

            # the order of these variables should correspond to self.csv_headers
            row = [order_id, order_date, title, quantity, seller, condition, purchase_price_pu, subtotal, shipping, sales_tax, total, method, shipped]
            self.write_row(row)
            self.scraped_data.append(row)

    def get_invoice_link(self, which):
        try:
            return self.driver.find_element(*AL().get_invoice_link(which))
        except NoSuchElementException:
            return False

    def scrape_invoices(self):
        self.wait.until(EC.presence_of_element_located(AL.FIRST_INVOICE))
        count = 1
        invoice_link = self.get_invoice_link(count)
        while (invoice_link):
            invoice_link.click()
            self.wait.until(EC.presence_of_element_located(IL.ORDER_ID))
            try:
                self.scrape_invoice_data()
            except:
                pass
            self.driver.back()
            count += 1
            self.wait.until(EC.presence_of_element_located(AL.FIRST_INVOICE))
            invoice_link = self.get_invoice_link(count)

    def go_next_page(self):
        next_btns = self.driver.find_elements(*AL.NAV_BTNS)
        next_btn = next_btns[self.current_page]
        next_btn.click()
        self.current_page += 1

    def next_page(self):
        try:
            next_btns = self.driver.find_elements(*AL.NAV_BTNS)
            last_btn = next_btns[len(next_btns) - 1]
            if last_btn.text[:4] == 'Next':
                return True
            else:
                return False
        except IndexError:
            return False
        except NoSuchElementException:
            return False

    def year_exists(self, which):
        picker = self.wait.until(EC.presence_of_element_located(AL.YEAR_PICKER))
        picker.click()
        try:
            self.wait.until(EC.element_to_be_clickable(AL().get_year_link(which)))
            return True
        except TimeoutException:
            return False

    def go_to_year(self, year):
        self.current_page = 1
        self.current_year = year
        try:
            year_field = self.driver.find_element(*AL().get_year_link(year))
            year_field.click()
        except:
            picker = self.wait.until(EC.presence_of_element_located(AL.YEAR_PICKER))
            picker.click()
            year_field = self.driver.find_element(*AL().get_year_link(year))
            year_field.click()

    def go_to_orders(self):
        if EC.visibility_of_element_located(AL.NAV_OVERLAY):
            self.driver.refresh()

        account_btn = self.driver.find_element(*AL.ACCOUNT_BTN)
        account_btn.click()

        orders_btn = self.wait.until(EC.presence_of_element_located(AL.ORDERS_BTN))
        ActionChains(self.driver).move_by_offset(-500, 100).click() # this allows for the menu background to fade before clicking orders btn
        self.wait.until(EC.element_to_be_clickable(AL.ORDERS_BTN))
        orders_btn.click()

    def sign_in(self, email, pass_word):
        sign_in_btn = self.wait.until(EC.presence_of_element_located(AL.ACCOUNT_BTN))
        sign_in_btn.click()

        email_field = self.driver.find_element(*SI.EMAIL_FIELD)
        pass_word_field = self.driver.find_element(*SI.PASS_FIELD)
        submit_btn = self.driver.find_element(*SI.SUBMIT_BTN)
        email_field.send_keys(email)
        pass_word_field.send_keys(pass_word)
        submit_btn.click()

    def write_row(self, row):
        self.writer.writerow(row)

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

scraper = amazonScraper('orders-new.csv')

email, passwd = scraper.get_credentials()
scraper.open_browser()
scraper.sign_in(email, passwd)
scraper.go_to_orders()
year = datetime.datetime.now().year
while scraper.year_exists(year):
    scraper.go_to_year(year)
    scraper.scrape_invoices()
    while scraper.next_page():
        scraper.go_next_page()
        scraper.scrape_invoices()
    year -= 1

scraper.close_browser()
