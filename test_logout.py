import pytest
from selenium import webdriver
from helpers import *

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.parametrize("username, password", user_data)
def test_logout(driver, login_first, username, password):
    logout(driver)

    expected_url = "https://www.saucedemo.com/"
    actual_url = driver.current_url

    assert expected_url == actual_url, f"User {username} got wrong url {actual_url}."

@pytest.mark.parametrize("username, password", user_data)
def test_session(driver, login_first, username, password):
    logout(driver)
    driver.back()
    time.sleep(1)

    expected_url = "https://www.saucedemo.com/"
    actual_url = driver.current_url

    current_error_message = driver.find_element(By. XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3').text
    expected_error_message = "Epic sadface: You can only access '/inventory.html' when you are logged in."

    if expected_url == actual_url and expected_error_message == current_error_message:
        assert True
    else:
        assert False, f"For user {username} got wrong url {actual_url} and/or wrong error message {current_error_message}."

