from selenium.webdriver.common.by import By
import datetime

class InvoiceLocators:
    """A container class for locators on the invoice page"""
    ORDER_ID = (By.XPATH, '/html/body/table/tbody/tr/td/table[1]/tbody/tr[2]/td')
    ORDER_DATE = (By.XPATH, '/html/body/table/tbody/tr/td/table[1]/tbody/tr[1]/td')

    ITEMS = (By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody//tr')
    TITLE = (By.XPATH, 'td[1]/i')
    # quantity fetches "<quantity> of:"
    QUANTITY = (By.XPATH, 'td[1]')
    # fetches condition and seller info
    SELLER_CONDITION = (By.XPATH, 'td[1]/span')
    PURCHASE_PRICE_PU = (By.XPATH, 'td[2]')

    SUBTOTAL = (By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]')
    SHIPPING = (By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]')
    SALES_TAX = (By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]')
    TOTAL = (By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[7]/td[2]/b')
    PAYMENT_METHOD = (By.XPATH, '/html/body/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td')
    DATE_SHIPPED = (By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/b/center')

class AmazonLocators:
    """A container class for locators necessary for navigation through amazon's website"""
    DISABLED_NEXT = (By.XPATH, '//*[@id="ordersContainer"]/div[8]/div/ul/li[@class="a-disabled a-last"]')
    NAV_BTNS = (By.XPATH, '//*[@id="ordersContainer"]/div[12]/div/ul//li/a')
    YEAR_PICKER = (By.XPATH, '//*[@id="timePeriodForm"]')
    CURRENT_YEAR_LINK = (By.LINK_TEXT, str(datetime.datetime.now().year))
    YEAR_FIELDS = (By.XPATH, '//*[@id="a-popover-1"]/div/div/ul//li/a')
    ORDERS_BTN = (By.XPATH, '//*[@id="your-orders-button-announce"]')
    ACCOUNT_BTN = (By.XPATH, '//*[@id="nav-link-yourAccount"]')
    FIRST_INVOICE = (By.XPATH, '//*[@id="ordersContainer"]/div[2]/div[1]/div/div/div/div[2]/div[2]/ul/a[2]')
    # SIGN_IN_BTN = (By.XPATH, '//*[@id="nav-signin-tooltip"]/a')
    def get_invoice_link(self, which):
        return (By.XPATH, '//*[@id="ordersContainer"]/div[' + str(which + 1) + ']/div[1]/div/div/div/div[2]/div[2]/ul/a[2]')

class SignInLocators:
    """A container class for locators on the sign-in page"""
    EMAIL_FIELD = (By.ID, 'ap_email')
    PASS_FIELD = (By.ID, 'ap_password')
    SUBMIT_BTN = (By.ID, 'signInSubmit')

