import pytest
from selenium import webdriver
from helpers import *


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

#test login
@pytest.mark.parametrize("username, password, expected_url", user_data_for_login)
def test_login(driver, username, password, expected_url):
    perform_login(driver, username, password)

    current_url = driver.current_url
    assert current_url == expected_url, f"Login failed for{username}. Got url {current_url}."

