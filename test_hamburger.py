import time
import pytest
from  selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from helpers import open_hamburger, perform_login, user_data, skip_users, skip_user_check
from selenium.common.exceptions import NoSuchElementException, TimeoutException

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login_and_open_hamburger(driver, username, password):
    skip_user_check(username, password)
    time.sleep(1)
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, username, password)
    open_hamburger(driver)

@pytest.mark.parametrize("username, password", user_data)
def test_ham_opening(driver, login_and_open_hamburger, username, password):
    target_element = driver.find_element(By.CLASS_NAME, "bm-menu-wrap")
    aria_value = target_element.get_attribute("aria-hidden")
    assert aria_value == "false", f"Test Failed for {username}: aria-hidden value is {aria_value}, expected 'false'."


@pytest.mark.parametrize("username, password", user_data)
@pytest.mark.parametrize("menu_action, expected_result", [
    ("inventory_sidebar_link", "https://www.saucedemo.com/inventory.html"),
    ("about_sidebar_link", "https://saucelabs.com/"),
    ("logout_sidebar_link", "https://www.saucedemo.com/")
])
def test_hammenu_options(driver, login_and_open_hamburger, username, password, menu_action, expected_result):
    time.sleep(1)
    action_button = driver.find_element(By.ID, menu_action)
    action_button.click()
    time.sleep(1)
    actual_url = driver.current_url
    assert actual_url == expected_result, f"Test Failed for {username}: Expected {expected_result}, but got {actual_url}."

@pytest.mark.parametrize("username, password", user_data)
def test_app_reset(driver, login_and_open_hamburger, username, password):
    control_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    control_button.click()
    time.sleep(1)

    reset_button = driver.find_element(By.ID, "reset_sidebar_link")
    reset_button.click()

    try:
        control_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        print("Control button still exists, but it should have been removed")
        assert False, f"Test Failed for {username}: Control button should not be present"
    except NoSuchElementException:
        print(f"Test Passed for {username}: Control button was successfully removed")
        assert True