import os
import time
import random
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from config import *

path_to_driver = os.path.abspath(__file__)
path_to_driver = path_to_driver[:path_to_driver.rfind('/') + 1] + 'chromedriver'


def error_handler(func):
    def wrapper(*args):
        try:
            return func(*args)
        except WebDriverException as error:
            print("An error occurred: ", error)
    return wrapper


@error_handler
def authorize(driver):
    for key in login_username:
        driver.find_element_by_id('ap_email').send_keys(key)
        time.sleep(random.random())
    driver.find_element_by_id('continue').click()
    for key in login_password:
        driver.find_element_by_id('ap_password').send_keys(key)
        time.sleep(random.random())
    driver.find_element_by_id('signInSubmit').click()


@error_handler
def place_order(driver):
    price = driver.find_element_by_css_selector('td.grand-total-price').text
    if price > price_limit:
        print("Too Expensive")
        exit()
    else:
        #driver.find_element_by_name('placeYourOrder1').click()
        pass


@error_handler
def navigate_to_cart(driver, url):
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_id('add-to-cart-button').click()
    time.sleep(1)
    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
    time.sleep(1)
    driver.find_element_by_name('proceedToRetailCheckout').click()


def main():
    try:
        driver = webdriver.Chrome(path_to_driver)
    except WebDriverException:
        print("Unable to locate web driver in script directory")
        exit()
    urls = []
    with open(urls_file, 'r') as file:
        for line in file.readlines():
            urls.append(line)
    for url in urls:
        navigate_to_cart(driver, url)
        authorize(driver)
        driver.execute_script("window.open('https://www.google.com');")
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])


if __name__ == '__main__':
    main()
