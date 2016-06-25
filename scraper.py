from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os

url = 'https://www.amazon.com'

driver = webdriver.Firefox()

def get_invoice_link(which):
    try:
        return driver.find_element_by_xpath('//*[@id="ordersContainer"]/div[' + str(which + 1) + ']/div[1]/div/div/div/div[2]/div[2]/ul/a[2]')
    except NoSuchElementException:
        return False

def sign_in(email, pass_word):
    driver.get(url)
    signInBtn = driver.find_element_by_xpath('//*[@id="nav-signin-tooltip"]/a')
    signInBtn.click()

    emailField = driver.find_element_by_xpath('//*[@id="ap_email"]')
    passWordField = driver.find_element_by_xpath('//*[@id="ap_password"]')
    signInBtn = driver.find_element_by_xpath('//*[@id="signInSubmit"]')
    emailField.send_keys(email)
    passWordField.send_keys(pass_word)
    signInBtn.click()

sign_in(os.environ['AMAZON_EMAIL'], os.environ['AMAZON_PASS'])

accountBtn = driver.find_element_by_xpath('//*[@id="nav-link-yourAccount"]')
accountBtn.click()

ordersBtn = driver.find_element_by_xpath('//*[@id="your-orders-button-announce"]')
ordersBtn.click()

count = 1
invoice_link = get_invoice_link(count)
while (invoice_link):
    invoice_link.click()
    time.sleep(3)
    driver.back()
    count += 1
    invoice_link = get_invoice_link(count)

time.sleep(5)

driver.quit()
