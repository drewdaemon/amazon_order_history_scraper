from selenium.webdriver.common.by import By

class InvoiceLocators:
    """A container class for locators on the invoice page"""
    ORDER_ID = (By.XPATH, '/html/body/table/tbody/tr/td/table[1]/tbody/tr[2]/td')
    ORDER_DATE = (By.XPATH, '/html/body/table/tbody/tr/td/table[1]/tbody/tr[1]/td')

    ORDER_ID_BIZ = (By.XPATH, '/html/body/table/tbody/tr/td/table[1]/tbody/tr[4]/td')
    ORDER_DATE_BIZ = (By.XPATH, '/html/body/table/tbody/tr/td/table[1]/tbody/tr[3]/td')

    ITEM_TABLES = (By.XPATH, '/html/body/table/tbody/tr/td/table')
    ITEMS = (By.XPATH, 'tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr')
    TITLE = (By.XPATH, 'td[1]/i')
    # quantity fetches "<quantity> of:"
    QUANTITY = (By.XPATH, 'td[1]')
    # fetches condition and seller info
    SELLER_CONDITION = (By.XPATH, 'td[1]/span')
    PURCHASE_PRICE_PU = (By.XPATH, 'td[2]')

    SUBTOTAL = (By.XPATH, 'tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]')
    SHIPPING = (By.XPATH, 'tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]')
    SALES_TAX = (By.XPATH, 'tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[5]/td[2]')
    TOTAL_FOR_SHIPMENT = (By.XPATH, 'tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[7]/td[2]/b')
    DATE_SHIPPED = (By.XPATH, 'tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/b/center')

    # these xpaths are relative to the last table in the invoice, the payment table
    PAYMENT_METHODS = (By.XPATH, 'tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr')
    PAYMENT_METHOD = (By.XPATH, 'tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td')
    TOTAL_FOR_ORDER = (By.XPATH, 'tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[7]/td[2]/b')

class AmazonLocators:
    """A container class for locators necessary for navigation through amazon's website"""
    DISABLED_NEXT = (By.XPATH, '//*[@id="ordersContainer"]/div[8]/div/ul/li[@class="a-disabled a-last"]')
    NAV_BTNS = (By.XPATH, '//*[@id="ordersContainer"]/div[12]/div/ul//li/a')
    YEAR_PICKER = (By.XPATH, '//*[@id="timePeriodForm"]')
    YEAR_FIELDS = (By.XPATH, '//*[@id="a-popover-1"]/div/div/ul//li/a')
    ORDERS_BTN = (By.XPATH, '//*[@id="your-orders-button-announce"]')
    ACCOUNT_BTN = (By.XPATH, '//*[@id="nav-link-yourAccount"]')
    NAV_OVERLAY = (By.ID, 'nav-cover')
    PAGE_DATES = (By.XPATH, '//*[@id="ordersContainer"]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/span')
    def get_invoice_link(self, which):
        return (By.XPATH, '//*[@id="ordersContainer"]/div[' + str(which + 1) + ']/div[1]/div/div/div/div[2]/div[2]/ul/a[2]')
    def get_invoice_link_business(self, which):
        return (By.XPATH, '//*[@id="ordersContainer"]/div[' + str(which + 1) + ']/div[1]/div/div/div/div[2]/div[2]/ul/span[1]/a')
    def get_year_link(self, year):
        return (By.LINK_TEXT, str(year))

class SignInLocators:
    """A container class for locators on the sign-in page"""
    EMAIL_FIELD = (By.ID, 'ap_email')
    PASS_FIELD = (By.ID, 'ap_password')
    SUBMIT_BTN = (By.ID, 'signInSubmit')

