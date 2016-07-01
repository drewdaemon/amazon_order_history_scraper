from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import getpass
import os

xpaths = {
    'disabled_next': '//*[@id="ordersContainer"]/div[8]/div/ul/li[@class="a-disabled a-last"]',
    'next_btn': '//*[@id="ordersContainer"]/div[12]/div/ul/li[12]/a',
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
            'condition': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/span',
            # seller fetches "Sold by: <seller>"
            'seller': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/span/text()[1]',
            'purchase_price_pu': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/text()',
            # quantity fetches "<quantity> of:"
            'quantity': '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/text()[1]',
        }
        self.scraped_data = []
        self.driver = None

    def scrape_invoice_data(self):
        order_id = self.driver.find_element_by_xpath(self.invoice_info_paths['order_id']).text
        order_date = self.driver.find_element_by_xpath(self.invoice_info_paths['order_date']).text
        title = self.driver.find_element_by_xpath(self.invoice_info_paths['title']).text
        condition = self.driver.find_element_by_xpath(self.invoice_info_paths['condition']).text

        row = [order_id, order_date, title, condition]
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
        self.driver.quit()

    def navigate_to_current_year(self):
        current_year = datetime.datetime.now().year
        picker = self.driver.find_element_by_xpath(xpaths['year_picker'])
        picker.click()
        current_year_field = self.driver.find_element_by_link_text(str(current_year))
        current_year_field.click()
        # all_options = picker.find_elements_by_tag_name('option')
        # for option in all_options:
        #     print(option.get_attribute('value'))
        #     print(current_year, option.text)
        #     print(option.text == str(current_year))
        #     if (option.text == str(current_year)):
        #         option.click()

    def go_to_orders(self):
        account_btn = self.driver.find_element_by_xpath(xpaths['account_btn'])
        account_btn.click()
        time.sleep(4)
        orders_btn = self.driver.find_element_by_xpath(xpaths['orders_btn'])
        orders_btn.click()
        time.sleep(4)
        self.navigate_to_current_year()

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

        self.go_to_orders()

    def get_credentials(self):
        try:
            email = os.environ['AMAZON_EMAIL']
        except KeyError:
            email = raw_input('Enter the email address you use to sign into amazon: ')
        try: 
            passwd = os.environ['AMAZON_PASS']
        except KeyError:
            passwd = getpass.getpass('Enter your password: ')
        
        self.sign_in(email, passwd)

scraper = amazonScraper()
# try:
scraper.get_credentials()
# except:
#     scraper.get_credentials()
