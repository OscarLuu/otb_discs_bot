import argparse
import os
import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

os.environ['WDM_LOG_LEVEL'] = '0'
logger = logging.getLogger()
#logging.basicConfig(filename="otb_error.log", encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class Card:
    def __init__(self, card_number, card_exp_date, csc):
        self.card_number = card_number
        self.card_exp_date = card_exp_date
        self.csc = csc
    
    def __str__(self):
        return f"Card number: {self.card_number}\nCard Exp Date: {self.card_exp_date}\nCSC: {self.csc}"


class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def __str__(self):
        return f"Email: {self.email}\nPassword: {self.password}"
    
    def get_password(self):
        return f"{self.password}"

    def get_username(self):
        return f"{self.email}"


class Disc:
    def __init__(self, disc_url, disc_color=None, disc_amount=1):
        self.disc_url = disc_url
        self.disc_color = disc_color
        self.disc_amount = disc_amount
    
    def __str__(self):
        return f"URL: {self.disc_url}\n Color: {self.disc_color}\nAmount: {self.disc_amount}"


def start(driver, card, login, disc):
    logger.info("Starting login")
    login_otb(driver, login)


def login_otb(driver, login):
    try:
        logger.info("Requesting OTB Login page..")
        driver.get("http://otbdiscs.com/my-account/")
    except TimeoutException:
        logger.error("Timed out waiting for page.")
    
    logger.info("Page successfully requested, delaying until page fully loads.")
    username_element = '//*[@id="username"]'
    password_element = '//*[@id="password"]'
    #button_element = '//*[@id="customer_login"]/div[1]/form/p[3]/button'
    delay(driver, username_element)

    user = driver.find_element_by_xpath(username_element)
    user.clear()
    user.send_keys(login.get_username())

    pwd = driver.find_element_by_xpath(password_element)
    pwd.clear()
    pwd.send_keys(login.get_password())
    pwd.send_keys(u'\ue007')

    # implement confirm that logged in
    logger.info("Logged in successfully")


def delay(driver, item):
    timeout = 10000
    poll = 0.1
    WebDriverWait(driver, timeout, poll).until(expected_conditions.visibility_of_element_located((By.XPATH, item)))

# TODO
# implement login

# implement checkout

# implement disc color finder

# implement disc amounts

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True, help="E-mail used to login to OTB.")
    parser.add_argument("--password", required=True, help="Password used to login to OTB.")
    parser.add_argument("--disc-url", required=True, help="Disc URL on OTB.")
    parser.add_argument("--disc-color", default=None, help="Disc color if preference, or else buy nth ones.")
    parser.add_argument("--disc-amount", default=1, help="Disc amounts, defaults to 1.")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--card-number", required=True, help="Card used to purchase on OTB.")
    parser.add_argument("--card-exp-date", required=True, help="Card Expiration date.")
    parser.add_argument("--csc", required=True, help="CSC code for card.")
    args = parser.parse_args()

    card = Card(args.card_number, args.card_exp_date, args.csc)
    login = Login(args.email, args.password)
    disc = Disc(args.disc_url, args.disc_color, args.disc_amount)

    start(driver, card, login, disc) 