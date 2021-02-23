import os
import time
import random
import gmail_api
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from config import *

path_to_driver = os.path.abspath(__file__)
path_to_driver = path_to_driver[:path_to_driver.rfind('/') + 1] + 'chromedriver'
authorization_url = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.' \
                    'amazon.com%2Fyour-account%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2' \
                    'Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.' \
                    'claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2' \
                    'F%2Fspecs.openid.net%2Fauth%2F2.0&'


def error_handler(func):
    def wrapper(*args):
        try:
            return func(*args)
        except NoSuchElementException as error:
            err_message = error.msg
            if "ap_password" in err_message:
                print("Check your email and password and try again")
                args[0].quit()
                exit()
            else:
                print("Something went wrong: ", error)
        except WebDriverException as error:
            print("An error occurred: ", error)
    return wrapper


@error_handler
def authorize(driver, url):
    driver.get(url)
    for key in login_username:
        driver.find_element_by_id('ap_email').send_keys(key)
        time.sleep(random.random())
    driver.find_element_by_id('continue').click()
    for key in login_password:
        driver.find_element_by_id('ap_password').send_keys(key)
        time.sleep(random.random())
    driver.find_element_by_id('signInSubmit').click()
    time.sleep(4)
    link = gmail_api.get_link()
    if "amazon" not in link:
        raise NoSuchElementException(msg="ap_password")
    driver.execute_script("window.open('https://www.google.com/');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(link)
    driver.find_element_by_name('customerResponseApproveButton').click()
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return driver


@error_handler
def place_order(driver):
    price = driver.find_element_by_id('sc-subtotal-amount-buybox').text
    price = float(price.lstrip("$"))
    if price > price_limit:
        print("Too Expensive")
        exit()
    else:
        #driver.find_element_by_name('placeYourOrder1').click()
        print("Bying...")
    return driver


@error_handler
def navigate_to_cart(driver, url):
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_id('add-to-cart-button').click()
    time.sleep(1)
    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
    time.sleep(1)
    #driver.find_element_by_name('proceedToRetailCheckout').click()
    #time.sleep(1)
    return driver


def main():
    try:
        driver = webdriver.Chrome(path_to_driver)
    except WebDriverException:
        print("Unable to locate web driver in script directory!")
        exit()
    urls = []
    with open(urls_file, 'r') as file:
        for line in file.readlines():
            urls.append(line)
    driver = authorize(driver, authorization_url)
    for url in urls:
        driver = navigate_to_cart(driver, url)
        driver = place_order(driver)


if __name__ == '__main__':
    main()
