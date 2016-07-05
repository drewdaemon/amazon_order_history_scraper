from selenium import webdriver
from locators import InvoiceLocators as IL, AmazonLocators as AL, SignInLocators as SI
from urls import URLS
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import datetime
import csv

class AmazonScraper:
    def __init__(self, email, pass_word, start_date, end_date, invoice_folder):
        self.driver = None
        self.wait = None
        self.current_page = 1
        self.current_year = start_date.year
        self.start_date = start_date
        self.end_date = end_date
        self.invoice_count = 0
        self.email = email
        self.pass_word = pass_word
        self.invoice_folder = invoice_folder
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
                        'Total for Shipment',
                        'Total for Order',
                        'Payment Method',
                        'Transaction Date',
                        'Date Shipped'
                        ]
        self.csv_file = open(self.get_csv_name(), 'wb')
        self.writer = csv.writer(self.csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        self.write_row(self.csv_headers)

    def get_csv_name(self):
        csv_name = self.email.split('@')[0] + ' - Amazon Scrape - ' + self.start_date.strftime('%Y.%m.%d') + ' thru '
        if self.end_date != None:
            csv_name += self.end_date.strftime('%Y.%m.%d')
        else:
            csv_name += 'end'
        csv_name += '.csv'
        return csv_name

    def open_browser(self):
        self.driver = webdriver.Firefox()
        self.driver.get(URLS.AMAZON_HOME)
        self.wait = WebDriverWait(self.driver, 10)

    def close(self):
        self.driver.quit()
        self.csv_file.close()

    def asciify(self, row):
        try:
            return [unicodedata.normalize('NFKD', datum).encode('ascii', 'ignore') for datum in row]
        except TypeError:
            return row

    def scrape_invoice_data(self):
        order_id = self.driver.find_element(*IL.ORDER_ID).text[25:] # cutting off "Amazon.com order number: "
        order_date = self.driver.find_element(*IL.ORDER_DATE).text[14:] # cutting off "Order Placed: "
        try:
            item_tables = self.driver.find_elements(*IL.ITEM_TABLES)
            item_tables.pop(0) # first table contains order placed, amazon order num, etc... we don't need it anymore'
            payment_table = item_tables.pop() # last table will always be payment info table
            method_elements = payment_table.find_elements(*IL.PAYMENT_METHODS)
            credit_card = True
            methods = []
            transaction_dates = []
            if len(method_elements) > 0:
                for el in method_elements:
                    info = el.text.split(':')
                    if len(info) >= 2: # sometimes there's a random blank line that needs to be ignored'
                        methods.append(info[0])
                        transaction_dates.append(info[1])
            else:
                credit_card = False
                methods.append(payment_table.find_element(*IL.PAYMENT_METHOD).text.splitlines()[8])
                transaction_dates.append('')

            total_for_order = payment_table.find_element(*IL.TOTAL_FOR_ORDER).text
            count = 0
            for table in item_tables:
                subtotal = table.find_element(*IL.SUBTOTAL).text
                shipped = table.find_element(*IL.DATE_SHIPPED).text[11:] # cutting off "Shipped on: "
                shipping = table.find_element(*IL.SHIPPING).text
                sales_tax = table.find_element(*IL.SALES_TAX).text
                total_for_shipment = table.find_element(*IL.TOTAL_FOR_SHIPMENT).text
                items = table.find_elements(*IL.ITEMS)
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

                    if credit_card:
                        # the order of these variables should correspond to self.csv_headers
                        row = [order_id, order_date, title, quantity, seller, condition, purchase_price_pu, subtotal, shipping, sales_tax,
                            total_for_shipment, total_for_order, methods[count], transaction_dates[count], shipped]
                    else:
                        row = [order_id, order_date, title, quantity, seller, condition, purchase_price_pu, subtotal, shipping, sales_tax,
                            total_for_shipment, total_for_order, methods[0], transaction_dates[0], shipped]

                    print(row)
                    self.write_row(row)
                count += 1
        except NoSuchElementException: # don't recognize invoice
            row = [order_id]
            print(row)
            self.write_row(row)

    def get_invoice_link(self, which):
        try:
            return self.driver.find_element(*AL().get_invoice_link(which))
        except NoSuchElementException:
            return False

    def save_invoice_as_html(self):
        self.invoice_count += 1
        order_id = self.driver.find_element(*IL.ORDER_ID).text[25:] # cutting off "Amazon.com order number: "
        order_date_str = self.driver.find_element(*IL.ORDER_DATE).text[14:] # cutting off "Order Placed: "
        order_date = datetime.datetime.strptime(order_date_str, '%B %d, %Y')
        fname = order_date.strftime('%Y.%m.%d') + ' - ' + order_id + ' (' + self.email.split('@')[0] + ').html'
        with open(self.invoice_folder + fname, 'wb') as invoice_file:
            invoice_file.write(self.driver.page_source.encode("UTF-8"))

    def scrape_invoices(self):
        self.wait.until(EC.presence_of_element_located(AL.FIRST_INVOICE))
        count = 1
        invoice_link = self.get_invoice_link(count)
        while (invoice_link):
            invoice_link.click()
            self.wait.until(EC.presence_of_element_located(IL.ORDER_ID))
            self.save_invoice_as_html()
            self.scrape_invoice_data()
            self.driver.back()
            count += 1
            self.wait.until(EC.presence_of_element_located(AL.FIRST_INVOICE))
            invoice_link = self.get_invoice_link(count)

    def go_next_page(self):
        next_btns = self.driver.find_elements(*AL.NAV_BTNS)
        next_btn = next_btns[len(next_btns) - 1]
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
        self.driver.get(URLS.AMAZON_ACCOUNT_PAGE)
        self.wait.until(EC.element_to_be_clickable(AL.ORDERS_BTN))

        orders_btn = self.wait.until(EC.presence_of_element_located(AL.ORDERS_BTN))
        orders_btn.click()

    def go_to_sign_in(self):
        sign_in_btn = self.wait.until(EC.presence_of_element_located(AL.ACCOUNT_BTN))
        sign_in_btn.click()

    def sign_in(self):
        email_field = self.driver.find_element(*SI.EMAIL_FIELD)
        pass_word_field = self.driver.find_element(*SI.PASS_FIELD)
        submit_btn = self.driver.find_element(*SI.SUBMIT_BTN)
        email_field.clear()
        email_field.send_keys(self.email)
        pass_word_field.clear()
        pass_word_field.send_keys(self.pass_word)
        submit_btn.click()

    def write_row(self, row):
        row = self.asciify(row)
        self.writer.writerow(row)
        self.csv_file.flush()

    def scrape_all_invoices(self):
        self.scrape_invoices()
        while self.next_page():
            self.go_next_page()
            self.scrape_invoices()

    def try_scrape_all_invoices(self):
        try:
            self.scrape_all_invoices()
        except TimeoutException: # we probably got signed out
            try:
                self.sign_in()
            except NoSuchElementException: # we signed back in and are currently on an invoice page
                self.scrape_invoice_data()
                self.driver.execute_script('window.history.go(-2)')
            self.try_scrape_all_invoices()


    def scrape(self):
        while self.year_exists(self.current_year):
            self.go_to_year(self.current_year)
            self.try_scrape_all_invoices()
            self.current_year -= 1