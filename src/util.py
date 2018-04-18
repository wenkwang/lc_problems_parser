import time
from selenium.webdriver.common.keys import Keys


def is_logged_in(driver):
    pass_input = driver.find_element_by_id('password')
    if pass_input is None:
        return True
    return False


def login(driver, user, pwd):
    print("[In Progress] Login the website.")
    user_input = driver.find_element_by_id("username")
    pass_input = driver.find_element_by_id("password")
    keep_checkbox = driver.find_element_by_class_name('ant-checkbox-input')
    user_input.click()
    user_input.send_keys(user)
    pass_input.click()
    pass_input.send_keys(pwd)
    keep_checkbox.click()
    pass_input.send_keys(Keys.ENTER)
    time.sleep(5)
    return