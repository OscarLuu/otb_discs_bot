import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# https://otbdiscs.com/my-account/


def start(driver, email, password, card_number, card_exp_date, csc, disc_amount=1, disc_color=None):
    driver.get("http://otbdiscs.com")
    sleep(5)

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

    start(driver, args.email, args.password, args.card_number, args.card_exp_date, args.csc) 